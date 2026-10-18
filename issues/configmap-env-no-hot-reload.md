---
categories: [containers-k8s]
domains: [infrastructure]
---

# ConfigMap Hot-Reload Assumption for Environment Variables

**MUST NOT** rely on environment-variable-injected ConfigMaps updating at runtime; env vars are fixed at container start, so mount files or restart the pod.

**Why:** Teams assume config changes propagate live, then ship with stale credentials or feature flags after a ConfigMap update.

**Detect:** `envFrom: configMapRef` where the app expects live updates; no checksum annotation or rollout trigger on ConfigMap change.

**References:** K8s docs configmap env immutability, CWE-676, Bitnami/Flux config-reload patterns
