---
categories: [security-practices]
domains: [backend]
---

# Remove Unused Attack Surface

**MUST** remove routes, listener ports, and integrations that no current client, test, or job uses, rather than leaving them deployed and reachable.

**Why:** Capability nobody maintains is capability nobody patches, and a reachable route is exploitable whether or not a UI links to it.

**Detect:** grep route tables and container/service port definitions for paths with no caller in the UI, SDK, or tests, and integrations whose credentials remain live; confirm from outside the host that the port or route is not reachable.

**References:** OWASP Attack Surface Analysis Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Attack_Surface_Analysis_Cheat_Sheet.html, NCSC Secure Development Principles, https://www.ncsc.gov.uk/collection/developers-collection/principles
