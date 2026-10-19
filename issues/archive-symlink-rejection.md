---
categories: [web-api-security]
domains: [backend]
---

# Archive Symlink Rejection

**MUST** reject archive entries that are symbolic or hard links unless explicitly required, and then only to allowlisted targets.

**Why:** A link entry that survives extraction points outside the destination, so the next read or write lands on a file the archive chose.

**Detect:** grep extraction code for link handling (`is_symlink`, `link_target`, `member.issym`, `tarfile` filter) and for a destination containment check.

**References:** OWASP ASVS v5.0 V5, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x14-V5-File-Handling.md, CWE-59
