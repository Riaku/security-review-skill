---
categories: [security-practices]
domains: [backend]
---

# Independent penetration testing cadence and finding remediation tracking

**SHOULD** commission an external penetration test at least annually and after major architectural changes, with every finding tracked to closure in a ticketing system.

**Why:** Self-assessment shares the builder's blind spots; untracked findings recur across engagements.

**Detect:** `pentest` reports dated within 12 months, `remediation` tracker with finding IDs, contract/engagement records

**References:** OWASP WSTG, PTES, NIST SP 800-115, PCI DSS 11.4
