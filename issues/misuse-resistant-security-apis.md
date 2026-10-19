---
categories: [api-design]
domains: [backend]
---

# Misuse-Resistant Security APIs

**SHOULD** make the safe path the default in security APIs, with every opt-out explicit, named and greppable.

**Why:** Developers use the default, so an unsafe default ships vulnerabilities at scale; an opt-out buried in configuration cannot be inventoried or restricted.

**Detect:** Security wrappers whose defaults disable checks: `verify=False`, `dangerouslyAllow*`, `Insecure*`, or `allow_all` as a parameter default.

**References:** Tink misuse-resistant crypto APIs, https://github.com/tink-crypto/tink
