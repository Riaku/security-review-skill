---
categories: [cloud-network]
domains: [infrastructure]
---

# Firewalls

**MUST** Default to deny for all inbound traffic, explicitly allowing only the ports and sources a service actually needs, with rules managed as code rather than clicked in a console.

**Why:** Rules added "temporarily" during incidents accumulate into a wide-open perimeter; a firewall whose real policy is unknown to anyone is not a control, and console-only changes leave no review trail.

**Detect:** Enumerate rulesets for `any`/`0.0.0.0/0` sources on management ports (22, 3389, 5432, 27017, 6379). Diff running state against committed config to catch console drift and ownerless rules.

**Bad:**
```
# "temporary" rule, now permanent
allow from 0.0.0.0/0 to port 22   # SSH open to the world
```

**Good:**
```
allow from 10.20.0.0/16 (ops-vpn) to port 22
deny  from any to any               # explicit default deny, logged
```

**References:** CWE-284, CIS Benchmark network rules sections, NIST SP 800-207 Zero Trust Architecture
