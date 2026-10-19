---
categories: [correctness-pitfalls]
domains: [backend]
---

# Unsafe Code Confinement

**MUST** confine escape-hatch code to the smallest possible region, forbid it where unnecessary, and audit every remaining block.

**Why:** Memory-safety guarantees stop at the first unchecked block, and one unchecked pointer invalidates the argument for the whole module. A short reviewed list is auditable; scattered blocks are not.

**Detect:** command: `cargo geiger`, `#![forbid(unsafe_code)]` or `-D unsafe` lints, and `grep -rn unsafe` against a per-crate allowed list.

**References:** ANSSI Secure Rust Guidelines, https://anssi-fr.github.io/rust-guide/, Empirical study of Rust unsafe code (arXiv 2003.03296), https://arxiv.org/abs/2003.03296
