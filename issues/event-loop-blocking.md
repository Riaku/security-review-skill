# Event Loop Blocking

**MUST NOT** run CPU-heavy or synchronous blocking calls inside an async event loop handler.

**Why:** One blocking call stalls every concurrent request on the loop, turning a slow endpoint into a full service outage.

**Detect:** `time.sleep(` in async code, sync file/DB/HTTP calls in `async def`, `requests.` inside handlers, missing `run_in_executor`/`spawn_blocking`.

**References:** CWE-400, CWE-662, OWASP ASVS 5.3
