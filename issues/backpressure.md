---
categories: [resilience]
domains: [reliability]
---

# Backpressure

**MUST** reject or delay requests once queues pass a high-water mark, signaling overload upstream instead of absorbing unbounded inflow.

**Why:** A spike fills queues until memory exhaustion, turning a slowdown into a total outage for every tenant.

**Detect:** grep `queue_size`, `max_concurrent_requests`, `high_watermark`, `429 Too Many Requests`, unbounded `Queue()`.

**References:** RFC 6585, Netflix Hystrix concurrency limits, CWE-770, AWS REL11-BP04
