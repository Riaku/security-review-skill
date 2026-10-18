# Least Privilege

**MUST** grant every service account, role, and credential only the permissions its workload actually uses, verified against observed access rather than assumed needs.

**Why:** Over-broad credentials turn any single compromise into a cluster-wide or account-wide breach.

**Detect:** `cluster-admin`, `roleRef`, `rbac.authorization.k8s.io/v1`, `aws:iam::*:*admin*`, wildcard `"*"` in policy Action/Resource fields.

**References:** OWASP ASVS V1.4.3, CWE-269, NIST SP 800-53 AC-6
