---
categories: [compliance-privacy, regulatory-frameworks]
domains: [governance, government-compliance]
---

# China PIPL (cross-border security assessment, separate consent, localization)

**MUST** use one of PIPL Art. 38's transfer mechanisms (CAC security assessment, CAC standard-contract filing, or PI-protection certification) where the Art. 40 thresholds apply, obtain separate consent for sensitive PI (Art. 29) and for the cross-border transfer (Art. 39), and localise within China where Art. 40 applies.

**Why:** Transferring Chinese user data abroad without CAC approval halts operations and triggers fines up to 5% of revenue plus criminal exposure.

**Detect:** grep for data flows from CN regions to overseas endpoints; missing "separate consent", CAC filing, localization config for CN deployments.

**References:** PIPL (2021), CAC Cross-Border Data Transfer Rules, GB/T 35273
