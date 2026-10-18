---
categories: [email-security]
domains: [governance]
---

# Lookalike-Domain Monitoring

**SHOULD** continuously monitor for typosquat/lookalike registrations of your brand domains and take takedown action.

**Why:** Brand-adjacent domains (`yourcompany-secure.com`, homoglyph variants) are pre-staged for phishing before you know they exist; takedown is far cheaper before a campaign runs.

**Detect:** review for a monitoring service/cron (Dmarcian, Red Points, custom diff of newly-registered domains vs brand patterns); check homoglyph/keyboard-adjacent variants are in scope.

**References:** M3AAWG brand abuse guidance, Unicode homoglyph attacks, phishing pretexting reports

---

**Part of:** [email-security](../categories/email-security.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
