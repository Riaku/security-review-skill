---
categories: [authentication]
domains: [backend]
---

# Step-Up Authentication

**MUST** require fresh re-authentication for high-consequence operations such as payments, credential changes, and privilege grants.

**Why:** A live session proves someone logged in earlier, not that the account owner is the person performing this action now.

**Detect:** grep the money-change, email-change, password-change, and role-grant handlers for a `reauth`, `auth_time`, `amr`, or MFA-challenge check; absence is the finding.

**References:** OWASP Transaction Authorization Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html, NIST SP 800-63B, https://pages.nist.gov/800-63-3/sp800-63b.html
