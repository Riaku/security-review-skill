---
categories: [api-design]
domains: [backend]
---

# Unsafe Boundary Obligations

**MUST** document the caller preconditions of every unsafe or privilege-crossing API at the function itself.

**Why:** An unsafe boundary is safe only if callers uphold specific invariants. Undocumented obligations get violated by the next developer and surface as memory corruption or privilege escalation.

**Detect:** `unsafe fn` blocks with no `# Safety` section; FFI/syscall wrappers and `raw`/`trusted` parameters with no documented precondition.

**References:** arXiv:2308.04785, https://arxiv.org/abs/2308.04785
