# Infrastructure Drift Detection (live state vs IaC diffed and alerted)

**MUST** continuously diff live infrastructure state against IaC definitions and alert on unauthorized manual changes.

**Why:** Console-clicked changes bypass review and become invisible security holes — an open security group nobody wrote down never gets fixed.

**Detect:** grep for `terraform plan -detailed-exitcode` scheduled jobs, `drift`, `terraformer`, Driftctl, AWS Config `detect-config-drift`, `kubectl diff -f` cron checks.

**References:** NIST SP 800-53 CM-3/CM-6, CIS Control 2, Terraform drift detection docs, AWS Config conformance packs
