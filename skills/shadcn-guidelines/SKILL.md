---
name: shadcn-guidelines
description: Use when implementing, styling, debugging, or reviewing shadcn/ui components and compositions. Applies to component contracts, interaction states, accessibility, layout constraints, clipping, scrolling, overlays, theming, and responsive behavior.
---

# Shadcn Guidelines

Apply project-aware shadcn rules without turning one example or fix into a universal prescription.

## Workflow

1. Inspect the installed component source and its actual composition. Check the component API and state styles, relevant ancestors, rendered structure, primitive base, and existing project variants, tokens, and utilities. This step is complete when the relevant behavior is explained by the project code rather than an upstream assumption.
2. Separate required behavior from incidental implementation. State what the component and its container must preserve, including accessibility and interaction behavior, before choosing a change.
3. Choose the smallest scoped change that satisfies those requirements. Prefer existing component APIs, variants, tokens, and composition patterns. Change a shared primitive only when its callers share the requirement; otherwise adapt the local usage.
4. Verify every affected state in the rendered UI, including keyboard and pointer interaction, invalid and disabled states, target breakpoints, zoom, scrolling, clipping, overlays, and theming where relevant. Reuse existing checks; when non-trivial code changes, leave the smallest runnable check that catches the regression.

## Rules

### Focus Indicators Inside Clipping Containers

A shadcn control may draw focus with an outline, ring, or shadow extending beyond its border box. Any clipping ancestor can cut off part of that indicator.

When this occurs:

- Locate both the rule drawing the focus indicator and the ancestor performing the clipping.
- Determine whether clipping is intentional for scrolling, rounded media, masking, or animation, or is merely incidental.
- Choose by context among removing or narrowing unnecessary clipping, moving clipping to an inner visual layer, adding local breathing room, using an equally visible inset focus treatment, adjusting the existing ring offset, or moving the control outside the clipping boundary.
- Compare each viable option's effects on sizing, scroll measurements, rounded corners, hit targets, responsive layout, theming, and reuse. The options have no fixed priority.
- Verify that keyboard focus is complete and visible on every edge without breaking the container behavior.

Raising `z-index` does not escape overflow clipping. Making overflow visible can break scrolling, masking, or rounded corners, while fixed padding can change geometry and scroll ranges. Preserve the intended behaviors rather than a particular CSS declaration.

## Guardrails

- Preserve accessible names, keyboard operation, visible focus, and ARIA state.
- Keep shared styling coherent through existing variants, semantic tokens, and utilities.
- Keep the default focus indicator or replace it with an equally visible treatment.
- State the tradeoff when a real constraint prevents preserving the exact default appearance.
