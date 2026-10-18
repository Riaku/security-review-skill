---
categories: [email-security]
domains: [governance]
---

# BIMI & VMC Certificates

**SHOULD** publish BIMI records with a Verified Mark Certificate (VMC) and aligned DMARC policy to authenticate brand-mark display in inboxes.

**Why:** Without BIMI/VMC, spoofed phishing emails render indistinguishable from legitimate brand mail; with it, forged senders visibly fail.

**Detect:** `dig default._bimi.<domain>` for BIMI record; verify logo is SVGZ with valid VMC/CMC; confirm DMARC alignment is a prerequisite (BIMI requires enforcement policy).

**References:** bimigroup.org, Google Postmaster BIMI requirements, M3AAWG sender best practices

---

**Part of:** [email-security](../categories/email-security.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
