# AGENTS.md — security-review-skill

Rules for AI agents (and humans) working in this repository.

## Contribution workflow (REQUIRED)

- The **initial bootstrap** (scaffold, topics.json, taxonomy) was committed directly to `main`.
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
python3 scripts/gen_manifests.py      # regenerate domains/categories/bundles
python3 scripts/check_generated.py    # generated artifacts must be in sync
python3 scripts/validate_skill.py     # structure invariants (exit 0)
```

All three must exit 0. Notes:

- `validate_skill.py` alone is NOT the gate. `scripts/tool-issues.json` (tool→issue
  mappings) and `bundles/` are a separate graph only `check_generated.py` verifies;
  a merge PR passed the validator and failed CI on stale tool mappings.
- After merges/refactors that remove or rename slugs, remap every reference in
  `topics.json`, all `categories/*.md` manifests, AND `scripts/tool-issues.json`
  (dedupe per tool), then regenerate.
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
   (e.g. `OK: 612 issues, 35 categories, 9 domains`), with checkboxes for
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

1. `scripts/topics.json` is the single source of coverage truth. Every item has a
   `issues/<slug>.md` file, is listed in ≥1 `categories/*.md` manifest, and every
   category is assigned to ≥1 `domains/*.md` manifest.
2. Every issue file: H1 title, a bolded BCP 14 keyword (**MUST / MUST NOT / SHOULD /
   SHOULD NOT / MAY**) within the first 300 characters, and a `**References:**` line.
3. Issue content is single-sourced: a straddling topic is listed in multiple
   manifests but its content lives in exactly one file. Never fork content to
   "customize" it per category.
4. Run the full Pre-PR gate (above) before opening any PR; it must exit 0.
5. Do not edit `scripts/discovery-rejected.json` into live content without going
   through the topics.json → manifest → issue-file flow.

## Adding an item

1. Add to `scripts/topics.json` (next sequential `num`, kebab-case `slug`, ≥1 category).
2. Create `issues/<slug>.md` in the required format.
3. Add the slug to the relevant `categories/*.md` manifest(s).
4. Run the Pre-PR gate, commit on a branch, open a PR.

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
