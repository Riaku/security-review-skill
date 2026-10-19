---
categories: [correctness-pitfalls]
domains: [backend]
---

# Blocking the Shared Concurrency Primitive

**MUST NOT** run CPU-heavy or synchronous blocking calls inside a shared event loop / cooperative-scheduling context.

**Why:** One blocking call stalls every concurrent request on that loop or worker pool, turning a slow endpoint into a full service outage.

**Detect:** sleep/sync file/DB/HTTP calls inside async handlers (e.g. `time.sleep` in `async def`, sync HTTP client calls in handlers), missing offload mechanisms (`run_in_executor`, `spawn_blocking`, dedicated worker pool) for blocking work.

**References:** CWE-400, CWE-662, OWASP ASVS V11.1.3/V11.1.4
