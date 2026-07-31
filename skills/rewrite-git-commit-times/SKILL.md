---
name: rewrite-git-commit-times
description: Use when a user asks to reorganize Git author and committer dates into specified working-hour ranges, defaulting to today's commits in the computer's local timezone, with official holiday and makeup-workday lookup for explicit date ranges or all history.
---

# Rewrite Git Commit Times

Rewrite time metadata only. Leave trees, messages, identities, the source ref,
the current worktree, and remotes unchanged.

## Resolve Rules

Resolve these inputs before mutation:

- one or more half-open working windows such as `[09:00,12:00)` and
  `[14:00,18:00)`; require them when the user did not provide them;
- the computer's current IANA timezone unless the user names another timezone;
- author email, defaulting to the repository's effective `git config
  user.email`; require an explicit value when it is missing, and require
  explicit approval for all authors;
- source ref and a separate, existing, local target branch.

When the user omits a date scope, select only commits whose original committer
date is today in the resolved timezone. Materialize that date in the rules file
so a later run cannot cross midnight. Accept an explicit inclusive
`start`/`end` range or the literal `all`.

Do not infer a timezone from a numeric UTC offset when the computer exposes an
IANA zone. Do not infer working hours.

## Resolve Holidays for Explicit Scopes

Skip network holiday lookup only for the implicit-today default. For every
explicit date, date range, or `all` scope:

1. Resolve the holiday jurisdiction separately from timezone. Use the user's
   stated jurisdiction; otherwise use the computer locale only when
   unambiguous, and ask before writing if it is ambiguous.
2. Determine every year covered by the selected commits. For `all`, inspect the
   matching commits first.
3. For each required year, check the system temporary directory for
   `<country>_holiday_schedule_<YYYY>.md`, using a lowercase country slug; for
   example, `china_holiday_schedule_2026.md`.
4. If that year's file exists and contains calendar data, read it directly.
   Do not expire it by fetch month or file age.
5. If the file is absent or empty, its calendar data is unusable, or the user
   asks to search again, query official sources. A refresh bypasses cached data
   and replaces the cache only after successful validation.

Only when the holiday jurisdiction is mainland China (`china`), search the
State Council results by incrementing `pageNo`:

```text
https://sousuo.www.gov.cn/sousuo/search.shtml?code=17da70961a7&searchWord=%E8%8A%82%E5%81%87%E6%97%A5%E5%AE%89%E6%8E%92%E7%9A%84%E9%80%9A%E7%9F%A5&dataTypeId=107&pageNo=<N>
```

This endpoint is not a global holiday source. Do not use it for Hong Kong,
Macau, Taiwan, or any other jurisdiction. Locate that jurisdiction's official
government source and keep its cache under its own country or region slug.

Open the official notice for each required year. Extract inclusive holiday
ranges and explicit makeup workdays from the notice itself, not from a search
snippet. Cache each year separately with the fetch time, jurisdiction,
normalized dates, and source URLs. Stop instead of guessing when a schedule is
unavailable.

## Build the Rules File

Write the JSON file under the system temporary directory:

```json
{
  "timezone": "Asia/Shanghai",
  "date_scope": {
    "start": "2026-07-01",
    "end": "2026-07-31"
  },
  "author_emails": ["developer@example.com"],
  "work_windows": [
    {"start": "09:00", "end": "12:00"},
    {"start": "14:00", "end": "18:00"}
  ],
  "holidays": [
    {"start": "2026-10-01", "end": "2026-10-07"}
  ],
  "workdays": ["2026-10-10"]
}
```

Omit `date_scope` only to let the script resolve today immediately; prefer an
explicit resolved date. Use `"date_scope": "all"` only for an explicit all-date
request. Use `"author_emails": ["*"]` only for an explicit all-author request.
Date ranges are inclusive. Work windows are half-open, ordered, non-overlapping,
and cannot cross midnight. `workdays` overrides weekends; `holidays` overrides
weekdays, and the sets cannot overlap.

## Dry Run and Apply

Inspect repository instructions, status, refs, worktrees, signatures, and the
selected count. The script accepts only linear source history; do not flatten
merges without a separate explicit request.

```bash
python3 scripts/rewrite_commit_times.py --self-test

python3 scripts/rewrite_commit_times.py \
  --repo <repo> \
  --source <linear-source-ref> \
  --target <existing-target-branch> \
  --rules <rules.json>

python3 scripts/rewrite_commit_times.py \
  --repo <repo> \
  --source <linear-source-ref> \
  --target <existing-target-branch> \
  --rules <rules.json> \
  --apply
```

The default run is a dry run. Before `--apply`, show the resolved timezone,
scope, author policy, work windows, calendar sources, selected count, changed
count, target, and signature loss. Obtain fresh confirmation for a public or
shared repository, signature loss, source-ref replacement, or any remote
publication. Never force-push or skip hooks automatically.

`--apply` rebuilds a linear chain, writes a source/result TSV mapping to the
system temporary directory, verifies it, and atomically updates the target ref.
It refuses a target checked out in any worktree.

## Validate

Verify that:

- only commits selected by original committer date and author policy receive
  new dates;
- selected author and committer dates land on workdays inside a work window;
- commit count, trees, messages, names, and emails remain identical;
- the source ref, worktree, unrelated files, and remotes remain unchanged;
- the target has no missing objects.

Report the new target head, selected and changed counts, resolved calendar
sources or cache path, mapping path, signature impact, and publication state.
Content sanitization belongs to `audit-git-history-sensitive-data` and a
separately approved remediation workflow.
