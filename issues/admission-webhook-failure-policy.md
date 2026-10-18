---
categories: [containers-k8s, resilience]
domains: [infrastructure, reliability]
---

# Admission Webhook failurePolicy:Fail Deadlock and TLS Misconfig

**SHOULD** set `failurePolicy: Fail` only where the webhook is highly available, with valid TLS certs and namespace exclusions for its own namespace.

**Why:** A failing fail-closed webhook blocks all API writes cluster-wide; bad TLS makes every admission request error the same way.

**Detect:** ValidatingWebhookConfiguration with `failurePolicy: Fail` and no `namespaceSelector` excluding kube-system/webhook ns; expired or self-signed `caBundle`.

**References:** CIS K8s 5.2, K8s docs admission-webhook, CWE-1041, SRE postmortem patterns

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [resilience](../categories/resilience.md) · [infrastructure](../domains/infrastructure.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
