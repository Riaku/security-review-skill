---
categories: [secrets-crypto]
domains: [backend]
---

# Constant Time After Compilation

**MUST** verify constant-time behavior on the compiled artifact, not only the source, because optimization passes can reintroduce timing leaks.

**Why:** A correct constant-time routine can be transformed into a branch on secret data, and only the generated code shows what the CPU executes.

**Detect:** command run a `dudect` or `ctgrind` timing harness against the built binary with the pinned compiler version and flags.

**References:** Compiler-introduced timing leaks, https://arxiv.org/abs/2507.06112, CWE-208 (Observable Timing Discrepancy)
