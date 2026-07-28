---
name: rewrite-git-history-safely
description: Use when a user asks to migrate or rebuild Git commits into another branch, sanitize secrets or database files from history, flatten or preserve merges, remove empty commits, or rewrite author and committer dates with custom timezone, holiday, makeup-workday, or forbidden-time rules.
---

# Rewrite Git History Safely

Rebuild Git history without changing the source branch or unrelated worktree
state. Treat content sanitization, topology changes, and date rewriting as
separate stages with explicit validation between them.

## Establish the Contract

Resolve these decisions before mutation:

- source ref, target branch, and target base or orphan-root behavior;
- a bounded commit scope, expressed with exact SHA endpoints and/or explicit
  date-time endpoints, plus an exact author identity;
- chronological order and merge policy: preserve topology or flatten;
- empty-commit policy and metadata fields that must remain unchanged;
- sensitive paths, secret patterns, databases, local configuration, and
  personal values to remove or anonymize;
- timezone, holidays, makeup workdays, forbidden time windows, movement
  direction, and interval boundaries;
- local-only or remote publication.

Default the author identity to the effective `git config user.name` and
`user.email` for the repository. If either value is absent, require an
explicit author. Never interpret an omitted range or author as all reachable
history or all authors. State date-time boundaries with their timezone and
whether each endpoint is inclusive.

Classify the repository before mutation as a personal project or another
person's/shared project, and as private or public. Use authenticated hosting
metadata when a remote exists; a remote URL alone does not prove visibility.
Treat an unverifiable classification as confirmation-required. For any
non-personal project, or for a personal project whose repository is public,
show the resolved repository, classification, scope, author, affected commit
count, target ref, and publication plan after inspection or dry-run, then
obtain a fresh explicit confirmation immediately before the first write.
The original rewrite request is not this second confirmation.

Accept additional date and time rules on every invocation. Do not silently
reuse a previous calendar. If a regional work calendar matters, retrieve the
official schedule for every year covered by the commits and cite it. State
time windows as half-open intervals, for example `[08:30,12:00)`.

## Inspect Before Rewriting

Read repository instructions and inspect:

```bash
git status --short --branch
git branch --all --verbose --no-abbrev
git worktree list --porcelain
git config --get user.name
git config --get user.email
git remote --verbose
git rev-list --count <source>
git rev-list --count --merges <source>
git log --reverse --date=iso-strict --format='%H%x09%aI%x09%cI%x09%s' <source>
```

Search all reachable filenames for databases, environment files, credentials,
private keys, local tool configuration, screenshots, and personal paths.
Scan secret values without printing the matched value. Determine whether
merge commits contain conflict resolutions before choosing a flattening plan.

Never rewrite the source ref in place. Preserve unrelated dirty and untracked
files by working in an isolated worktree or with temporary refs. Follow the
repository's database-backup rule before any operation that can remove a live
database from its current worktree.

## Rebuild and Sanitize

Process commits from oldest to newest. Keep a source-to-result mapping.

- For linear consecutive commits, materialize the source tree, apply the
  agreed sanitization, then commit the resulting snapshot.
- Remove database files and confirmed sensitive data from every historical
  snapshot, not only from the final tree.
- Preserve commit message bytes, tree content after sanitization, author,
  committer, and requested metadata. Record unavoidable signature loss.
- When flattening a merge, insert its side commits at the merge point. If the
  merge contains manual conflict resolution, fold the verified final merge
  result into the last inserted side commit.
- Skip commits that become empty only when the contract says to remove them.

Use exact refs and paths. Do not use broad destructive commands, force-push,
skip hooks, or garbage-collect dangling objects as part of the rewrite.

## Apply Date and Time Rules

Use `scripts/rewrite_commit_times.py` only after the target history is linear
and content-clean. The script uses a JSON rules file that may be extended for
each request:

```json
{
  "timezone": "Asia/Shanghai",
  "holidays": [
    {"start": "2026-02-15", "end": "2026-02-23"}
  ],
  "workdays": ["2026-02-14", "2026-02-28"],
  "forbidden_windows": [
    {"start": "08:30", "end": "12:00", "when": "workday"},
    {"start": "14:00", "end": "21:00", "when": "workday"}
  ]
}
```

`holidays` and `workdays` accept individual dates or inclusive ranges.
`workdays` overrides normal weekends; `holidays` overrides normal weekdays.
The two sets must not overlap. `when` is `workday` or `all`. Windows are
half-open, non-crossing ranges; split a range that crosses midnight. A
`00:00`–`24:00` workday window moves commits to the next eligible day.

Write the rules file outside the repository, then run:

```bash
python3 scripts/rewrite_commit_times.py --self-test

python3 scripts/rewrite_commit_times.py \
  --repo <repo> \
  --source <clean-linear-ref> \
  --target <target-branch> \
  --rules <rules.json>

python3 scripts/rewrite_commit_times.py \
  --repo <repo> \
  --source <clean-linear-ref> \
  --target <target-branch> \
  --rules <rules.json> \
  --apply
```

The default run is a dry run. `--apply` creates a new linear chain, verifies
it, writes a TSV mapping under the system temporary directory, and atomically
updates the target ref. It refuses a checked-out target branch. If signed
commits would be invalidated, obtain explicit approval before adding
`--allow-signature-loss`.

## Validate and Report

Before completion, verify:

- expected commit count, root count, merge count, order, and no missing
  objects;
- no commit outside the agreed SHA/date-time and author scope was rewritten;
- every source/result pair has identical message, tree, names, and emails
  except for explicitly sanitized content or rewritten dates;
- all author and committer dates satisfy the final calendar rules and remain
  strictly ordered;
- forbidden files, personal paths, and high-confidence secret patterns have
  zero reachable-history matches;
- the final tree differs from the source only by the agreed sanitization.

Run project lint, tests, and build when tree content changed. For a time-only
rewrite, prove tree identity instead of rerunning unchanged code. Leave the
source branch, current worktree, and remote untouched unless the user
explicitly expands the scope. Report the new head, skipped commits, changed
date counts, validation results, reflog recovery point, and publication state.
