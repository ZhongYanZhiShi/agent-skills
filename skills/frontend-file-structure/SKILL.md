---
name: frontend-file-structure
description: Use when Codex needs to plan, review, or refactor frontend project file structure for React, Vue, Next.js, Nuxt, Vite, Remix, or similar web apps. Applies to component folders, hooks or composables, helpers, utils, constants, pages or routes, stores, barrel exports, path aliases, colocation decisions, and framework-specific routing conventions.
---

# Frontend File Structure

## Overview

Use this skill to create a clear, incrementally adoptable file structure for React, Vue, and their frameworks. Prefer minimal changes based on the existing code, framework constraints, and team conventions instead of imposing a complete template.

## Workflow

Read project facts before recommending a structure. At minimum, inspect `package.json`; `src`, `app`, or `pages`; TypeScript or build configuration; routing and state-management directories; existing import aliases; tests; and the main component organization.

Identify the project type and framework constraints. React projects can often be recognized through `react`, `next`, `remix`, `react-router`, `.tsx`, `app`, or `pages`. Vue projects can often be recognized through `vue`, `nuxt`, `@vitejs/plugin-vue`, `.vue`, `composables`, `views`, or `pages`. Do not conclude from one filename; cross-check dependencies, directories, and entry points.

Determine whether the project primarily groups by file type, domain or feature, framework convention, or a hybrid. Preserve local conventions that are already consistent and maintainable. Reorganize only where navigation is difficult, imports are duplicated, layer boundaries are confused, component directories have become bloated, or framework conventions are being bypassed.

For migration plans, move low-risk files with clear boundaries first, then address shared modules and aliases. For every step, identify imports to update, tests or builds that verify the change, and a rollback path.

## Recommended Structure

Respect the project's current application root. Typical Vite, React Router, and Vue Router projects use `src`; Next.js App Router may use root-level `app` or `src/app`; Nuxt normally uses its framework-defined root. Create only the few top-level directories that current responsibilities require.

```text
src/
  components/
  hooks/ or composables/
  helpers/
  utils/
  stores/
  constants.ts
  pages/ or views/ or routes/ or framework-defined directories
```

Put general UI reused across pages in `components`. Put React hooks shared by multiple features in `hooks`, and Vue composables shared by multiple features in `composables`. Put project-specific pure business functions in `helpers`; put truly project-independent utilities in `utils`. Keep cross-page Pinia, Redux, or Zustand state in the project's existing `stores`, `store`, or `state` directory. Small global constants may live in `constants.ts`; constants used by only one component, page, or domain should stay colocated.

Do not create empty directories in advance. Create a directory only when matching files already exist or an immediate migration step needs it.

## React Component Directories

Simple components may remain single files. For complex components, use a same-named directory and align the directory name, main component filename, and default import semantics:

```text
components/
  FileViewer/
    FileViewer.tsx
    index.ts
    FileViewer.helpers.ts
    FileViewer.types.ts
    use-file-viewer.ts
```

Use `index.ts` only to expose the component's public API. A common form is:

```ts
export { default } from './FileViewer';
export * from './FileViewer';
```

Do not invent a default export in `index.ts` when the main file has none. Check project preference first: some codebases consistently use named exports, while some component libraries prefer defaults. Consistency matters more than one universal rule.

Keep private subcomponents, component-specific hooks, helpers, types, and constants inside the component directory. External callers should import only through the directory's public entry point.

## Vue Component Directories

Simple Vue components may remain single `.vue` files. For complex components, use a same-named directory and align the directory name, main component filename, and external import semantics:

```text
components/
  FileViewer/
    FileViewer.vue
    index.ts
    FileViewer.helpers.ts
    FileViewer.types.ts
    use-file-viewer.ts
```

If the project already uses `script setup` and component auto-imports, do not add `index.ts` merely for uniformity. Use it only when the directory needs a stable public entry point or the project imports components through directory entries.

Place Vue composables inside the component directory or `composables` according to project convention. Keep a composable used by one component local; promote it only after multiple pages, components, or domains reuse it. Pinia stores usually belong in `stores`, but Nuxt auto-import and directory conventions take priority.

## Colocation and Promotion

Colocate first and promote only after real reuse appears. Logic used by one component stays in its directory. Logic shared by several components in one domain may move to the domain directory. Promote to top-level `hooks`, `composables`, `helpers`, `utils`, `stores`, or `components` only when multiple domains or pages share it.

Check dependency direction before promotion. Low-level shared modules must not depend on pages, routes, or concrete business containers. Keep code colocated if promotion would introduce a cycle or require vague naming.

## Imports and Aliases

Prefer the project's configured import style. When relative imports repeatedly contain `../../..`, recommend an existing or new path alias such as `@/components/Button` or `@/helpers/category.helpers`.

Update alias resolution in TypeScript, the bundler, test runner, and lint configuration together. Updating only `tsconfig.json` may leave tests or runtime resolution broken.

Use broad barrel files carefully. Directory-level `index.ts` files are useful for hiding component internals; global aggregate exports are appropriate only at a clear public API boundary. Avoid a top-level `index.ts` that exports the entire application because it obscures dependencies and increases cycle risk.

For Vue projects using Nuxt, `unplugin-auto-import`, or `unplugin-vue-components`, inspect auto-import configuration and generated type files during migration. Do not add unnecessary manual imports or expose the same APIs through both auto-imports and handwritten barrels.

## Framework Considerations

React Router, Vue Router, Vite, Next.js, Nuxt, Remix, and similar frameworks define their own entry-point and routing constraints. Required filenames, default exports, server/client boundaries, auto-imports, and special directories take priority over this skill's general guidance.

In Next.js App Router, preserve conventional files such as `page.tsx`, `layout.tsx`, `loading.tsx`, and `error.tsx` under `app`. Route segments may contain colocated `_components`, `components`, or private modules, but must preserve server and client component boundaries.

In Nuxt, directories such as `pages`, `layouts`, `components`, `composables`, `plugins`, `middleware`, `server`, and `stores` have auto-registration or runtime semantics. Do not turn them into generic layer directories or promote server-only code into a client-importable location.

In standard Vite React or Vite Vue projects, keep `src/main.tsx`, `src/main.ts`, `src/App.tsx`, `src/App.vue`, and routing entry points clear. Do not rename stable `views` conventions to `pages`, or vice versa, merely because examples for another project use the other name.

## Output

Explain the following concisely in the user's language:

1. Current observations: structural facts read and the main pain points.
2. Framework assessment: React, Vue, or hybrid, with supporting evidence.
3. Recommended structure: the target tree containing only directories that are actually needed.
4. Migration steps: ordered from low to high risk, including affected imports.
5. Verification commands: typecheck, tests, build, or lint.
6. Risks and rollback: aliases, cycles, default exports, auto-imports, and framework constraints that could break, plus how to revert.

If the user asks only for review or recommendations, do not edit files. Edit files only when the user explicitly requests implementation, refactoring, or migration.
