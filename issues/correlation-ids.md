# Correlation IDs

**MUST** attach a unique correlation ID to every inbound request and carry it through all downstream calls, logs, and error reports.

**Why:** Without a shared ID, reconstructing one attack's path across services means guessing by timestamps — slow, error-prone, often abandoned.

**Detect:** grep middleware for `X-Request-ID` / `request_id` generation and propagation; verify log schema includes the field on every line.

**References:** OWASP Logging Cheat Sheet, AWS Prescriptive Guidance tracing, Google SRE Book Ch.6

---

**Part of:** [observability](../categories/observability.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
