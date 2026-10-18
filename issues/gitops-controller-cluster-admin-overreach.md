---
categories: [authorization-access-control, containers-k8s]
domains: [backend, infrastructure]
---

# GitOps Controller Running as cluster-admin

**SHOULD** scope GitOps controllers (Flux, ArgoCD) to least-privilege per-namespace roles instead of the blanket `cluster-admin` ClusterRoleBinding.

**Why:** A compromised repo, PR, or controller CVE becomes instant full-cluster takeover when the sync engine holds cluster-admin.

**Detect:** grep deploy manifests for `cluster-admin` bound to `system:serviceaccount:flux-system` / `argocd`; check ClusterRoleBinding subjects and reconciliation scopes.

**References:** OWASP A05 Security Misconfiguration, CWE-250 Execution with Unnecessary Privileges, ArgoCD security docs, NIST SP 800-190
