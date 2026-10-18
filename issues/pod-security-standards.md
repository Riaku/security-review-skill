# Pod Security Standards: seccomp, readOnlyRootFilesystem, allowPrivilegeEscalation

**MUST** apply `RuntimeDefault` seccomp, `readOnlyRootFilesystem: true`, and `allowPrivilegeEscalation: false` on all pod security contexts.

**Why:** Permissive security contexts let exploits persist writes to the container root and escalate via setuid binaries.

**Detect:** Pod YAML missing `securityContext.seccompProfile`, `readOnlyRootFilesystem`, or showing `allowPrivilegeEscalation: true`.

**References:** CIS K8s 5.2.1-5.2.8, K8s Pod Security Standards restricted, CWE-250, MITRE ATT&CK T1611
