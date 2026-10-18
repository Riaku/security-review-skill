---
categories: [authentication, third-party-integrations]
domains: [backend]
---

# OAuth Third-Party Scope Minimization

**MUST** request the minimum OAuth scopes from identity providers and audit granted-scope drift for third-party app integrations.

**Why:** Over-scoped integrations (`offline_access`, full mailbox, full repo) turn a third-party breach into your breach; scopes granted years ago silently persist.

**Detect:** review OAuth app registrations for scopes beyond current feature needs; grep client code for scope strings vs actual API calls used; check admin consent logs for over-granted apps.

**References:** OAuth 2.0 BCP scope guidance, OWASP API Security (insufficient scope), Microsoft/Google admin consent audit docs

---

**Part of:** [authentication](../categories/authentication.md) · [third-party-integrations](../categories/third-party-integrations.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
