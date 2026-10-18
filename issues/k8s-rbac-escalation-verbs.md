# K8s RBAC Escalation via impersonate/bind/escalate Verbs

**MUST NOT** grant `impersonate`, `bind`, or `escalate` verbs to non-admin subjects; each is a direct path to cluster-admin.

**Why:** `bind` lets a user attach cluster-admin to themselves, `impersonate` borrows any identity, `escalate` upgrades any role — self-grant with no audit trail of intent.

**Detect:** `kubectl auth can-i --list` and grep ClusterRole YAML for `impersonate`, `bind`, `escalate` in verbs; flag RoleBindings to ClusterRole admin.

**References:** RBAC: The Bad Parts (Kubernetes blog), CWE-269, MITRE ATT&CK T1098.001, NIST SP 800-190
