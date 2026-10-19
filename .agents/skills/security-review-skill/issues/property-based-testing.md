---
categories: [testing-strategy]
domains: [backend]
---

# Property-Based Testing

**SHOULD** assert invariants that must hold for all inputs — parsers never accept overlong payloads, validators reject every boundary case — rather than spot-checking examples.

**Why:** Example-based tests miss edge inputs (empty, huge, Unicode, negative) that are exactly where injection and overflow bugs live.

**Detect:** hypothesis (`@given`), fast-check (`fc.assert`), jqwik usage on parsers/validators; missing property specs on input-handling modules.

**References:** CWE-20, OWASP ASVS V5.1 (validation), NIST SP 800-218 (SSDF)
