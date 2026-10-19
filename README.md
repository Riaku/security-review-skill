# security-review-skill

An agent skill that performs a systematic security, deployment and reliability
review of a codebase, fanned out to parallel sub-agents. The checklist is
organised into categories and domains; each item is a small reference file
carrying a normative statement in BCP 14 keywords
(**MUST / MUST NOT / SHOULD / SHOULD NOT / MAY**), a *Why*, a *Detect* line and
a *References* line.

Use it when asked to review a project for security issues, production
readiness, deployment concerns, compliance posture, or a security audit.

## Layout

- `SKILL.md` — the skill definition: when to use it and the phased workflow
  (triage → dispatch → merge → verdict).
- `issues/<slug>.md` — canonical source of truth, one file per checklist item.
  Its YAML frontmatter (`categories:`, `domains:`) is the only record of what
  the item belongs to. Best for targeted reviews: load only the slugs you need.
- `categories/<category>.md` — the category's title and a one-line overview.
  It lists no items; the bundle carries those.
- `domains/<domain>.md` — detection signals and a stack quick-map for triage.
- `bundles/<category>.md` — generated bulk artifact: every item of a category
  inlined in one file.
- `references/` — hand-authored reference material: the tooling catalog, the
  MITRE ATT&CK mapping, platform-hosting notes, the severity rubric and the
  tree-traversal guide.
- `templates/` — sub-agent prompt and review-report templates.
- `scripts/` — the generator and the checks. There is no data file: an item's
  category and domain membership lives in its own frontmatter.

`bundles/` are generated: edit `issues/<slug>.md` and re-run the generator.
`issues/`, `categories/` and `domains/` are authored end to end — no item
carries a nav footer, no category carries an item list.

## Contributing

See `AGENTS.md` for the required workflow (branch per change, PR-only to
`main`, pre-PR gate). The rules in brief:

```bash
python3 scripts/check_generated.py   # FIRST: report bundles that no longer match
python3 scripts/gen_artifacts.py     # then write every bundle from the frontmatter
```

Both must exit 0 before opening a PR. The order matters: the check runs the
generator itself, so generating first would overwrite the drift it looks for.

## Sources

Full attribution in `SOURCES.md`.
