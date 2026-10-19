---
categories: [cloud-network, deployment-release, observability]
domains: [infrastructure, reliability]
---

# Infrastructure Drift Detection (live state vs IaC and GitOps reconciliation)

**MUST** continuously diff live infrastructure against IaC definitions and alert on unauthorized manual changes; **SHOULD** also run periodic drift detection on the GitOps path (Flux `diff`/`check`, ArgoCD health) that alerts when live cluster state diverges from the reconciled Git revision.

**Why:** A hand-applied manifest silently overrides GitOps intent, so the next sync either reverts an emergency fix or entrenches an unauthorized change unnoticed; console-clicked changes bypass review and become invisible holes — an undocumented open security group never gets fixed.

**Detect:** grep `terraform plan -detailed-exitcode` cron jobs, Driftctl, AWS Config drift rules, `kubectl diff -f`; check Flux `Kustomization` for `interval`/`retryInterval` with drift alerts, ArgoCD `syncPolicy.automated` plus `selfHeal: true`; grep for out-of-band `kubectl apply` in audit logs.

**References:** Flux drift detection docs, ArgoCD selfHeal, OWASP K8s misconfiguration, NIST SP 800-190 integrity monitoring, NIST SP 800-53 CM-3/CM-6, CIS Control 2, Terraform drift docs
