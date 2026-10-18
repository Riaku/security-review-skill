# PII leakage into application logs, traces, and error reporters

**SHOULD NOT** log raw request bodies, headers, or stack traces containing PII without redaction or masking.

**Why:** Unredacted PII in logs spreads personal data into observability systems, creating unauthorized secondary processing and breach surface.

**Detect:** grep for `log.*request`, `log.*body`, `console.log(err)` without redaction; check `redact_fields`, `mask_pii`, log filter config absent.

**References:** CWE-532, OWASP A05:2021, GDPR Art. 5(1)(c), NIST SP 800-92
