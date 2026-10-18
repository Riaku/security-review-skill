---
categories: [deployment-release, observability]
domains: [infrastructure, reliability]
---

# Manual kubectl apply Drift Not Detected Against Git

**SHOULD** run periodic drift detection (Flux `diff`/`check`, ArgoCD health) that alerts when live cluster state diverges from the reconciled Git revision.

**Why:** A hand-applied manifest silently overrides GitOps intent, so the next sync either reverts an emergency fix or entrenches an unauthorized change unnoticed.

**Detect:** check Flux `Kustomization` for `interval`/`retryInterval` with drift alerts, ArgoCD `syncPolicy.automated` plus `selfHeal: true`; grep for out-of-band `kubectl apply` in audit logs.

**References:** Flux drift detection docs, ArgoCD selfHeal, OWASP K8s misconfiguration, NIST SP 800-190 integrity monitoring

---

**Part of:** [deployment-release](../categories/deployment-release.md) · [observability](../categories/observability.md) · [infrastructure](../domains/infrastructure.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
