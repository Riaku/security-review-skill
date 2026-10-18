---
name: security-review-skill
description: >-
  Systematic security, deployment, and reliability review of a codebase using 501
  checklist items across 28 categories and 8 domains, fanned out to parallel
  sub-agents. Use when asked to review a project for security issues, production
  readiness, deployment concerns, compliance posture, or a security audit.
license: MIT
metadata:
  author: security-review-skill contributors
  version: "0.1.0"
  spec: https://agentskills.io/specification
  attribution: Original 250-item list by @ghumare64 (https://x.com/ghumare64/status/2111332908657148356); system-design concepts from Arjay McCandless's System Design Cheat Sheet; expanded with curated, government/regulatory, cloud-native, ops, and discovery-agent additions.
---

# Security Review Skill

Reviews a codebase and its deployment against 501 checklist items. Each item is a
small reference file with a normative statement written in BCP 14 keywords
(**MUST / MUST NOT / SHOULD / SHOULD NOT / MAY**). Items are grouped into 28
categories, and categories into 8 domains so a reviewer only loads what matches
the target's stack — a Rust backend is never shown frontend rules.

## When to Use

- "Review this repo for security issues" / "Is this production-ready?"
- Pre-launch or pre-deployment audit of a service, app, or infrastructure repo
- Periodic reliability / compliance posture check
- Don't use for: fixing one specific known vulnerability (just read that one
  `issues/<slug>.md` file directly), or reviewing code style alone.

## Workflow

### Phase 1 — Triage

Inspect the target repo (manifests, frameworks, IaC, migrations, queue/LLM/payment
code). For each of the 8 domains in `domains/`, check its `Detection signals`
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
| database | data |
| distributed-systems | data |
| messaging-async | data |
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
| hardening-benchmarks | government-compliance |
| regulatory-frameworks | government-compliance |

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

Do not mix granularities for the same review: pick per-item or per-bundle, so
findings cite consistently (`issues/<slug>.md` is always the citation).

## Pitfalls

- Never load all 501 items into one context — triage first; that is the whole
  point of the domain layer.
- Triage wrong is recoverable: the user can add/remove domains before dispatch.
- Findings are advisory. A `pass` verdict means "no violation found in the code
  read", not "guaranteed safe". Ground every finding in a file:line you read.
- Sub-agents must not modify the target repo. Enforce read-only in the prompt.
- If a category returns zero findings, still report it as reviewed — silence is
  not the same as coverage.

## Verification

`python3 scripts/validate_skill.py` exits 0 with
`OK: 501 issues, 28 categories, 8 domains`.
