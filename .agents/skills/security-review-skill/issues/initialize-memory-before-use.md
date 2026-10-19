---
categories: [correctness-pitfalls]
domains: [backend]
---

# Initialize Memory Before Use

**MUST** initialize every buffer, struct, and allocation before it is read, and zero padding in structures passed across a trust boundary.

**Why:** An uninitialized read returns whatever the previous owner left there, leaking data and making security decisions nondeterministic.

**Detect:** MemorySanitizer build (`-fsanitize=memory`) in CI, plus grep for `malloc(` followed by field reads with no `memset`/struct initializer.

**References:** SEI CERT C Coding Standard, https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard
