---
categories: [testing-strategy]
domains: [backend]
---

# Authorization Test Matrix

**MUST** test authorization as a matrix of actors against actions and objects, including cross-user, cross-tenant, and expired-role denials.

**Why:** Functional tests exercise the happy owner path; authorization bugs live in the pairs nobody wrote a test for.

**Detect:** grep the test suite for each endpoint's owner case only, and for absent `403`/`forbidden` assertions against a second user or tenant.

**References:** OWASP Authorization Regression Testing Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Regression_Testing_Cheat_Sheet.html
