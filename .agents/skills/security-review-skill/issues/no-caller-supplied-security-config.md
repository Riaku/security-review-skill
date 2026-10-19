---
categories: [api-design]
domains: [backend]
---

# No Caller-Supplied Security Config

**MUST** let a caller pass in the sanitizer, validator or policy that governs its own operation.

**Why:** A pass-through parameter turns the safety check into an argument the attacker controls, and each call site can opt out without touching the library.

**Detect:** Security-helper signatures taking `sanitizer=`, `validator=`, `policy=` or `trusted=` and forwarding them to the sink.

**References:** Trusted Types, https://w3c.github.io/trusted-types/dist/spec/
