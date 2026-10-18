# Cloud IAM privilege escalation path review (PassRole, policy inheritance, wildcards)

**MUST** review every IAM policy diff for escalation vectors — role-passing grants, inherited or propagated policy chains, and wildcard patterns — before it reaches a live account, not after an incident hunt finds it.

**Why:** Escalation rarely arrives as one obvious admin grant; it hides in combinations (PassRole plus a role that trusts you, or a wildcard that later resolves to a new powerful action). Reviewing the diff in isolation misses how the new permission composes with what already exists.

**Detect:** For each PR touching IAM: does it add `PassRole`, and to whom can that principal pass roles? Do managed-policy attachments or GCP folder/organization inheritance silently widen the effective set? Does any `NotAction` or `Resource: "*"` exist that future service launches will inherit? Run PMapper or IAM Access Analyzer before/after the change and diff the reachable-permissions graph.

**Bad:**
```hcl
# "just for CI" — but any repo can now pass the org-admin role to itself
resource "aws_iam_policy" "ci" {
  policy = jsonencode({ Statement = [{
    Effect = "Allow", Action = "iam:PassRole", Resource = "*" }] })
}
```

**Good:**
```hcl
resource "aws_iam_policy" "ci" {
  policy = jsonencode({ Statement = [{
    Effect = "Allow", Action = "iam:PassRole",
    Resource = aws_iam_role.ci-runner.arn   # only its own low-priv role
  }] })
}
```

**References:** MITRE ATT&CK T1548.005, Cloudsplaining, AWS IAM Access Analyzer, GCP Policy Analyzer
