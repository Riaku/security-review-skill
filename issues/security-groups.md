# Security Groups

**MUST NOT** A security group admit `0.0.0.0/0` or `::/0` on administrative or data ports; prefer referencing other security groups over raw CIDR ranges.

**Why:** SGs are the de facto perimeter for every instance in a VPC, and one wide-open rule on Redis, Postgres, or SSH is internet-scanned within hours — ransomware entry points start exactly like this.

**Detect:** Grep Terraform for `cidr_blocks = ["0.0.0.0/0"]` in `ingress` blocks, especially paired with ports 22/3389/5432/3306/6379/27017. Flag blanket self-referencing groups and unused groups with unclear ownership.

**Bad:**
```hcl
ingress { from_port = 5432 to_port = 5432 protocol = "tcp"
         cidr_blocks = ["0.0.0.0/0"] }
```

**Good:**
```hcl
ingress { from_port = 5432 to_port = 5432 protocol = "tcp"
         security_groups = [aws_security_group.app.id] }  # SG-to-SG
```

**References:** CIS AWS Foundations 5.x, CWE-284, AWS VPC security group best practices
