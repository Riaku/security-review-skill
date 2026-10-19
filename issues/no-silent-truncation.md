---
categories: [correctness-pitfalls]
domains: [backend]
---

# No Silent Truncation

**MUST** reject values that exceed a fixed-size field or buffer instead of silently truncating security-relevant identifiers, paths, or hashes.

**Why:** A truncated identifier can collide with another principal or pass validation on a prefix while the consumer acts on the full intent.

**Detect:** grep fixed-size columns and slices on identifiers: `VARCHAR(16)`, `[:32]`, `substring(0,`, `strncpy(` on tokens, hashes, usernames, and paths.

**References:** SEI CERT C Coding Standard, https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard
