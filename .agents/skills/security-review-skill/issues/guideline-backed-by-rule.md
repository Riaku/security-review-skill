---
categories: [security-practices]
domains: [backend, governance]
---

# Guidelines Backed by Rules

**SHOULD** pair every written security guideline with an automated rule in the repository and a severity that routes findings to the right reviewer.

**Why:** Guidelines without enforcement decay into folklore, while rules without guidance produce findings developers cannot act on.

**Detect:** grep the security guideline document and the linter configs, and list guidelines with no corresponding rule id.

**References:** GitLab Secure Coding Guidelines, https://docs.gitlab.com/development/secure_coding_guidelines/
