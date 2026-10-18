---
name: security-review-skill
description: >-
  Systematic security, deployment, and reliability review of a codebase using 612
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

Reviews a codebase and its deployment against 612 checklist items. Each item is a
small reference file with a normative statement written in BCP 14 keywords
(**MUST / MUST NOT / SHOULD / SHOULD NOT / MAY**). Items are grouped into 35
categories, and categories into 9 domains so a reviewer only loads what matches
the target's stack — a Rust backend is never shown frontend rules.

## When to Use

- "Review this repo for security issues" / "Is this production-ready?"
- Pre-launch or pre-deployment audit of a service, app, or infrastructure repo
- Periodic reliability / compliance posture check
- Don't use for: fixing one specific known vulnerability (just read that one
  `issues/<slug>.md` file directly), or reviewing code style alone.

## Workflow

Execute the phases below as an autonomous tree traversal — see
`references/tree-traversal.md` for the frontier/rounds mental model
(same tree-walking shape as the `grilling` skill, minus the interview:
the frontier is evaluated against the code, not asked to a human).

### Phase 1 — Triage

Inspect the target repo (manifests, frameworks, IaC, migrations, queue/LLM/payment
code). For each of the 9 domains in `domains/`, check its `Detection signals`
section and select the domains that apply. Use each domain's `Stack quick-map` to
resolve the concrete category list. State the selected domains/categories to the
user and accept overrides before dispatch.

### Phase 2 — Dispatch

For each selected category, spawn one sub-agent via your harness's parallel-task
facility (e.g. Hermes `delegate_task`, Claude Code Task tool; sequential fallback
if none). Fill `templates/subagent-prompt.md` with:
- `{category}` — the category name
- `{manifest_path}` — absolute path to `categories/<category>.md`
- `{issues_dir}` — absolute path to this skill's `issues/` directory
- `{repo_path}` — absolute path to the target repo

Launch all categories concurrently where the harness allows.

### Phase 3 — Merge

Collect findings (JSON arrays), dedupe by file:line + slug, rank by severity
(critical > high > medium > low), and render `templates/review-report.md`.
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

- Persist the findings set per `references/review-lifecycle.md` so the
  next review diffs instead of cold-starting.
- Render the verdict gate (see `references/severity-rubric.md`):
  **BLOCK** (any critical open) / **SHIP-WITH-CONDITIONS** (highs present
  or unresolved needs-human on critical paths) / **SHIP** (clean).

## Category Index

| Category | Domain |
|---|---|
| web-api-security | backend |
| authentication | backend |
| authorization-access-control | backend |
| secrets-crypto | backend |
| api-design | backend |
| correctness-pitfalls | backend |
| testing-strategy | backend |
| security-practices | backend |
| web-client-security | frontend |
| seo-web-quality | frontend |
| multi-tenancy | backend |
| third-party-integrations | backend |
| documentation-quality | backend |
| database | data |
| distributed-systems | data |
| messaging-async | data |
| data-pipelines | data |
| supply-chain | infrastructure |
| cloud-network | infrastructure |
| deployment-release | infrastructure |
| containers-k8s | infrastructure |
| cicd-pipeline-security | infrastructure |
| resilience | reliability |
| caching | reliability |
| observability | reliability |
| sre-incidents | reliability |
| scaling-capacity | reliability |
| compliance-privacy | governance |
| ai-llm | governance |
| payments-fraud | governance |
| mobile | mobile |
| email-security | governance |
| hardening-benchmarks | government-compliance |
| regulatory-frameworks | government-compliance |
| iot-embedded | iot-embedded |

Item counts per category: `python3 scripts/merge_discovery.py` is not needed —
read `scripts/topics.json` and count, or run `scripts/validate_skill.py`.

## File Layout & Access Patterns

- `issues/<slug>.md` — canonical source of truth, one file per checklist item.
  Best for targeted reviews: load only the slugs you need.
- `categories/<category>.md` — slug lists per category (routing).
- `domains/<domain>.md` — detection signals and stack quick-maps (triage).
- `bundles/<category>.md` — **generated** bulk artifact: every item of a
  category inlined in one file. Prefer these when a harness reads whole
  categories at once (few large reads instead of many small ones). Never
  hand-edit bundles; edit `issues/<slug>.md` and re-run
  `python3 scripts/gen_manifests.py`.
- `references/tooling.md` — human-readable scanner/tool catalog by class.
- `references/mitre-attack.md` — ATT&CK tactic→issue mapping for tagging
  detection findings and reviewing telemetry coverage.
- `references/platform-hosting.md` — verified vendor security guides +
  review surfaces per platform (Cloudflare, Vercel, GitHub Pages, Fly.io,
  Azure, GCP); read the matching section when triage detects the platform.
- `references/tree-traversal.md` — frontier/rounds evaluation model
  (adapted from the `grilling` skill) for Phases 1–3.
- `references/severity-rubric.md` — severity definition (exploitability ×
  blast radius × modifiers); sub-agents MUST rate findings against it.
- `references/review-lifecycle.md` — baseline artifacts, finding states
  (open/fixed/wontfix/regressed), and diff-based re-review.
- `scripts/tool-issues.json` — machine-readable tool→issues mapping (the
  standard format; edit here to link tools to issues).
- `references/tool-index.md` — **generated** reverse index: each tool →
  the `issues/*.md` files it detects.

Do not mix granularities for the same review: pick per-item or per-bundle, so
findings cite consistently (`issues/<slug>.md` is always the citation).

## Pitfalls

- Never load all 612 items into one context — triage first; that is the whole
  point of the domain layer.
- Triage wrong is recoverable: the user can add/remove domains before dispatch.
- Findings are advisory. A `pass` verdict means "no violation found in the code
  read", not "guaranteed safe". Ground every finding in a file:line you read.
- Sub-agents must not modify the target repo. Enforce read-only in the prompt.
- If a category returns zero findings, still report it as reviewed — silence is
  not the same as coverage.

## Verification

`python3 scripts/validate_skill.py` exits 0 with
`OK: 612 issues, 35 categories, 9 domains`.
