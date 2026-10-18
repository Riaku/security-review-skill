# Dangerous IAM Policies (admin/*, *:*, PassRole chains flagged by policy linting)

**MUST NOT** grant wildcard actions/resources (`*:*`, `admin/*`) or unscoped PassRole; linters must fail CI on them.

**Why:** Over-broad grants turn one leaked credential into full account takeover; IaC makes the blast radius reproducible across every environment the module touches, and PassRole hides escalation inside "read-only" roles.

**Detect:** Grep IAM JSON for `"Action": "*"`, `"Resource": "*"`, bare `iam:PassRole`, `AdministratorAccess`. Lint Terraform `aws_iam_policy`/`google_service_account_iam_*`, CloudFormation `AWS::IAM::Policy`, and Pulumi policy docs for wildcards and modules that accept `policy_json` verbatim; run Cloudsplaining or `tfsec`/`checkov` IAM rules in CI and flag any policy the analyzer reports as admin-equivalent.

**References:** AWS IAM best practices, CWE-269, NIST SP 800-53 AC-6, Cloudsplaining, GCP Policy Intelligence, CIS AWS 5.28–5.36
