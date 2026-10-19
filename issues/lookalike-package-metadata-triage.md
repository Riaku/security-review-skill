---
categories: [supply-chain]
domains: [infrastructure]
---

# Lookalike Package Triage

**SHOULD** triage package-name-similarity alerts with registry metadata — age, downloads, maintainer history, release cadence — before treating them as malicious.

**Why:** Edit distance alone flags thousands of benign lookalikes, so teams mute the alert class; metadata turns an unusable similarity score into a triage decision.

**Detect:** `npm view <pkg> time maintainers` (or the registry API) against the canonical package, comparing publish date, maintainers, and downloads before escalating.

**References:** ConfuGuard package-confusion detection, https://arxiv.org/abs/2502.20528
