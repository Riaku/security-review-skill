---
categories: [sre-incidents]
domains: [reliability]
---

# Stateless Services

**SHOULD** keep session and application state external (datastore, token) so any replica can serve any request.

**Why:** Locally stored sessions break autoscaling and failover; a killed node silently logs users out or loses their cart.

**Detect:** `session.save_path` on local disk, `JSESSIONID` sticky sessions, writes to `/tmp` or pod-local volumes, `sessionAffinity: ClientIP`.

**References:** The Twelve-Factor App (processes), NIST SP 800-178, CWE-384

---

**Part of:** [sre-incidents](../categories/sre-incidents.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
