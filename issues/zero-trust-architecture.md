# Zero Trust Architecture

**SHOULD** verify every request explicitly regardless of network location — no implicit trust for internal networks, device posture checked, per-request authorization, least-privilege service identity.

**Why:** Perimeter-based trust collapses the moment one host is compromised; zero trust contains blast radius by treating every call as coming from an attacker until proven otherwise.

**Detect:** look for mTLS everywhere / service mesh, identity-aware proxies (BeyondCorp-style), absence of "trusted internal network" CIDR allow-lists as sole authz, continuous session validation rather than once-at-connect.

**References:** NIST SP 800-207 Zero Trust Architecture, CISA Zero Trust Maturity Model

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [security-practices](../categories/security-practices.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
