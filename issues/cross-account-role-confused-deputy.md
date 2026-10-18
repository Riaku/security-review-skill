# Confused Deputy: Cross-Account Roles Without ExternalId or Source Conditions

**MUST** require a caller-specific `sts:ExternalId` (or equivalent source-account/source-ARN conditions) in the trust policy of every cross-account role, so third parties cannot trick the role into acting on another customer's behalf.

**Why:** Without an ExternalId, any account that learns the role's ARN can ask the STS to assume it — the "deputy" cannot tell which client actually requested the action, letting one tenant read or modify another's resources.

**Detect:** Review trust policies (`assume_role_policy` in Terraform, `AssumeRolePolicyDocument` in CloudFormation) for cross-account principals lacking a `Condition` block on `sts:ExternalId`, `aws:SourceArn`, or `aws:SourceAccount`. Check partner-integration docs and IaC modules that accept a bare `principal_arn` parameter with no external-id input.

**Bad:**
```json
"Principal": {"AWS": "arn:aws:iam::999988887777:root"}
```

**Good:**
```json
"Principal": {"AWS": "arn:aws:iam::999988887777:root"},
"Condition": {"StringEquals": {
  "sts:ExternalId": "acme-tenant-42",
  "aws:SourceArn": "arn:aws:events:us-east-1:999988887777:rule/nightly-sync"}}
```

**References:** AWS Confused Deputy Prevention Guide, CWE-915, AWS Security Best Practices SEC3-BP05
