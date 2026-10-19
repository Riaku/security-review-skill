---
categories: [web-api-security]
domains: [backend]
---

# Cross-Field Validation

**MUST** validate semantic relationships between fields — date orderings, totals, and business bounds — not only each field's type and length.

**Why:** A start date after its end date, or a negative quantity, passes per-field checks and then corrupts scheduling, billing, or inventory. Fields are only meaningful in relation to each other.

**Detect:** grep request validators and schemas for cross-field rules (`start < end`, amount bounds, mutually exclusive flags); schemas with type and length checks only are the finding.

**References:** OWASP Proactive Controls C5 (validate all inputs), https://github.com/OWASP/www-project-proactive-controls, CWE-20 Improper Input Validation
