---
categories: [authentication, containers-k8s]
domains: [backend, infrastructure]
---

# Auto-Mounted Service Account Tokens in Pods That Don't Need the API

**SHOULD** set `automountServiceAccountToken: false` on pods and serviceaccounts that never call the Kubernetes API.

**Why:** An unnecessary mounted token is a standing credential an attacker with any file-read bug can use against the API server.

**Detect:** Pod specs without `automountServiceAccountToken: false`; mounted path `/var/run/secrets/kubernetes.io/serviceaccount` in non-API workloads.

**References:** CIS K8s 5.1.5, CWE-522, OWASP Kubernetes Top 10 K06, NIST SP 800-190 5.2
