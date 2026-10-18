# Retry Storms

**MUST NOT** retry without a hard budget shared across the call graph; nested retries multiply one failure into dozens.

**Why:** Three layers each retrying twice turns one blip into eight requests per caller.

**Detect:** count nested `@Retryable`, `max_retries`, `retry_times` per path; flag retry-on-timeout with no `retry_budget`.

**References:** Google SRE Book retry storms, AWS retry budget guidance, CWE-400, REL11-BP06
