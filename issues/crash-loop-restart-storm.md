---
categories: [containers-k8s, observability]
domains: [infrastructure, reliability]
---

# Crash-Loop Restart Storms Bounded and Alarmed

**SHOULD** bound restart backoff and alarm on CrashLoopBackOff so a failing pod cannot hammer the control plane or mask a persistent fault.

**Why:** Unbounded rapid restarts amplify load on kubelet and API server while the underlying error goes unnoticed until an outage.

**Detect:** No alert on `kube_pod_container_status_waiting_reason{reason="CrashLoopBackOff"}`; `restartPolicy` with no backoff ceiling or paging rule.

**References:** K8s docs backoff, kube-state-metrics CrashLoopBackOff, CWE-770, SRE alerting practices
