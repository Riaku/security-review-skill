---
categories: [correctness-pitfalls]
domains: [backend]
---

# Uninitialized Memory Reads

**MUST NOT** read uninitialized memory on any path, including panic and early-exit paths between allocation and first write.

**Why:** A value always overwritten on the happy path is still observable when unwinding interrupts the sequence, leaking stale heap contents.

**Detect:** clippy MEM_REPLACE_WITH_UNINIT, or MSan on the C/C++ build

**References:** rust-clippy, https://github.com/rust-lang/rust-clippy
