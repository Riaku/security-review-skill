# Long Polling

**MAY** use long polling where SSE or WebSockets are unavailable, but each held request MUST have a server-side timeout and per-client connection cap.

**Why:** Held-open requests with no timeout let clients pin worker threads indefinitely, collapsing capacity under modest concurrency.

**Detect:** polling handlers with no `setTimeout`/deadline, absent per-IP connection limits on `/poll` endpoints.

**References:** CWE-400, OWASP ASVS V5.2, MDN long polling guidance
