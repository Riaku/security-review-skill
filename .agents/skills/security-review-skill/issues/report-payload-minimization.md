---
categories: [web-client-security]
domains: [frontend]
---

# Report Payload Minimization

**SHOULD** strip sensitive context from violation and error reports, sending the origin instead of full URLs and referrers.

**Why:** Reporting endpoints exfiltrate exactly the data the application is trying to protect, and they are often third-party. Full URLs carry tokens, search terms and internal paths.

**Detect:** `report-uri`/`report-to` endpoints and error-tracker DSNs receiving full `document.URL`, `Referer`, query strings or headers unscrubbed.

**References:** W3C CSP Level 3, https://w3c.github.io/webappsec-csp/
