---
categories: [containers-k8s, observability]
domains: [infrastructure, reliability]
---

# Crash-Loop Restart Storms Bounded and Alarmed

**SHOULD** bound a crash-looping workload's blast radius (restart deadline, quota, node-level backoff tuning where available) and alarm on CrashLoopBackOff so a failing pod cannot hammer the control plane or mask a persistent fault.

**Why:** Unbounded rapid restarts amplify load on kubelet and API server while the underlying error goes unnoticed until an outage.

**Detect:** No alert on `kube_pod_container_status_waiting_reason{reason="CrashLoopBackOff"}` and no paging rule for it; no `activeDeadlineSeconds` or quota bounding an endlessly restarting workload (`restartPolicy` accepts only `Always`/`OnFailure`/`Never` and carries no backoff ceiling).

**References:** K8s docs backoff, kube-state-metrics CrashLoopBackOff, CWE-770, SRE alerting practices
