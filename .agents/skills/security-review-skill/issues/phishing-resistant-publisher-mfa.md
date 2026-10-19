---
categories: [authentication]
domains: [governance]
---

# Phishing-Resistant Publisher MFA

**MUST** require phishing-resistant authentication for accounts that can publish artifacts or change package ownership.

**Why:** One-time codes are relayed through a proxy page in real time, so a phished maintainer still hands over a valid code. Hardware-bound credentials do not transfer.

**Detect:** IdP and registry policy: publish-capable accounts enforce FIDO2/WebAuthn rather than TOTP or SMS.

**References:** Filippo Valsorda: compromise survey, https://words.filippo.io/dispatches/compromise-survey/
