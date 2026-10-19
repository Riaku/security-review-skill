---
categories: [observability]
domains: [backend]
---

# Rejected Input Logging

**SHOULD** log server-side-only security anomalies: rejected out-of-range values, attempts to change non-modifiable fields, and access-control denials.

**Why:** These events are invisible to the client and are the earliest signal of tampering, enumeration, or a broken authorization rule. Without them an attack looks like ordinary traffic.

**Detect:** grep validation and authorization middleware for log calls on rejection paths; flag handlers that return an error without recording principal, route, and rejected value.

**References:** OWASP Proactive Controls C9 (implement logging), https://github.com/OWASP/www-project-proactive-controls, OWASP Logging Cheat Sheet
