---
categories: [messaging-async]
domains: [data]
---

# Background Jobs

**MUST** enforce timeouts and retry limits on background jobs; a hung job holding a lock or connection pool slot can cascade into outage.

**Why:** Untimed jobs accumulate, exhaust DB pools and workers, and mask failures that surface only as total system stall.

**Detect:** grep for job definitions missing `timeout`, `max_retries`, `dead_timeout`; Sidekiq/Celery configs without `soft_time_limit` or `expires`.

**References:** OWASP ASVS 7.4, CWE-400, Celery task timeout guidance
