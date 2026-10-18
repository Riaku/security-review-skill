---
categories: [sre-incidents]
domains: [reliability]
---

# Failover

**MUST** automatically redirect traffic to healthy replicas within the documented failover time, with the promotion path tested.

**Why:** Manual failover fails at 3 a.m.; an untested standby collapses under real load.

**Detect:** `failover_priority`, `primary`/`replica` config, no `automatic failover` in DB/LB settings, runbook-only failover docs.

**References:** AWS RDS Multi-AZ, Patroni failover, NIST SP 800-34, CWE-1049
