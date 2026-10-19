---
categories: [security-practices]
domains: [backend]
---

# No Opt-In Security Controls

**MUST** enable security controls by default on every path, requiring an explicit recorded exception to disable one for a caller.

**Why:** A control that each developer must remember to invoke is absent wherever someone forgot, which is exactly where the exploit lands.

**Detect:** grep security helpers gated on a default-false flag or optional parameter (strict=False, verify=False, enable_xss=false)

**References:** Linux kernel self-protection, https://kernel.org/doc/html/latest/security/self-protection.html
