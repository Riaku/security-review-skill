# exec/attach/debug RBAC Verbs Are Root-in-Pod Equivalent

**MUST NOT** grant `pods/exec`, `pods/attach`, or `pods/debug` broadly; restrict them to named break-glass groups with audit.

**Why:** exec into a pod bypasses every app-layer control — anyone with the verb reads secrets, env vars, and tokens as the workload's user.

**Detect:** grep ClusterRole/Role YAML for `exec`, `attach`, `debug` verbs on `pods`/`pods/exec`; check who can `kubectl exec` via `kubectl auth can-i create pods/exec --as=...`.

**References:** Kubernetes RBAC docs, CWE-269, MITRE ATT&CK T1611 Escape to Host, NIST SP 800-190
