---
categories: [cloud-network]
domains: [infrastructure]
---

# Subnets

**MUST NOT** Stateful application servers or databases sit in subnets that auto-assign public IPs; only load balancers, NAT gateways, and bastions belong in public subnets.

**Why:** A compute instance with a routable public address is directly exposed to internet-wide scanning, bypasses the load balancer's WAF and TLS termination, and becomes the easiest lateral entry point.

**Detect:** In Terraform/CloudFormation check `map_public_ip_on_launch = true` on non-edge subnets and `associate_public_ip_address` in launch templates. Verify app/DB subnets have no IGW route.

**Bad:**
```hcl
resource "aws_subnet" "app" {
  map_public_ip_on_launch = true   # every app pod internet-reachable
  route_table_id          = aws_route_table.igw.id
}
```

**Good:**
```hcl
resource "aws_subnet" "app_private" {
  map_public_ip_on_launch = false
  route_table_id = aws_route_table.nat_only.id  # no IGW route
}
```

**References:** CIS AWS Foundations 1.x, AWS VPC best practices, CWE-284
