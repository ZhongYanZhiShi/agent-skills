---
name: post-code-reflection
description: Use when the user wants to learn from generated code, reflect on implementation decisions, or compare design alternatives for understanding. Not for routine bug fixing, delivery reviews, or merely finishing an implementation.
---

# Post-Code Reflection

Help the user understand code and retain design judgment. Reflect only on the requested learning or review scope.

## Workflow

1. Read the actual code or diff and identify the question the user wants to understand. If no implementation exists, use the supplied design; ask for missing context only when necessary.
2. Explain the relevant intent, data flow, boundaries, and assumptions. Support problems and tradeoffs with concrete code locations.
3. Compare an alternative only when it helps answer the question. Explain when the existing design is worth keeping; do not invent a rewrite to fill a step.
4. Summarize reusable lessons that follow from the evidence. When the user wants practice, offer one small exercise with an acceptance criterion; otherwise omit exercises.

Edit files only within an existing implementation or fix authorization. A request to explain or reflect does not authorize edits. When a request combines reflection with delivery, complete the authorized work and its checks, keeping exercises optional.

## Output

Answer the learning question directly, with relevant code locations and tradeoffs. Distinguish observed defects from unverified concerns. Avoid generic praise and mandatory follow-up questions.

When the user needs reusable prompts, read [prompt templates](references/prompt-templates.md) and select only the relevant template.
