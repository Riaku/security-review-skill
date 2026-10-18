---
categories: [secrets-crypto]
domains: [backend]
---

# Git-History Secret Remediation

**MUST** remediate a committed secret by rewriting history (filter-repo/BFG), rotating the credential, and notifying collaborators to re-clone — deleting the file in a new commit is NOT remediation.

**Why:** The secret remains fully recoverable from history after deletion; the rotation must cover the entire exposure window since the key was public from first push, not last commit.

**Detect:** on any discovered secret: verify history was rewritten (not just deleted-at-HEAD), credential rotated with expiry-before-exposure-window logic, forks/clones notified; judgment on incident record completeness.

**References:** GitHub secret removal guidance, git-filter-repo/BFG docs, credential-exposure incident practice

---

**Part of:** [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
