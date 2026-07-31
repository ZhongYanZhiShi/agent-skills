---
name: manage-frontend-debug-tools
description: >
  Detect React, Next.js, Vue, Nuxt, and Vite projects, then compare, recommend, install, update,
  configure, and verify project-local debugging packages. Use for repeatable tools recorded in a
  target package.json, such as React Doctor, React Grab, React Scan, why-did-you-render,
  vite-plugin-vue-devtools, vue-tsc, query devtools, Vitest UI, Playwright, or Storybook. Excludes
  browser extensions, standalone apps, global installs,
  framework-bundled panels, and one-off packages that are not persisted in the project.
---

# Manage Frontend Debug Tools

Build the smallest useful project-local debugging toolkit for the detected application. A tool is in
scope only when it is or will be declared in the target project's `dependencies` or `devDependencies`.
An initializer is eligible only when its resulting project dependency and configuration are retained.

## 1. Determine Mode and Scope

Infer one mode:

- **Advise or audit:** inspect and recommend without changing files.
- **Install or set up:** add only packages directly justified by the need and complete their minimum
  configuration.
- **Update or refresh:** update only matching packages already present or explicitly named.

If mutation intent is unclear, remain read-only and show proposed packages and commands. Permission to
install or update includes the target manifest, lockfile, and minimum project configuration. It does
not include framework upgrades, CI, Git hooks, or broad dependency updates.

Keep these outside this skill's current scope:

- browser extensions and standalone DevTools applications;
- global npm, pnpm, Yarn, or Bun installs;
- framework-bundled panels that add no project dependency, such as current Nuxt DevTools;
- transient `npx`, `pnpm dlx`, `yarn dlx`, or `bunx` runs whose package is not retained.

If an excluded tool would be the only sensible answer, report that no eligible project package is
needed. Do not install an inferior package merely to satisfy the scope.

Use the repository or path named by the user; otherwise use the current project. Before mutation, run
`git status --short` when Git is available and preserve unrelated changes.

## 2. Map the Project

Inspect the nearest `package.json`, workspace root manifest, workspace declarations, lockfiles, and
framework configuration.

1. Detect the package manager from the root `packageManager` field, then the authoritative lockfile:
   `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, or `bun.lock`/`bun.lockb`. Never create a second
   lockfile.
2. Confirm React from dependencies such as `react`, `react-dom`, `next`, or `@remix-run/react`, plus
   config or source entry points. Confirm Vue from `vue`, `nuxt`, `@vitejs/plugin-vue`, `.vue` files,
   and config. Do not infer a framework from a directory name alone.
3. Record framework, build tool, major versions, scripts, runtime boundaries, and existing debugging,
   test, query, and state packages.
4. In a monorepo, map each frontend application and install into its owning workspace. Use the root
   only when that class of dependency is already centralized there.
5. Preserve pnpm catalogs, Yarn constraints or resolutions, npm overrides, workspace protocols, and
   the repository's exact dependency-range convention.

If no supported frontend is found, stop and report the evidence.

## 3. Match Need to Package

Classify the request or symptom:

- static React diagnostics;
- selecting rendered UI and locating React source for a developer or agent;
- render performance or unnecessary re-renders;
- Vue components, reactivity, events, routing, or source inspection;
- Vue SFC and template type diagnostics;
- query-cache state;
- interactive unit-test debugging;
- reproducible browser flows and traces;
- isolated component, visual, or accessibility work.

Read [the tool catalog](references/tool-catalog.md) before recommending or changing packages. Use only
the detected framework and matching need. Verify current official docs, registry metadata, peer
dependencies, and engine requirements at execution time; current evidence overrides the catalog.

For comparisons, refresh GitHub Stars only for shortlisted repositories:

```sh
node <skill-directory>/scripts/github-stars.mjs --json owner/repository ...
```

If the script is unavailable, query the official GitHub API or repository pages. Record the query date,
mark monorepo-level counts with `†`, and use `—` when no dedicated repository exists. Stars indicate
popularity, not compatibility or quality.

Prefer an existing eligible package. Otherwise recommend at most one package per distinct need. There
is no universal React or Vue package bundle: if the project has no stated debugging need, recommend no
installation.

## 4. Install or Update Safely

Before mutation, query the selected package's current registry metadata and official compatibility.
Do not upgrade React, Vue, Next.js, Nuxt, Vite, Node.js, or the package manager to accommodate it; pick
a compatible package version or report the constraint.

- Use the repository's package manager and workspace syntax.
- Add a project package with the same dependency type and version-range convention used by the project.
- For scaffolders such as React Grab, inspect `--help`, use a preview when available, and require the
  result to retain the intended package in `package.json`.
- For updates, name only the selected packages. Never run an unscoped `update`, `upgrade`, or dependency
  rewrite.
- Re-run an initializer only when current official docs define it as the supported update path.
- Wire only the configuration required to expose the package. Keep panels and instrumentation
  development-only.

When React Doctor is selected, install `react-doctor` as a project-local development dependency only
for repeatable, versioned scans. Run its scan command through the local package runner or a package
script. Never run `react-doctor install`, `ci install`, or hook setup unless the user separately expands
the scope.

After each package-manager or initializer command, inspect the target manifest, lockfile, and relevant
configuration diff. Stop on unexplained unrelated churn or compatibility conflicts.

## 5. Verify

Run the smallest checks that prove the change:

1. Confirm the intended package and version resolve in the target workspace and are recorded in its
   manifest.
2. Confirm no second lockfile, duplicate plugin, provider, wrapper, script, or panel was created.
3. Run the package's local `--help`, diagnostic command, or nearest affected typecheck, test, or build.
4. For a runtime panel or overlay, start the existing development command and verify the app loads and
   the tool exposes the intended signal when practical.
5. Inspect the final scoped diff and confirm no unrelated package or framework was upgraded.

## Output

Report:

1. mode and target workspace;
2. detected framework, versions, package manager, and evidence;
3. a Markdown table grouped by React, Vue, and shared packages as applicable, with columns `Priority`,
   `Need`, `Package`, `Project install / update`, `GitHub Stars`, and `Decision`;
4. packages, configuration, and commands changed or proposed;
5. verification results;
6. skipped packages, exclusions, compatibility constraints, and remaining risks.

Show only the detected framework by default. Show separate React and Vue tables for a cross-framework
comparison or a repository containing both. Put `Stars checked: YYYY-MM-DD` beside the tables, link
each count to its repository, and explain `†`. Distinguish **recommended**, **installed**, **updated**,
**already current**, and **skipped** so the result never implies work that was not completed.
