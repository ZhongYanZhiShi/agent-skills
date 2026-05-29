---
name: frontend-file-structure
description: Use when Codex needs to plan, review, or refactor frontend project file structure for React, Vue, Next.js, Nuxt, Vite, Remix, or similar web apps. Applies to component folders, hooks or composables, helpers, utils, constants, pages or routes, stores, barrel exports, path aliases, colocation decisions, and framework-specific routing conventions.
---

# Frontend File Structure

## 总览

使用这个技能为 React、Vue 及其上层框架项目建立清晰、可渐进迁移的文件结构。优先根据现有代码、框架约束和团队习惯做最小改动，而不是强行套用完整模板。

## 工作流

先读取项目事实，再提出结构建议。至少检查 `package.json`、`src`、`app` 或 `pages` 目录、TypeScript 或构建配置、路由目录、状态管理目录、已有导入别名、测试目录和主要组件组织方式。

先判断项目类型和框架约束。React 项目通常可从 `react`、`next`、`remix`、`react-router`、`.tsx`、`app` 或 `pages` 识别。Vue 项目通常可从 `vue`、`nuxt`、`@vitejs/plugin-vue`、`.vue`、`composables`、`views` 或 `pages` 识别。不要只凭单个文件名下结论；依赖、目录和入口文件要交叉验证。

判断项目当前主要采用哪种组织方式：按文件类型分组、按领域或功能分组、框架约束分组，还是混合结构。保留已经一致且可维护的局部约定，只整理造成查找困难、重复导入、跨层引用混乱、组件目录膨胀或框架约定被绕开的部分。

给出迁移方案时，先移动低风险、边界清楚的文件，再处理共享模块和别名。每一步都说明需要更新哪些导入路径、哪些测试或构建命令可以验证结果，以及如何回滚。

## 推荐结构

默认尊重项目已有应用根目录。普通 Vite、React Router 或 Vue Router 项目通常使用 `src`；Next.js App Router 可能使用根目录或 `src/app`；Nuxt 通常使用框架约定的根目录。按职责建立少量顶层目录，只创建真实需要的目录。

```text
src/
  components/
  hooks/ 或 composables/
  helpers/
  utils/
  stores/
  constants.ts
  pages/ 或 views/ 或 routes/ 或框架约定目录
```

将跨页面复用的通用 UI 放到 `components`。React 中跨多个功能复用的 Hook 放到 `hooks`；Vue 中跨多个功能复用的组合式函数放到 `composables`。将项目业务相关的纯函数放到 `helpers`。将跨项目也成立的通用函数放到 `utils`。将 Pinia、Redux、Zustand 等跨页面状态放到项目已有或约定的 `stores`、`store` 或 `state` 目录。将小型全局常量集中到 `constants.ts`；如果常量只服务于一个组件、页面或领域，优先就近放置。

不要提前创建空目录。只有当项目中已经出现对应职责的文件，或迁移步骤马上需要它时，才创建目录。

## React 组件目录

简单组件可以保留为单文件。复杂组件使用同名目录，并让目录名、主组件文件名和默认导入语义保持一致：

```text
components/
  FileViewer/
    FileViewer.tsx
    index.ts
    FileViewer.helpers.ts
    FileViewer.types.ts
    use-file-viewer.ts
```

`index.ts` 只暴露组件的公共 API。常见形式是：

```ts
export { default } from './FileViewer';
export * from './FileViewer';
```

如果主文件没有默认导出，不要在 `index.ts` 伪造默认导出。先检查项目偏好：有些代码库统一使用命名导出，有些组件库偏好默认导出。保持一致比套用单一规则更重要。

私有子组件、组件专属 hook、helper、类型和常量放在组件目录内。不要从组件目录外部导入这些私有文件；外部调用者只应经过该目录的公共入口。

## Vue 组件目录

简单 Vue 组件可以保留为单个 `.vue` 文件。复杂组件使用同名目录，并让目录名、主组件文件名和外部导入语义保持一致：

```text
components/
  FileViewer/
    FileViewer.vue
    index.ts
    FileViewer.helpers.ts
    FileViewer.types.ts
    use-file-viewer.ts
```

如果项目已使用 `script setup` 和自动导入组件，不要为了统一形式强行增加 `index.ts`。只有当组件目录需要稳定公共入口，或项目明确通过目录入口导入组件时，才使用 `index.ts`。

Vue 的组合式函数按项目约定放在组件目录内或 `composables`。只服务于一个组件的组合式函数留在组件目录内；被多个页面、组件或领域复用时再提升。Pinia store 通常放在 `stores`，但 Nuxt 项目要优先尊重 Nuxt 自动导入和目录约定。

## 就近放置与提升

先就近放置，再按真实复用提升。只被一个组件使用的逻辑留在组件目录内。被同一领域多个组件使用时，可以提升到该领域目录。被多个领域或页面使用时，再提升到顶层 `hooks`、`composables`、`helpers`、`utils`、`stores` 或 `components`。

提升前检查引用方向。底层通用模块不应依赖页面、路由或具体业务容器。若提升会引入循环依赖或让命名变得抽象，保持就近放置。

## 导入与别名

优先使用项目已经配置的导入风格。若相对路径频繁出现 `../../..`，建议配置或使用现有路径别名，例如 `@/components/Button`、`@/helpers/category.helpers`。

同时更新 TypeScript、bundler、test runner 和 lint 配置中的别名解析。不要只改 `tsconfig.json`，否则测试或运行时可能仍然失败。

谨慎使用宽泛 barrel 文件。目录级 `index.ts` 适合隐藏组件内部结构；全局聚合导出只在公共 API 边界明确时使用。避免让一个顶层 `index.ts` 导出整个应用，因为这会模糊依赖边界并增加循环依赖风险。

Vue 项目如果依赖 Nuxt、unplugin-auto-import 或 unplugin-vue-components 的自动导入，迁移时要同步检查自动导入配置和生成的类型文件。不要在不需要的地方新增手写导入，也不要让自动导入和手写 barrel 同时暴露同一批 API。

## 框架注意事项

React Router、Vue Router、Vite、Next.js、Nuxt、Remix 等框架都有自己的入口和路由约束。框架要求的文件名、默认导出、server/client 边界、自动导入和特殊目录优先于本技能的通用建议。

在 Next.js App Router 中，`app` 目录下的 `page.tsx`、`layout.tsx`、`loading.tsx`、`error.tsx` 等文件按框架约定保留。可在路由段内就近放置 `_components`、`components` 或私有模块，但不要破坏服务端组件与客户端组件边界。

在 Nuxt 中，`pages`、`layouts`、`components`、`composables`、`plugins`、`middleware`、`server` 和 `stores` 等目录有自动注册或运行时语义。不要将这些目录改成普通分层目录，也不要把只应运行在服务端的代码提升到客户端可导入的位置。

在普通 Vite React 或 Vite Vue 项目中，`src/main.tsx`、`src/main.ts`、`src/App.tsx`、`src/App.vue` 和路由入口应保持清晰。若项目使用 `views` 表示路由页面，不要强行改成 `pages`；若项目已经稳定使用 `pages`，也不要仅因 Vue Router 示例常见 `views` 而迁移。

## 输出要求

给用户建议时，用简洁的中文说明以下内容：

1. 当前观察：列出已读取的结构事实和主要痛点。
2. 框架判断：说明项目是 React、Vue 或混合项目，并列出判断依据。
3. 推荐结构：展示目标目录形态，只包含实际需要的目录。
4. 迁移步骤：按低风险到高风险排序，说明导入更新范围。
5. 验证命令：给出类型检查、测试、构建或 lint 命令。
6. 风险与回滚：说明可能破坏的别名、循环依赖、默认导出、自动导入和框架约束，以及如何回退。

如果用户只要求评审或建议，不要修改文件。只有用户明确要求实现、重构或迁移时，才执行文件编辑。
