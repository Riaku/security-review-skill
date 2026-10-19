---
categories: [supply-chain]
domains: [infrastructure]
---

# Cooldown Before Adopting Releases

**SHOULD** delay automated adoption of newly published dependency releases by a configured cooldown, so poisoned releases are caught upstream first.

**Why:** The hours after publication are when malicious or broken releases get reported by others; immediate automation ingests them first.

**Detect:** grep renovate minimumReleaseAge or dependabot cooldown settings in the update configuration

**References:** zizmor, https://github.com/zizmorcore/zizmor
