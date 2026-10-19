---
categories: [testing-strategy]
domains: [backend]
---

# Test From the Attacker's View

**MUST** test the deployed system end to end against attacker paths, not only per-unit happy paths inside the code.

**Why:** Most exploitable flaws live in the seams between middleware, routing, and services, and unit tests mock exactly those seams away.

**Detect:** run an authenticated black-box pass (`zap-baseline.py -r report.html <url>` or the OWASP WSTG checklist) against a deployed environment in CI or pre-release.

**References:** OWASP Web Security Testing Guide, https://owasp.org/www-project-web-security-testing-guide/
