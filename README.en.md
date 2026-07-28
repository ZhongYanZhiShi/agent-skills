# Agent Skills

[简体中文](README.md) | [English](README.en.md)

This repository maintains reusable Agent skills. Each skill lives under
`skills/<skill-name>/`. The English `SKILL.md` is the required runtime
instruction file, while `SKILL.zh-Hans.md` provides a Simplified Chinese
version for readers. Add other resources only when needed to avoid duplicate
documentation and maintenance overhead.

## Directory Structure

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

`SKILL.md` is the primary English file loaded at runtime and describes
triggers, constraints, and execution steps. `SKILL.zh-Hans.md` is the
Simplified Chinese counterpart for readers and is not used for skill
discovery. `zh-Hans` follows BCP 47 and explicitly denotes Simplified Chinese;
use `SKILL.zh-Hant.md` if a Traditional Chinese version is added later.
`agents/openai.yaml` provides the display name, short description, and default
prompt, and should stay synchronized with both language versions.
`references/` stores longer reference material, templates, or examples that
should be loaded only when needed instead of expanding `SKILL.md`.

Skill directories do not need a `README.md` by default. Add one only for
maintainer-facing notes that should not be loaded at runtime.

## Included Skills

| Skill | Purpose |
| --- | --- |
| `skills/audit-project` | Performs comprehensive read-only reviews of React, Next.js, Vue, Nuxt, Node.js, and monorepo projects, reporting coverage, evidence, prioritized risks, optimizations, and refactoring recommendations. |
| `skills/commit-message` | Generates Conventional Commit messages according to project conventions and history, and runs local `git commit` only when explicitly requested; defaults to Simplified Chinese when the language cannot be determined. |
| `skills/code-simplify` | Reviews, simplifies, and cleans up code changes with an emphasis on reuse, maintainability, and runtime efficiency. |
| `skills/frontend-file-structure` | Plans, reviews, or refactors file structures and directory boundaries for React, Vue, Next.js, Nuxt, Vite, and similar frontend projects. |
| `skills/post-code-reflection` | Turns reviews, comparisons, rewriting exercises, and lessons from AI-generated code into a learning loop. |
| `skills/rewrite-git-history-safely` | Safely migrates and sanitizes Git history, rewriting commit times with extensible timezone, holiday, makeup-workday, and forbidden-time rules. |

## Maintenance Conventions

When adding or modifying a skill, first ensure that the `name` and
`description` fields in the `SKILL.md` frontmatter accurately cover its
triggering scenarios. Then maintain the body and update `SKILL.zh-Hans.md` in
sync. The `description` should explain when to use the skill without repeating
the full workflow, so the model does not skip the body after reading only the
description.

Keep `SKILL.md` concise and prioritize core decisions, constraints, and
execution steps. Put long templates, detailed examples, and domain references
under `references/`, and explain in `SKILL.md` when to read them.

Skills that perform commits must respect local safety boundaries: do not push
automatically, bypass hooks, or use destructive Git commands to work around
problems.

Before committing, stage only files related to the target skill. Do not include
`.DS_Store`, temporary scripts, cache directories, or other unfinished skills.
