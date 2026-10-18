---
categories: [correctness-pitfalls]
domains: [backend]
---

# Thread Safety

**MUST** protect shared mutable state with locks, atomics, or immutability; never assume single-threaded execution.

**Why:** Unprotected races corrupt data intermittently and produce security holes that only appear under production load.

**Detect:** Shared dict/list mutated without `Lock`/`mutex`/`synchronized`, check-then-act on globals, non-atomic `count += 1`, cached mutable singletons.

**References:** CWE-362, CWE-366, OWASP ASVS 12.3
