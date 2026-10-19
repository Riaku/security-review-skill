---
categories: [containers-k8s, hardening-benchmarks]
domains: [government-compliance, infrastructure]
---

# No Admission Policy Engine (Pod Security Standards / Gatekeeper / Kyverno)

**MUST** run an admission policy engine enforcing Pod Security Standards or equivalent custom policy at cluster scope.

**Why:** Without admission control, any YAML that passes review can deploy privileged or unsegmented workloads; policy drift goes unchecked.

**Detect:** No ValidatingWebhookConfiguration for gatekeeper/kyverno; namespaces missing `pod-security.kubernetes.io/enforce` labels.

**References:** CIS K8s 5.2, K8s Pod Security Admission, OWASP Kubernetes Top 10 K04
