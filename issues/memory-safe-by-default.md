---
categories: [correctness-pitfalls]
domains: [backend]
---

# Memory-Safe by Default

**SHOULD** implement parsers and other untrusted-input handling in a memory-safe language or runtime.

**Why:** Memory-safety defects are the largest share of exploitable weakness classes, and they disappear entirely in a memory-safe runtime.

**Detect:** `pygount` language mix for newly added parsers and protocol decoders; a new C/C++ component on an untrusted-input path is the finding (unsafe blocks inside Rust/Go code belong to unsafe-code-confinement).

**References:** CWE Top 25 (2024), https://cwe.mitre.org/top25/archive/2024/2024_cwe_top25.html, The Rustonomicon, https://doc.rust-lang.org/nomicon/, CISA Secure by Design, https://www.cisa.gov/securebydesign
