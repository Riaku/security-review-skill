---
categories: [supply-chain]
domains: [infrastructure]
---

# Signed Commits

**SHOULD** require cryptographically signed commits on protected branches so authorship and provenance stay verifiable after the fact.

**Why:** Without signing, anyone who can reach the repository can attribute a change to a colleague, and provenance ends at the forge's own logs. Signature verification is what makes the history evidence.

**Detect:** command: `git log --show-signature` or `git verify-commit` over the branch range in CI, plus a branch-protection setting that rejects unsigned commits.

**References:** NCSC: protect your code repository, https://www.ncsc.gov.uk/collection/developers-collection/principles/protect-your-code-repository, SLSA v1.0 source requirements
