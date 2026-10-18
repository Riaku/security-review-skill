# Infrastructure Drift Detection (live state vs IaC diffed and alerted)

**MUST** continuously diff live infrastructure against IaC definitions and alert on unauthorized manual changes.

**Why:** Console-clicked changes bypass review and become invisible holes — an undocumented open security group never gets fixed.

**Detect:** grep `terraform plan -detailed-exitcode` cron jobs, Driftctl, AWS Config drift rules, `kubectl diff -f`.

**References:** NIST SP 800-53 CM-3/CM-6, CIS Control 2, Terraform drift docs
