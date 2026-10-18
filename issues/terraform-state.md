---
categories: [deployment-release]
domains: [infrastructure]
---

# Terraform State

**MUST NOT** commit Terraform state files to repositories or store them on unencrypted disks; use a remote backend with encryption and state locking.

**Why:** State files embed plaintext secrets, resource IDs, and network topology, handing attackers a complete map plus credentials in one file.

**Detect:** grep tracked files for `terraform.tfstate`, `*.tfstate.backup`, check backend block for `backend "s3"` with `encrypt = true` and DynamoDB locking.

**References:** CIS Terraform 1.2/1.3, OWASP Secrets Management, CWE-312, HashiCorp backend security docs

---

**Part of:** [deployment-release](../categories/deployment-release.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
