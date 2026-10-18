---
categories: [observability]
domains: [reliability]
---

# Structured Logging

**MUST** emit application logs as structured JSON with consistent field names (timestamp, level, event, actor, request_id) rather than free-form text.

**Why:** Unstructured logs defeat automated search and correlation, so attackers' actions hide in noise during incident response.

**Detect:** grep for `console.log(` / `print(` in request handlers; check for logging config with `format: json` or structlog/pino/loguru setup.

**References:** OWASP Logging Cheat Sheet, CWE-1118, NIST SP 800-92

---

**Part of:** [observability](../categories/observability.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
