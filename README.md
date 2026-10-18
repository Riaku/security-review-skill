# security-review-skill

An agent skill that performs a systematic security, deployment, and reliability
review of a codebase: **612 checklist items** across **35 categories** and
**9 domains**, fanned out to parallel sub-agents. Each item is a small
reference file with a normative statement written in BCP 14 keywords
(**MUST / MUST NOT / SHOULD / SHOULD NOT / MAY**), a *Why*, a *Detect* line,
and a *References* line.

Use it when asked to review a project for security issues, production
readiness, deployment concerns, compliance posture, or a security audit.

## Layout

- `SKILL.md` — the skill definition: when to use it and the 4-phase workflow
  (triage → dispatch → merge → baseline & verdict).
- `issues/<slug>.md` — canonical source of truth, one file per checklist item.
  Best for targeted reviews: load only the slugs you need.
- `categories/<category>.md` — slug lists per category (routing). Generated.
- `domains/<domain>.md` — detection signals and stack quick-maps (triage). Generated.
- `bundles/<category>.md` — generated bulk artifact: every item of a category
  inlined in one file. Prefer these when a harness reads whole categories at
  once. Never hand-edit bundles; edit `issues/<slug>.md` and re-run
  `python3 scripts/gen_manifests.py`.
- `references/` — hand-authored references (tooling catalog, MITRE ATT&CK
  mapping, platform-hosting guides, severity rubric, review lifecycle) plus the
  generated `tool-index.md`.
- `templates/` — sub-agent prompt and review-report templates.
- `scripts/` — `topics.json` (single source of coverage truth),
  `gen_manifests.py`, `validate_skill.py`, `check_generated.py`,
  `check_links.py`, `tool-issues.json`.

## Contributing

See `AGENTS.md` for the required workflow (branch per change, PR-only to
`main`, pre-PR gate). The rules in brief:

```bash
python3 scripts/gen_manifests.py      # regenerate domains/categories/bundles
python3 scripts/check_generated.py    # generated artifacts must be in sync
python3 scripts/validate_skill.py     # structure invariants (exit 0)
```

All three must exit 0 before opening a PR. Never edit `bundles/` by hand.

## Sources

Full attribution in `SOURCES.md`.
