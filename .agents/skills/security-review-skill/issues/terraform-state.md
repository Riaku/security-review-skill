---
categories: [deployment-release, secrets-crypto]
domains: [backend, infrastructure]
---

# Infrastructure-as-code state kept out of repositories and encrypted at rest

**MUST NOT** commit infrastructure-as-code state to a repository or keep it on an unencrypted disk; use a remote backend with encryption at rest and state locking, and mark secret-bearing variables and outputs `sensitive` so plan output, CI logs, and pull requests cannot echo them. Terraform's `terraform.tfstate` and `terraform output` are the common case; any IaC tool's state artifact is the same class of secret-bearing file.

**Why:** State files and plan artifacts record every resource attribute in plaintext — secrets, resource IDs, network topology — so a leaked backend, backup, or CI log hands over all managed credentials at once.

**Detect:** grep tracked files for `terraform.tfstate`, `*.tfstate.backup`; check the backend block for `backend "s3"` with `encrypt = true` and DynamoDB locking; scan variables and outputs for missing `sensitive = true` and CI steps that print `terraform output`/`terraform plan` unmasked.

**References:** CIS Terraform 1.2/1.3, OWASP Secrets Management, CWE-312, HashiCorp backend security docs
