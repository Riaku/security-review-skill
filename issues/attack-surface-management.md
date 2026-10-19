---
categories: [cloud-network, security-practices]
domains: [backend, infrastructure]
---

# Attack Surface Management (continuous exposure discovery)

**MUST** continuously discover and inventory every internet-facing asset (domains, subdomains, IPs, cloud endpoints) rather than relying on a static list.

**Why:** Forgotten shadow IT and stale exposed services are the most common initial-access entry points attackers find before defenders do.

**Detect:** Certstream/subdomain enumeration output, `external-exposure.csv`, cloud security hub findings, diff of DNS zone records vs. approved inventory.

**References:** OWASP WSTG-INFO-02, CWE-1059, NIST SP 800-53 RA-5/CM-8, AWS Security Hub, Cloudflare One
