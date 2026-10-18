# Attack Surface Management (continuous exposure discovery)

**MUST** continuously discover and inventory every internet-facing asset (domains, subdomains, IPs, cloud endpoints) rather than relying on a static list.

**Why:** Forgotten shadow IT and stale exposed services are the most common initial-access entry points attackers find before defenders do.

**Detect:** Certstream/subdomain enumeration output, `external-exposure.csv`, cloud security hub findings, diff of DNS zone records vs. approved inventory.

**References:** OWASP WSTG-INFO-02, CWE-1059, NIST SP 800-119, AWS Security Hub, Cloudflare for Teams

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [security-practices](../categories/security-practices.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
