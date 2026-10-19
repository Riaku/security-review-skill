---
categories: [correctness-pitfalls]
domains: [backend]
---

# Debouncing

**SHOULD** debounce or throttle high-frequency triggers (keystrokes, resize, webhooks) so bursts do not fan out into redundant work.

**Why:** Without it, each event fires a request or job, overwhelming backends and amplifying a small client into a self-inflicted DoS.

**Detect:** Keyup/scroll/resize handlers calling APIs directly, webhook consumer with no dedupe window, missing `debounce`/`throttle`/rate-limit middleware.

**References:** CWE-770, CWE-400, OWASP API4:2023
