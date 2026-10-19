---
categories: [security-practices]
domains: [governance]
---

# Advisory Scope Precision

**MUST** publish each security advisory with affected version ranges, vulnerable usage patterns, fixed versions, mitigations, and a CVE identifier.

**Why:** A vague advisory leaves consumers unable to decide whether they are affected, so the fix never ships. Precision is what turns disclosure into protection.

**Detect:** Advisory files and CHANGELOG entries carrying `Affected versions`, `Fixed in`, `CVE-20` - flag any advisory missing one of the three.

**References:** OpenSSF Concise Guide for Developing More Secure Software, https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Concise-Guide-for-Developing-More-Secure-Software.md, ISO/IEC 29147 Vulnerability disclosure, ISO/IEC 30111 Vulnerability handling processes
