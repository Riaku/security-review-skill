---
categories: [messaging-async]
domains: [data]
---

# Exactly-Once Semantics

**MUST NOT** claim exactly-once delivery unless transactional produce/consume (or equivalent dedup store) is actually configured end to end.

**Why:** Marketing-level guarantees without transactions hide duplicates at the consumer boundary, corrupting financial and audit records.

**Detect:** grep for `exactly_once`, `isolation.level=read_committed`, `transactional.id`, then verify no non-transactional side effects (HTTP calls, DB writes) inside the transaction.

**References:** Kafka EOS docs, CWE-662, NIST SP 800-53 SI-7

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
