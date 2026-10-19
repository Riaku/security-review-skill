---
categories: [secrets-crypto]
domains: [backend]
---

# Class-Identifying Secret Prefixes

**MUST** give every token the system issues a fixed, non-configurable prefix that identifies its class, and register that prefix with every secret scanner.

**Why:** Without a prefix a leaked token is indistinguishable from noise, so it survives in scanners, logs, and commit history undetected and unrevocable by pattern.

**Detect:** grep token issuance code for a constant prefix beside the signing call, and for that prefix in the secret-scanning rule set.

**References:** GitLab Secure Coding Guidelines, https://docs.gitlab.com/development/secure_coding_guidelines/
