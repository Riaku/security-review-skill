---
categories: [cloud-network]
domains: [infrastructure]
---

# Firewalls & Security Groups

**MUST** Default to deny for all inbound traffic, explicitly allowing only the ports and sources a service actually needs, with rules managed as code rather than clicked in a console; security groups in particular **MUST NOT** admit `0.0.0.0/0` or `::/0` on administrative or data ports, and prefer referencing other security groups over raw CIDR ranges.

**Why:** Rules added "temporarily" during incidents accumulate into a wide-open perimeter; a firewall whose real policy is unknown to anyone is not a control, and console-only changes leave no review trail. Security groups are the de facto perimeter for every instance in a VPC, and one wide-open rule on Redis, Postgres, or SSH is internet-scanned within hours — ransomware entry points start exactly like this.

**Detect:** Enumerate rulesets for `any`/`0.0.0.0/0` sources on management ports (22, 3389, 5432, 27017, 6379). Grep Terraform `ingress` blocks for `cidr_blocks = ["0.0.0.0/0"]` or `::/0` on administrative or data ports (22/3389/5432/3306/6379/27017), and flag blanket self-referencing groups and unused groups with unclear ownership. Diff running state against committed config to catch console drift.

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

**References:** CWE-284, CIS Benchmark network rules sections, CIS AWS Foundations 5.x, AWS VPC security group best practices, NIST SP 800-207 Zero Trust Architecture
