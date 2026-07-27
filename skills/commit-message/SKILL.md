---
name: commit-message
description: Use when the user asks to commit changes, run git commit, generate a commit message, or write a Conventional Commit from a Git diff in the language established by the project.
---

# Commit Message

Generate Conventional Commits that follow the project's language conventions, defaulting to Simplified Chinese when the language cannot be determined. Generate a message only by default; run `git commit` only when the user explicitly asks. Preserve unrelated dirty-worktree changes and split commits by atomic intent.

## Mode Gate

Determine the user's intent first:

- `MESSAGE`: generate a message without changing Git state.
- `COMMIT`: stage and commit local changes, optionally as multiple atomic groups.
- `REVERT`: generate or execute a `revert` commit.

Do not commit, push, force-push, reset, pop a stash, delete files, or bypass hooks unless the user explicitly requests the corresponding action. For investigation-only requests, report the result and stop.

## Collect Facts

Read these facts in parallel when possible:

```bash
git rev-parse --show-toplevel
git status --short
git diff --cached --stat
git diff --cached
git diff --stat
git diff
git branch --show-current
git log -30 --no-merges --pretty=format:'%h%x09%s'
```

From the repository root to the current directory, read applicable `AGENTS.md` files. Inspect existing `CONTRIBUTING*`, `README*`, `.github` documentation, and commit configuration for explicit commit-language rules. Do not infer the commit language from the technology stack or the language used in ordinary documentation.

A failed query means only that the fact is unavailable; it proves nothing. Read the full diff, not only filenames.

## Choose the Language

Choose one language in this order:

1. The user explicitly selects a language in the current request.
2. Applicable project instructions or configuration explicitly define the commit language.
3. After removing Conventional Commit prefixes, code identifiers, and issue numbers from the latest 30 non-merge commits, one language accounts for more than half of recognizable subjects.
4. If no explicit rule exists, history is insufficient, or no language has a majority, use Simplified Chinese.

Explicit project rules override historical convention. Use the chosen language for the explanatory text in the subject, body, and footer; preserve Conventional Commit tokens such as `type`, `scope`, `BREAKING CHANGE:`, and `Closes`.

## MESSAGE Mode

When the index contains changes, use staged changes as the only source. Mention unstaged and untracked files only as risks; do not include them in the message.

When the index is empty:

- If the user asks only for a message, it may be based on the unstaged diff. The final output must still contain only the commit message.
- If `??` untracked files exist, read relevant content or confirm whether it belongs in the analysis.
- If the user asks to commit, enter `COMMIT` mode and stage only the requested scope.

Check whether the diff contains independent intents. When it can be split, generate one candidate message per atomic group without analysis, numbering, or headings. If the user explicitly requests one commit, choose the dominant intent for the header and put only necessary secondary details in the body.

Before returning, verify that the type is accurate, the scope is necessary and specific, the subject is concise, the body and footer appear only when needed, and no AI or tool attribution is present.

## COMMIT Mode

Commit only changes requested by the user and preserve unrelated dirty-worktree changes. Include all current changes only when the user gives a clear scope such as “commit everything.”

Atomic grouping:

- Group by behavior, module, and independent reversibility. Separate unrelated features, configuration, documentation, and test-only changes by default.
- Keep implementation with tests that directly verify it.
- Keep generated files with the source changes that produce them unless the user explicitly excludes them.
- Do not hide failed, unrelated, or unexplained changes in a broad commit.

Execution:

1. Divide the full diff into atomic groups. If the boundary cannot be determined safely, ask the user.
2. Stage each group by path or hunk without including unrelated files. When one file contains multiple intents, prefer `git add -p <file>`; if a hunk still mixes intents, use `git add -e` or split the edit instead of forcing one commit.
3. Before every commit, inspect `git diff --cached --stat` and enough of the staged diff to confirm that the index contains only the current group. After `git add -p` or `git add -e`, inspect both `git diff --cached` and `git diff` to verify the split.
4. Generate a Conventional Commit using the language rules above.
5. Use `git diff --cached --quiet` to detect an empty index. Do not create an empty commit unless the user explicitly requests `--allow-empty`.
6. Use `git commit -m` for a single line. For multiline messages, write a temporary file outside the repository and use `git commit -F <file>`.
7. After committing, inspect `git log -1 --oneline`.
8. Report the commit hash, message, and any files still uncommitted.

Never use `--no-verify` or push automatically. Store temporary commit-message files outside the repository and remove them after the commit.

## REVERT Mode

Use this fixed format:

```text
revert: <original subject>

This reverts commit <hash>.
```

If the target hash cannot be determined, ask the user instead of guessing. Confirm that the hash matches the user's intent before reverting.

## Output Rules

When the user asks only for a message, output plain commit-message text with no code fence or reasoning. For multiple atomic groups, output only the candidate messages separated by two blank lines. When the user requests a commit, briefly report the message and hash on success; on failure, report the cause and next step.

Format:

```text
<type>(<scope>): <subject>

<body>

<footer>
```

Only the header is required. Omit unused body or footer sections and their adjacent blank lines.

## Header

Choose a type from this list:

| type | Purpose |
| --- | --- |
| feat | Add user-visible functionality |
| fix | Correct a defect or erroneous behavior |
| refactor | Change internal structure without changing external behavior |
| perf | Deliver a verified performance improvement |
| style | Make formatting, whitespace, semicolon, or lint-only changes |
| docs | Change documentation |
| test | Add or modify tests |
| build | Change build systems, dependency management, or packaging |
| ci | Change CI/CD configuration |
| chore | Perform maintenance that does not affect product behavior |
| revert | Revert a commit |

The scope is optional. Prefer a component, page or module, directory, or specific business domain. Omit it for unrelated cross-module changes with no shared boundary. Do not use vague scopes such as `misc`, `common`, or `update`.

Write the subject naturally in the selected language using a concise imperative action and no ending punctuation. In Simplified Chinese, use an imperative verb-object phrase no longer than 50 Chinese characters and avoid filler words such as “了”, “的”, “的问题”, “进行”, “为了”, and “来”. Keep other languages concise and on one line.

## Body and Footer

Write only the header by default. Add a body only when omitting it would hide essential behavior, motivation, impact, or migration information that the subject cannot express. File count, diff size, and logic complexity alone do not justify a body; omit it when uncertain.

When a body is necessary, use `-` bullets. Every bullet must add information required to understand or use the commit and must not repeat the subject. Complex commits often need three to five bullets, but use only as many as necessary. Do not pad the list, enumerate files, or translate the diff line by line. Split the commit when essential information exceeds five bullets.

Put each bullet on its own line with real newline characters. Never join bullets on one line or output literal `\n` or `\\n` escapes in place of newlines. Commit multiline messages with `git commit -F <file>`, not `git commit -m` with escaped strings.

For an explicit incompatible change, start the footer with `BREAKING CHANGE:` and explain the impact and migration. Add `Closes #<ID>` only when the user, branch name, diff, or context explicitly supplies an issue number.

## Forbidden Content

Never include AI-agent, tool, or platform attribution, including `Co-Authored-By`, `Co-authored-by`, `Signed-off-by`, `Generated by`, `Powered by`, `Assisted by`, AI or bot links, `AI-generated`, or emoji watermarks. Do not add trailers unless the user explicitly requests them.

## Examples

```text
style(Button): 调整边框颜色
```

```text
docs: 更新部署文档
```

When project rules or commit history primarily use English:

```text
docs: update deployment guide
```

```text
fix(utils): 修复日期格式化异常

Closes #1024
```

```text
feat(api): 统一接口响应结构

BREAKING CHANGE: 响应体从 { data, code } 改为 { data, status, message }，调用方需要适配字段读取逻辑
```
