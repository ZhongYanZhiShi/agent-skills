---
name: audit-project
description: Use when reviewing an entire project or codebase, or assessing repository-wide code health, technical debt, dead or deprecated code, performance, UI/UX, refactoring opportunities, and overall quality in React/Next.js, Vue/Nuxt, Node.js, or monorepos. Do not use for a Git diff, one component or file, or a single localized concern.
---

# Full Project Audit

## Core Principles

- Treat the coverage ledger as the source of truth for completion. Never substitute sampling, impressions, or context exhaustion for full coverage.
- Read-only means no changes to the audited project, persistent user state, or external business state. Temporary evidence and the coverage ledger may be written to the system temporary directory. Do not install or upgrade dependencies or switch, overwrite, revert, or clean the worktree.
- This skill reports findings only. Do not expand it into repairs; code changes or persistent reports require explicit user authorization.
- Inspect project scripts and configuration before running them. Execute only commands confirmed to be safe, non-interactive, and directly relevant.
- Do not read `.env*`, keys, or certificates. Do not inspect, read, or output login state or browser caches by default. With explicit authorization, Playwright may use only `.playwright/user-data` inside the project, and the agent still must not read or disclose its contents directly.
- Support definitive findings with reproducible evidence. Downgrade weak findings to investigation items or remove them.
- Distinguish “complete” from “partially complete.” Any pending review or investigation, scan-only unit, blocker, or applicable but unfinished runtime validation means the audit is partially complete.

## Conditional References

Read these two core contracts first:

- Use the [audit matrix](references/audit-matrix.md) to assign dimensions and determine whether each is complete.
- Use the [report contract](references/report-contract.md) to calculate coverage, record findings, and determine run status.

Load specialist references only after detecting the matching project shape:

- React or Next.js: [React and Next.js reference](references/framework-react-next.md).
- Vue or Nuxt: [Vue and Nuxt reference](references/framework-vue-nuxt.md).
- Standalone Node.js backend, service, or package: [Node.js reference](references/framework-node.md).
- Workspace or multi-package repository: [Monorepo reference](references/monorepo.md).
- Any frontend application in full scope: [UI runtime review reference](references/ui-runtime-review.md). Skip it only when the user explicitly excludes UI and disclose the scope change.

Do not load specialist references unrelated to the current project.

## Eight-Step Control Flow

### 1. Freeze the Snapshot

1. Locate the repository root and read the user scope, repository and path instructions, and necessary project documentation.
2. Use the current filesystem state by default, including relevant tracked modifications and untracked files. If the user specifies a commit, branch, or directory, audit that scope without switching or overwriting the worktree.
3. Record audit time, root, scope, current branch, commit, and initial worktree state. For non-Git projects, record the detected root and scope boundaries.
4. Exclude generated, cached, and large irrelevant directories such as `node_modules`, `dist`, `build`, `.next`, `.nuxt`, `.output`, `coverage`, Playwright reports, test results, and package-manager caches.
5. Ignore `.svg` unless explicitly in scope. Always exclude sensitive files and login-state directories from file search and semantic review. Playwright may use project login state only with explicit authorization through a persistent context; never inspect those files directly.

**Completion gate:** record a reproducible snapshot identifier, included scope, exclusions, and initial worktree state.

### 2. Build the Project Map and Coverage Ledger

1. Identify package managers, workspaces, applications, packages, frameworks, entry points, routes, server boundaries, tests, build configuration, database boundaries, and deployment configuration.
2. Create review units for production source, shared libraries, framework entry points, tests, quality gates, configuration, scripts, code-generation entry points, schemas, migrations, routes, pages, APIs, manifests, lockfiles, and architecture documentation.
3. For each unit, record: scope disposition (`included` or `excluded` with reason); review method (`not started`, `semantic review`, `deterministic tool validation`, or `scan only`); and a `unit × applicable dimension` substatus (`pending`, `complete`, `not applicable`, or `blocked`).
4. Derive one display status from those facts: excluded units are `excluded`; included units with any blocked dimension are `blocked`; fully closed units become `semantic review complete` or `tool validation complete` based on method and type; scan-only units are `static scan only`; all others are `pending`. Do not maintain another independently editable overall status.
5. A source, test, configuration, or documentation unit counts as semantically complete only when every applicable dimension is `complete` or has a specific `not applicable` reason. Pending or blocked dimensions never count toward qualified coverage.
6. Semantically review source, tests, configuration, and documentation. Use full-content deterministic tools only for machine-generated structured units such as lockfiles. Text search is not tool validation, and tool validation cannot replace source-code semantic review.
7. Record reasons for exclusions and blockers. Store the ledger in the system temporary directory; ask the user before persisting it across tasks.
8. If one context cannot reliably cover every unit, divide the repository into non-overlapping, exhaustive batches by workspace, domain, or module and update the ledger after each batch. Never sample silently.

**Completion gate:** the map covers root configuration and every workspace; each unit has a scope disposition; each included required unit has a method, batch, complete dimension substatuses, and reproducible derived status; no completed unit has an open substatus.

### 3. Run Safe Diagnostics

1. Determine the existing package manager from lockfiles and prefer project-defined lint, typecheck, test, and build commands.
2. Before running a script, inspect its command and related configuration for network use, source or business-data writes, snapshot updates, external services, database migrations, or lifecycle hooks.
3. Run only commands confirmed to be safe, non-interactive, directly relevant, and unable to write to the target project, persistent user state, or external business state. Obtain explicit authorization before any command that may create build artifacts, caches, snapshots, browser profiles, or other persistent files; otherwise mark it blocked.
4. Never install or upgrade dependencies, connect to production, or run migrations, seeds, releases, or scripts that may write business data. Start a development server only after confirming it binds to `localhost` or `127.0.0.1` and cannot load production configuration or connect to production. Project-directory writes still require authorization.
5. For authorized writes, compare worktree state before and after and disclose changed paths. Do not delete pre-existing content or silently clean generated output.
6. Classify failures as code, environment, or missing-dependency failures. Record the command, exit status, and reproducible error summary. Provide progress updates as required by the host and stop only after confirmed timeout or lack of progress.

**Completion gate:** record either a result or a reason for not running every applicable diagnostic. Unsafe, unauthorized, blocked, missing, or incomplete validation enters the ledger and forces partial completion.

### 4. Assign Work Packages

1. Use the audit matrix to assign all ten dimensions; record a specific reason for each inapplicable dimension.
2. When subagents are available, combine independent read-only reviews into three or four packages and execute them in waves. Do not create ten agents mechanically. Without subagents, process the same boundaries sequentially.
3. Default packages: architecture, correctness, and data boundaries; maintainability, dead code, and dependencies; performance, UI/UX, and accessibility; tests, builds, observability, and security baseline.
4. Require every package to return `unit × applicable dimension` substatuses, dimension status, candidate findings, evidence locators, and unverified items. Reject vague summaries.
5. The primary agent owns the coverage ledger, checks overlap and omissions, validates across packages, deduplicates, and decides final status.

**Completion gate:** every required unit and applicable dimension has an owner and returned status, with no unassigned scope.

### 5. Run UI Validation

1. Apply only to frontend projects. Inventory every route and statically review pages, layouts, state components, and critical flows first.
2. When the project can run safely, its server listens only locally, and required project writes are authorized, use Playwright's bundled Chromium for smoke validation of accessible routes and deep interaction checks of core flows. Do not use system Chrome.
3. Default to headless mode, a `1280x720` viewport, and concurrency 1, plus at least one common mobile viewport. Check reachable success, loading, empty, error, and disabled states, keyboard operation, and the basic accessibility tree.
4. Login state requires explicit authorization to create or update persistent browser data. Use only `.playwright/user-data` under the project root. If `.playwright/` is not ignored, obtain separate authorization before changing `.gitignore`. Without authorization, mark those runtime checks blocked and never use the system browser profile.
5. Do not take full-page screenshots. Close pages and contexts at the end. Record routes blocked by dynamic parameters, permissions, data, backend availability, or sandbox restrictions.

**Completion gate:** report route inventory, runtime smoke coverage, and core-flow coverage. Static-only UI review, partial runtime validation, or blocked routes force partial completion.

### 6. Validate Findings

1. Complete the report-contract fields for every candidate: evidence locator and type, impact, recommendation, and verification method.
2. A deterministic, single-file static chain that proves causality and excludes reasonable alternatives can close semantic review; static evidence is not automatically blocked.
3. Cross-file, runtime, framework-behavior, or quantitative claims that require measurement need a second independent source such as a call chain, configuration, test, build output, browser behavior, or current official documentation. Mark explicitly applicable but unfinished runtime or measurement validation as blocked.
4. Do not classify convention-based entry points, auto-imports, dynamic imports, plugin registration, reflection, generated code, or public package exports as dead code merely because static references are absent.
5. Classify dead-code findings as confirmed, high probability, or investigation required. Use confirmed only after excluding conventions, dynamic use, and public APIs. Any retained investigation item is unresolved and forces partial completion.
6. Label unmeasured performance, bundle-size, and runtime benefits as static inference, never measured improvement.
7. For versions, deprecated APIs, framework behavior, and migrations, query current official documentation matching the project's version, preferably through Context7. If unavailable, use current official docs. Record source and applicable version; lower confidence when verification is impossible.
8. Perform only a security baseline. Do not call it a deep security audit, read sensitive files, or conduct offensive validation. Route deep audits to a dedicated security skill.

**Completion gate:** every definitive finding satisfies the common field and evidence requirements. Weak items remain investigation items or are removed. Any retained investigation item limits the audit to partial completion.

### 7. Merge and Prioritize

1. Merge package results by root cause and remove duplicates expressed through different files, dimensions, or symptoms.
2. Use P0–P3 for defects and risks. Rank optimizations and refactors by benefit, confidence, S/M/L cost, and regression risk.
3. Separate usability and accessibility defects from aesthetic suggestions; do not present preference as defect.
4. Assign each result to `fix now`, `low cost / high value`, `planned refactor`, or `defer / investigate`.
5. Preserve traceability from findings to review units, dimensions, and evidence.

**Completion gate:** every finding has a unique ID with consistent priority, confidence, cost, regression risk, and action tier.

### 8. Report and Determine Completion

1. Return structured Markdown in the conversation by default. Write a report to the target repository only when the user explicitly asks.
2. Follow the report contract: executive summary; project and workspace map; coverage and blind spots; command results; prioritized findings; action roadmap; residual risks; and unverified items.
3. State `complete` or `partially complete` at the beginning and keep it consistent with the ledger.
4. Mark complete only when every required unit qualifies, every applicable dimension and diagnostic or runtime validation is complete, every finding is validated and deduplicated, and every blind spot is disclosed.
5. Any pending review or investigation, scan-only unit, blocker, environment failure, missing dependency, unfinished command, or incomplete runtime check means partially complete. List remaining batches, blockers, and how to continue.
6. If the report is too long, return counts, coverage status, and highest-priority summary first, then ask whether to save the full report or continue in batches. Never truncate silently or keep only the top findings.
7. If there are no validated findings, say “No reportable issues found” while retaining coverage, command, and blind-spot information.

**Completion gate:** fields and counts reconcile, status can be recomputed from the ledger, and static inference, blockers, and security baselines are not overstated as measured completion.

## Handling Blockers

- Missing dependencies: do not install; continue static review, record skipped commands, and mark partially complete.
- Timed-out or stalled command: stop it, record covered scope and failure class, and provide the continuation command.
- Browser sandbox restriction: fall back to static UI review plus safe type, test, or build validation and mark partially complete.
- Partially verifiable monorepo: record each workspace separately; success elsewhere does not make the whole repository complete.
- Weak evidence: downgrade to investigation or remove the finding. Retained investigation items force partial completion.
- Lost temporary ledger: regenerate it from the project map; never reconstruct completion from memory.

## Completion Checklist

Declare complete only when every item is true:

- [ ] Snapshot, scope, and initial worktree state are frozen and recorded.
- [ ] The ledger covers all workspaces, review units, routes, and dimensions.
- [ ] Every required unit and `unit × applicable dimension` substatus is closed, with no pending, scan-only, or blocked item.
- [ ] Every applicable dimension is complete and every inapplicable one has a reason.
- [ ] Every applicable diagnostic and runtime validation is complete and reported, with none skipped for safety, authorization, or environment limitations.
- [ ] Every candidate finding is validated, deduplicated, and report-contract compliant, with no retained investigation item.
- [ ] Exclusions, failure classes, blind spots, and worktree state before and after commands are disclosed.

If any item is false, report `partially complete`.

## Common Failures

- Do not treat file inventories, text searches, or static scans as completed semantic review.
- Do not equate missing static references with dead code, especially for Nuxt convention entry points, dynamic plugins, and public package exports.
- Do not run tests, builds, migrations, code generation, or other project commands before inspecting their scripts.
- Do not claim full-repository coverage after sampling or silently drop remaining batches when context is limited.
- Do not use one successful workspace, one passing command, or static UI inspection as proof of overall completion.
- Do not describe performance inference as measured gain or a security baseline as a deep security audit.
- Do not omit evidence type, confidence, cost, regression risk, or verification method, and keep reported counts consistent with actual findings.
