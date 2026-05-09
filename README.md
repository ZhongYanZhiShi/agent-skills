# Agent Skills

这个仓库用于维护可复用的 Agent 技能。每个技能放在 `skills/<skill-name>/` 目录下，`SKILL.md` 是必需的运行时说明；其他资源只在确有需要时添加，避免重复文档和维护负担。

## 目录结构

```text
skills/
  <skill-name>/
    SKILL.md
    agents/
      openai.yaml
    references/
      ...
```

`SKILL.md` 是技能运行时读取的主文件，描述触发条件、约束和执行流程。`agents/openai.yaml` 提供界面展示名称、简短说明和默认提示词，推荐与 `SKILL.md` 同步维护。`references/` 用于存放按需读取的长参考资料、模板或示例，避免把运行时不一定需要的内容塞进 `SKILL.md`。

技能目录下默认不需要 `README.md`。只有存在面向维护者、且不适合被运行时加载的补充说明时，才单独添加 README。

## 已收录技能

| 技能 | 用途 |
| --- | --- |
| `skills/commit-message` | 根据 Git diff 生成简体中文 Conventional Commit 提交信息，并在用户明确要求时执行本地 `git commit`。 |
| `skills/code-simplify` | 审查、精简并清理代码改动，重点关注复用性、可维护性和运行效率。 |
| `skills/post-code-reflection` | 将 AI 生成代码后的审查、对比、改写练习和经验沉淀整理成学习闭环。 |

## 维护约定

新增或修改技能时，先保证 `SKILL.md` frontmatter 中的 `name` 和 `description` 能准确覆盖触发场景，再维护正文流程。`description` 只描述何时使用该技能，不复述完整工作流，避免模型只看描述就跳过正文。

`SKILL.md` 应保持精简，优先写核心判断、约束和执行步骤。长模板、详细示例、领域资料等内容放入 `references/`，并在 `SKILL.md` 中说明何时读取。

涉及提交行为的技能必须遵守本地安全边界：不自动推送、不跳过钩子、不用破坏性 Git 命令绕过问题。

提交前只暂存本次目标技能相关文件，避免把 `.DS_Store`、临时脚本、缓存目录或其他未完成技能一起提交。
