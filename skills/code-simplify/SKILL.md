---
name: code-simplify
description: >
  Review, simplify, and clean up code changes with emphasis on reuse, maintainability, and runtime efficiency.
  Use after implementation, refactoring, bug fixes, or feature work for pre-commit quality checks. Triggers include
  "simplify code", "cleanup", "clean up", "optimize my code", "review my changes", "review the diff",
  "code review", "check code quality", and "audit changes". If the user asks only for a review, report findings
  without editing. Modify files only when the user explicitly asks to fix, clean up, simplify, or optimize.
---

# Code Simplify

Review and simplify existing code changes with emphasis on reuse, maintainability, and efficiency. First decide whether the user wants review only or direct cleanup. Edit files only when the user explicitly requests cleanup, simplification, optimization, or a fix, or when the context clearly indicates pre-commit cleanup.

## 1. Determine Mode and Scope

Read the current context and the user's wording:

- Review mode: when the user asks to review, audit, check a diff, or assess quality, report findings first and do not edit.
- Cleanup mode: when the user asks to clean up, simplify, optimize, fix, prepare changes for commit, or finish an implementation, review and then apply only the minimum necessary changes.

Start scope collection with `git status --short`. Read `git diff` and `git diff --cached` for tracked files; use `git diff HEAD` when all tracked changes must be covered. For untracked files, use `git ls-files --others --exclude-standard`, then read only candidates within the user's scope or recent editing context. If the user supplies a path, patch, or diff, use that scope.

Do not include unrelated dirty-worktree changes in a fix. If there is no diff, no relevant untracked file, and no recently edited file, say there is nothing to review and stop.

## 2. Review Three Dimensions

The dimensions are independent. If the environment and authorization allow subagents, they may be delegated in parallel; otherwise review them sequentially. Never bypass host restrictions on subagent use.

### Reuse

Check whether new or modified code duplicates existing codebase capabilities. Search nearby files, `utils`, `lib`, `shared`, component libraries, service layers, type definitions, and existing tests first. Pay particular attention to handwritten string or path handling, environment checks, type guards, formatters, request wrappers, error handling, permission checks, query builders, and component variant logic.

When duplication exists, record the existing implementation, the duplicate, and the replacement. Recommend or apply reuse only when semantics match and migration cost is low.

### Quality

Look for maintenance-heavy patterns: derived values stored in state; `useState` plus `useEffect` used only to compute a value; parameter bloat; copied variants; leaking abstraction boundaries; raw strings instead of existing constants or unions; pointless JSX wrappers; over-coupled components or functions; and one-off logic written only to satisfy the current tests.

In React, when an effect only derives a value from dependencies and calls a setter, prefer inline computation or `useMemo`. Use `useMemo` only when computation is expensive, reference stability matters, or downstream memoization depends on it.

### Efficiency

Check repeated computation, file reads or network calls; N+1 queries; independent I/O serialized unnecessarily; blocking work in startup or request hot paths; unconditional state/store updates in polling or event callbacks; static objects or arrays rebuilt every render; leaked listeners and timers; unbounded caches; and check-then-act TOCTOU patterns.

For timers, polling, subscriptions, and external events, verify that unchanged data can reuse the previous reference or skip dispatch. For utilities wrapping updaters or reducers, verify that returning the same reference is not forced into a new object.

## 3. Handle Findings

Combine and deduplicate findings from all three dimensions before acting.

In review mode, list issues by severity with file, line, reason, and recommended fix. Do not edit files.

In cleanup mode, apply low-risk, clearly scoped fixes directly. Keep the diff minimal, avoid unrelated refactoring, and never delete files or revert the user's changes. Skip false positives, fixes whose cost exceeds their benefit, and changes that reduce readability; mention skipped items in the result.

## 4. Verify

After edits, run the project's available verification commands. Prefer diagnostics provided by the host; otherwise follow project conventions for lint, typecheck, tests, or builds. If the command is unclear, inspect scripts in `package.json`, `Makefile`, language configuration, or README. State why validation could not run when commands are absent, dependencies are missing, or the sandbox blocks execution.

## Output

In review mode, lead with findings, followed by a short summary and remaining risks. In cleanup mode, state what changed, what was skipped, and the validation result. If the code is already clean enough, say that no worthwhile changes were found.
