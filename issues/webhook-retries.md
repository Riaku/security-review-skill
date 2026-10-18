# Webhook Retries

**SHOULD** retry failed webhook deliveries with exponential backoff and jitter, capped attempts, and a terminal failure path rather than infinite hammering.

**Why:** Naive fixed-interval retries amplify load on a struggling receiver, converting one outage into a self-inflicted DDoS loop.

**Detect:** grep for retry loops without `backoff`, `jitter`, `max_attempts`; receivers lacking idempotent handling of repeated deliveries.

**References:** OWASP Webhook Security Best Practices, CWE-400, Stripe retry docs
