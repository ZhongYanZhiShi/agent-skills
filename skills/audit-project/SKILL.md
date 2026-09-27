---
name: audit-project
description: Use when auditing an entire React/Next.js, Vue/Nuxt, Node.js, or monorepo project for code health, risks, technical debt, performance, or UI/UX. Excludes diff reviews, individual components or files, and single localized concerns.
---

# Full Project Audit

## Boundaries and References

- Report findings without repairing code. Preserve the audited project, persistent user state, and external business state; temporary evidence may go in the system temporary directory. Reuse existing authorization for explicitly requested writes.
- Do not install or upgrade dependencies, switch or clean the worktree, read `.env*`, keys, certificates, login-state files, or browser caches. Authorized browser access follows the UI reference below.
- Use the [audit matrix](references/audit-matrix.md) for review dimensions and their required evidence. The [report contract](references/report-contract.md) is the sole definition of ledger fields, coverage formulas, finding fields, and completion status. Read both before building the ledger.
- Load specialist references only for the detected project shape: [React/Next.js](references/framework-react-next.md), [Vue/Nuxt](references/framework-vue-nuxt.md), [standalone Node.js](references/framework-node.md), and [monorepos](references/monorepo.md).
- For a frontend application, also read [UI runtime review](references/ui-runtime-review.md), unless the user explicitly excludes UI; disclose that scope change.

## 1. Freeze the Snapshot

1. Read the user's scope, applicable project instructions, and necessary architecture documentation.
2. Audit the current filesystem by default, including relevant tracked modifications and untracked files. Honor an explicit ref or directory without switching or overwriting the worktree.
3. Record time, root, scope, branch, commit, and initial worktree state. For a non-Git project, record root and scope boundaries. Use a snapshot identifier that also accounts for in-scope uncommitted content.
4. Exclude generated or cached output, package-manager caches, reports, large irrelevant directories, sensitive files, and login-state directories. Ignore SVG unless explicitly in scope. Record each exclusion.

**Gate:** the snapshot and included/excluded scope are reproducible.

## 2. Map the Project and Build the Ledger

1. Map packages, workspaces, frameworks, entry points, routes, server and database boundaries, tests, builds, and deployment configuration.
2. Inventory production source, shared code, tests, configuration, scripts, schemas, migrations, manifests, lockfiles, code-generation entry points, and architecture documentation as review units.
3. Record each unit using the report-contract fields. Keep semantic review progress separate from required command/runtime validation; classify candidate findings separately by evidence confidence.
4. Semantically read source, tests, configuration, and documentation. Full-content deterministic validation may cover machine-generated structured units such as lockfiles. Text search locates evidence but does not complete semantic review.
5. Keep the ledger in the system temporary directory. Persist elsewhere only when authorized. Split large scopes into exhaustive, non-overlapping batches and update the ledger after each; do not silently sample.

**Gate:** every workspace and required unit has a scope disposition, applicable dimensions, and a batch.

## 3. Run Safe Diagnostics

1. Identify the existing package manager and project-defined lint, typecheck, test, and build commands.
2. Inspect each command and its configuration for network use, source or business-data writes, snapshot updates, external services, migrations, and lifecycle hooks.
3. Run only safe, non-interactive, relevant commands. Commands that create project artifacts, caches, snapshots, browser profiles, or other persistent files need authorization covering those writes. Use existing authorization; otherwise record the blocked validation.
4. Never connect to production or run migrations, seeds, releases, or commands that may write business data. Start a development server only when it binds locally and cannot load production configuration or reach production services.
5. Compare worktree state before and after authorized writes. Disclose changed paths without deleting pre-existing content or silently cleaning output.
6. Record commands, exit status, and reproducible error summaries. Distinguish code failures from environment or missing-dependency failures. For a confirmed timeout or stalled command, stop it and record how to continue.

**Gate:** every applicable diagnostic has a recorded result or blocker.

## 4. Review the Work Packages

1. Assign all ten audit dimensions, recording reasons for inapplicable dimensions.
2. When subagents are available and authorized, group independent read-only work into three or four packages; otherwise use the same boundaries sequentially. Suggested groups: architecture/correctness/data; maintainability/dead code/dependencies; performance/UI/accessibility; tests/builds/observability/security baseline.
3. Require each package to return review substatuses, required-validation results, candidate findings, evidence locators, and unknowns.
4. The primary agent maintains the ledger, checks overlap and omissions, validates cross-package claims, and deduplicates findings.

**Gate:** every assigned batch has returned evidence and explicit remaining work.

## 5. Validate the UI

For frontend scope, inventory every route and statically review pages, layouts, states, and critical flows. Follow the UI reference for startup safety, browser choice, authorized login state, viewports, interaction checks, and cleanup. Record route-template smoke coverage and core-flow validation separately from source review; keep blocked routes in the ledger.

**Gate:** route inventory, runtime results, and missing evidence are recorded.

## 6. Validate and Prioritize Findings

1. Support each definitive finding with the report-contract fields. A deterministic, single-file causal chain that excludes reasonable alternatives can be sufficient. Cross-file, runtime, framework-behavior, or quantitative claims need an independent supporting source such as a call chain, configuration, test, browser behavior, measurement, or matching official documentation.
2. For dead-code claims, exclude convention entry points, auto-imports, dynamic loading, plugins, reflection, generated code, and public consumers. Classify the result as confirmed, high probability, or investigation required.
3. Preserve useful but inconclusive leads as investigation items with missing evidence and a next check. An investigation item alone does not mean the review is unfinished; any unmet required review or validation remains pending or blocked in the ledger.
4. Label unmeasured performance and bundle-size benefits as static inference. Verify version-sensitive behavior or migration advice against official documentation matching the project's version, using Context7 when available. Lower confidence when verification is unavailable.
5. Limit security work to a baseline; route deep audits to a dedicated skill. Do not read secrets or perform offensive validation.
6. Deduplicate by root cause. Use P0–P3 for defects and risks; rank optimizations and refactors by benefit, confidence, cost, and regression risk. Separate aesthetic preferences from usability/accessibility defects.

**Gate:** definitive findings satisfy evidence requirements; investigation items disclose uncertainty; every result has a unique ID and action tier.

## 7. Report

Follow the report contract to derive completion status and present coverage, required validation, and investigation items separately. Default to Markdown in the conversation; persist a report only when requested. Include remaining batches and continuation steps for blockers. If the temporary ledger is lost, regenerate it from the project map rather than inventing completion from memory.
