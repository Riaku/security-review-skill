# security-review-skill

An agent skill that performs a systematic security, deployment and reliability
review of a codebase, fanned out to parallel sub-agents. The checklist is
organised into categories and domains; each item is a small reference file
carrying a normative statement in BCP 14 keywords
(**MUST / MUST NOT / SHOULD / SHOULD NOT / MAY**), a *Why*, a *Detect* line and
a *References* line.

Use it when asked to review a project for security issues, production
readiness, deployment concerns, compliance posture, or a security audit.

## Install

A skill is a directory with a `SKILL.md` at its root, so installing is a clone or
a copy into whatever directory your harness reads skills from:

```bash
npx skills add Riaku/security-review-skill      # or your harness's own installer

git clone https://github.com/Riaku/security-review-skill.git \
  "$SKILLS_DIR/security-review-skill"
```

There is nothing to build and no service to run: the checklist is plain
Markdown, and a harness that takes a path rather than a directory can simply be
pointed at `SKILL.md`.

**Installing from an archive.** The installer also accepts a direct download URL
to a `.zip`, `.tar`, `.tar.gz`, `.tgz` or a bare `SKILL.md` — the path for a
release asset, a mirror, or an offline machine. Its extractor refuses archives
with more than 1,000 files by default, and this skill is 1,064 (998 items plus
the manifests, references and scripts), so that path needs the limit raised:

```bash
SKILLS_EXTRACT_MAX_FILES=2000 npx skills add <archive-url>
```

The `owner/repo` and git-clone paths above have no file-count limit and need no
override.

## Usage

Ask your agent to use it, naming the target and the scope you care about:

```
Review ~/src/my-service with the security-review-skill checklist.
Focus on the backend and data domains; report MUST violations first.
```

The skill triages the target against `domains/`, loads only the category bundles
that apply, and reports findings with item slugs, `file:line` evidence and a
verdict; `templates/` carries the sub-agent prompt and report format it uses.

Without an agent harness it still works by hand — start at `SKILL.md` and walk the
phases yourself, since everything is plain Markdown.

## Layout

- `SKILL.md` — the skill definition: when to use it and the phased workflow
  (triage → dispatch → merge → verdict).
- `issues/<slug>.md` — canonical source of truth, one file per checklist item.
  Its YAML frontmatter (`categories:`, `domains:`) is the only record of what
  the item belongs to. Best for targeted reviews: load only the slugs you need.
- `categories/<category>.md` — the category's scope: its one-line overview plus
  what it covers, what it does not cover, and what a finding in it looks like.
  It lists no items; each item's own frontmatter carries that.
- `domains/<domain>.md` — detection signals and a stack quick-map for triage.
- `bundles/<category>.md` — generated on demand and gitignored, never shipped:
  every item of a category inlined in one file.
- `references/` — hand-authored reference material: the tooling catalog, the
  MITRE ATT&CK mapping, platform-hosting notes, the severity rubric and the
  tree-traversal guide.
- `templates/` — sub-agent prompt and review-report templates.
- `scripts/` — the generator and the checks. There is no data file: an item's
  category and domain membership lives in its own frontmatter.

`bundles/` is **generated on demand and not committed** — run
`python3 scripts/gen_artifacts.py` when you want whole categories in one read.
`issues/`, `categories/` and `domains/` are authored end to end — no item
carries a nav footer, no category carries an item list.

## Contributing

See `AGENTS.md` for the required workflow (branch per change, PR-only to
`main`, pre-PR gate). The rules in brief:

```bash
python3 scripts/check_generated.py   # the whole gate — must exit 0
```

It validates every item's frontmatter and fails if a generated bundle has been
committed. The success line reads `items-valid: … ; no generated or installed
artifacts tracked`.

## Sources

Full attribution in `SOURCES.md`.

## Licence

[MIT](LICENSE.md). Provenance of the sources this corpus derives from is in
[SOURCES.md](SOURCES.md), and each item cites its own references.

## Security

See [SECURITY.md](SECURITY.md): report workflow, script or supply-chain issues
privately through GitHub advisories. Disagreement with an item, and dead or moved
reference links, are normal issues rather than vulnerabilities.

## Scope and caveats

This is review guidance, not a scanner, and not a substitute for a penetration
test or a professional audit. Items describe what to look for and why it matters;
they cannot prove absence, and passing every item is not evidence that a system is
secure. Nothing here is legal advice — licensing, privacy and regulatory items
point at the obligations a reviewer should check, not at a legal conclusion.
