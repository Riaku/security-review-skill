---
categories: [web-api-security]
domains: [backend]
---

# Format String Injection

**MUST** never let untrusted data become the format string itself; pass it only as an argument to a fixed format.

**Why:** Attacker-controlled format strings read or write memory in native code and silently swallow argument mismatches everywhere else.

**Detect:** grep `printf(user`, `fmt.Sprintf(user`, `.format(request`, `% (request`, and `String.format(` calls whose first argument is a variable.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md
