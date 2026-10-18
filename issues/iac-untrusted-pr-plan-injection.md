# IaC Plan/Apply Triggered from Untrusted Pull Requests

**MUST NOT** run `terraform apply` (or equivalent) directly from fork or untrusted PR content; apply only from a reviewed, trusted branch after human approval.

**Why:** Malicious HCL in a PR can exfiltrate state, open security-group holes, or destroy resources the moment CI auto-applies it.

**Detect:** CI configs auto-applying on `pull_request` events; plan jobs echoing full state containing secrets; missing manual approval gate before apply stage.

**References:** OWASP IaC Security, CWE-913, NIST SP 800-218 (SSDF), Terraform Cloud PR workflow docs, Checkov tfsec guidance