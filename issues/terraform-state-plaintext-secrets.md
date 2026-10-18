# Plaintext Secrets Persisted in Terraform State and Outputs

**MUST** mark sensitive Terraform variables and outputs with `sensitive = true` and store state remotely with access controls and encryption; never expose raw state in logs or PRs.

**Why:** State files record every resource attribute in plaintext, so a leaked backend, backup, or plan output hands over all managed credentials at once.

**Detect:** `sensitive = false` or absent on secret attributes, `terraform.tfstate` in git, `terraform output` without `-json | jq` masking, unencrypted S3 backend.

**References:** HashiCorp sensitive data guidance, CWE-312, NIST SP 800-53 SC-28
