---
categories: [containers-k8s, observability]
domains: [infrastructure, reliability]
---

# Kubernetes API Audit Logging Not Enabled

**MUST** enable the kube-apiserver audit policy with persistent, tamper-resistant shipping of audit events.

**Why:** Without API audit logs, privileged actions — secret reads, RBAC changes, pod exec — leave no trace, so cluster compromise is undetectable forensically.

**Detect:** check kube-apiserver flags `--audit-policy-file`, `--audit-log-path`; grep manifests for `audit.k8s.io/v1` Policy; verify long retention on the sink.

**References:** CIS Kubernetes Benchmark 1.2.x (API-server audit settings: --audit-policy-file, --audit-log-path, rotation and retention), CWE-778, NIST SP 800-92, K8s docs audit-policy
