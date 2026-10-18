# AGENTS.md — security-review-skill

Rules for AI agents (and humans) working in this repository.

## Contribution workflow (REQUIRED)

- The **initial bootstrap** (scaffold and taxonomy) was committed directly to `main`.
- **Every change after the bootstrap commit MUST go in via pull request.** Do not push
  directly to `main`, do not commit directly to `main`.
- Branch per change: `feat/<slug>`, `fix/<slug>`, `content/<category>`, `docs/<slug>`.
  One logical change per branch/PR — do not batch unrelated work into one PR.
- `main` is protected: direct pushes are rejected by branch protection; PRs require
  all CI checks to pass before merge (see Pre-PR gate).

## Pre-PR gate: ALL checks green before opening or updating a PR

Never open a PR — and never ask for review — with a red or pending-critical check.
Run the full CI-equivalent **locally** before pushing:

```bash
python3 scripts/gen_artifacts.py      # regenerate bundles, manifest lists, footers
python3 scripts/check_generated.py    # generated artifacts must be in sync
python3 scripts/validate_skill.py     # structure invariants (exit 0)
python3 scripts/check_links.py --offline   # relative links + crawl graph
```

All four must exit 0. Notes:

- `validate_skill.py` alone is NOT the gate. `bundles/` and the generated tails of
  the manifests are a separate graph only `check_generated.py` verifies — a past
  merge PR passed the validator and failed CI on stale generated content.
- `check_links.py --offline` is the fourth leg: it resolves every relative link and
  crawls the graph from `SKILL.md`, so a dangling or orphaned document fails here
  while the other three stay green. CI runs it without `--offline` (external URLs
  too); run it that way before requesting review if you touched reference links.
- After merges/refactors that remove or rename slugs, remap every reference in the
  items' frontmatter and in SKILL.md's Category Index table, then regenerate.
  Membership is declared once, in `issues/*.md`, so those are the only places a
  rename has to reach.
- If CI still fails after pushing, fix before requesting review; do not merge with a
  failing check and do not re-trigger blindly — read the failing log first.
- During incremental authoring `validate_skill.py --allow-missing` may be used,
  but the PR itself must pass the full validation.

## Branch & merge rules

- Keep branches short-lived (days, not weeks); rebase onto the current base branch
  before requesting review so the diff stays clean.
- Rebase feature branches locally; never rebase or force-push shared branches.
  When a force-push to your own PR branch is unavoidable, use
  `git push --force-with-lease` — never bare `--force`.
- Merge method: squash-merge to `main` (one logical unit per merged commit), as
  enforced by repo settings.
- PR size: small and reviewable. If a PR grows past a few hundred changed lines of
  content, split it by category or concern.
- Never merge your own PR on a red check, and never bypass branch protection
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
- Conventional types are also the input for automated changelogs/version bumps —
  keep the type honest (`feat` vs `fix`), because releases are derived from it.

## PR body conventions

Every PR body MUST contain:

1. **Summary** — what changed and why (one short paragraph + list).
2. **Test plan** — the exact commands run and their real output line
   (e.g. `OK: 616 issues, 35 categories, 9 domains`), with checkboxes for
   anything verified in CI.
3. **Deferred/follow-ups** — anything noticed but intentionally not done here.

State honest counts; never carry a number remembered from a previous session —
recount from the validator output.

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
   other machine-readable index, and no Python-side taxonomy. Everything derivable
   (membership lists, bundles, nav footers) is derived at generation time from the
   documents themselves.
6. Cross-references between documents are relative markdown links generated by
   `scripts/gen_artifacts.py`; the ONLY hand-authored link list is SKILL.md's
   Category Index table. `scripts/check_links.py` resolves every relative link in
   CI, so a hand-broken link fails the build.
7. The link graph must stay navigable from `SKILL.md`. `scripts/linkgraph.py` is
   the crawl engine; CI fails if any document under `issues/`, `categories/`,
   `domains/`, `references/`, `templates/` or `bundles/` has no path from
   SKILL.md. Every document is one level below the root, so a link target is
   always `../<dir>/<file>.md` (SKILL.md itself is the exception: root-level,
   unprefixed).
8. Hand-authored documents must be *named*: a file in `references/` or
   `templates/` is not satisfied by reachability alone, it needs an inbound link
   from another document — adding a file there without linking it fails CI. The
   generated directories are the opposite and are reached through their
   directory links. Root-level `SKILL.md`, `AGENTS.md` and `SOURCES.md` are the
   only documents exempt from needing an inbound link.
9. Bundles are assembled by *crawling*: the generator follows each
   `categories/<category>.md` manifest's item links — which it has just written
   from the items' frontmatter — and inlines the files they resolve to. It asserts
   that every item and every category manifest is reachable from `SKILL.md` and
   that no link is broken, failing loudly and naming the offender otherwise.

## Adding an item

1. Create `issues/<slug>.md`: the frontmatter block (`categories:` and `domains:`,
   both sorted), then the H1 title, the BCP 14 statement and the `**Why:**` /
   `**Detect:**` / `**References:**` lines. Frontmatter is the only place
   membership is declared — there is nothing else to update.
2. Run `python3 scripts/gen_artifacts.py`. It writes the category and domain
   membership lists AND each issue's trailing `**Part of:**` nav footer from that
   frontmatter — never hand-edit either; edit the frontmatter and re-run. It then
   re-crawls the graph and asserts every item and category is reachable.
4. Run the Pre-PR gate, commit on a branch, open a PR.

## Adding a document (not an item)

Hand-authored documents (a new `references/<name>.md`, a template, a root-level
doc) must be *named*: link them from `SKILL.md` — usually its file-layout section
— as [`references/<name>.md`](references/<name>.md), the way every other file
there is linked. A directory link is not enough for `references/` or
`templates/`, and the crawl check fails if a document has no inbound link.

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
