# Security & Deployment Review — {repo_name}

**Date:** {date} · **Skill:** security-review-skill
**Domains reviewed:** {domains}
**Categories dispatched:** {categories} · **Items covered:** {item_count}
**Depth profile:** {quick | standard | deep}

## Verdict: {BLOCK | SHIP-WITH-CONDITIONS | SHIP}

{one-line justification per the verdict gates in references/severity-rubric.md}

## Summary

| Severity | Count |
|---|---|
| Critical | {critical_count} |
| High | {high_count} |
| Medium | {medium_count} |
| Low | {low_count} |
| Needs-human | {needs_human_count} |

{one-paragraph executive summary: the dominant risks and the single most important
action}

## Findings

### Critical
- **{slug}** ({category}) — `{file}:{line}`
  {recommendation citing the issue's MUST wording}
  → details: `issues/{slug}.md`

### High
...

### Medium
...

### Low
...

## Needs-Human Verification

Findings the reviewer could not decide from code alone (runtime config, org
process, cloud console state). Each needs a human check before sign-off:

- **{slug}** ({category}) — {what to check and where}

## Not Applicable

Categories/items structurally absent from this stack (listed for coverage
completeness): {na_summary}

---
Findings are advisory: a `pass` means no violation was found in the code read,
not a guarantee. Attribution: original list by @ghumare64; see SOURCES.md.
