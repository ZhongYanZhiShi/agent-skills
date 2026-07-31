---
name: manage-frontend-debug-tools
description: >
  自动识别 React、Next.js、Vue、Nuxt 和 Vite 项目，并比较、推荐、安装、更新、配置及验证项目本地调试包。
  适用于会写入目标 package.json 的可复用工具，例如 React Doctor、React Grab、React Scan、
  why-did-you-render、vite-plugin-vue-devtools、vue-tsc、查询 DevTools、Vitest UI、Playwright 或
  Storybook。不包含浏览器扩展、独立应用、全局安装、框架自带面板，以及不会
  持久化到项目的一次性包。
---

# 管理前端调试工具

为检测到的应用建立最小够用的项目本地调试工具集。只有已写入或将写入目标项目 `dependencies` 或
`devDependencies` 的工具才属于范围；脚手架只有在最终保留项目依赖和配置时才符合条件。

## 1. 判断模式与范围

根据请求判断模式：

- **建议或审查：**只检查和推荐，不修改文件。
- **安装或配置：**只添加需求直接需要的包，并完成最小配置。
- **更新或刷新：**只更新已经存在或用户明确点名的包。

若无法确定是否允许修改，保持只读并列出拟执行的包和命令。安装或更新权限只涵盖目标清单、锁文件和最小
项目配置，不包含框架升级、CI、Git Hooks 或批量依赖更新。

当前明确排除：

- 浏览器扩展和独立 DevTools 应用；
- npm、pnpm、Yarn 或 Bun 全局安装；
- 不新增项目依赖的框架自带面板，例如当前 Nuxt DevTools；
- 包不会保留到项目的临时 `npx`、`pnpm dlx`、`yarn dlx` 或 `bunx` 执行。

若排除项才是唯一合理方案，报告“不需要符合范围的项目包”，不要为了凑数安装更差的替代品。

优先使用用户指定的仓库或路径，否则使用当前项目。修改前在 Git 可用时运行 `git status --short`，保留所有
无关改动。

## 2. 建立项目地图

检查最近的 `package.json`、工作区根清单、工作区声明、锁文件和框架配置。

1. 先根据根清单的 `packageManager`，再根据唯一权威锁文件识别包管理器：`pnpm-lock.yaml`、
   `yarn.lock`、`package-lock.json` 或 `bun.lock`/`bun.lockb`。不能产生第二种锁文件。
2. 结合 `react`、`react-dom`、`next`、`@remix-run/react` 等依赖、配置和源码入口确认 React；结合
   `vue`、`nuxt`、`@vitejs/plugin-vue`、`.vue` 文件和配置确认 Vue。不能只凭目录名判断。
3. 记录框架、构建工具、主要版本、脚本、运行边界，以及已有调试、测试、查询和状态包。
4. Monorepo 中要识别每个前端应用，并安装到所属 workspace。只有仓库本来集中管理此类依赖时才放根目录。
5. 保留 pnpm catalogs、Yarn constraints/resolutions、npm overrides、workspace 协议及现有版本范围风格。

若没有识别到受支持的前端项目，报告证据后停止。

## 3. 将需求映射为包

把请求或现象归类：

- React 静态诊断；
- 在页面点选 UI，并为开发者或 Agent 定位 React 源码；
- 渲染性能或多余重渲染；
- Vue 组件、响应式状态、事件、路由或源码检查；
- Vue SFC 和模板类型诊断；
- 查询缓存状态；
- 交互式单元测试调试；
- 可复现浏览器流程和 Trace；
- 组件隔离、视觉或可访问性工作。

提出建议或修改前读取[工具目录](references/tool-catalog.md)，只使用已识别框架和需求对应的部分。执行时核对
当前官方文档、Registry 元数据、Peer Dependencies 和 Engines；当前证据优先于目录内容。

比较工具时，只刷新入围仓库的 GitHub Stars：

```sh
node <skill-directory>/scripts/github-stars.mjs --json owner/repository ...
```

脚本不可用时查询 GitHub 官方 API 或仓库页面。记录日期，Monorepo 级数字标 `†`，无独立仓库时填 `—`。
Stars 只表示流行度，不代表兼容性或质量。

优先复用已有且符合范围的包，否则每类实际需求最多推荐一个包。React 和 Vue 都没有必须安装的通用套餐；
没有明确调试需求时，建议不安装。

## 4. 安全安装或更新

修改前查询所选包的当前 Registry 元数据与官方兼容要求。不能为了调试包顺带升级 React、Vue、Next.js、
Nuxt、Vite、Node.js 或包管理器；应选择兼容版本或报告约束。

- 使用仓库现有包管理器和 workspace 语法。
- 沿用项目现有依赖类型和版本范围风格。
- React Grab 等脚手架先检查 `--help`，有预览时先预览，并确认结果把目标包保留在 `package.json`。
- 更新时只点名所选包，不能运行无范围的 `update`、`upgrade` 或依赖重写。
- 只有当前官方文档把重新运行脚手架定义为升级方式时才重跑。
- 只接入让包可用所需的配置，面板和插桩只在开发环境启用。

选择 React Doctor 时，仅为可复用、可固定版本的扫描把 `react-doctor` 安装为项目本地开发依赖，通过本地包
执行器或 package script 运行普通扫描。除非用户另行扩大范围，否则不能运行 `react-doctor install`、
`ci install` 或 Hooks 配置。

每次包管理器或脚手架命令后都检查目标清单、锁文件和相关配置 diff。若出现无法解释的无关变动或兼容冲突，
立即停止。

## 5. 验证

运行能证明改动有效的最小检查：

1. 确认目标 workspace 能解析到预期包和版本，且清单已记录该包。
2. 确认没有第二种锁文件、重复 Plugin、Provider、根包装、脚本或面板。
3. 运行该包的本地 `--help`、诊断命令，或最近的受影响 typecheck、test、build。
4. 对运行时面板或 Overlay，在可行时启动现有开发命令，确认应用能加载且工具能暴露目标信号。
5. 检查最终范围内 diff，确认没有升级无关包或框架。

## 输出

报告：

1. 模式和目标 workspace；
2. 检测到的框架、版本、包管理器和证据；
3. 按适用情况分为 React、Vue 和通用包的 Markdown 表格，列名为`优先级`、`需求`、`包`、
   `项目安装 / 更新`、`GitHub Stars`和`结论`；
4. 已修改或拟执行的包、配置和命令；
5. 验证结果；
6. 跳过项、排除项、兼容约束和剩余风险。

默认只展示识别到的框架；跨框架比较或仓库同时包含两者时分别展示 React 与 Vue 表。表旁标注
`Stars 查询日期：YYYY-MM-DD`，数字链接到对应仓库，并解释 `†`。明确区分**建议安装**、**已安装**、
**已更新**、**已经最新**和**已跳过**，不能暗示未实际完成的工作。
