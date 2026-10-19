---
name: security-review-skill
description: >-
  Systematic security, deployment, and reliability review of a codebase using a
  checklist of items grouped into categories and domains, fanned out to parallel
  sub-agents. Use when asked to review a project for security issues, production
  readiness, deployment concerns, compliance posture, or a security audit.
license: MIT
metadata:
  author: security-review-skill contributors
  spec: https://agentskills.io/specification
  attribution: "Full source list in SOURCES.md. Seed: 250-item list by @ghumare64 (https://x.com/ghumare64/status/2111332908657148356); system-design content from Arjay McCandless's Cheat Sheet and Ultimate System Design Playbook; expanded from OWASP/NIST/MITRE/SLSA and vendor platform guides."
---

# Security Review Skill

Reviews a codebase and its deployment against the full item checklist. Each item
is a small reference file with a normative statement written in BCP 14 keywords
(**MUST / MUST NOT / SHOULD / SHOULD NOT / MAY**). Items are grouped into
categories, and categories into domains so a reviewer only loads what matches
the target's stack — a Rust backend is never shown frontend rules.

## When to Use

- "Review this repo for security issues" / "Is this production-ready?"
- Pre-launch or pre-deployment audit of a service, app, or infrastructure repo
- Periodic reliability / compliance posture check
- Don't use for: fixing one specific known vulnerability (just read that one
  [`issues/<slug>.md`](issues/) file directly), or reviewing code style alone.

## Workflow

Execute the phases below as an autonomous tree traversal — see
[`references/tree-traversal.md`](references/tree-traversal.md) for the
frontier/rounds mental model (same tree-walking shape as the `grilling` skill,
minus the interview: the frontier is evaluated against the code, not asked to a
human).

### Phase 1 — Triage

Inspect the target repo (manifests, frameworks, IaC, migrations, queue/LLM/payment
code). For each domain in [`domains/`](domains/), check its `Detection
signals` section and select the domains that apply. Use each domain's `Stack
quick-map` to resolve the concrete category list. State the selected
domains/categories to the user and accept overrides before dispatch.

### Phase 2 — Dispatch

Build the bulk artifacts once, then hand each sub-agent a single file:

```bash
python3 scripts/gen_artifacts.py    # writes bundles/<category>.md; gitignored, never shipped
```

For each selected category, spawn one sub-agent via your harness's parallel-task
facility (e.g. Hermes `delegate_task`, Claude Code Task tool; sequential fallback
if none). Fill [`templates/subagent-prompt.md`](templates/subagent-prompt.md)
with:
- `{category}` — the category name
- `{bundle_path}` — absolute path to `bundles/<category>.md`: every item of the
  category inlined in one file, so the sub-agent does one read, not forty
- `{manifest_path}` — absolute path to [`categories/<category>.md`](categories/):
  the category's scope, and what a finding in it looks like
- `{repo_path}` — absolute path to the target repo

Pass the bundle rather than the item directory: it is generated from the items'
own frontmatter, so it cannot disagree with them as long as it was built after
the last edit. If `python3` is unavailable where the skill is installed, pass
`{issues_dir}` instead and let the sub-agent select items by frontmatter.

Launch all categories concurrently where the harness allows.

### Phase 3 — Merge

Each sub-agent returns one JSON object per line. Before you trust a return, check
it against the slugs the category owns:

```bash
python3 scripts/category_slugs.py <category> --check <findings.jsonl>
```

The script reads the same frontmatter the generator does, so its list is the
category's full membership. Exit 0 means every owned slug came back. Exit 1 lists
what is missing or unknown, and exit 2 means nothing parsed.

- A missing slug MUST become a `needs-human` finding reading "not reported by
  sub-agent", never a silent gap: a partial return parses cleanly, so nothing else
  catches it.
- An unknown slug MUST be dropped and noted; it does not belong to the category.

Then dedupe by file:line + slug, rank by severity (critical > high > medium >
low), and render [`templates/review-report.md`](templates/review-report.md).
Include the needs-human section verbatim — never silently drop findings.

**Cross-category dedupe:** the same evidence often surfaces under different
slugs (a missing authz check reported as `idor`, `missing-auth-middleware`,
and `server-side-authorization`). Dedupe by evidence location: when two
findings cite the same `file:line`, merge them — keep the most specific
slug, list the others as related, count ONCE in the summary.
**Severity conflicts:** when merged findings disagree on severity, the
higher severity wins and the report flags the disagreement.
**Provenance:** every merged finding keeps all contributing slugs so
nothing is silently lost.

The findings JSON is a transport format between agent and caller. It MUST NOT be
written into this repository or shipped with a report; the report is Markdown.

### Phase 4 — Verdict

- Render the verdict gate (see
  [`references/severity-rubric.md`](references/severity-rubric.md)):
  **BLOCK** (any critical open) / **SHIP-WITH-CONDITIONS** (highs present
  or unresolved needs-human on critical paths) / **SHIP** (clean).

## Category Index

| Category | Domain |
|---|---|
| [web-api-security](categories/web-api-security.md) | [backend](domains/backend.md) |
| [authentication](categories/authentication.md) | [backend](domains/backend.md) |
| [authorization-access-control](categories/authorization-access-control.md) | [backend](domains/backend.md) |
| [secrets-crypto](categories/secrets-crypto.md) | [backend](domains/backend.md) |
| [api-design](categories/api-design.md) | [backend](domains/backend.md) |
| [correctness-pitfalls](categories/correctness-pitfalls.md) | [backend](domains/backend.md) |
| [testing-strategy](categories/testing-strategy.md) | [backend](domains/backend.md) |
| [security-practices](categories/security-practices.md) | [backend](domains/backend.md) |
| [web-client-security](categories/web-client-security.md) | [frontend](domains/frontend.md) |
| [seo-web-quality](categories/seo-web-quality.md) | [frontend](domains/frontend.md) |
| [multi-tenancy](categories/multi-tenancy.md) | [backend](domains/backend.md) |
| [third-party-integrations](categories/third-party-integrations.md) | [backend](domains/backend.md) |
| [documentation-quality](categories/documentation-quality.md) | [backend](domains/backend.md) |
| [database](categories/database.md) | [data](domains/data.md) |
| [distributed-systems](categories/distributed-systems.md) | [data](domains/data.md) |
| [messaging-async](categories/messaging-async.md) | [data](domains/data.md) |
| [data-pipelines](categories/data-pipelines.md) | [data](domains/data.md) |
| [supply-chain](categories/supply-chain.md) | [infrastructure](domains/infrastructure.md) |
| [cloud-network](categories/cloud-network.md) | [infrastructure](domains/infrastructure.md) |
| [deployment-release](categories/deployment-release.md) | [infrastructure](domains/infrastructure.md) |
| [containers-k8s](categories/containers-k8s.md) | [infrastructure](domains/infrastructure.md) |
| [cicd-pipeline-security](categories/cicd-pipeline-security.md) | [infrastructure](domains/infrastructure.md) |
| [resilience](categories/resilience.md) | [reliability](domains/reliability.md) |
| [caching](categories/caching.md) | [reliability](domains/reliability.md) |
| [observability](categories/observability.md) | [reliability](domains/reliability.md) |
| [sre-incidents](categories/sre-incidents.md) | [reliability](domains/reliability.md) |
| [scaling-capacity](categories/scaling-capacity.md) | [reliability](domains/reliability.md) |
| [compliance-privacy](categories/compliance-privacy.md) | [governance](domains/governance.md) |
| [ai-llm](categories/ai-llm.md) | [governance](domains/governance.md) |
| [payments-fraud](categories/payments-fraud.md) | [governance](domains/governance.md) |
| [mobile](categories/mobile.md) | [mobile](domains/mobile.md) |
| [email-security](categories/email-security.md) | [governance](domains/governance.md) |
| [hardening-benchmarks](categories/hardening-benchmarks.md) | [government-compliance](domains/government-compliance.md) |
| [regulatory-frameworks](categories/regulatory-frameworks.md) | [government-compliance](domains/government-compliance.md) |
| [iot-embedded](categories/iot-embedded.md) | [iot-embedded](domains/iot-embedded.md) |

Other references: [`references/tooling.md`](references/tooling.md) (scanner
catalog), [`references/mitre-attack.md`](references/mitre-attack.md) (ATT&CK
tactic→slug mapping) and
[`references/platform-hosting.md`](references/platform-hosting.md) (per-platform
review surfaces; read the matching section when triage detects the platform).

## Pitfalls

- Never load every item into one context — triage first; that is the whole
  point of the domain layer.
- Triage wrong is recoverable: the user can add/remove domains before dispatch.
- Findings are advisory. A `pass` verdict means "no violation found in the code
  read", not "guaranteed safe". Ground every finding in a file:line you read.
- Sub-agents must not modify the target repo. Enforce read-only in the prompt.
- If a category returns zero findings, still report it as reviewed — silence is
  not the same as coverage.

## Verification

Run [`python3 scripts/check_generated.py`](scripts/check_generated.py) — the
whole gate. It runs the generator into a throw-away directory, so a malformed
item fails there with the offending file named, and it fails if any bundle has
been re-added to git, since generated files in the index are exactly what makes
the skill expensive to install. Its last line names the counts it saw; read that
line for the numbers, never a figure remembered from a previous session.
