---
categories: [cloud-network]
domains: [infrastructure]
---

# IPv6

**MUST NOT** IPv6 be enabled on an interface or load balancer without the same firewall coverage applied to IPv4; every rule set needs a `::/0` exposure review.

**Why:** IPv6 is often enabled by default or by an OS upgrade while firewall tooling manages only IPv4, leaving a fully routable, unfiltered second path into every host — and IPv4-only audits can't see it.

**Detect:** Audit security groups and host firewalls for IPv6 separately; flag `::/0` ingress on non-edge ports. Check `ip -6 addr` and SLAAC/Accept-RA settings on server subnets; verify WAF and logging actually bind the v6 listener.

**Bad:**
```bash
# IPv4 firewalled, IPv6 autoconfigured and wide open
ip6tables -L   # policy ACCEPT on everything
```

**Good:**
```bash
# same default-deny posture on both families, one policy source
ip6tables -P INPUT DROP
ip6tables -A INPUT -p tcp --dport 443 -j ACCEPT
```

**References:** CIS Benchmarks dual-stack sections, AWS IPv6 security group guidance, NIST SP 500-267r1
