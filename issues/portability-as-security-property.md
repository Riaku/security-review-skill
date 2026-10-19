---
categories: [supply-chain]
domains: [governance]
---

# Portability as Security Property

**MUST** prefer open, standard interfaces for policy, identity, and telemetry so a provider compromise or outage does not trap the system.

**Why:** Proprietary formats on the decision path turn a single provider's incident into an un-exitable outage, because migration cost exceeds the risk tolerance.

**Detect:** read the integration ADR for each security-critical dependency and check it names an export or replacement path that has been exercised.

**References:** NIST SP 800-207 §5.6, https://doi.org/10.6028/NIST.SP.800-207, NIST SP 800-161 (C-SCRM)
