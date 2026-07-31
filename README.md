# Agent Skills

[简体中文](README.md) | [English](README.en.md)

这个仓库用于维护可复用的 Agent 技能。每个技能放在 `skills/<skill-name>/` 目录下，英文版 `SKILL.md` 是必需的运行时说明；面向用户阅读的简体中文版使用 `SKILL.zh-Hans.md`。其他资源只在确有需要时添加，避免重复文档和维护负担。

## 目录结构

```text
skills/
  <skill-name>/
    SKILL.md
    SKILL.zh-Hans.md
    agents/
      openai.yaml
    references/
      ...
```

`SKILL.md` 是技能运行时读取的英文主文件，描述触发条件、约束和执行流程。`SKILL.zh-Hans.md` 是供用户查看的简体中文对照版，不参与技能发现。`zh-Hans` 遵循 BCP 47，明确表示简体中文；若以后增加繁体中文版，使用 `SKILL.zh-Hant.md`。`agents/openai.yaml` 提供界面展示名称、简短说明和默认提示词，推荐与两个版本同步维护。`references/` 用于存放按需读取的长参考资料、模板或示例，避免把运行时不一定需要的内容塞进 `SKILL.md`。

技能目录下默认不需要 `README.md`。只有存在面向维护者、且不适合被运行时加载的补充说明时，才单独添加 README。

## 已收录技能

| 技能 | 用途 |
| --- | --- |
| `skills/audit-project` | 面向 React、Next.js、Vue、Nuxt、Node.js 及 Monorepo 执行全量只读审查，输出带覆盖情况、证据和优先级的风险、优化项与重构建议。 |
| `skills/audit-git-history-sensitive-data` | 只读分析 Git 历史中的密钥、个人信息、本机路径及其他敏感数据，并以脱敏证据报告结果。 |
| `skills/commit-message` | 根据项目约定和提交历史选择语言生成 Conventional Commit，并在用户明确要求时执行本地 `git commit`；无法判断时默认使用简体中文。 |
| `skills/code-simplify` | 审查、精简并清理代码改动，重点关注复用性、可维护性和运行效率。 |
| `skills/frontend-file-structure` | 规划、评审或重构 React、Vue、Next.js、Nuxt、Vite 等前端项目的文件结构与目录边界。 |
| `skills/manage-frontend-debug-tools` | 自动识别 React、Vue、Next.js、Nuxt 与工作区，按需求比较 Stars、推荐、安装、更新并验证写入项目的本地调试包；不管理浏览器扩展。 |
| `skills/post-code-reflection` | 将 AI 生成代码后的审查、对比、改写练习和经验沉淀整理成学习闭环。 |
| `skills/rewrite-git-history-safely` | 安全迁移并清洗 Git 历史，按可补充的时区、节假日、补班日和禁用时段规则改写提交时间。 |

## 维护约定

新增或修改技能时，先保证 `SKILL.md` frontmatter 中的 `name` 和 `description` 能准确覆盖触发场景，再维护正文流程，并同步更新 `SKILL.zh-Hans.md`。`description` 只描述何时使用该技能，不复述完整工作流，避免模型只看描述就跳过正文。

`SKILL.md` 应保持精简，优先写核心判断、约束和执行步骤。长模板、详细示例、领域资料等内容放入 `references/`，并在 `SKILL.md` 中说明何时读取。

涉及提交行为的技能必须遵守本地安全边界：不自动推送、不跳过钩子、不用破坏性 Git 命令绕过问题。

提交前只暂存本次目标技能相关文件，避免把 `.DS_Store`、临时脚本、缓存目录或其他未完成技能一起提交。
