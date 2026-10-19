---
categories: [web-api-security]
domains: [backend]
---

# WASM Host Boundary

**MUST** restrict the host functions a sandboxed module may import to validated, capability-scoped calls, and assume module memory bugs reach them.

**Why:** The sandbox contains crashes, not bad code: an over-permissive host import turns a contained memory bug into host compromise or cross-tenant state leakage.

**Detect:** Read the module's import table and glue code; every host function needs typed, bounded arguments and no ambient filesystem or network authority.

**References:** OWASP WSTG WebAssembly Testing, https://github.com/OWASP/wstg/blob/master/document/4-Web_Application_Security_Testing/13-WebAssembly_Testing/00-WebAssembly_Testing_Overview.md
