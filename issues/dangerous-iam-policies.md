# Dangerous IAM Policies (admin/*, *:*, PassRole chains flagged by policy linting)

**MUST NOT** grant wildcard actions or resources (`*:*`, `admin/*`) or unscoped PassRole chains; policy linters must fail CI on them.

**Why:** Over-broad grants are the shortest path from a single leaked credential to full account takeover, and PassRole chains hide escalation inside "read-only" roles.

**Detect:** grep IAM JSON for `"Action": "*"`, `"Resource": "*"`, `iam:PassRole` without condition, `AdministratorAccess`; run policy-sentry, pmapper, tfsec checks.

**References:** AWS IAM security best practices, CWE-269, NIST SP 800-53 AC-6, Cloudsplaining, GCP Policy Intelligence
