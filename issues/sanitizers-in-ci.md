---
categories: [testing-strategy]
domains: [backend]
---

# Sanitizers in CI

**MUST** build and test memory-unsafe code that parses untrusted input with address, undefined-behaviour, and thread sanitizers in CI.

**Why:** Sanitizers turn latent memory and concurrency bugs into loud, reproducible CI failures instead of remote code execution in production.

**Detect:** two CI jobs: `-fsanitize=address,undefined` and a separate `-fsanitize=thread` (MSan where the runtime allows), each running the parser test suite; a single combined flag set is a bug in the pipeline, not a passing gate.

**References:** OWASP C-Based Toolchain Hardening Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/C-Based_Toolchain_Hardening_Cheat_Sheet.html
