---
categories: [third-party-integrations]
domains: [backend]
---

# Third-Party Spend Caps

**MUST** configure a hard spend cap on every metered third-party API the application calls, with alerting thresholds below the cap.

**Why:** Retry loops, scraping, or a leaked key turn a metered API into an unbounded bill within hours; an alert tells you after the money is gone, a cap stops it.

**Detect:** grep integration client config and provider billing settings for quota, budget, and usage-limit settings; a metered endpoint with no limit is the finding.

**References:** OWASP API Security Top 10 (2023) API4 (unrestricted resource consumption), https://github.com/OWASP/API-Security
