---
categories: [cloud-network]
domains: [infrastructure]
---

# Address Context Scoping

**MUST NOT** key durable trust, credentials, or cached state on a bare network address; re-validate whenever the network context changes.

**Why:** A private address means different devices on different networks, so address-keyed state silently authorizes a stranger after a network change.

**Detect:** grep for IP-keyed trust stores and caches (`allowlist[remote_addr]`, `sessions[ip]`, `trusted_ips.append`) and for any invalidation on address or network change.

**References:** WICG Private Network Access §5.5, https://wicg.github.io/private-network-access/, CWE-350
