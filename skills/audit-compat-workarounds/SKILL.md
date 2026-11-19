---
name: audit-compat-workarounds
description: Use when asked to find project-maintained compatibility code, dependency patches, or workarounds for specific defects, or to assess whether they are still needed.
---

# Audit compatibility workarounds

Perform a read-only review of the whole project by default. If the user names a directory, limit findings to that directory. Consult shared manifests, callers, or support policies as needed to explain a finding.

## Find the compatibility path

- Identify what the project still promises to read, run on, or build with. Check support declarations, import and upgrade entry points, and the versions selected for each relevant build or release target.
- Follow readers, API adapters, and platform or version branches even when there is no `legacy` or `workaround` comment. For a field fallback, trace which producer wrote the older shape and how that data can reach the reader today. A current writer emitting only the new shape says little about an imported backup.
- Inspect project-owned source, configuration, build scripts, and dependency patches. For a patch file, trace its registration or application command through the relevant install or build entry point and check which dependency version it targets. Exclude compatibility code maintained by third parties inside their packages.
- For a suspected defect workaround, identify the concrete failure it compensates for. A regression test, upstream issue, or code history can explain why it exists. Report a delay, retry, or default value only when evidence connects it to a specific defect or compatibility requirement.

## Decide and report

Report each distinct workaround once. Cite its definition and the entry point that reads, calls, or applies it using `file:line`. If no entry point was found, say where you looked. Identify the affected data, API, environment, or defect and the condition that triggers the workaround. Choose one conclusion and cite the evidence for it.

| Conclusion | Evidence to report |
| --- | --- |
| Keep | A supported target is affected, or a supported import or upgrade path can still supply the old data. Identify that target or path. |
| Cleanup candidate | Show why the trigger can no longer occur. For an upstream fix, cite the fix and verify that every relevant target uses a version containing it. Name the behavior to test after removal. |
| Needs confirmation | The purpose is established, but necessity is unresolved. Name the missing fact, such as the oldest supported backup format or the SDK version supplied by a host. |

Close with the scope actually inspected and any gaps that affect the conclusion. If there are no findings, limit that statement to the inspected scope.
