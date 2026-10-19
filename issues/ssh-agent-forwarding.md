---
categories: [secrets-crypto]
domains: [infrastructure]
---

# SSH Agent Forwarding Disabled

**MUST NOT** leave SSH agent forwarding enabled on bastion or jump hosts.

**Why:** Forwarding hands any compromised intermediate host the developer's identity, without that host ever touching the key.

**Detect:** grep for ForwardAgent yes, AllowAgentForwarding yes, and ssh -A in scripts and config

**References:** Fystack Developer Security Handbook, https://github.com/fystack/developer-security-handbook
