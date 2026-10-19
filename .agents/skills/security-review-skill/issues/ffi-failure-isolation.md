---
categories: [correctness-pitfalls]
domains: [backend]
---

# FFI Failure Isolation

**MUST** isolate foreign or abort-capable code at the boundary and convert its failures into the host runtime's error model.

**Why:** An exception or panic crossing a language boundary is undefined behaviour in most runtimes, and an abort takes the whole process with it. Catching at the boundary keeps the failure local and attributable.

**Detect:** grep FFI wrappers for calls into foreign code with no `catch_unwind`/`try`/`except` around them, and for `abort`/`exit` on error paths.

**References:** ANSSI Secure Rust Guidelines, https://anssi-fr.github.io/rust-guide/, CWE-248 Uncaught Exception
