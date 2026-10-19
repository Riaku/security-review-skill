---
categories: [compliance-privacy]
domains: [backend]
---

# Strip Upload Metadata

**MUST** strip embedded metadata from user-submitted files before storage or publication unless the user explicitly consents to keeping it.

**Why:** Location, device, and author fields travel inside ordinary photos and documents, publishing facts the user never chose to disclose.

**Detect:** exiftool on stored uploads and check for GPS, device, and author tags.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x23-V14-Data-Protection.md, CWE-200
