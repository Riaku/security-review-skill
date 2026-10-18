---
categories: [testing-strategy]
domains: [backend]
---

# Unit Tests

**MUST** cover every security-relevant function (auth checks, parsers, validators) with fast isolated tests asserting both accept and reject paths.

**Why:** Untested validation logic silently passes malformed input straight into privileged code paths.

**Detect:** test files named `*_test.py`, `*.test.js` adjacent to auth/parser modules; coverage reports showing <80% on security-critical files.

**References:** OWASP ASVS V4.1, CWE-1232, NIST SP 800-218 (SSDF)

---

**Part of:** [testing-strategy](../categories/testing-strategy.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
