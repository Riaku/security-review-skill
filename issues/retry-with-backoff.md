# Retry with Backoff (explicit policy: bounded retries, exponential + jitter)

**SHOULD** declare retry policy per call site: bounded count, exponential delay, randomized jitter; never infinite immediate retries.

**Why:** Unbounded or instant retries on transient errors become self-inflicted denial-of-service against recovering infrastructure.

**Detect:** grep `maxRetries`, `backoff_multiplier`, `jitter`, `RetryPolicy`.

**References:** AWS exponential backoff and jitter, resilience4j Retry, CWE-400
