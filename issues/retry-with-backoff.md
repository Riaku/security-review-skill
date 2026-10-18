# Retry with Backoff (explicit policy: bounded retries, exponential + jitter)

**SHOULD** declare retry policy per call site: bounded count, exponential delay, randomized jitter; never infinite immediate retries.

**Why:** Unbounded or instant retries on transient errors become self-inflicted denial-of-service against recovering infrastructure; fixed-interval webhook delivery retries amplify a receiver outage into a hammering loop.

**Detect:** Grep `maxRetries`, `backoff_multiplier`, `jitter`, `RetryPolicy`; webhook senders lacking backoff/jitter/capped attempts or a terminal failure path; receivers lacking idempotent handling of repeated deliveries.

**References:** AWS exponential backoff and jitter, resilience4j Retry, CWE-400, OWASP Webhook Security Best Practices, Stripe retry docs

---

**Part of:** [resilience](../categories/resilience.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
