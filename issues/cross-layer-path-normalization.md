---
categories: [web-api-security]
domains: [backend, infrastructure]
---

# Cross-Layer Path Normalization

**MUST** verify that every component deciding on a URL path — proxy, router, cache, WAF, application — normalizes it identically before enforcing path-based rules.

**Why:** Syntactically valid but inconsistently normalized paths let one layer allow what another denies, bypassing path-matched controls without any traversal sequence.

**Detect:** grep path-matching rules in each layer (`location ~`, `pathPrefix`, route patterns) and compare their trailing-slash, case, and percent-encoding handling.

**References:** OWASP WSTG Path Confusion, https://github.com/OWASP/wstg/blob/master/document/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management/13-Path_Confusion.md
