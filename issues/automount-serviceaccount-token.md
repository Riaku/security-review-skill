# Auto-Mounted Service Account Tokens in Pods That Don't Need the API

**SHOULD** set `automountServiceAccountToken: false` on pods and serviceaccounts that never call the Kubernetes API.

**Why:** An unnecessary mounted token is a standing credential an attacker with any file-read bug can use against the API server.

**Detect:** Pod specs without `automountServiceAccountToken: false`; mounted path `/var/run/secrets/kubernetes.io/serviceaccount` in non-API workloads.

**References:** CIS K8s 5.1.5, CWE-522, OWASP K8s PS1, NIST SP 800-190 5.2

---

**Part of:** [authentication](../categories/authentication.md) · [containers-k8s](../categories/containers-k8s.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
