---
categories: [web-api-security]
domains: [backend]
---

# Disable Setup Endpoints

**MUST** remove or disable installer, setup, and bootstrap endpoints once provisioning completes, and verify they are unreachable afterwards.

**Why:** Setup paths trust whoever reaches them first, so a forgotten one lets a stranger create an administrator account months after install.

**Detect:** grep routes for `setup`, `install`, `bootstrap`, `first-run`, and `wizard`; then curl each on a provisioned instance and expect 404 or 403.

**References:** NVD CVE-2023-22515, https://nvd.nist.gov/vuln/detail/CVE-2023-22515
