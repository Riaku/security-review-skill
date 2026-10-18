---
categories: [deployment-release, secrets-crypto]
domains: [backend, infrastructure]
---

# Plaintext secrets persisted in infrastructure-as-code state and outputs

**MUST** mark secret-bearing variables and outputs sensitive and store generated state and plan artifacts encrypted under access control; never expose raw state in logs, CI output or pull requests. Terraform's `sensitive = true` and `terraform output` are the common case.

**Why:** State files record every resource attribute in plaintext, so a leaked backend, backup, or plan output hands over all managed credentials at once.

**Detect:** `sensitive = false` or absent on secret attributes, `terraform.tfstate` in git, `terraform output` without `-json | jq` masking, unencrypted S3 backend.

**References:** HashiCorp sensitive data guidance, CWE-312, NIST SP 800-53 SC-28

---

**Part of:** [deployment-release](../categories/deployment-release.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
