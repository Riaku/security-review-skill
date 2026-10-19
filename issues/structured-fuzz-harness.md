---
categories: [testing-strategy]
domains: [backend]
---

# Structured Fuzz Harness

**SHOULD** derive typed, structured inputs from the fuzz bytes so each harness reaches the parser's real code paths instead of one shallow entry point.

**Why:** Coverage is decided by harness design: a harness that never decodes its input exercises almost none of the parsing logic it claims to fuzz.

**Detect:** each fuzz target body: targets that forward raw bytes without constructing the format's typed message have no structured coverage

**References:** Trail of Bits Testing Handbook, https://github.com/trailofbits/testing-handbook
