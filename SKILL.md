---
name: security-review-skill
description: >-
  Systematic security, deployment, and reliability review of a codebase using 616
  checklist items across 35 categories and 9 domains, fanned out to parallel
  sub-agents. Use when asked to review a project for security issues, production
  readiness, deployment concerns, compliance posture, or a security audit.
license: MIT
metadata:
  author: security-review-skill contributors
  spec: https://agentskills.io/specification
  attribution: Full source list in SOURCES.md. Seed: 250-item list by @ghumare64 (https://x.com/ghumare64/status/2111332908657148356); system-design content from Arjay McCandless's Cheat Sheet and Ultimate System Design Playbook; expanded from OWASP/NIST/MITRE/SLSA and vendor platform guides.
---

# Security Review Skill

Reviews a codebase and its deployment against 616 checklist items. Each item is a
small reference file with a normative statement written in BCP 14 keywords
(**MUST / MUST NOT / SHOULD / SHOULD NOT / MAY**). Items are grouped into 35
categories, and categories into 9 domains so a reviewer only loads what matches
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
code). For each of the 9 domains in [`domains/`](domains/), check its `Detection
signals` section and select the domains that apply. Use each domain's `Stack
quick-map` to resolve the concrete category list. State the selected
domains/categories to the user and accept overrides before dispatch.

### Phase 2 — Dispatch

For each selected category, spawn one sub-agent via your harness's parallel-task
facility (e.g. Hermes `delegate_task`, Claude Code Task tool; sequential fallback
if none). Fill [`templates/subagent-prompt.md`](templates/subagent-prompt.md)
with:
- `{category}` — the category name
- `{manifest_path}` — absolute path to [`categories/<category>.md`](categories/)
- `{issues_dir}` — absolute path to this skill's [`issues/`](issues/) directory
- `{repo_path}` — absolute path to the target repo

Launch all categories concurrently where the harness allows.

### Phase 3 — Merge

Collect findings (JSON arrays), dedupe by file:line + slug, rank by severity
(critical > high > medium > low), and render
[`templates/review-report.md`](templates/review-report.md).
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

### Phase 4 — Baseline & Verdict

- Persist the findings set per
  [`references/review-lifecycle.md`](references/review-lifecycle.md) so the next
  review diffs instead of cold-starting.
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

Item counts per category: no separate script is needed — read
[`scripts/topics.json`](scripts/topics.json) and count, or run
[`python3 scripts/validate_skill.py`](scripts/validate_skill.py).

## File Layout & Access Patterns

- [`issues/<slug>.md`](issues/) — canonical source of truth, one file per
  checklist item. Best for targeted reviews: load only the slugs you need.
- [`categories/<category>.md`](categories/) — slug lists per category (routing).
- [`domains/<domain>.md`](domains/) — detection signals and stack quick-maps
  (triage).
- [`bundles/<category>.md`](bundles/) — **generated** bulk artifact: every item
  of a category inlined in one file. Prefer these when a harness reads whole
  categories at once (few large reads instead of many small ones). Never
  hand-edit bundles; edit [`issues/<slug>.md`](issues/) and re-run
  [`python3 scripts/gen_manifests.py`](scripts/gen_manifests.py) — the
  generator assembles each bundle by crawling its category manifest's links.
- [`references/tooling.md`](references/tooling.md) — human-readable scanner/tool
  catalog by class.
- [`references/mitre-attack.md`](references/mitre-attack.md) — ATT&CK
  tactic→issue mapping for tagging detection findings and reviewing telemetry
  coverage.
- [`references/platform-hosting.md`](references/platform-hosting.md) — verified
  vendor security guides + review surfaces per platform (Cloudflare, Vercel,
  GitHub Pages, Fly.io, Azure, GCP); read the matching section when triage
  detects the platform.
- [`references/tree-traversal.md`](references/tree-traversal.md) —
  frontier/rounds evaluation model (adapted from the `grilling` skill) for
  Phases 1–3.
- [`references/severity-rubric.md`](references/severity-rubric.md) — severity
  definition (exploitability × blast radius × modifiers); sub-agents MUST rate
  findings against it.
- [`references/review-lifecycle.md`](references/review-lifecycle.md) — baseline
  artifacts, finding states (open/fixed/wontfix/regressed), and diff-based
  re-review.
- [`scripts/tool-issues.json`](scripts/tool-issues.json) — machine-readable
  tool→issues mapping (the standard format; edit here to link tools to issues).
- [`references/tool-index.md`](references/tool-index.md) — **generated** reverse
  index: each tool → the [`issues/*.md`](issues/) files it detects.
- [`scripts/linkgraph.py`](scripts/linkgraph.py) — the crawl engine: follows
  the relative links from [`SKILL.md`](SKILL.md), expanding a directory link to
  that directory's `*.md` files, and reports unreachable documents and
  round-trip breaks. The generator and the checks are built on it; crawl the
  graph yourself with
  [`python3 scripts/check_links.py`](scripts/check_links.py).

Every document cross-links its neighbours with relative markdown links
([`issues/<slug>.md`](issues/) ↔ category ↔ domain ↔ [`SKILL.md`](SKILL.md)),
so any entry point reaches any other. The link lists in
[`categories/`](categories/), [`domains/`](domains/), [`bundles/`](bundles/) and
[`references/tool-index.md`](references/tool-index.md) are generated by
[`python3 scripts/gen_manifests.py`](scripts/gen_manifests.py), which assembles
each bundle by following its category manifest's links; each issue file ends
with a generated `**Part of:**` footer.
[`scripts/check_links.py`](scripts/check_links.py) resolves that whole graph
and crawls it from [`SKILL.md`](SKILL.md): a broken link, a document no link
reaches, or a navigation claim that does not round-trip (a category lists an
issue whose footer omits the back-link) fails CI. Hand-authored documents are
held to the stricter rule — [`references/`](references/) and
[`templates/`](templates/) must each be *named* by an inbound link, so a new
file there cannot arrive unnoticed.

Do not mix granularities for the same review: pick per-item or per-bundle, so
findings cite consistently ([`issues/<slug>.md`](issues/) is always the citation).

## Pitfalls

- Never load all 616 items into one context — triage first; that is the whole
  point of the domain layer.
- Triage wrong is recoverable: the user can add/remove domains before dispatch.
- Findings are advisory. A `pass` verdict means "no violation found in the code
  read", not "guaranteed safe". Ground every finding in a file:line you read.
- Sub-agents must not modify the target repo. Enforce read-only in the prompt.
- If a category returns zero findings, still report it as reviewed — silence is
  not the same as coverage.

## Verification

[`python3 scripts/validate_skill.py`](scripts/validate_skill.py) exits 0 with
`OK: 616 issues, 35 categories, 9 domains`.
