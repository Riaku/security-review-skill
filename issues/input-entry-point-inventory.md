---
categories: [security-practices, web-api-security]
domains: [backend, mobile]
---

# Input Entry Point Inventory

**MUST** enumerate every data-entry point — network, IPC, files, deep links, clipboard, background sync — and validate each as an untrusted boundary.

**Why:** Teams validate the HTTP API and forget the deep link, the shared file, or the IPC message, each of which reaches the same privileged code. An unlisted entry point never gets reviewed.

**Detect:** judgment: the data-flow diagram or threat model — every entry point listed with its parser, validation, and trust level, cross-checked against platform entry declarations in the app manifest.

**References:** OWASP MASVS-CODE-4 (input validation), https://github.com/OWASP/masvs/blob/master/controls/MASVS-CODE-4.md, OWASP Threat Modeling
