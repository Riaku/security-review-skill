# Dead Letter Queues

**MUST** route messages that exhaust retries to a monitored dead letter queue instead of silently discarding them.

**Why:** Dropped messages mean lost transactions, audit gaps, and undetected data corruption between services.

**Detect:** grep for `dead_letter`, `DLQ`, `x-dead-letter-exchange`, `maxReceiveCount`, `redrive`, `purge` in queue configs and consumer handlers.

**References:** OWASP ASVS 7.4, CWE-390, NIST SP 800-53 AU-9
