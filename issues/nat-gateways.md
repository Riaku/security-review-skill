---
categories: [cloud-network]
domains: [infrastructure]
---

# NAT Gateways

**SHOULD** Outbound traffic from private subnets traverse a managed NAT gateway deployed one-per-AZ, and long-lived NAT instances with static EIPs be eliminated.

**Why:** A NAT instance is an ordinary VM: if compromised, the attacker inherits a trusted outbound path for exfiltration and C2, and one shared NAT turns a zonal failure into a region-wide egress outage.

**Detect:** Search IaC for `aws_instance` with `source_dest_check = false` — the DIY-NAT tell. Compare NAT gateway count against AZ count, and flag egress `0.0.0.0/0` where a filtering proxy is expected.

**Bad:**
```hcl
resource "aws_instance" "nat" {
  source_dest_check = false        # DIY NAT on a patchable VM
  associate_public_ip_address = true
}
```

**Good:**
```hcl
resource "aws_nat_gateway" "az_a" {
  allocation_id = aws_eip.nat_a.id
  subnet_id     = var.edge_subnet_a
}   # one per AZ; private route tables use their local NAT
```

**References:** AWS NAT gateway best practices, CIS AWS Foundations 2.x, AWS Well-Architected Reliability pillar

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
