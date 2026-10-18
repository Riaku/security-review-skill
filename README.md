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
- `categories/<category>.md` — authored scope plus a generated list of the
  items that declare the category.
- `domains/<domain>.md` — authored detection signals and stack quick-map plus a
  generated list of the categories whose items declare the domain.
- `bundles/<category>.md` — generated bulk artifact: every item of a category
  inlined in one file.
- `references/` — hand-authored reference material: the tooling catalog, the
  MITRE ATT&CK mapping, platform-hosting notes, the severity rubric and the
  tree-traversal guide.
- `templates/` — sub-agent prompt and review-report templates.
- `scripts/` — the generator and the checks. There is no data file: an item's
  category and domain membership lives in its own frontmatter.

Nothing under `categories/`, `domains/` or `bundles/`, no generated list, and
no item's trailing `**Part of:**` footer is hand-edited: edit `issues/<slug>.md`
and re-run the generator.

## Contributing

See `AGENTS.md` for the required workflow (branch per change, PR-only to
`main`, pre-PR gate). The rules in brief:

```bash
python3 scripts/gen_artifacts.py           # regenerate bundles, manifest lists, footers
python3 scripts/check_generated.py         # generated regions must be committed in sync
python3 scripts/validate_skill.py          # structure and membership invariants
python3 scripts/check_links.py --offline   # link graph and cross-reference consistency
```

All four must exit 0 before opening a PR.

## Sources

Full attribution in `SOURCES.md`.
