# PII & Secrets Leakage into Application Logs

**MUST** redact passwords, tokens, API keys, and PII at the logging layer before anything reaches disk or an aggregator.

**Why:** Logs are widely readable and long-retained, making them the easiest place for attackers — and auditors — to harvest credentials and personal data.

**Detect:** grep logs and appenders for `password`, `authorization`, `id_card`, `redact`, `mask`; test by logging a known secret and checking it never appears in output.

**References:** OWASP Logging Cheat Sheet, CWE-532, CWE-200, PCI DSS 3.2.1 Req 3
