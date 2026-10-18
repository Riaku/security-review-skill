# Dependency Vulnerabilities

**MUST** scan third-party libraries against a current advisory database (OSV/GHSA) in CI and fail builds on critical or high findings.

**Why:** Unpatched library CVEs are the most common entry point for remote code execution and data breaches.

**Detect:** `requirements.txt`, `package-lock.json`, `go.mod`; run `pip-audit`, `npm audit`, `govulncheck`; grep `.github/workflows` for `osv-scanner`.

**References:** OWASP A06:2021, CWE-1104, SCB-001
