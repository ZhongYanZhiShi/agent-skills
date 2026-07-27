---
name: post-code-reflection
description: Use after AI-generated code or module implementation, or when the user asks to reflect on generated code, explain design choices, self-review, find bugs, compare alternatives, or extract lessons. Turns an AI coding task into a learning loop by reconstructing intent, reviewing quality and edge cases, comparing alternatives, assigning a manual rewrite, and capturing reusable lessons.
---

# Post-Code Reflection

## Core Goal

Replace “accept AI-generated code immediately” with a learning loop of design, review, rewriting, and retention. The goal is not to praise the AI, but to help the user preserve architectural judgment, code-reading skill, and the ability to make changes by hand.

## Workflow

First determine the current situation. If no code has been generated yet, ask the user to write a minimal design in no more than five lines: the goal, inputs, outputs, core flow, and likely edge cases. If code or a diff already exists, read the actual code or `git diff` before drawing conclusions.

Proceed in this order:

1. Reconstruct design intent: explain the problem being solved, data flow, important module boundaries, and implicit assumptions.
2. Expose problems: check likely bugs, edge cases, failure paths, maintainability risks, performance or I/O cost, and areas that will be painful to extend.
3. Compare alternatives: offer a simpler, safer, or more maintainable option and explain whether the current approach is worth keeping.
4. Assign a rewrite: choose one small, real change for the user or Codex to complete manually, such as renaming, extracting a function, adding an edge-case guard or test, or deleting redundant logic. Edit files only when the user explicitly asks.
5. Capture lessons: summarize reusable lessons, including applicable scenarios, key principles, common pitfalls, and what to do next time.

## Output

Keep the response concise and useful. Prefer concrete code locations, risks, and rewrite suggestions over generic praise such as “the code is well structured.”

If the user's goal is learning, end with a small exercise or question, such as “Which two functions would you extract first without AI?” If the goal is delivery, end with relevant tests, type checks, or manual paths to verify.

When reusable prompts are needed, read `references/prompt-templates.md`, select the closest template, and do not dump every template at once.
