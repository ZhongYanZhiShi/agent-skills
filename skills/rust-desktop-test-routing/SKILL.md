---
name: rust-desktop-test-routing
description: Use when planning, implementing, reviewing, debugging, or testing native Rust desktop changes involving Tauri, Wry, egui, iced, Slint, or GPUI. Excludes ordinary Rust libraries, backends, CLIs, and browser/WASM apps when no native desktop target is affected.
---

# Rust Desktop Test Routing

Choose evidence by the layer that runs the changed behavior. Browser success alone cannot prove native desktop integration.

## Inspect the Project

Read project instructions, manifests, affected files, existing tests, workspace scripts, and CI. Identify the actual framework, target, and owning layer before choosing a command. If no native desktop target is affected, this skill does not apply.

## Route Each Affected Behavior

| Category | Boundary | Smallest sufficient evidence |
| --- | --- | --- |
| Pure Rust logic | Framework-independent algorithms, parsing, data structures, or state transitions | The smallest existing unit or integration test exercising that logic |
| Browser-complete renderer | HTML/WebView UI fully available without native bridges, mocks, or desktop-only state | The project's browser test for that specific behavior |
| Desktop-native integration | OS/runtime behavior: IPC, WebView initialization, filesystem, database persistence, dialogs, menus, tray, windows, lifecycle, restart recovery, single-instance, event loop, native input or rendering | A native harness, integration test driving the real runtime, or actual desktop execution exercising the behavior |
| Mixed | More than one category | Separate evidence for each owning layer; one passing layer does not close the others |

For browser acceptance, confirm the project already uses that tooling for this purpose and that the affected behavior is browser-complete. Browser results may supplement native integration evidence but cannot replace it. If the required execution path is unavailable, report that behavior as **blocked** or **unverified**.

## Report

For each affected behavior, state its category, chosen command or test, result, and any missing evidence. Keep renderer-only results separate from native-runtime results.

Keep project-specific commands in the project's instructions, scripts, and CI instead of hardcoding them here.
