# Control-Plane Quorum (etcd) Health Monitored Separately from Workloads

**MUST** monitor etcd quorum and leader health independently of application dashboards, alerting before quorum loss.

**Why:** Losing etcd quorum freezes the entire cluster's API; a workload-only dashboard misses the failure until everything is already down.

**Detect:** No etcd metrics scrape (`etcd_server_has_leader`, `etcd_server_health_failures`); no separate control-plane alert rule or runbook.

**References:** CIS K8s 2.0, etcd monitoring docs, NIST SP 800-190 5.4, K8s HA control-plane docs
