# Memory Safety: Buffer Overflow & Use-After-Free

**MUST** bound every buffer write and never dereference freed or dangling memory in unsafe languages.

**Why:** Overflows and use-after-free are classic primitives for arbitrary code execution and privilege escalation.

**Detect:** `strcpy`/`sprintf`/`memcpy` without size checks, raw `malloc`/`free` lifetimes, indexing past array length, missing bounds sanitizer.

**References:** CWE-120, CWE-416, CWE-787, CERT MEM rules

---

**Part of:** [correctness-pitfalls](../categories/correctness-pitfalls.md) · [security-practices](../categories/security-practices.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
