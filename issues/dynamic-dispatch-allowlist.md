---
categories: [web-api-security]
domains: [backend]
---

# Dynamic Dispatch Allowlist

**MUST** allowlist the dispatchable targets of any method-by-name, handler-by-string, or plugin-by-name path that touches request data.

**Why:** Dynamic dispatch promotes any attacker-chosen name into an entry point, including internals never meant to be reachable from the edge.

**Detect:** grep for dispatch on request data: `send(params`, `public_send(`, `getattr(obj, request`, `Class.forName(`, `method_call(user_input)`.

**References:** Brakeman: dangerous send, https://brakemanscanner.org/docs/warning_types/, CWE-470 (Unsafe Reflection)
