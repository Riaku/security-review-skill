# VPCs

**MUST** Workloads of different trust levels live in separate VPCs or equivalent network boundaries, with explicit, audited peering rather than one flat network.

**Why:** A single VPC holding production, staging, and third-party integrations means one compromised host can laterally scan everything; the blast radius equals the entire address space.

**Detect:** Map VPCs and CIDR allocations; flag one VPC mixing prod with dev/staging. Review peering for transitive-routing hacks, `0.0.0.0/0` routes into peering connections, and missing flow logs.

**Bad:**
```hcl
# one VPC for everything: prod, staging, vendor VPN
resource "aws_vpc" "everything" { cidr_block = "10.0.0.0/8" }
```

**Good:**
```hcl
resource "aws_vpc" "prod"    { cidr_block = "10.10.0.0/16" }
resource "aws_vpc" "staging" { cidr_block = "10.20.0.0/16" }
# peering only where required, flow logs on
```

**References:** AWS VPC Peering FAQ, AWS Well-Architected Security pillar, CIS AWS Foundations 1.x
