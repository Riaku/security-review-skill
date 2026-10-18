---
categories: [compliance-privacy, web-client-security]
domains: [frontend, governance]
---

# Cookie Consent

**SHOULD** block non-essential cookies until explicit user consent is obtained, with granular category controls.

**Why:** Setting tracking cookies before consent violates ePrivacy Directive and GDPR, exposing sites to regulatory fines and user distrust.

**Detect:** grep for analytics/advertising cookie initialization before consent check; inspect `CookieConsent`, `googleAnalytics`, `fbq` calls preceding consent gate.

**References:** ePrivacy Directive Art. 5(3), GDPR Recital 30, IAB TCF 2.0

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [web-client-security](../categories/web-client-security.md) · [frontend](../domains/frontend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
