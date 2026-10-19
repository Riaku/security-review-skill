---
categories: [api-design]
domains: [backend]
---

# Capability Wrapper Types

**MUST** confine dangerous capabilities inside validated wrapper types so an untrusted value cannot reach the sink unparsed.

**Why:** A rule enforced by the type system cannot be forgotten at a new call site. Raw strings everywhere make every sink a fresh review question.

**Detect:** Inspect sink signatures: the safe API takes a wrapper (parsed URL, trusted markup, bound query) rather than a raw string.

**References:** Trusted Types, https://w3c.github.io/trusted-types/dist/spec/
