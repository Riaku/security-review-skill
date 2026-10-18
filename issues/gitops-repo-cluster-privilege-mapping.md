---
categories: [authorization-access-control, cicd-pipeline-security]
domains: [backend, infrastructure]
---

# GitOps Repo Write Access Equals Cluster Write Access

**MUST** treat write access to a GitOps repo as production cluster admin and restrict it accordingly with review, CODEOWNERS, and separation of duties.

**Why:** Anyone who can commit manifests can create privileged workloads or read cluster secrets without ever touching the cluster API.

**Detect:** Repo without CODEOWNERS on `manifests/` or `apps/`; ArgoCD/Flux repo write granted to broad teams; no admission policy blocking high-privilege kinds from Git.

**References:** OWASP GitOps Security, CWE-269, NIST SP 800-218 PO.3, ArgoCD RBAC best practices, Flux multi-tenancy guide

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
