---
categories: [web-api-security]
domains: [backend]
---

# Bot Protection

**MUST** challenge automated clients on login, signup, password-reset, and other abuse-prone flows with bot detection or a challenge (fingerprinting, proof-of-work, CAPTCHA), on top of whatever rate limiting applies.

**Why:** Credential stuffing and signup abuse are spread across large proxy pools, so per-IP throttling alone does not stop them; a challenge is what separates a script from a user.

**Detect:** grep auth flows for a challenge step (`captcha`, `recaptcha`, `turnstile`, `hcaptcha`, `bot_detection`, `proof_of_work`) or bot-detection middleware; a login route with throttling but no challenge at all.

**References:** OWASP A04:2021, CWE-770, OWASP Credential Stuffing Prevention Cheat Sheet
