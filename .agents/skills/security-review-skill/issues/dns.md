---
categories: [cloud-network]
domains: [infrastructure]
---

# DNS

**MUST NOT** base any security decision on DNS names or reverse DNS without validation; resolvers in use **MUST** be configured explicitly rather than inherited from DHCP.

**Why:** DNS is spoofable at the resolver, cache, and host-file level; trusting `*.internal` names or PTR records for authentication lets an attacker with resolver access impersonate services.

**Detect:** Inspect `/etc/resolv.conf` and container base images for unset or DHCP-supplied nameservers. Grep code for `gethostbyaddr` or auth checks keyed on hostname strings; review CoreDNS upstream forwarders.

**Bad:**
```python
if request.remote_addr.resolve_ptr().endswith(".internal.corp"):
    grant_admin(request)   # spoofable via PTR control
```

**Good:**
```python
# authenticate by certificate identity, never by name
if client_cert.subject == expected_service_identity:
    grant_admin(request)
```

**References:** CWE-350 (Reliance on Reverse DNS Resolution for a Security-Critical Action), OWASP A08:2021, RFC 1034
