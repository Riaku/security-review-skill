# AGENTS.md — security-review-skill

Rules for AI agents (and humans) working in this repository.

## Contribution workflow (REQUIRED)

- The **initial bootstrap** (scaffold and taxonomy) was committed directly to `main`.
- **Every change after the bootstrap commit MUST go in via pull request.** Do not push
  directly to `main`, do not commit directly to `main`.
- Branch per change: `feat/<slug>`, `fix/<slug>`, `content/<category>`, `docs/<slug>`.
  One logical change per branch/PR — do not batch unrelated work into one PR.
- `main` takes changes by pull request only, and a PR requires all CI checks to
  pass before merge (see Pre-PR gate). Do not push to `main` directly.
- This is **enforced, not just documented**: the `main: PR + validate gate` ruleset
  rejects direct pushes and force-pushes, requires a pull request, and requires the
  `validate` check to pass on a branch that is up to date with `main`. It permits
  squash merges only.

## Pre-PR gate: ALL checks green before opening or updating a PR

Never open a PR — and never ask for review — with a red or pending-critical check.
Run the full CI-equivalent **locally** before pushing:

```bash
python3 scripts/check_generated.py    # FIRST: reports bundles that no longer match
python3 scripts/gen_artifacts.py      # then write every bundle from the frontmatter
```

Both must exit 0. Notes:

- **Order matters.** `check_generated.py` snapshots the committed bundles and
  then runs the generator itself, so it catches a commit where an item changed
  but its bundle did not. Running the generator first overwrites exactly the
  drift it is looking for and turns the check green — never script the two the
  other way round.
- `gen_artifacts.py` is also the format gate: it refuses to write anything and
  names the offending file when an item's frontmatter is missing, malformed,
  unsorted, declared twice or names a category or domain with no file, when an
  item body does not open with an H1, when a category manifest has no overview
  line or nothing declares it, and when `bundles/` holds a file no category
  regenerates. A format problem cannot reach a bundle.
- After merges/refactors that remove or rename slugs, remap every reference in the
  items' frontmatter and in SKILL.md's Category Index table, then regenerate.
  Membership is declared once, in `issues/*.md`, so those are the only places a
  rename has to reach.
- If CI still fails after pushing, fix before requesting review; do not merge with a
  failing check and do not re-trigger blindly — read the failing log first.

## Branch & merge rules

- Keep branches short-lived (days, not weeks); rebase onto the current base branch
  before requesting review so the diff stays clean.
- Rebase feature branches locally; never rebase or force-push shared branches.
  When a force-push to your own PR branch is unavoidable, use
  `git push --force-with-lease` — never bare `--force`.
- Merge method: squash-merge to `main` (one logical unit per merged commit) — the
  only method the ruleset permits, so merge-commit and rebase are refused.
- PR size: small and reviewable. If a PR grows past a few hundred changed lines of
  content, split it by category or concern.
- Never merge your own PR on a red check, and never bypass the required checks
  (`--no-verify`, admin override) for content changes.

## Commit message conventions (Conventional Commits)

Format: `type(scope): imperative summary`

- **Imperative mood**, as if completing "If applied, this commit will …":
  `add`, `fix`, `refactor`, `remove` — not `added`/`fixes`/`updated`.
- Summary ≤ 50 characters, no trailing period, says WHAT changed; the body says
  WHY and lists the effects (blank line, then bullets).
- Types: `feat` (new items/categories), `fix` (corrections to existing items,
  validator/CI repairs), `docs` (SKILL.md, AGENTS.md, SOURCES.md prose),
  `refactor` (restructuring with no coverage change), `test`/`ci`/`chore`
  (validation tooling), `revert`.
- Scope for this repo: the category, subsystem, or tool touched
  (`secrets-crypto`, `topics`, `ci`, `bundles`, `agents`).
- Vague messages are rejected in review: `update`, `fix bug`, `wip`,
  `address review comments` carry no information.
- Reference issues/PRs in the footer (`Closes #N`).
- **Sign every commit** (`git commit -s`). CI fails any PR whose commits lack a
  `Signed-off-by` trailer matching the author — inbound-equals-outbound is
  enforced, not aspirational. Turn it on permanently for this repo:
  `git config format.signOff true`.
- Conventional types are also the input for automated changelogs/version bumps —
  keep the type honest (`feat` vs `fix`), because releases are derived from it.

## PR body conventions

Every PR body MUST contain:

1. **Summary** — what changed and why (one short paragraph + list).
2. **Test plan** — the exact commands run and their real output line
   (e.g. the generator's `wrote N bundles from N items …` line, or
   `bundles-in-sync: N bundles OK`), with checkboxes for anything verified in
   CI.
3. **Deferred/follow-ups** — anything noticed but intentionally not done here.

State honest counts; never carry a number remembered from a previous session —
recount from the generator's or the check's own output line.

## Versioning policy

- **Select exactly ONE versioning strategy for this repo and enforce it; do not mix
  strategies.** This repo does not mandate which strategy — the project (or the
  PR author, agreed in review) picks the one that fits how the corpus is consumed,
  then applies it consistently. Candidate strategies: SemVer-style
  (MAJOR.MINOR.PATCH), date-based (CalVer), or a simple monotonically increasing
  corpus-revision number (the `vN` markers currently in commit history).
- Whichever strategy is selected, it MUST be:
  - **Documented** — named in this file with its bump rules, so every contributor
    applies the same meaning to a version.
  - **Enforced** — the version marker appears in the commit/PR title
    (`feat: v16 — …`), and review rejects changes that under-state the bump
    (e.g. a slug-breaking taxonomy change shipped as a patch-level change).
  - **Single** — two live schemes in one repo is a failure state. Switching
    strategy is itself the biggest possible bump and MUST replace, not
    supplement, the old scheme.
- If SemVer (or a compatibility-driven scheme) is the selected strategy, the
  mapping for this corpus is: **MAJOR** = incompatible taxonomy changes
  (category renames/removals, item merges that delete slugs consumers may
  reference, manifest-format changes); **MINOR** = backward-compatible
  additions (new items/categories); **PATCH** = compatible fixes (wording,
  references, detect lines, tooling). Pre-release labels (`-rc.1`) MAY mark
  taxonomy reworks under review.
- Independent of strategy: keep slug compatibility where possible — prefer adding
  a new slug over renaming in place; merges that delete slugs (dedupe) must be
  announced with an explicit removed-slugs list in the release notes.

## Non-negotiable invariants

1. An item's frontmatter is the single source of membership. Every item has an
   `issues/<slug>.md` file whose YAML frontmatter declares the `categories:` and
   `domains:` it belongs to, and every value names a real `categories/*.md` or
   `domains/*.md` manifest. Nothing else records membership, so nothing can drift
   out of step with it.
2. Every issue file: H1 title, a bolded BCP 14 keyword (**MUST / MUST NOT / SHOULD /
   SHOULD NOT / MAY**) within the first 300 characters, and a `**References:**` line.
3. Issue content is single-sourced: a straddling topic is listed in multiple
   manifests but its content lives in exactly one file. Never fork content to
   "customize" it per category.
4. Run the full Pre-PR gate (above) before opening any PR; it must exit 0.
5. No data files. The corpus is markdown plus issue frontmatter — no JSON, CSV or
   other machine-readable index, and no Python-side taxonomy. The one thing
   derived at generation time is the bundles, and they are derived from the
   documents themselves.
6. Nothing is generated into `issues/`, `categories/` or `domains/`: an item
   carries no nav footer, a category carries no item list, and a domain's stack
   quick-map names its categories in plain text. The hand-authored relative
   links that remain are SKILL.md's Category Index and the links in
   `references/` and `templates/`.
7. Every document is one level below the root, so a relative link target is
   always `../<dir>/<file>.md` (SKILL.md itself is the exception: root-level,
   unprefixed). Keep new documents linked from SKILL.md's file layout so a
   reader or agent can still find them by following links.
8. Bundles are grouped from the items' own frontmatter: every item naming a
   category is inlined into that category's bundle in slug order, body only.
   Anything the generator cannot derive — bad frontmatter, an unknown category
   or domain, a category with nothing in it — stops it with exit 1.

## Adding an item

1. Create `issues/<slug>.md`: the frontmatter block (`categories:` and `domains:`,
   both sorted), then the H1 title, the BCP 14 statement and the `**Why:**` /
   `**Detect:**` / `**References:**` lines. Frontmatter is the only place
   membership is declared — there is nothing else to update.
2. Run `python3 scripts/gen_artifacts.py`. It rebuilds every bundle from the
   frontmatter; nothing else in the tree needs editing, and it exits 1 naming the
   offender if the frontmatter is malformed or names a category or domain that
   does not exist.
3. Run the Pre-PR gate, commit on a branch, open a PR.

## Adding a document (not an item)

Hand-authored documents (a new `references/<name>.md`, a template, a root-level
doc) should be linked from `SKILL.md` — usually its file-layout section — as
[`references/<name>.md`](references/<name>.md), the way every other file there
is linked, so a reader or agent can still find them by following links.

## Attribution

- Original 250-item list: **@ghumare64 (Sahil Ghumare)** —
  https://x.com/ghumare64/status/2111332908657148356 — kudos for the curation.
- System-design concepts (retry/backoff, self-healing, queues, worker pools,
  workflow engines, batching, async writes): **Arjay McCandless's System Design
  Cheat Sheet**.
- Government/regulatory, cloud-native, ops, and discovery-agent additions: curated
  for this skill.
- Workflow/commit/PR/versioning rules above distilled from: freeCodeCamp git best
  practices (imperative mood, ≤50-char summary, PR review hygiene), EnLume
  Conventional Commits guide (type-driven semantic release), DEV.to commit & PR
  guide (type table, scope conventions), daily.dev git best practices
  (`--force-with-lease`, squash discipline, rebase-before-merge) and daily.dev
  API-versioning guide (pick one strategy, plan early, communicate breaks).

## Detect-line convention

Every issue's `Detect:` line is one of three kinds — label-free, but authors
should keep each line honestly one kind:

1. **grep-pattern** — concrete tokens a reviewer can grep
   (`tenant_id` from request body, `verify=False`, `unsafe-inline`).
   Preferred wherever a code pattern exists.
2. **command-procedure** — an external check with a named command/tool
   (`dig CAA <domain>`, `oasdiff breaking`, `kube-bench`). Name the tool.
3. **judgment** — things only a reader can decide (process, org, runtime
   state). Keep these rare and state what artifact the judgment reads.

Never write a Detect line that is none of the three (e.g. "check for good
security"). If a concern can't be detected from any artifact, it belongs
in `needs-human` guidance, not a Detect line.
