# AGENTS.md — security-review-skill

Rules for agents and humans who change this repository.

This repository is a security-review checklist that an agent loads as a skill.
`SKILL.md` is the entry point. Requirements below use the BCP 14 keywords MUST,
MUST NOT, SHOULD, SHOULD NOT and MAY, defined in RFC 2119 and RFC 8174.

## Repository layout

| Path | Contents |
|---|---|
| `SKILL.md` | Skill definition: triage, dispatch, merge and verdict phases. |
| `issues/<slug>.md` | One checklist item per file. Its frontmatter is the only membership record. |
| `categories/<name>.md` | Category manifest: scope and boundaries. Names no items. |
| `domains/<name>.md` | Domain manifest: detection signals and stack quick-map. |
| `bundles/<name>.md` | Generated. Never committed. See [Generated artifacts](#generated-artifacts). |
| `references/` | Long-form material: tooling catalog, ATT&CK map, platform notes, severity rubric, traversal model. |
| `templates/` | Sub-agent prompt and review report. |
| `scripts/` | `gen_artifacts.py` (generator and format gate), `check_generated.py` (CI gate), `category_slugs.py` (category membership and return-coverage check), `check_links.py` (link probe). |

## Item format

An item MUST be one file, `issues/<slug>.md`, with four parts:

1. YAML frontmatter declaring `categories:` and `domains:` as inline lists.
2. An H1 title.
3. One statement led by a single BCP 14 keyword, in bold.
4. Three labelled lines: `**Why:**`, `**Detect:**`, `**References:**`.

```markdown
---
categories: [cicd-pipeline-security, supply-chain]
domains: [infrastructure]
---

# CI Action Pinning

**MUST** reference third-party actions by full commit SHA, not a mutable tag.

**Why:** A retagged tag swaps in attacker-controlled code with the workflow's permissions.
**Detect:** Grep `.github/workflows/*.yml` for `uses:` values matching `@v[0-9]` or `@main`.
**References:** CWE-829, NIST SP 800-218, OWASP Top 10 CI/CD CICD-SEC-3
```

### Frontmatter

- Both lists MUST be sorted, MUST NOT repeat a name, and MUST name an existing
  `categories/<name>.md` or `domains/<name>.md`.
- Both lists MUST hold at least one name.
- The frontmatter MUST be valid YAML. Quote any value that contains `: `.

### Statement

- An item MUST carry exactly one obligation. If `Detect:` would check two
  different things, write two items.
- The statement SHOULD stay under 30 words; the corpus median is 19.
- The title SHOULD stay short; the corpus median is 3 words and most are 1–5.
- `References:` SHOULD list one to four sources.
- An item MUST read as a rule for any stack. A source MAY be about one language,
  framework or vendor; the rule MUST NOT be.

### Membership

- An item MUST NOT fork content to serve several categories. A straddling item
  lists every category it applies to and lives in exactly one file.

## Detect lines

`Detect:` MUST be one of three kinds:

| Kind | Shape | Example |
|---|---|---|
| Pattern | Tokens a reviewer can search for. | `tenant_id` read from the request body |
| Command | A named tool and the check it runs. | `oasdiff breaking`, `kube-bench` |
| Judgment | A decision only a reader makes; MUST name the artifact it reads. | Read the incident runbook. |

`Detect:` MUST NOT carry advice such as "check for good security". A concern
with no inspectable artifact belongs in `needs-human` guidance.

## Category and domain manifests

- A category manifest MUST open with an H1 and one overview line, and MUST be
  named by at least one item.
- A category manifest SHOULD state what the category covers, what it does not
  cover, and what a finding in it looks like.
- A domain manifest MUST list detection signals and a stack quick-map. The
  quick-map MUST name categories in plain text, with no links.
- A manifest MUST NOT list items.

## Generated artifacts

`bundles/` is generated and ignored by git.

- You MUST NOT commit `bundles/`. It duplicates the items and doubles the
  installed size.
- Run `python3 scripts/gen_artifacts.py` to write every bundle into the ignored
  `bundles/`. Add `--out DIR` to write elsewhere.
- You MUST NOT edit a bundle. Edit the item and regenerate.
- A bundle MUST hold every item whose frontmatter names the category, in slug
  order, bodies only.

## Installer output

Running an installer inside the working tree writes `.agents/` and
`skills-lock.json`. Both are ignored and neither is authored.

- You MUST NOT commit them. They carry a second copy of the corpus and double
  every install.
- `git add -A` will stage them anyway; check `git status` before you commit.
- The gate fails when either is tracked.

## Findings format

A sub-agent returns one JSON object per line: `slug`, `verdict`, `severity`,
`evidence`, `recommendation`. Lines, not an array, so a truncated reply still
delivers what it finished.

- You MUST NOT commit findings. The payload is a transport format between a
  sub-agent and its caller; the deliverable is the Markdown report.
- Before you merge a return, check it against the category it claims to cover:
  `python3 scripts/category_slugs.py <category> --check <findings.jsonl>`. Exit 0
  means every owned slug came back; exit 1 names what is missing or unknown. The
  script reads membership through `gen_artifacts.read_item`, the generator's own
  reader, so the two cannot disagree about who belongs where.
- A slug that did not come back MUST appear in the report as `needs-human` — "not
  reported by sub-agent". A partial return parses cleanly, so nothing else catches
  it.

## Gate

Run the gate before you open or update a pull request. It MUST exit 0.

```bash
python3 scripts/check_generated.py
```

The success line reads `items-valid: … ; no generated or installed artifacts
tracked; routing: 0 orphans, 0 dead routes, N/36 stranded-pair budget`.

The gate checks four things:

1. `SKILL.md` frontmatter parses as YAML and has non-empty `name` and
   `description`.
2. Every item's frontmatter is complete, sorted, unique and names real
   manifests; every body opens with an H1; every category has an overview line.
3. No build product or installed copy is tracked by git: nothing under
   `bundles/` or `.agents/`, and no `skills-lock.json`.
4. Routing coverage: no orphan category (routed by no quick-map), no dead
   quick-map route (no item declares that domain+category), and the stranded
   pair count (item declares a category none of its declared domains routes)
   stays at or below `STRANDED_MAX` in the gate script. Lower the cap as debt
   is paid; never raise it to pass.

CI installs PyYAML 6.0.2 for check 1. When PyYAML is absent, the gate falls back
to a pattern check that flags an unquoted scalar containing `: `.

## Branches, commits, pull requests

- Create one branch per logical change, named `feat/<slug>`, `fix/<slug>`,
  `content/<category>`, `docs/<slug>` or `chore/<slug>`. Do not batch unrelated
  work.
- You MUST sign off every commit with `git commit -s`. CI rejects a commit whose
  `Signed-off-by` trailer is missing or names a different author. Set
  `git config format.signOff true` once per clone.
- Use Conventional Commits: `type(scope): imperative summary`, 50 characters or
  fewer, no trailing period. Types are `feat`, `fix`, `docs`, `refactor`,
  `chore`, `ci`, `test` and `revert`. The body states why.
- `main` accepts pull requests only, merges squash only, and requires the
  `validate` check on a branch that is up to date with `main`. A ruleset
  enforces this with no bypass. You MUST NOT push to `main`, force-push it, or
  override a check.
- You MAY update your own branch with `git push --force-with-lease`. You MUST
  NOT use bare `--force`.
- Split a pull request that changes more than a few hundred lines of content.

A pull request body MUST contain three sections:

1. **Summary** — what changed and why.
2. **Test plan** — the commands you ran and their real output, with checkboxes
   for what CI covers.
3. **Deferred** — what you noticed and chose not to do here.

Measure every number you quote. Do not carry a figure from an earlier session.

## CI

| Workflow | Trigger | Blocks merge |
|---|---|---|
| `validate` | Pull request | Yes |
| `link-check` | Mondays 06:00 UTC, manual | No |

`validate` runs the DCO check, the gate, and two size budgets: `SKILL.md` under
500 lines, and every item under 1500 words.

When a check fails, read its log. You MUST NOT merge on a red check, and MUST
NOT re-run one without a change.

`link-check` probes every URL on an item's `References:` line and runs only on a
schedule, so reference rot never blocks a pull request. It reports 401, 403 and
429 as blocked rather than broken, because those hosts refuse datacenter IPs. A
dead citation is a normal issue.

## Adding an item

1. Create `issues/<slug>.md` in the format above.
2. Run `python3 scripts/check_generated.py`.
3. Commit on a branch and open a pull request.

You do not need to run the generator. The gate runs it in a temporary directory.

## Adding a document

1. Write it under `references/`, `templates/` or the repository root.
2. Link it from `SKILL.md`, so a reader finds it by following links.
3. Run the gate.

## Content rules

- A citation MUST resolve. Fetch each URL before you add it; a moved or invented
  link is the most common defect in a contributed item.
- You MUST paraphrase. Do not paste text you cannot license under MIT.
- You MUST NOT write credentials, real internal hostnames or personal data into
  an item. Use `example.com`, `10.0.0.0/8` and placeholder tokens.
- A regulatory item MUST state the obligation a reviewer checks, not a legal
  conclusion.
- Prefer a specific artifact over a general principle: a file path, a config key
  or a command.

## Security

Report a vulnerability in a workflow, a script or a pinned action through GitHub
private vulnerability reporting. `SECURITY.md` describes the scope. Do not open a
public issue for it.

## Attribution

- Seed list: @ghumare64 (Sahil Ghumare),
  [original list](https://x.com/ghumare64/status/2111332908657148356).
- System-design material: Arjay McCandless, System Design Cheat Sheet and
  Ultimate System Design Playbook.
- Everything else: curated for this skill. Per-item sources sit on each item's
  `References:` line; `SOURCES.md` holds the collection list.
