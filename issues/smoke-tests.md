---
categories: [testing-strategy]
domains: [backend]
---

# Smoke Tests

**MAY** run a minimal post-deploy check (health endpoint, login round-trip, TLS handshake) to catch catastrophic security misconfiguration before full traffic shifts.

**Why:** A bad deploy that breaks TLS or disables auth needs seconds to detect, not a full suite run.

**Detect:** `curl -k`-free health checks, smoke stage in pipeline (`smoke.yml`, `post-deploy` job) asserting HTTPS status and auth cookie issuance.

**References:** OWASP ASVS 14.2 (configuration), NIST SP 800-218 (SSDF), WSTG v4.2 (configuration testing)
