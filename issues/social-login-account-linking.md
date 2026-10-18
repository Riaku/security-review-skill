---
categories: [authentication]
domains: [backend]
---

# Social Login Account-Linking Takeover

**SHOULD NOT** auto-link a social identity (Google/GitHub) to an existing local account by matching email alone without verifying the user controls that account.

**Why:** An attacker registers a social account using the victim's email, then logs in and gets auto-linked to the victim's existing profile with full access.

**Detect:** grep OAuth callback for auto-link on `email` match without prior password/MFA confirmation, missing `account_linking` verification step, `findOrCreate` by email.

**References:** OWASP A07:2021, CWE-287, CWE-346, Auth0 Account Linking Vulnerability advisory

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
