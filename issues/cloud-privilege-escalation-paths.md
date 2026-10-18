# Cloud Privilege-Escalation Paths (cross-role/cross-account escalation graph reviewed)

**SHOULD** periodically compute the role-to-role and cross-account escalation graph and prune every path from low-privilege identities to admin.

**Why:** Individually reasonable permissions compose into escalation ladders (create-role, assume-role, modify-trust) that no single policy review catches.

**Detect:** run pmapper `analyze --enum`, cloudsplaining cross-account reports, IAM Access Analyzer `unreachable`/external findings; grep trust policies for `AWS: "*"`.

**References:** AWS IAM Access Analyzer, NIST SP 800-53 AC-3/AC-6, CWE-269, Cloudsplaining, Azure AD escalation graph
