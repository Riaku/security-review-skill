---
categories: [hardening-benchmarks]
domains: [infrastructure]
---

# Compiler Hardening Flags

**MUST** compile native release artifacts with stack protection, PIE/ASLR, full RELRO, FORTIFY, and non-executable memory enabled.

**Why:** Exploit mitigations raise the cost of every memory bug that review and testing failed to catch.

**Detect:** `checksec --file=<binary>` on the built artifact — expect canary, NX, PIE, Full RELRO, and FORTIFY reported as enabled.

**References:** OWASP C-Based Toolchain Hardening Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/C-Based_Toolchain_Hardening_Cheat_Sheet.html
