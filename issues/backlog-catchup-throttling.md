# Backlog Catch-Up Throttling

**SHOULD** throttle post-outage backlog replay below full consumer capacity so catch-up traffic does not overwhelm downstream services still recovering.

**Why:** Releasing a queued storm at full speed after an outage can knock over the very dependency that just came back, restarting the failure cycle.

**Detect:** grep recovery/runbook configs for missing `rate_limit`, `throttle`, `max_concurrency` on replay; consumers configured to drain queues unbounded on startup.

**References:** AWS SQS long polling backpressure, NIST SP 800-61 incident containment, Google SRE overload handling
