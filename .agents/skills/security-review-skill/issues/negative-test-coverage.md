---
categories: [testing-strategy]
domains: [backend]
---

# Negative Test Coverage

**MUST** include negative tests asserting that unauthorized, malformed, and out-of-policy operations fail, not only that valid operations succeed.

**Why:** A suite that tests only the happy path passes just as loudly when an authorization check is deleted. Negative tests are what make 'merge if green' a meaningful gate.

**Detect:** grep test suites for assertions on 401/403/400 paths, `pytest.raises`, and `expect(...).toThrow`; modules with only success-path cases are the finding.

**References:** GitLab secure coding guidelines, https://docs.gitlab.com/development/secure_coding_guidelines/, OpenSSF Concise Guide for Developing More Secure Software, https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Concise-Guide-for-Developing-More-Secure-Software.md
