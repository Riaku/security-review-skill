# Missing ResourceQuota / LimitRange Allowing Namespace Exhaustion

**SHOULD** apply ResourceQuota and LimitRange to every tenant namespace so one team cannot consume the whole cluster's compute.

**Why:** Without quotas, a runaway or malicious workload exhausts shared CPU/memory, degrading every other namespace on the cluster.

**Detect:** Namespaces with no `ResourceQuota` or `LimitRange` objects; tenant namespaces sharing unbounded node pools.

**References:** CIS K8s 5.2.1, K8s quotas/limitranges docs, CWE-770, NIST SP 800-190 5.3
