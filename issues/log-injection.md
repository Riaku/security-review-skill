# Log Injection & Log Forging

**MUST NOT** write unsanitized user input into log lines; strip CR/LF and control characters before logging any request data.

**Why:** Injected newlines let attackers forge fake log entries or split one entry into many, poisoning the audit trail you rely on during investigations.

**Detect:** grep for user-controlled values interpolated into logger calls (`log.info("User " + username)`) without newline stripping; check for encoder/sanitizer in log appender config.

**References:** OWASP Logging Cheat Sheet, CWE-117, OWASP WSTG-INPV-009
