# Default & Weak Credentials in Shipped Software

**MUST NOT** ship software with default usernames/passwords or demo accounts enabled in production; force credential change on first login.

**Why:** Scanners sweep the internet for known default credentials (admin/admin, root/toor) and compromise unmodified deployments within minutes of exposure.

**Detect:** grep configs/seed files for `admin:admin`, `changeme`, `default_password`, hardcoded credentials in Docker images, demo accounts in fixtures shipped to prod.

**References:** CWE-1188, OWASP A05:2021, CIS Control 5.4, NIST SP 800-118

---

**Part of:** [authentication](../categories/authentication.md) · [hardening-benchmarks](../categories/hardening-benchmarks.md) · [backend](../domains/backend.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)
