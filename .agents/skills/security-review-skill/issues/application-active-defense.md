---
categories: [observability]
domains: [backend]
---

# Application-Level Active Defense

**SHOULD** aggregate misuse signals across endpoints — repeated authorization failures, malformed structures, out-of-order steps — and respond rather than only logging each event.

**Why:** Per-endpoint validation lets an attacker probe the whole application without ever tripping a control, and the owner learns nothing until the breach.

**Detect:** grep for alerting or throttling keyed on aggregated 403/422 rates and workflow-order violations, not only per-route rate limits.

**References:** OWASP WSTG Business Logic Testing, https://github.com/OWASP/wstg/tree/master/document/4-Web_Application_Security_Testing
