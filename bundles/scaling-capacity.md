# scaling-capacity — full checklist (20 items)

Scaling behavior and capacity limits.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/scaling-capacity.md](../categories/scaling-capacity.md) · Index: [SKILL.md](../SKILL.md)

# Autoscaling

**SHOULD NOT** scale on metrics an attacker can inflate cheaply (raw request count, queue depth) without a max-replica ceiling and scale-up stabilization window.

**Why:** A flood or spam burst can trigger runaway scale-out, exhausting cluster quota and cloud budget while serving nothing legitimate.

**Detect:** grep HPA/KEDA configs for `maxReplicas`, `stabilizationWindowSeconds`, target metric source; flag missing ceilings or scale-up driven by unauthenticated request rate.

**References:** CWE-770, AWS Well-Architected REL08-BP05

# Capacity Planning

**MUST** forecast capacity against projected peak (not average) load with explicit headroom, reviewed on a recurring cadence tied to growth data.

**Why:** Planning to average utilization guarantees saturation at the first promotional spike or seasonal peak, turning a predictable event into an outage.

**Detect:** grep runbooks/planning docs for `headroom`, `peak_utilization`, `capacity_forecast`, growth-rate assumptions; check dashboards for peak-vs-average reporting and review-date stamps.

**References:** Google SRE Book capacity planning, NIST SP 800-184, ITIL Capacity Management

# Cold Starts

**MUST** bound cold-start latency (provision plus warm-up) below the client timeout for every scale-from-zero or lazily-loaded path.

**Why:** A cold instance that initializes slower than the caller's timeout drops the very requests that triggered the scale-up, amplifying the surge.

**Detect:** grep for `minReplicas: 0`, `scaleDownDelaySecondsAfterFinish`, initContainer warm-up steps, `timeoutSeconds` in client config; compare recorded cold-start timings against those timeouts.

**References:** AWS Well-Architected REL11-BP03, CWE-400, Google SRE scaling practices

# Storage Operating Degraded (Degraded RAID/Mirror) Runbook

**MUST** provide a runbook for degraded RAID/mirror states: rebuild procedure, performance limits, escalation threshold.

**Why:** A degraded mirror silently loses redundancy; the next disk failure becomes an unrecoverable array collapse.

**Detect:** `mdadm --detail` showing `degraded`, `zpool status` DEGRADED, absence of `degraded` runbook, no rebuild-priority or scrub schedule.

**References:** NIST SP 800-34, RAID recovery procedures, ZFS administration guide

# Disk and inode exhaustion forecasted with lead time

**MUST** forecast disk and inode consumption from historical growth rates and alert early enough (days, not hours) to act before full.

**Why:** A full disk or exhausted inode table corrupts writes and takes down every workload on the volume simultaneously, with no graceful degradation path.

**Detect:** grep monitoring for `disk_free_percent`, `inodes_free`, `predict_linear`/forecast queries in alert rules, log-rotation and cleanup cron jobs; flag alerts that fire only at >95% with no trend projection.

**References:** CWE-400, NIST SP 800-184, Google SRE monitoring four golden signals

# Garbage Collection

**MAY** tune GC pause targets and heap sizing per workload, but only after measuring pause distributions rather than defaulting to aggressive tuning.

**Why:** Untuned GC causes latency spikes at high allocation rates; blindly tuned GC causes thrashing and CPU starvation — both hurt tail latency under load.

**Detect:** grep for `GOGC`, `-Xmx`, `-XX:MaxGCPauseMillis`, `gc_pause_seconds` histograms in dashboards; check GC logs for pause p99 vs SLO and full-GC frequency.

**References:** CWE-400, Google SRE tail latency chapter, Java GC tuning guide (Oracle), Go runtime metrics docs

# Horizontal vs Vertical Scaling

**SHOULD** prefer horizontal scaling for stateless tiers and reserve vertical scaling for stateful components, documenting each datastore's single-node ceiling.

**Why:** Vertical-only growth creates a single point of failure and a hard wall that arrives mid-incident with no headroom to add replicas.

**Detect:** grep manifests for `replicas: 1`, `resources.limits` near node capacity, `nodeSelector` pinning; check stateful services for a documented max-node-size plan.

**References:** NIST SP 800-184, AWS Well-Architected REL05-BP02, CWE-400

# Latency vs Throughput

**MUST** define separate SLOs for latency (p95/p99) and throughput, and scale on the metric that breaches first rather than a single aggregate.

**Why:** Optimizing only average throughput hides tail-latency spikes that time out clients and cascade into retry storms during peak load.

**Detect:** grep for `p99`, `histogram_quantile`, `latency_slo`, `throughput_slo` in dashboards and alert rules; absence of percentile thresholds in prometheus rules or load-test reports.

**References:** Google SRE Book SLO chapter, CWE-400, NIST SP 800-184

# Denial-of-wallet: unbounded LLM token spend per user/tenant

**MUST** enforce per-user and per-tenant token budgets, rate limits, and alerting on LLM API spend.

**Why:** A scripted attacker or runaway agent loop can burn thousands of dollars in tokens within hours on a metered API.

**Detect:** no rate_limit, max_tokens, or budget keys on LLM gateway routes; provider usage alerts not configured.

**References:** OWASP LLM10:2025, CWE-770, CWE-400

# Load Testing

**SHOULD** load-test at or above expected peak with realistic traffic mix, including failure injection, before committing to a capacity number.

**Why:** Untested capacity claims collapse under real traffic composition — burst patterns, hot keys, and slow dependencies never appear in synthetic averages.

**Detect:** grep repo for `k6`, `locust`, `gatling`, `wrk`, `chaos`, test reports with `p99` and error-rate thresholds; flag tests that only check mean latency or run below peak.

**References:** NIST SP 800-184, AWS Well-Architected REL11-BP04

# Memory Leaks

**MUST NOT** ship long-running services without leak detection (heap trend monitoring or periodic profiling) wired into alerting.

**Why:** A slow leak stays invisible for days, then triggers OOM kills at the worst moment — during peak traffic — rather than at deploy time.

**Detect:** grep for `heap_dump`, `tracemalloc`, `pprof`, `jcmd`, `memory_usage` alerts with trend/slope thresholds; check for unbounded caches (`lru_cache` without maxsize, growing global dicts).

**References:** CWE-401, NIST SP 800-53 SI-7

# Missing ResourceQuota / LimitRange Allowing Namespace Exhaustion

**SHOULD** apply ResourceQuota and LimitRange to every tenant namespace so one team cannot consume the whole cluster's compute.

**Why:** Without quotas, a runaway or malicious workload exhausts shared CPU/memory, degrading every other namespace on the cluster.

**Detect:** Namespaces with no `ResourceQuota` or `LimitRange` objects; tenant namespaces sharing unbounded node pools.

**References:** CIS K8s 5.2.1, K8s quotas/limitranges docs, CWE-770, NIST SP 800-190 5.3

# Non-Functional Requirements Traceability

**SHOULD** record non-functional requirements (scale targets, latency SLOs, availability, durability, compliance) as explicit, testable constraints that architecture decisions reference.

**Why:** Untestable "should be fast" requirements hide their violation until production; hard constraints (10M DAU, <200ms p95, 99.99% uptime) make every design choice auditable and every gap visible before launch.

**Detect:** look for an NFR/requirements doc or ADRs citing concrete numbers; check SLO definitions trace back to stated requirements rather than post-hoc guesses.

**References:** Google SRE SLO chapter, DDIA requirements-driven design, ADR practice

# Noisy-neighbor isolation between tenants/workloads

**MUST** enforce per-tenant or per-workload resource quotas (CPU, memory, I/O, connection rate) so one tenant's burst cannot degrade others sharing the host.

**Why:** Without isolation, a single abusive or misbehaving tenant saturates shared CPU, disk I/O, or network, violating SLAs for everyone co-located.

**Detect:** grep for `ResourceQuota`, `LimitRange`, `CPUShares`/`cpu_weight`, `blkio`/`IOClass`, per-tenant `rate_limit` in gateway config; flag shared pools with no per-tenant caps.

**References:** CWE-770, Kubernetes QoS/ResourceQuota docs

# OOM Killer

**SHOULD** set explicit memory requests/limits and OOM-score priorities so the kernel evicts disposable workers before critical stateful processes.

**Why:** With unbounded memory, the OOM killer picks by size, not importance — it will happily terminate the database while the leaking cache survives.

**Detect:** grep manifests for `resources.limits.memory`, `oom_score_adj`, and dmesg/journal for `Out of memory: Killed process`; flag containers with no limit or critical services at default scores.

**References:** CWE-400, Kubernetes QoS docs, NIST SP 800-184, kernel OOM protection (oom_score_adj)

# Quadratic Complexity & Nested Loops (O(n²) on unbounded input)

**MUST NOT** nest loops over two externally sized collections without a bound on either dimension.

**Why:** A modest payload (10k × 10k) becomes 100M operations, letting one cheap request saturate CPU for everyone.

**Detect:** `for ... for` over request arrays, `.map` inside `.filter` on user lists, join without index, no max-length on both sides.

**References:** CWE-407, CWE-834, OWASP API DoS guidance

# Sticky Sessions & Load-Balancer Affinity

**SHOULD NOT** rely on sticky sessions to make a stateful design work; if affinity is required (websockets, streaming), make it explicit, session-aware, and resilient to node loss.

**Why:** Affinity as a patch for server-side state silently breaks horizontal scaling — a rebalanced or failed node drops every "remembered" session, and scale-out multiplies the problem.

**Detect:** grep LB config for `sticky`, `affinity: cookie`, `sessionAffinity: ClientIP`; check whether session state lives in-app vs external store; test node drain behavior.

**References:** Kubernetes service sessionAffinity docs, AWS ALB stickiness docs, stateless-services issue

# Volume IOPS/throughput ceilings profiled before launch

**SHOULD** benchmark the storage volume's IOPS and throughput ceilings under a realistic workload before launch, and size expected database load against them with headroom.

**Why:** Cloud volumes advertise tiers, but the database discovers the ceiling at the worst moment: launch day. A volume pinned at its IOPS limit surfaces as mysterious slow queries and rising `await`, and the application gets blamed for a provisioning mistake.

**Detect:** Ask for fio results tied to the launch checklist. Compare peak read/WAL generation against provisioned IOPS in IaC (`aws_ebs_volume.iops`, StorageClass annotations). No storage numbers, no pass.

**Bad:**
```hcl
resource "aws_ebs_volume" "pg" {
  type = "gp2"   # burst credits; steady-state surprise
}
```

**Good:**
```hcl
resource "aws_ebs_volume" "pg" {
  type = "io2"
  iops = 8000   # fio peak 5.2k + 50% headroom
}
```

**References:** AWS EBS volume types docs, fio benchmarking guide, Google SRE Book capacity planning

# Stalled replication retention accumulating log segments until disk fills

**MUST** monitor log retention pinned by an absent replica or consumer, alerting well below free-disk headroom, since the primary cannot recycle the log segments those retention markers hold open (PostgreSQL replication slots holding a stale `restart_lsn` are the classic case).

**Why:** A dropped replica leaves its slot behind, and the primary keeps every WAL byte "just in case." Days later the disk fills and the primary — not the missing replica — stops accepting writes. A classic self-inflicted Postgres outage.

**Detect:** Check monitoring on slot byte lag — `pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)` on `pg_replication_slots`, plus `wal_status`/`safe_wal_size` (PG 13+) — inactive-slot state, and disk alerts tied to `pg_wal` growth. Grep runbooks for `pg_drop_replication_slot` and whether replica decommissioning removes its slot.

**Bad:**
```sql
-- replica decommissioned; slot never dropped
SELECT * FROM pg_replication_slots;  -- inactive, lag growing daily
```

**Good:**
```sql
-- alert when slot byte lag > 5GB or inactive_since > 15min
SELECT slot_name, active,
  pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS lag
FROM pg_replication_slots;
```

**References:** PostgreSQL replication slots & WAL retention docs, pgBackRest/WAL-G slot management, CWE-400 disk exhaustion

# Worker Pools

**SHOULD** size worker pools against queue arrival rates and set autoscaling bounds with starvation detection; undersized pools silently age jobs.

**Why:** A pool too small for peak load creates growing latency invisible until customers complain, while an oversized one wastes capacity and hides throughput regressions.

**Detect:** grep for `concurrency`, `pool_size`, `num_workers` without autoscaling policy; metrics showing queue depth rising while workers idle or saturated.

**References:** CWE-400, NIST SP 800-53 SC-5, Kubernetes HPA guidance

