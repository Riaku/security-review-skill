# Kubernetes RBAC & NetworkPolicies

**MUST** bind least-privilege RBAC roles and enforce default-deny NetworkPolicies per namespace instead of flat open cluster networking.

**Why:** Cluster-admin bindings and absent network segmentation let any compromised pod read secrets or laterally reach every service.

**Detect:** `ClusterRoleBinding` to `cluster-admin` for app serviceaccounts; no `NetworkPolicy` with `podSelector` matching all ingress in namespace.

**References:** CIS K8s 5.1, RBAC Least Privilege, CWE-284, OWASP K8s PS1/PS5

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
