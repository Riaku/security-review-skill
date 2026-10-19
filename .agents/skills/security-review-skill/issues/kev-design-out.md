---
categories: [security-practices]
domains: [governance]
---

# Design Out Exploited Flaws

**MUST** design out any vulnerability with confirmed in-the-wild exploitation rather than accepting a compensating control.

**Why:** Active exploitation means an adversary has already solved the mitigation problem, so the compensating control is a speed bump in front of a working exploit.

**Detect:** command match SBOM findings against the CISA KEV catalog (`grype` output joined with the KEV list) and fail on matches without a removal plan.

**References:** CISA Known Exploited Vulnerabilities Catalog, https://www.cisa.gov/known-exploited-vulnerabilities-catalog, FDA premarket cybersecurity guidance (design out KEV-listed vulnerabilities), https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cybersecurity-medical-devices-quality-system-considerations-and-content-premarket-submissions
