# Pod Security Standards: seccomp, readOnlyRootFilesystem, allowPrivilegeEscalation

**MUST** apply `RuntimeDefault` seccomp, `readOnlyRootFilesystem: true`, and `allowPrivilegeEscalation: false` on all pod security contexts.

**Why:** Permissive security contexts let exploits persist writes to the container root and escalate via setuid binaries; unconfined or unmasked syscall surfaces turn one broken container into full node compromise — the classic escape path Falco and Tracee alert on.

**Detect:** Pod YAML missing `securityContext.seccompProfile`, `readOnlyRootFilesystem`, or showing `allowPrivilegeEscalation: true`; grep manifests for `unconfined`, `unmasked`, `CAP_SYS_*`; run container escape test suites (e.g. cdve).

**References:** CIS K8s 5.2.1-5.2.8, K8s Pod Security Standards restricted, CWE-250, MITRE ATT&CK T1611, CIS Docker 5.3

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [hardening-benchmarks](../categories/hardening-benchmarks.md) · [infrastructure](../domains/infrastructure.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)
