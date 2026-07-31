---
name: audit-git-history-sensitive-data
description: Use when a user asks to inspect Git history for secrets, API keys, credentials, private keys, personal information, local computer paths, databases, environment files, or other sensitive data without rewriting history.
---

# Audit Git History Sensitive Data

Perform a read-only audit. Report evidence without exposing the sensitive value,
and do not rewrite, delete, push, or garbage-collect anything.

## Resolve the Scope

Read repository instructions first. Resolve the repository and reachable-history
scope before scanning:

- Default to commits reachable from `HEAD`.
- Use `--all` only when the user requests all local refs.
- Honor explicit refs, SHA endpoints, dates, and author filters.
- Record submodules and Git LFS separately; ordinary object traversal does not
  inspect the content stored in their external object stores.

Inspect without changing state:

```bash
git status --short --branch
git rev-parse --show-toplevel
git log --date=iso-strict --format='%H%x09%aI%x09%an%x09%ae%x09%s' <scope>
git rev-list --objects <scope>
```

## Scan the Reachable History

Prefer an already-installed history-aware secret scanner. Do not install a new
dependency merely for the audit. Regardless of the scanner, inspect these
surfaces:

1. Commit messages, author and committer metadata, filenames, and symlink
   targets.
2. Each unique reachable blob, mapped back to every commit and path that
   exposes it. Avoid rescanning identical blobs.
3. Deleted and renamed files, not only the current tree.
4. Text and decodable structured files; classify unreadable binaries for
   follow-up instead of treating them as clean.

Cover at least:

- API keys, access tokens, passwords, cookies, private keys, certificates,
  connection strings, and credential assignments;
- `.env` files, local configuration, shell histories, cloud credentials,
  database files, backups, archives, and debug dumps;
- names, personal email addresses, phone numbers, physical addresses,
  government identifiers, account numbers, and other personal information;
- absolute local paths such as `/Users/<name>/`, `/home/<name>/`,
  `C:\Users\<name>\`, `file://` URLs, and paths embedded in logs or tool
  metadata.

Treat pattern or entropy matches as candidates, not proof. Verify candidates in
context without contacting the credential's service. Distinguish expected Git
author metadata from personal data accidentally embedded in repository content,
but report both when they match the requested policy.

## Protect Sensitive Output

Never print a full matched value. Redact it and identify the finding with a
detector name or a one-way digest. Do not place raw findings in the repository,
shell history, command arguments, or chat output. Store any necessary detailed
artifact under the system temporary directory with restrictive permissions.

## Report

Report:

- exact scope, refs, commit count, and surfaces scanned;
- severity and confidence;
- first reachable commit, abbreviated object ID, path, and line when available;
- category and redacted evidence;
- whether the value remains reachable from the requested refs;
- scanner limitations and uninspected external stores.

Return zero findings only after checking commit metadata, paths, and reachable
blob content. Recommend remediation separately; perform it only when the user
explicitly asks to rewrite history.
