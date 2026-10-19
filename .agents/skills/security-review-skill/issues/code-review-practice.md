---
categories: [cicd-pipeline-security, testing-strategy]
domains: [backend, infrastructure]
---

# Code Review Practice

**MUST** require at least one independent reviewer for every change touching authentication, cryptography, or input handling, with a documented security checklist and a response SLA.

**Why:** Single-author security code ships logic errors and backdoors that a second pair of eyes reliably catches.

**Detect:** CODEOWNERS covering auth/crypto paths, PR templates with security checklist items, branch protection requiring ≥1 approval; self-merged security PRs in git log.

**References:** OWASP ASVS V1.1.7, NIST SP 800-218 (SSDF) (code review), OWASP Code Review Guide v2, CWE-1068 (Inconsistency Between Implementation and Documented Design)
