# At-Least-Once Delivery

**SHOULD** document at-least-once semantics explicitly and require idempotent consumers, since redelivery on ack failure is guaranteed.

**Why:** Duplicate charges, double emails, and duplicated inventory movements arise when handlers assume single delivery.

**Detect:** grep for `ack` after processing, `auto_ack=True`, missing idempotency keys, `at_least_once`, unguarded side effects in consumers.

**References:** CWE-362, AWS SQS delivery semantics, Designing Data-Intensive Applications (delivery semantics)