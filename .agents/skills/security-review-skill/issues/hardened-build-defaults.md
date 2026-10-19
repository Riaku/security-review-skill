---
categories: [hardening-benchmarks]
domains: [infrastructure]
---

# Hardened Build Defaults

**MUST NOT** disable compiler or runtime hardening defaults for performance or compatibility without a recorded, approved exception.

**Why:** Stack protection, ASLR and RELRO are cheap only until removed; one build-flag tweak turns a memory bug into reliable code execution.

**Detect:** `-fno-stack-protector`, `-z execstack`, `-no-pie`, `-Wl,-z,norelro` or `mprotect(PROT_EXEC)` in build files and Dockerfiles.

**References:** SAFECode Fundamental Practices v3 (2018), https://safecode.org/wp-content/uploads/2018/03/SAFECode_Fundamental_Practices_for_Secure_Software_Development_March_2018.pdf, CWE-693
