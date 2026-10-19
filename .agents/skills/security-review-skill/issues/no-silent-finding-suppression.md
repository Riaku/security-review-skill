---
categories: [cicd-pipeline-security]
domains: [backend]
---

# No Silent Finding Suppression

**MUST NOT** let automated repair resolve a finding by adding a suppression directive, ignore-comment, or disabled check.

**Why:** Suppression makes the report clean without changing the defect, so the review gate reports success while the vulnerability stays in production.

**Detect:** grep diffs from automated fixes for `# nosec`, `# noqa`, `// nolint`, `@SuppressWarnings`, `ignore_errors`, and `skip` additions unaccompanied by a code change.

**References:** TerraRepair (arXiv 2607.11390), https://arxiv.org/abs/2607.11390
