# Dangerous IAM Policies (admin/*, *:*, PassRole chains flagged by policy linting)

**MUST NOT** grant wildcard actions/resources (`*:*`, `admin/*`) or unscoped PassRole; linters must fail CI on them.

**Why:** Over-broad grants turn one leaked credential into full account takeover; PassRole hides escalation inside "read-only" roles.

**Detect:** grep IAM JSON for `"Action": "*"`, `"Resource": "*"`, bare `iam:PassRole`, `AdministratorAccess`.

**References:** AWS IAM best practices, CWE-269, NIST SP 800-53 AC-6, Cloudsplaining, GCP Policy Intelligence
