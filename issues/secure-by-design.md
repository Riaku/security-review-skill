---
categories: [security-practices]
domains: [backend]
---

# Secure by Design (architectural input, not a patch)

**MUST** treat security requirements as architectural inputs at design time — least privilege, defense in depth, secure defaults — not bolt-ons retrofitted after review.

**Why:** Architecture that assumes trust is unpatchable later; every bolt-on inherits the original flaw's blast radius.

**Detect:** design docs citing `least privilege` / `defense in depth`, ADRs with security sections, default-deny network policies

**References:** NIST SP 800-160, Saltzer & Schroeder principles, OWASP ASVS V1, CISA Secure by Design Pledges

---

**Part of:** [security-practices](../categories/security-practices.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
