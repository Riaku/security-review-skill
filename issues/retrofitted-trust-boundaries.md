---
categories: [correctness-pitfalls, security-practices]
domains: [backend, infrastructure]
---

# Retrofitted Trust Boundaries

**MUST** re-review every interface that retrofitting isolation creates — a module promoted to a service, a sidecar, a plugin, a worker, or a sandboxed process — as an untrusted boundary, because both sides were written assuming in-process trust.

**Why:** The split creates a trust boundary the code was never designed for: the callee must now be assumed hostile, since isolating it is the whole point, so every return value, callback registration, shared-memory field and call-order assumption becomes attacker-controlled input to code that used to share an address space with it. The same test applies before any split — a native library loaded in-process already returns values across a boundary that exists today.

**Detect:** a new service, sidecar or worker whose handler consumes the other side's return values, callbacks or shared fields with no local validation; plugins handed host objects by reference or given hooks into host state; FFI/native library returns used without checks; an interface whose contract lives only in documentation; a decomposition PR with no boundary-interface review attached.

**References:** CWE-501, CWE-345
