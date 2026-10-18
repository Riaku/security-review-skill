# Cloud Metadata Endpoint Credential Theft (IMDS / 169.254.169.254)

**MUST** treat the link-metadata range (`169.254.169.254/32`, GCE `metadata.google.internal`, Azure `169.254.169.254/metadata`) as hostile territory: block it at the network layer from any workload that processes user-supplied URLs.

**Why:** Reaching the metadata service from a compromised or SSRF-able workload hands the attacker the node's IAM credentials verbatim — no exploitation needed, just a GET — and any single missing layer in the chain (v1-tolerant instance, open egress, string-only URL filter) completes the attack.

**Detect:** In SSRF filters, confirm the blocklist covers link-local, loopback, and cloud-specific IPs and is applied after DNS resolution, not on the raw string; test filters with decimal (`2852039166`), IPv6-mapped, and DNS-rebind forms. Check Kubernetes `hostAliases`, egress NetworkPolicies denying `169.254.169.254`, iptables/ip sets on nodes, container `hostNetwork` settings that sidestep pod-level blocks, and proxy configurations that allow CONNECT to it. On instances, verify `HttpTokens=required` plus `HttpPutResponseHopLimit=1` on launch templates. Search code for hardcoded `169.254.169.254` outside legitimate credential-fetching libraries.

**Bad:**
```python
url = user_input
if "localhost" not in url:      # trivially bypassed by decimal/hex IP forms
    requests.get(url)
```

**Good:**
```
# egress deny at the pod network boundary
ipset -A blacklist 169.254.169.254
iptables -A FORWARD -m set --match-set blacklist dst -j DROP
```

**References:** CWE-200, AWS IMDSv2 bulletin, GCP metadata protection docs, OWASP SSRF Prevention Cheat Sheet, CIS AWS 5.6/5.7

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [containers-k8s](../categories/containers-k8s.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
