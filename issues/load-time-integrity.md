---
categories: [supply-chain]
domains: [backend]
---

# Load-Time Integrity Verification

**SHOULD** verify a checksum or signature over interpreted code, plugins, and configuration files at load time against values recorded at deploy time.

**Why:** Deployment-time trust decays; a file modified after release executes with the application's own privileges and no other control notices.

**Detect:** grep plugin, script, and config loaders that read a file with no digest or signature check

**References:** OWASP A08:2021 Software and Data Integrity Failures, OWASP Go Secure Coding Practices, https://github.com/OWASP/Go-SCP
