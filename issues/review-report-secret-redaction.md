---
categories: [secrets-crypto]
domains: [governance]
---

# Secret Redaction in Review Findings

**MUST NOT** reproduce a secret's value in review findings, pull-request comments, tickets or agent transcripts; cite the location and a short fingerprint instead.

**Why:** A finding that quotes the live key re-publishes it to everyone who can read the report, a wider audience than the repository had, and the copy outlives the fix in comment and ticket history.
**Detect:** read the latest review report and its thread for full key-shaped strings (`AKIA…`, `ghp_…`, `sk-…`, PEM headers, 32+ character hex) and for `.env` excerpts; every hit must appear as a path plus at most four trailing characters.
**References:** CWE-532, https://cwe.mitre.org/data/definitions/532.html, OWASP ASVS (V7 logging), https://owasp.org/www-project-application-security-verification-standard/, GitHub secret scanning, https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning
