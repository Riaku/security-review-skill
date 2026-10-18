# Double-Charge Prevention

**MAY** rely on client-side button disabling alone; a server-side idempotency key per charge request is the real safeguard.

**Why:** Retried requests, network timeouts, and scripted replays duplicate charges, eroding customer trust and triggering refund cascades.

**Detect:** grep for `Idempotency-Key`, `idempotency_key UNIQUE`, `dedupe` in payment API routes and migration files.

**References:** Stripe idempotency docs, CWE-360, OWASP ASVS 14.3.3, NIST SP 800-53 SI-7
