---
categories: [regulatory-frameworks, security-practices]
domains: [backend, government-compliance]
---

# Cyber insurance alignment: coverage preconditions and denial clauses

**MUST NOT** let representations on insurance applications (MFA everywhere, EDR deployed, backups tested) drift from actual configuration, since denial clauses void claims on misrepresentation.

**Why:** Insurers investigate post-incident and deny payouts when stated controls are absent—leaving the breach cost entirely self-funded.

**Detect:** grep policy "warranty", "condition precedent" against live config: MFA, EDR/antivirus, offline backups, patch SLA mismatches.

**References:** ISO 27001/27017, CVE-based exclusion clauses, Marsh/Gallagher cyber underwriting guidance
