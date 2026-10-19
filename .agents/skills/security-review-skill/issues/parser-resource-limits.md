---
categories: [web-api-security]
domains: [backend]
---

# Parser Resource Limits

**MUST** cap structural parser limits - nesting depth, node or element counts, header counts - inside the parser itself, not only the request body size.

**Why:** A small body can still carry a deeply nested or million-element document, and a parser that allocates first has already lost.

**Detect:** grep parser configuration for `max_depth`, `max_nodes`, `max_header`, `max_element_depth`, `XMLConstants.FEATURE_SECURE_PROCESSING`; a parser relying solely on an edge body-size limit is the finding.

**References:** OWASP Denial of Service Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html, OWASP XXE Prevention Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html
