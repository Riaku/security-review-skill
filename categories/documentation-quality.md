# documentation-quality

Docs and comments quality: BCP 14 keywords, style, sync with code, runnable READMEs.

## What this category covers

This category covers the quality of the prose a project ships alongside its code: READMEs, architecture notes, runbooks, API and policy documents, comments, and the instruction files that steer AI coding agents. Its member items span requirement-keyword usage, style and terminology consistency, docs-code synchronization, single-sourcing, inclusive and accessible language, controlled-language procedures, architecture overviews and ADRs, and agent instruction files. A reviewer here should read documentation the way a newcomer or an on-call engineer would, checking that every stated command, requirement, and claim still matches the code it describes. The common failure is a document that was true once: a README command that no longer runs, a spec whose "must" reads as advice, or two files describing the same fact differently.

- Requirement-keyword rigor: all-caps BCP 14 (RFC 2119/RFC 8174) usage and the keyword boilerplate.
- Style and terminology consistency via a single documented style guide.
- Docs-code synchronization and tested, runnable READMEs.
- Single-sourcing so each fact is documented once and linked.
- Architecture overviews, ADRs, and agent instruction files kept current.

## What it does not cover

- [api-design](../categories/api-design.md) — the shape of the contract itself (resources, verbs, versioning, error schema) belongs there; this category covers whether the prose documenting it is correct and current.
- [testing-strategy](../categories/testing-strategy.md) — what gets tested and which quality gates exist belong there; this category covers keeping documented behavior and examples in step with the code.
- [observability](../categories/observability.md) — the metrics, alerts, and dashboards an operator watches belong there; the runbook or procedure as a written document belongs here.

## What a finding here looks like

- a README step that fails on a clean checkout because a service name it references changed.
- a spec sentence "the service should retry" that a reader cannot tell is a requirement or a suggestion.
- the same config example copy-pasted into three docs, two of which now list an old port.
- an agent instruction file grown past 500 lines of task-specific one-offs, so reviewers no longer treat it as policy.
- a comment reading `// set timeout to 30` directly above a line that sets it to 30.
- a README still carrying generator boilerplate and a build badge for a pipeline that has never run.
