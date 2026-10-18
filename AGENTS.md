# AGENTS.md — security-review-skill

Rules for AI agents (and humans) working in this repository.

## Contribution workflow (REQUIRED)

- The **initial bootstrap** (scaffold, topics.json, taxonomy) was committed directly to `main`.
- **Every change after the bootstrap commit MUST go in via pull request.** Do not push
  directly to `main`, do not commit directly to `main`.
- Branch per change: `feat/<slug>`, `fix/<slug>`, `content/<category>`.
- `main` is protected: direct pushes are rejected by branch protection; PRs require
  the validator to pass before merge.

## Non-negotiable invariants

1. `scripts/topics.json` is the single source of coverage truth. Every item has a
   `issues/<slug>.md` file, is listed in ≥1 `categories/*.md` manifest, and every
   category is assigned to ≥1 `domains/*.md` manifest.
2. Every issue file: H1 title, a bolded BCP 14 keyword (**MUST / MUST NOT / SHOULD /
   SHOULD NOT / MAY**) within the first 300 characters, and a `**References:**` line.
3. Issue content is single-sourced: a straddling topic is listed in multiple
   manifests but its content lives in exactly one file. Never fork content to
   "customize" it per category.
4. Run `python3 scripts/validate_skill.py` before opening any PR; it must exit 0.
   During incremental authoring `--allow-missing` may be used, but the PR itself
   must pass the full validation.
5. Do not edit `scripts/discovery-rejected.json` into live content without going
   through the topics.json → manifest → issue-file flow.

## Adding an item

1. Add to `scripts/topics.json` (next sequential `num`, kebab-case `slug`, ≥1 category).
2. Create `issues/<slug>.md` in the required format.
3. Add the slug to the relevant `categories/*.md` manifest(s).
4. Validate, commit on a branch, open a PR.

## Attribution

- Original 250-item list: **@ghumare64 (Sahil Ghumare)** —
  https://x.com/ghumare64/status/2111332908657148356 — kudos for the curation.
- System-design concepts (retry/backoff, self-healing, queues, worker pools,
  workflow engines, batching, async writes): **Arjay McCandless's System Design
  Cheat Sheet**.
- Government/regulatory, cloud-native, ops, and discovery-agent additions: curated
  for this skill.
