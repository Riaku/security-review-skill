---
categories: [authentication, mobile]
domains: [backend, mobile]
---

# Push-Token Binding & Rotation

**MUST** bind APNs/FCM device tokens to the authenticated user+device and invalidate on logout/account change; never accept a token from an unauthenticated registration.

**Why:** Unbound push tokens let an attacker register their device against someone's account (token swap) and receive their notifications — 2FA codes, account alerts, private messages.

**Detect:** grep push registration endpoints for auth requirement and user+device binding; check logout path unregisters tokens; flag token storage without account association or per-install rotation.

**References:** OWASP MASVS-AUTH, APNs/FCM security guidance, push-token hijacking CVEs

---

**Part of:** [authentication](../categories/authentication.md) · [mobile](../categories/mobile.md) · [backend](../domains/backend.md) · [mobile](../domains/mobile.md) · [SKILL.md](../SKILL.md)
