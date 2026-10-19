---
categories: [compliance-privacy, web-api-security]
domains: [backend, frontend]
---

# Partial Data Display

**MUST** return and display only the minimum sensitive value the feature needs, masking all but the last few characters by default.

**Why:** Full values in a response or a screen become full values in a screenshot, a support ticket, and a browser cache, for a user who only needed to recognize them.

**Detect:** grep API serializers and templates for full card, account, or identity numbers where a masked form would serve.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x23-V14-Data-Protection.md, CWE-200
