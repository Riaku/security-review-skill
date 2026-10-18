# Push-Payload Sensitivity

**MUST NOT** put secrets, tokens, full PII, or account-identifying detail in push notification payloads (they are stored/transmitted by third-party OS infrastructure and shown on lock screens).

**Why:** Push bodies pass through Apple/Google infrastructure and render on unlocked screens; a notification with a magic-login link or full card number is a shoulder-surf and relay attack.

**Detect:** grep push payload construction for tokens, codes, amounts, addresses; verify payloads are content-neutral ("You have a new message — open the app") with sensitive detail fetched in-app.

**References:** OWASP MASVS-STORAGE, APNs payload security guidance, lock-screen disclosure studies

---

**Part of:** [mobile](../categories/mobile.md) · [mobile](../domains/mobile.md) · [SKILL.md](../SKILL.md)
