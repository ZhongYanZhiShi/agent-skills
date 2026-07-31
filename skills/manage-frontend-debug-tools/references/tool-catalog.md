# Project-Local Frontend Debug Package Catalog

Use this catalog only after detecting the framework, versions, package manager, workspace, existing
packages, and debugging need. Every candidate below can be retained in a target `package.json`.
Browser extensions, standalone apps, global installs, and framework-bundled/no-install panels are
deliberately excluded.

Package names and links are routing hints, not pinned versions. Verify current official docs, registry
metadata, compatibility, and Stars before every recommendation or mutation.

Stars snapshot: **2026-08-01**, queried from GitHub. `†` means the count belongs to a larger monorepo.
Stars are a popularity signal, never the selection rule.

## Contents

- [Selection order](#selection-order)
- [Recommended starting points](#recommended-starting-points)
- [React and Next.js](#react-and-nextjs)
- [Vue and Nuxt](#vue-and-nuxt)
- [Shared and dependency-specific packages](#shared-and-dependency-specific-packages)
- [Excluded for now](#excluded-for-now)
- [Package-manager patterns](#package-manager-patterns)
- [Refreshing Stars](#refreshing-stars)
- [Update rules](#update-rules)

## Selection Order

Stop at the first option that handles the stated need:

1. Reuse an existing project package or script.
2. If built-in browser or framework capabilities are sufficient, recommend no package installation.
3. Add one framework-specific project package for the missing signal.
4. Add one dependency-specific package only when its parent library is already present.
5. Add a test harness only when the problem requires it.

Do not install a baseline bundle merely because a framework was detected.

## Recommended Starting Points

| Detected stack or need | Project-local starting point | Add only when | Default decision |
| --- | --- | --- | --- |
| React or Next.js, repeatable static diagnostics | `react-doctor` | The team wants a pinned local command or package script | No universal baseline package |
| React UI-to-source context for an agent | `react-grab` via the official `grab` initializer | The initializer retains the package and development-only setup | Prefer over adding multiple source locators |
| React render performance | `react-scan` | A concrete performance issue exists | Add why-did-you-render only for deeper cause analysis |
| Vue 3 with Vite 6+ | `vite-plugin-vue-devtools` | Add `vue-tsc` for TypeScript SFC diagnostics | Preferred persistent Vue inspector |
| Nuxt | No baseline package: current Nuxt DevTools is bundled and out of scope | `vue-tsc` or a shared package for a distinct need | Do not add duplicate DevTools |
| Interaction or test failure | Existing Vitest setup, then `@vitest/ui`; otherwise existing Playwright setup | Add the missing focused test package only for a repeatable workflow | Do not scaffold both by default |

## React and Next.js

| Priority | Need | Package | Project install / integration | GitHub Stars | Recommendation |
| --- | --- | --- | --- | ---: | --- |
| Need-based | Repeatable static code-health scans | [`react-doctor`](https://www.react.doctor/docs/reference/cli-reference) | Add as a development dependency and run the local binary or package script; never invoke its broad `install` path by default | [⭐ 14,214](https://github.com/millionco/react-doctor) | Use only when a pinned, updateable project command is wanted; otherwise no persistent package is needed. |
| Need-based | Select rendered UI and copy source context for an agent | [`react-grab`](https://www.react-grab.com/) | Run the official `grab` initializer, inspect its diff, and require `react-grab` to remain in the target manifest | [⭐ 7,480](https://github.com/aidenybai/react-grab) | Best match for agent-assisted UI work; keep the integration development-only. |
| Need-based | Detect React render hot spots | [`react-scan`](https://github.com/aidenybai/react-scan) | Add as a development dependency and wire the smallest development-only integration, or use the official initializer | [⭐ 21,725](https://github.com/aidenybai/react-scan) | Add for a concrete performance problem, not every React project. |
| Deep diagnosis | Explain which changing inputs trigger unnecessary renders | [`@welldone-software/why-did-you-render`](https://github.com/welldone-software/why-did-you-render) | Add as a development dependency and enable targeted development-only instrumentation | [⭐ 12,506](https://github.com/welldone-software/why-did-you-render) | Use after a render problem is confirmed and its cause remains unclear. |

Ordinary breakpoints need no package. For Next.js, reuse source maps and the existing browser or Node
debugger configuration and return “no project package needed.”

## Vue and Nuxt

| Priority | Need | Package | Project install / integration | GitHub Stars | Recommendation |
| --- | --- | --- | --- | ---: | --- |
| Preferred for Vue 3 + Vite 6+ | Components, reactivity, events, routing, and source inspection | [`vite-plugin-vue-devtools`](https://devtools.vuejs.org/guide/vite-plugin) | Add as a development dependency and register `vueDevTools()` once in Vite config | [⭐ 2,876](https://github.com/vuejs/devtools) | Default persistent Vue inspector when compatible; its component inspector avoids another locator package. |
| Need-based for TypeScript | SFC and template type diagnostics | [`vue-tsc`](https://github.com/vuejs/language-tools) | Add as a development dependency and reuse or add one focused typecheck script | [⭐ 6,697](https://github.com/vuejs/language-tools) | Static diagnostics companion, not a runtime panel; verify Vue and TypeScript compatibility. |

For Nuxt, the bundled DevTools do not meet this catalog's “installed project package” rule. Recommend
no baseline package instead of adding a duplicate. Vue 2 also has no default eligible package here;
report the compatibility boundary.

## Shared and Dependency-Specific Packages

Install these only when the detected dependency or debugging problem calls for them.

| Applies when | Package | Project install / integration | GitHub Stars | Recommendation |
| --- | --- | --- | ---: | --- |
| React already uses TanStack Query | [`@tanstack/react-query-devtools`](https://tanstack.com/query/latest/docs/react/devtools) | Add with the dependency class required by the existing build and wire once near the Query client root | [⭐ 50,028†](https://github.com/TanStack/query) | Inspect query cache and mutations; never add TanStack Query solely for DevTools. |
| Vue already uses TanStack Query | [`@tanstack/vue-query-devtools`](https://tanstack.com/query/latest/docs/framework/vue/devtools) | Add with the dependency class required by the existing build and wire one panel | [⭐ 50,028†](https://github.com/TanStack/query) | Avoid duplicate panels and require the parent Vue Query package. |
| Project already uses Vitest | [`@vitest/ui`](https://vitest.dev/guide/ui.html) | Add as a development dependency at the exact compatible Vitest version; run the local `vitest --ui` | [⭐ 16,888†](https://github.com/vitest-dev/vitest) | Add only for interactive test inspection. |
| Reproducible browser flow or CI trace | [`@playwright/test`](https://playwright.dev/docs/debug) | Add as a development dependency, reuse config, and install only required browser binaries | [⭐ 93,764](https://github.com/microsoft/playwright) | Preferred for intermittent interaction and end-to-end failures. |
| Repeated isolated component, visual, or accessibility work | [Storybook packages](https://storybook.js.org/docs) | Use the official initializer, inspect its broad scaffold, and require resulting dependencies in the manifest | [⭐ 90,724](https://github.com/storybookjs/storybook) | Too large for one broken component; add only when a persistent workbench pays off. |

Pinia state is already exposed by Vue DevTools. Redux DevTools normally depends on a browser extension.
Do not add either as a separate project-package recommendation.

## Excluded for Now

| Tool or path | Why excluded |
| --- | --- |
| React Developer Tools browser extension or standalone app | Not retained as a target project dependency |
| Vue DevTools browser extension or standalone app | Use only the eligible Vite plugin in this skill |
| Redux DevTools browser extension | Requires a browser extension rather than a self-contained project package |
| Current built-in Nuxt DevTools | No package installation is needed |
| One-off `npx react-doctor@latest` scan | The package is transient; use the local `react-doctor` dependency only when persistence is requested |
| Global `react-devtools`, CLI, or package-manager installs | Global state is outside the project and cannot be reliably audited from its manifest |

## Package-Manager Patterns

Use the repository's exact package manager and target workspace. Confirm workspace syntax with the
installed manager version.

| Action | npm | pnpm | Yarn | Bun |
| --- | --- | --- | --- | --- |
| Add development package | `npm install -D <package>@<version>` | `pnpm add -D <package>@<version>` | `yarn add -D <package>@<version>` | `bun add -d <package>@<version>` |
| Add runtime package | `npm install <package>@<version>` | `pnpm add <package>@<version>` | `yarn add <package>@<version>` | `bun add <package>@<version>` |
| Run retained local binary | `npm exec -- <binary>` | `pnpm exec <binary>` | `yarn exec <binary>` or the repository's script | `bunx --no-install <binary>` when supported, otherwise a script |

An initializer may itself run through `npx`, `pnpm dlx`, `yarn dlx`, or `bunx`, but it is eligible only
when the resulting debugging package is retained in the target manifest. Follow official integration
guidance for dependency type; build-time imports are not automatically safe in `devDependencies` for
every deployment model.

## Refreshing Stars

Run the bundled script with only shortlisted repositories:

```sh
node <skill-directory>/scripts/github-stars.mjs --json \
  millionco/react-doctor aidenybai/react-grab aidenybai/react-scan
```

The script uses the public GitHub REST API and optionally reads `GITHUB_TOKEN` or `GH_TOKEN`. If it
cannot run, query official GitHub repository pages or API directly. Report the exact count and date;
use `—` instead of an old estimate when current data cannot be verified.

## Update Rules

1. Compare declared range, lockfile version, registry release, peer dependencies, and engine requirements.
2. Update only direct packages named by the decision; never run a repository-wide dependency update.
3. Preserve stable channels and the repository's exact/range/catalog convention.
4. Re-run scaffolders only when current official docs define that as the supported upgrade path.
5. If a framework bundles the capability, recommend no package; do not upgrade the framework to obtain it.
6. Run the smallest affected validation and inspect the scoped manifest, lockfile, and config diff.
