---
categories: [containers-k8s, hardening-benchmarks]
domains: [government-compliance, infrastructure]
---

# No Admission Policy Engine (Pod Security Standards / Gatekeeper / Kyverno)

**MUST** run an admission policy engine enforcing Pod Security Standards or equivalent custom policy at cluster scope.

**Why:** Without admission control, any YAML that passes review can deploy privileged or unsegmented workloads; policy drift goes unchecked.

**Detect:** No ValidatingWebhookConfiguration for gatekeeper/kyverno; namespaces missing `pod-security.kubernetes.io/enforce` labels.

**References:** CIS K8s 5.2, K8s Pod Security Admission, OWASP K8s PS1, NIST SP 800-190 5.4

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [hardening-benchmarks](../categories/hardening-benchmarks.md) · [government-compliance](../domains/government-compliance.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
