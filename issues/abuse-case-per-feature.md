---
categories: [security-practices]
domains: [governance]
---

# Abuse Cases Per Feature

**SHOULD** write an abuse case for every user-facing feature, naming the attacker goal, the abused flow, and the control that stops it.

**Why:** User stories describe intended behavior; the gap between that and what an attacker can make the system do is the bug backlog.

**Detect:** grep feature specs and PRDs for `abuse` or `misuse`; a feature directory with no abuse case is the finding.

**References:** OWASP A04:2021 Insecure Design, OWASP Abuse Case Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet.html
