---
categories: [testing-strategy]
domains: [data]
---

# Test Fixture Data Hygiene

**MUST NOT** place production personal data, live credentials, or real customer records in test fixtures, examples, or seed data.

**Why:** Fixtures are copied into repositories, CI logs, and image layers with none of the controls that protect the production store. Once committed, the exposure is permanent and unrevokable.

**Detect:** grep fixture, seed, and example files for real-looking addresses and account numbers plus live key prefixes (`AKIA`, `sk_live_`, `ghp_`); confirm generators or synthetic data are used instead.

**References:** OWASP User Privacy Protection Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html, CWE-312 Cleartext Storage of Sensitive Information
