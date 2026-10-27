---
categories: [messaging-async, web-api-security]
domains: [backend, data]
---

# Webhook Replay Protection

**MUST NOT** rely on signatures alone for webhook authenticity; add timestamp windows and nonce deduplication to block valid-signature replays.

**Why:** A captured signed webhook stays replayable forever without expiry — an attacker resends a legitimate payment event days later undetected.

**Detect:** grep webhook receivers for missing `timestamp` validation, absent `nonce`/`event_id` dedup store, signature checks with no freshness window.

**References:** OWASP API10:2023 Unsafe Consumption of APIs, OWASP Webhook Security Best Practices, CWE-294, Stripe/GitHub webhook verification docs
