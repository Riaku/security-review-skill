---
categories: [messaging-async]
domains: [data]
---

# Message Queues

**MUST** set queue depth limits, TTLs, and alerting thresholds; unbounded buffering hides downstream failure until memory or disk exhaustion.

**Why:** A queue that grows silently becomes a time bomb — messages expire or the broker crashes exactly when the backlog peaks.

**Detect:** grep broker configs for missing `max-length`/`message-ttl` policies (or `x-max-length`/`x-message-ttl`), `vm_memory_high_watermark`, `x-max-priority`; dashboards tracking only rate, not depth.

**References:** OWASP ASVS 7.4, CWE-770, RabbitMQ memory alarms docs
