---
categories: [correctness-pitfalls]
domains: [backend]
---

# Check Return Values

**MUST** check and act on the return value of every call that can fail, including writes, closes, and authorization lookups.

**Why:** An ignored failure leaves the system in a state the next line assumes is valid, so a failed check silently becomes an allow.

**Detect:** grep discarded results: `_ = `, `except.*:\s*pass`, `if err != nil { }` with an empty body, `(void)` casts, and bare `write(`/`close(`/`send(` statements.

**References:** CWE Top 25 (2024), https://cwe.mitre.org/top25/archive/2024/2024_cwe_top25.html, SEI CERT C Coding Standard, https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard
