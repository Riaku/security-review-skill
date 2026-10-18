---
categories: [deployment-release]
domains: [infrastructure]
---

# GitOps

**MUST** make Git the single source of truth for cluster state, with sync controllers denying out-of-band mutation and requiring signed commits for merge.

**Why:** Unsigned or bypassed changes let an attacker persist malicious workloads that survive incidents and appear legitimate during audits.

**Detect:** check Flux `GitRepository` secretRef/gpgGCM, ArgoCD `signedCrds`/commit verification, and RBAC blocking `kubectl apply` outside the controller service account.

**References:** OWASP Kubernetes Top 10 K04 (centralized policy enforcement), NIST SP 800-190, Sigstore/cosign, Git signed commits

---

**Part of:** [deployment-release](../categories/deployment-release.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
