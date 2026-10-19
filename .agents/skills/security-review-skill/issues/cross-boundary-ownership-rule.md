---
categories: [correctness-pitfalls]
domains: [backend]
---

# Cross-Boundary Ownership Rule

**MUST** define, for each resource crossing a language or runtime boundary, who allocates it, who frees it, and which side owns it.

**Why:** When both sides assume the other frees, memory leaks; when both free, the second free is a write primitive. Ambiguous ownership across a boundary is a memory-safety bug waiting for load.

**Detect:** judgment: the FFI or native interface declarations and their doc comments — every opaque pointer, buffer, and handle has a stated owner and free path.

**References:** ANSSI Secure Rust Guidelines, https://anssi-fr.github.io/rust-guide/, CWE-415 Double Free
