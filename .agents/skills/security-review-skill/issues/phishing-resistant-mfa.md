---
categories: [authentication]
domains: [backend]
---

# Phishing-Resistant MFA

**SHOULD** require phishing-resistant authenticators, such as passkeys or hardware tokens, for privileged and administrative accounts.

**Why:** Passwords, SMS codes, and push approvals are phishable and remain the primary initial-access route to account takeover.

**Detect:** grep identity-provider policy as code for `sms`, `voice`, `push`, and `password` still enabled for admin groups, and for `webauthn`/`fido2` as optional rather than required.

**References:** OWASP Multifactor Authentication Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html, OWASP Passkey Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Passkey_Security_Cheat_Sheet.html
