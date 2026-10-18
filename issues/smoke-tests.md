---
categories: [testing-strategy]
domains: [backend]
---

# Smoke Tests

**MAY** run a minimal post-deploy check (health endpoint, login round-trip, TLS handshake) to catch catastrophic security misconfiguration before full traffic shifts.

**Why:** A bad deploy that breaks TLS or disables auth needs seconds to detect, not a full suite run.

**Detect:** `curl -k`-free health checks, smoke stage in pipeline (`smoke.yml`, `post-deploy` job) asserting HTTPS status and auth cookie issuance.

**References:** OWASP ASVS V14.2 (config), NIST SP 800-218 PO.3, WSTG v4.2 (config management testing)

---

**Part of:** [testing-strategy](../categories/testing-strategy.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
