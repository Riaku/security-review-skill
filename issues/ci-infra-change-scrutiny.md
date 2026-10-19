---
categories: [cicd-pipeline-security]
domains: [governance]
---

# CI Infrastructure Change Scrutiny

**MUST** subject changes to CI, build, and release infrastructure, and grants of maintainer rights over them, to the same review as production code.

**Why:** Infrastructure contributions persist and are trusted afterwards, so a patient attacker delivers the payload through pipeline edits reviewed as housekeeping.

**Detect:** grep CODEOWNERS for .github/workflows, release scripts, and action definitions; every path without an owner is unreviewed

**References:** xz backdoor attack reconstruction, https://arxiv.org/abs/2504.17473
