---
categories: [supply-chain]
domains: [infrastructure]
---

# Fork Patch Tracking

**MUST** verify that a forked or renamed dependency tracks upstream security fixes before adopting it, not merely that it resolves and builds.

**Why:** Clones replicate an old snapshot without the upstream's later patches, so importing a plausible lookalike silently forfeits the fix history the original earned.

**Detect:** command compare the fork's commit log and releases against canonical upstream (`git log upstream/main ^fork/main`), recording the last synced release.

**References:** SpellBound typosquatting and code clones, https://arxiv.org/abs/2003.03471
