---
categories: [compliance-privacy, observability]
domains: [governance, reliability]
---

# PII & Secrets Leakage into Application Logs

**MUST** redact passwords, tokens, API keys, and PII at the logging layer before anything reaches disk or an aggregator.

**Why:** Logs are widely readable and long-retained, making them the easiest place for attackers — and auditors — to harvest credentials and personal data; unredacted request bodies, headers, and stack traces spread PII into traces and error-reporters as secondary sinks.

**Detect:** Grep logs and appenders for `password`, `authorization`, `id_card`, `redact`, `mask`; grep for `log.*request`, `log.*body`, `console.log(err)` without redaction and missing `redact_fields`/`mask_pii` filter config. Test by logging a known secret and checking it never appears in logs, traces, or error-reporter payloads.

**References:** OWASP Logging Cheat Sheet, CWE-532, CWE-200, PCI DSS 3.2.1 Req 3, GDPR Art. 5(1)(c), NIST SP 800-92

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [observability](../categories/observability.md) · [governance](../domains/governance.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
