---
categories: [secrets-crypto]
domains: [governance]
---

# Crypto Finding Scope Triage

**SHOULD** assign severity to cryptographic findings by what the code protects, treating non-security uses as out of scope.

**Why:** A hash used for cache keys is not a weak password hash. Grading both the same floods the queue and hides the finding that protects a credential.

**Detect:** For each crypto finding, name the asset it protects (confidentiality, integrity, neither) before assigning severity.

**References:** arXiv:2209.11103, https://arxiv.org/abs/2209.11103
