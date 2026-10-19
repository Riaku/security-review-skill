---
categories: [web-api-security]
domains: [backend, infrastructure]
---

# Served Extension Allowlist

**MUST** configure the web tier to serve only an allowlist of file extensions, so carelessly placed source or configuration files cannot be downloaded.

**Why:** Uploads, editor backups, and deployment artifacts land in the document root, and a permissive handler serves them as text.

**Detect:** grep web-server config for extension allowlisting (`location ~* \.(css|js|png)$`, `FilesMatch`) and for a catch-all static handler.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x22-V13-Configuration.md, CWE-552
