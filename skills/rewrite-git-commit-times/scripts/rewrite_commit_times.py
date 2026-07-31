"""Rewrite selected Git commit times into configured working windows."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from itertools import pairwise
from pathlib import Path
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class Window:
    start: int
    end: int


@dataclass(frozen=True)
class DateScope:
    start: date
    end: date

    def contains(self, day: date) -> bool:
        return self.start <= day <= self.end

    def describe(self) -> str:
        if self.start == self.end:
            return self.start.isoformat()
        return f"{self.start.isoformat()}..{self.end.isoformat()}"


@dataclass(frozen=True)
class Rules:
    timezone: ZoneInfo
    holidays: frozenset[date]
    workdays: frozenset[date]
    windows: tuple[Window, ...]
    scope: DateScope | None
    author_emails: frozenset[str]

    def is_workday(self, day: date) -> bool:
        if day in self.workdays:
            return True
        if day in self.holidays:
            return False
        return day.weekday() < 5

    def is_allowed(self, value: datetime) -> bool:
        local = value.astimezone(self.timezone)
        second = local.hour * 3600 + local.minute * 60 + local.second
        return self.is_workday(local.date()) and any(
            window.start <= second < window.end for window in self.windows
        )

    def move_forward(self, value: datetime) -> datetime:
        candidate = value.astimezone(self.timezone)
        while True:
            if self.is_workday(candidate.date()):
                second = (
                    candidate.hour * 3600 + candidate.minute * 60 + candidate.second
                )
                for window in self.windows:
                    if window.start <= second < window.end:
                        return candidate
                    if second < window.start:
                        return datetime.combine(
                            candidate.date(),
                            time(
                                window.start // 3600,
                                (window.start % 3600) // 60,
                                window.start % 60,
                            ),
                            self.timezone,
                        )
            candidate = datetime.combine(
                candidate.date() + timedelta(days=1),
                time(
                    self.windows[0].start // 3600,
                    (self.windows[0].start % 3600) // 60,
                    self.windows[0].start % 60,
                ),
                self.timezone,
            )

    def adjust(self, value: datetime, previous: datetime | None) -> datetime:
        candidate = self.move_forward(value)
        if previous is not None and candidate <= previous:
            candidate = self.move_forward(previous + timedelta(seconds=1))
        return candidate

    def selects(self, commit: Commit) -> bool:
        local_day = commit.committer_date.astimezone(self.timezone).date()
        in_scope = self.scope is None or self.scope.contains(local_day)
        author_matches = (
            "*" in self.author_emails or commit.author_email in self.author_emails
        )
        return in_scope and author_matches

    def describe_scope(self) -> str:
        return "all" if self.scope is None else self.scope.describe()


@dataclass(frozen=True)
class Commit:
    oid: str
    tree: str
    parent: str | None
    author_name: str
    author_email: str
    author_date: datetime
    committer_name: str
    committer_email: str
    committer_date: datetime
    message: bytes
    signed: bool


def run_git(
    repo: Path,
    args: list[str],
    *,
    input_bytes: bytes | None = None,
) -> bytes:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        input=input_bytes,
        capture_output=True,
        check=True,
    ).stdout


def parse_time(value: str, *, allow_24: bool = False) -> int:
    if allow_24 and value == "24:00":
        return 24 * 3600
    parsed = time.fromisoformat(value)
    if parsed.tzinfo is not None:
        raise ValueError(f"time must not include an offset: {value}")
    return parsed.hour * 3600 + parsed.minute * 60 + parsed.second


def expand_dates(values: list[object]) -> frozenset[date]:
    result: set[date] = set()
    for value in values:
        if isinstance(value, str):
            result.add(date.fromisoformat(value))
            continue
        if not isinstance(value, dict) or set(value) != {"start", "end"}:
            raise ValueError("dates must be YYYY-MM-DD or {start, end}")
        current = date.fromisoformat(str(value["start"]))
        end = date.fromisoformat(str(value["end"]))
        if end < current:
            raise ValueError(f"date range ends before it starts: {value}")
        while current <= end:
            result.add(current)
            current += timedelta(days=1)
    return frozenset(result)


def load_rules(path: Path) -> Rules:
    payload = json.loads(path.read_text(encoding="utf-8"))
    timezone = ZoneInfo(payload["timezone"])
    holidays = expand_dates(payload.get("holidays", []))
    workdays = expand_dates(payload.get("workdays", []))
    overlap = holidays & workdays
    if overlap:
        raise ValueError(
            f"dates cannot be both holidays and workdays: {sorted(overlap)}"
        )

    windows = []
    for raw in payload.get("work_windows", []):
        start = parse_time(raw["start"])
        end = parse_time(raw["end"], allow_24=True)
        if start >= end:
            raise ValueError(
                "work windows must be non-crossing half-open ranges; split "
                "cross-midnight ranges"
            )
        windows.append(Window(start, end))
    windows.sort(key=lambda item: item.start)
    if not windows:
        raise ValueError("at least one work window is required")
    for previous, current in pairwise(windows):
        if current.start < previous.end:
            raise ValueError("work windows must not overlap")

    raw_scope = payload.get("date_scope")
    if raw_scope is None:
        today = datetime.now(timezone).date()
        scope = DateScope(today, today)
    elif raw_scope == "all":
        scope = None
    elif isinstance(raw_scope, dict) and set(raw_scope) == {"start", "end"}:
        scope = DateScope(
            date.fromisoformat(str(raw_scope["start"])),
            date.fromisoformat(str(raw_scope["end"])),
        )
        if scope.end < scope.start:
            raise ValueError("date_scope ends before it starts")
    else:
        raise ValueError("date_scope must be 'all' or {start, end}")

    raw_authors = payload.get("author_emails")
    if (
        not isinstance(raw_authors, list)
        or not raw_authors
        or not all(isinstance(value, str) and value for value in raw_authors)
    ):
        raise ValueError("author_emails must be a non-empty string list")
    author_emails = frozenset(raw_authors)
    if "*" in author_emails and len(author_emails) != 1:
        raise ValueError("'*' must be the only author_emails entry")

    return Rules(
        timezone,
        holidays,
        workdays,
        tuple(windows),
        scope,
        author_emails,
    )


def parse_commit(repo: Path, oid: str) -> Commit:
    raw = run_git(repo, ["cat-file", "commit", oid])
    header, message = raw.split(b"\n\n", 1)
    fields = (
        run_git(
            repo,
            [
                "show",
                "-s",
                "--format=%T%x00%P%x00%an%x00%ae%x00%aI%x00%cn%x00%ce%x00%cI",
                oid,
            ],
        )
        .decode()
        .rstrip("\n")
        .split("\0")
    )
    (
        tree,
        parents,
        author_name,
        author_email,
        author_date,
        committer_name,
        committer_email,
        committer_date,
    ) = fields
    parent_list = parents.split()
    if len(parent_list) > 1:
        raise ValueError(f"merge commit is not supported: {oid}")
    return Commit(
        oid=oid,
        tree=tree,
        parent=parent_list[0] if parent_list else None,
        author_name=author_name,
        author_email=author_email,
        author_date=datetime.fromisoformat(author_date),
        committer_name=committer_name,
        committer_email=committer_email,
        committer_date=datetime.fromisoformat(committer_date),
        message=message,
        signed=b"\ngpgsig " in b"\n" + header,
    )


def format_git_date(value: datetime) -> str:
    return value.isoformat(timespec="seconds")


def metadata_digest(commit: Commit) -> str:
    digest = hashlib.sha256()
    for value in (
        commit.tree,
        commit.author_name,
        commit.author_email,
        commit.committer_name,
        commit.committer_email,
    ):
        digest.update(value.encode())
        digest.update(b"\0")
    digest.update(commit.message)
    return digest.hexdigest()


def checked_out_refs(repo: Path) -> set[str]:
    output = run_git(repo, ["worktree", "list", "--porcelain"]).decode()
    return {
        line.removeprefix("branch ")
        for line in output.splitlines()
        if line.startswith("branch ")
    }


def normalize_target(repo: Path, target: str) -> str:
    name = target.removeprefix("refs/heads/")
    run_git(repo, ["check-ref-format", "--branch", name])
    return f"refs/heads/{name}"


def load_commits(repo: Path, source: str) -> list[Commit]:
    merge_count = int(
        run_git(repo, ["rev-list", "--count", "--merges", source]).strip()
    )
    if merge_count:
        raise ValueError(
            "source contains merges; resolve the topology before rewriting time"
        )
    oids = run_git(repo, ["rev-list", "--reverse", source]).decode().splitlines()
    if not oids:
        raise ValueError("source has no commits")
    return [parse_commit(repo, oid) for oid in oids]


def calculate_schedule(
    commits: list[Commit],
    rules: Rules,
) -> tuple[list[tuple[datetime, datetime]], int, int, int, int]:
    schedule = []
    previous_selected_author = None
    previous_selected_committer = None
    selected = 0
    changed_author = 0
    changed_committer = 0
    signature_loss = 0
    chain_changed = False

    for commit in commits:
        if rules.selects(commit):
            selected += 1
            author = rules.adjust(commit.author_date, previous_selected_author)
            committer = rules.adjust(
                commit.committer_date,
                previous_selected_committer,
            )
            previous_selected_author = author
            previous_selected_committer = committer
        else:
            author = commit.author_date
            committer = commit.committer_date
        author_changed = author != commit.author_date
        committer_changed = committer != commit.committer_date
        changed_author += author_changed
        changed_committer += committer_changed
        chain_changed = chain_changed or author_changed or committer_changed
        if commit.signed and chain_changed:
            signature_loss += 1
        schedule.append((author, committer))

    return schedule, selected, changed_author, changed_committer, signature_loss


def create_commit(
    repo: Path,
    source: Commit,
    parent: str | None,
    author: datetime,
    committer: datetime,
) -> str:
    if (
        source.parent == parent
        and source.author_date == author
        and source.committer_date == committer
    ):
        return source.oid
    if (
        b"\nencoding "
        in b"\n"
        + run_git(repo, ["cat-file", "commit", source.oid]).split(b"\n\n", 1)[0]
    ):
        raise ValueError(
            f"cannot safely rewrite non-UTF-8 commit without preserving "
            f"encoding header: {source.oid}"
        )

    args = ["commit-tree", source.tree]
    if parent:
        args.extend(["-p", parent])
    env = os.environ | {
        "GIT_AUTHOR_NAME": source.author_name,
        "GIT_AUTHOR_EMAIL": source.author_email,
        "GIT_AUTHOR_DATE": format_git_date(author),
        "GIT_COMMITTER_NAME": source.committer_name,
        "GIT_COMMITTER_EMAIL": source.committer_email,
        "GIT_COMMITTER_DATE": format_git_date(committer),
    }
    return (
        subprocess.run(
            ["git", *args],
            cwd=repo,
            env=env,
            input=source.message,
            capture_output=True,
            check=True,
        )
        .stdout.decode()
        .strip()
    )


def write_map(
    path: Path,
    old_target: str,
    rows: list[tuple[Commit, str, datetime, datetime]],
) -> None:
    lines = [
        f"# previous_target={old_target}",
        (
            "# source\tnew\tauthor_before\tauthor_after"
            "\tcommitter_before\tcommitter_after"
        ),
    ]
    for source, new_oid, author, committer in rows:
        lines.append(
            "\t".join(
                (
                    source.oid,
                    new_oid,
                    format_git_date(source.author_date),
                    format_git_date(author),
                    format_git_date(source.committer_date),
                    format_git_date(committer),
                )
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def self_test() -> None:
    rules = Rules(
        ZoneInfo("Asia/Shanghai"),
        frozenset({date(2026, 1, 1)}),
        frozenset({date(2026, 1, 4)}),
        (
            Window(parse_time("09:00"), parse_time("12:00")),
            Window(parse_time("14:00"), parse_time("18:00")),
        ),
        DateScope(date(2026, 1, 1), date(2026, 1, 31)),
        frozenset({"*"}),
    )
    assert rules.is_allowed(datetime.fromisoformat("2026-01-04T10:00:00+08:00"))
    assert not rules.is_allowed(datetime.fromisoformat("2026-01-01T10:00:00+08:00"))
    assert rules.move_forward(
        datetime.fromisoformat("2026-01-05T08:00:00+08:00")
    ) == datetime.fromisoformat("2026-01-05T09:00:00+08:00")
    assert rules.move_forward(
        datetime.fromisoformat("2026-01-05T12:30:00+08:00")
    ) == datetime.fromisoformat("2026-01-05T14:00:00+08:00")
    assert rules.move_forward(
        datetime.fromisoformat("2026-01-05T18:00:00+08:00")
    ) == datetime.fromisoformat("2026-01-06T09:00:00+08:00")
    print("self-test passed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--source")
    parser.add_argument("--target")
    parser.add_argument("--rules", type=Path)
    parser.add_argument("--map", dest="map_path", type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--allow-signature-loss", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return
    if not all((args.repo, args.source, args.target, args.rules)):
        parser.error("--repo, --source, --target, and --rules are required")

    repo = args.repo.resolve()
    run_git(repo, ["rev-parse", "--git-dir"])
    target_ref = normalize_target(repo, args.target)
    old_target = run_git(repo, ["rev-parse", target_ref]).decode().strip()
    commits = load_commits(repo, args.source)
    rules = load_rules(args.rules)
    (
        schedule,
        selected,
        changed_author,
        changed_committer,
        signature_loss,
    ) = calculate_schedule(commits, rules)

    summary = {
        "mode": "apply" if args.apply else "dry-run",
        "source": args.source,
        "target": target_ref,
        "commits": len(commits),
        "selected_commits": selected,
        "date_scope": rules.describe_scope(),
        "changed_author_dates": changed_author,
        "changed_committer_dates": changed_committer,
        "signatures_invalidated": signature_loss,
        "first_result": format_git_date(schedule[0][1]),
        "last_result": format_git_date(schedule[-1][1]),
    }
    if not args.apply:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return
    if not selected:
        raise ValueError("no commits match date_scope and author_emails")
    if target_ref in checked_out_refs(repo):
        raise ValueError(f"target branch is checked out in a worktree: {target_ref}")
    if signature_loss and not args.allow_signature_loss:
        raise ValueError(
            f"{signature_loss} signed commit(s) would lose signatures; "
            "re-run with --allow-signature-loss after explicit approval"
        )

    parent = None
    rows = []
    for source, (author, committer) in zip(commits, schedule, strict=True):
        new_oid = create_commit(repo, source, parent, author, committer)
        rows.append((source, new_oid, author, committer))
        parent = new_oid

    new_tip = parent
    assert new_tip is not None
    rebuilt = load_commits(repo, new_tip)
    if len(rebuilt) != len(commits):
        raise RuntimeError("rewritten commit count differs from source")
    for source, rewritten, (author, committer) in zip(
        commits, rebuilt, schedule, strict=True
    ):
        if metadata_digest(source) != metadata_digest(rewritten):
            raise RuntimeError(
                f"non-time metadata changed: {source.oid} -> {rewritten.oid}"
            )
        if rewritten.author_date != author or rewritten.committer_date != committer:
            raise RuntimeError(f"rewritten time mismatch: {rewritten.oid}")
        if rules.selects(source) and (
            not rules.is_allowed(author) or not rules.is_allowed(committer)
        ):
            raise RuntimeError(f"time remains outside work windows: {rewritten.oid}")

    missing = [
        line
        for line in run_git(repo, ["rev-list", "--objects", "--missing=print", new_tip])
        .decode()
        .splitlines()
        if line.startswith("?")
    ]
    if missing:
        raise RuntimeError(f"rewritten history has missing objects: {missing}")

    map_path = args.map_path or Path(tempfile.gettempdir()) / (
        f"rewrite-git-commit-times-{new_tip[:12]}.tsv"
    )
    write_map(map_path, old_target, rows)
    run_git(
        repo,
        [
            "update-ref",
            "-m",
            "rewrite selected commit times into work windows",
            target_ref,
            new_tip,
            old_target,
        ],
    )
    summary |= {"new_tip": new_tip, "map": str(map_path)}
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
