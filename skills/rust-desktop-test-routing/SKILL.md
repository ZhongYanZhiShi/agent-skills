---
name: rust-desktop-test-routing
description: >
  Use when planning, implementing, reviewing, debugging, testing, or verifying native Rust desktop work
  involving Tauri, Wry, egui, iced, Slint, or GPUI. Routes testing and acceptance evidence by the real
  runtime surface so browser-only checks are never reported as native desktop acceptance. Excludes
  ordinary Rust libraries, backends, and CLIs, and complete browser/WASM apps when no native desktop
  target is affected.
---

# Rust Desktop Test Routing

Route verification by the surface that actually runs the changed behavior. The recurring failure this
skill prevents is launching a browser test against an incomplete web build of a Rust desktop app and
reporting success while the native runtime was never exercised.

## Before Choosing Any Command

Inspect the project before deciding how to verify:

- project instructions (AGENTS.md or equivalent) and documented test or verification conventions;
- manifests and build files that reveal the framework and targets (Tauri, Wry, egui, iced, Slint,
  GPUI, or a plain library/binary/CLI);
- package and workspace scripts plus CI configuration, to reuse the commands the project already uses;
- the affected files and the layer that owns them;
- the existing test suite, so you pick the smallest test that already covers the layer.

If the change does not touch a native desktop target, this skill does not apply.

## Classify the Changed Behavior

Assign the change to one category:

1. **Pure Rust logic** — framework-independent logic, algorithms, parsing, data structures, or state
   transitions that never cross into the OS, WebView, IPC, or renderer.
2. **Browser-complete renderer behavior** — UI that runs entirely inside the WebView/HTML layer with no
   native bridge, no IPC, no filesystem or database, and no desktop-only state.
3. **Desktop-native integration** — anything reaching the OS or native runtime: IPC, WebView
   initialization, filesystem, database persistence, dialogs, menus, tray, window management,
   lifecycle, restart recovery, single-instance, the event loop, native input or rendering.
4. **Mixed behavior** — a change that spans more than one category.

## Choose the Smallest Test for the Owning Layer

- For **pure Rust logic**, run the smallest existing unit or integration test that exercises that
  logic. A passing unit test proves only the logic, never the native surface.
- For **browser-complete renderer behavior**, a browser test may be final acceptance — but only for the
  specific behavior that is fully available without native bridges, mocks, or desktop-only state.
- For **desktop-native integration**, browser evidence is auxiliary at best. It may confirm the
  renderer side but cannot prove the native runtime works.
- For **mixed behavior**, split verification by owning layer. Each layer needs its own evidence, and
  one passing layer does not close acceptance for the others.

## Decide When Browser Evidence Counts

Treat a Playwright/browser test as final acceptance only when all of the following hold:

- the affected behavior is classified as browser-complete renderer behavior;
- it runs fully without native bridges, mocks, or desktop-only state;
- the project already uses that browser test tooling for this purpose.

Treat browser evidence as auxiliary — helpful for the renderer but not proof of the native surface —
for anything involving IPC, WebView integration, filesystem, database persistence, dialogs, menus,
tray, windows, lifecycle, restart recovery, single-instance, the event loop, native input or rendering,
or OS integration.

## Require Native Evidence for Desktop Acceptance

For desktop-native integration, acceptance requires a native test or real desktop execution: the
project's own native test harness, an integration test that drives the real runtime, or running the
desktop app and exercising the behavior. If no such path is available, report the native behavior as
**blocked** or **unverified** — never as passed. Do not infer native correctness from a browser run.

## Report

For each affected behavior, state:

- its category;
- the command or test chosen and why it owns that layer;
- whether native evidence was obtained, or explicitly blocked/unverified;
- a clear separation between renderer-only evidence and native-runtime evidence.

Keep project-specific commands in that project's instructions, scripts, and CI. Do not hardcode
framework, build, or test commands here.
