---
categories: [deployment-release]
domains: [infrastructure]
---

# Infrastructure-as-code state kept out of repositories and encrypted at rest

**MUST NOT** commit infrastructure-as-code state to a repository or keep it on an unencrypted disk; use a remote backend with encryption at rest and state locking. Terraform's `terraform.tfstate` is the common case; any IaC tool's state artifact is the same class of secret-bearing file.

**Why:** State files embed plaintext secrets, resource IDs, and network topology, handing attackers a complete map plus credentials in one file.

**Detect:** grep tracked files for `terraform.tfstate`, `*.tfstate.backup`, check backend block for `backend "s3"` with `encrypt = true` and DynamoDB locking.

**References:** CIS Terraform 1.2/1.3, OWASP Secrets Management, CWE-312, HashiCorp backend security docs

---

**Part of:** [deployment-release](../categories/deployment-release.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
