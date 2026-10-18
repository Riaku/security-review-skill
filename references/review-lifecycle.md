# Review Lifecycle — Baselines, Finding States, Regression

A review should not be a cold start. Persist findings so re-reviews show
*what changed* rather than re-deriving everything.

## Baseline artifact

After every full review, save the findings set as `review-baseline.json`
(or `.hermes/review-baseline.json` in the target repo, if the user agrees):

```json
{
  "review_date": "YYYY-MM-DD",
  "skill_commit": "<sha of this skill repo>",
  "scope": {"domains": [...], "categories": [...], "depth": "standard"},
  "findings": [ { "slug": "...", "verdict": "...", "severity": "...",
                  "evidence": "path:line", "recommendation": "..." } ]
}
```

## Finding lifecycle states

Every finding in a baseline carries a lifecycle state (set by the team,
default `open`):

- `open` — unaddressed
- `fixed` — remediation merged (verified in next review)
- `wontfix` — accepted risk, with recorded reason + owner
- `regressed` — was fixed, now failing again

## Re-review = diff, not re-audit

When a baseline exists:
1. Re-evaluate only categories whose files changed since `review_date`
   (git log), plus every `open` and `wontfix` finding's evidence path
   (verify still accurate).
2. A `fixed` finding that now fails → mark `regressed`, report at its
   original severity +1 level of attention.
3. New findings → `open`.
4. Findings whose evidence file no longer exists → verify removal was the
   fix, not a rename, before closing.

## Pass decay

A `pass` is dated. State the baseline date in every report: "last full
review <date>; since then N commits touched reviewed areas." Never present
a stale pass as current.
