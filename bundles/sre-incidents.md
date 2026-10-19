# sre-incidents — full checklist (35 items)

Operational readiness: DR, incidents, SLOs, on-call.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/sre-incidents.md](../categories/sre-incidents.md) · Index: [SKILL.md](../SKILL.md)

# Availability Zones

**MUST** spread replicas across at least two availability zones — three for N+1 with quorum — and size each surviving zone to carry peak load, so one zone's failure cannot drop the service below minimum capacity.

**Why:** All replicas in one zone means a datacenter event takes down 100% of capacity despite looking available.

**Detect:** `topologySpreadConstraints`, `podAntiAffinity` on zone topology, ASG `VPCZoneIdentifier` with one subnet.

**References:** AWS Well-Architected reliability pillar, K8s topology docs, NIST SP 800-34

# Backup Encryption & Immutable/Offsite Copies

**MUST** encrypt backups at rest and keep copies that are immutable (object-lock/WORM) and offsite, so a compromised production environment cannot destroy or tamper with every copy.

**Why:** Ransomware crews target backup repositories first: if backups are writable with production credentials, "we have backups" is an illusion. Encryption blocks exposure of regulated data; immutability survives both the ransomware and the burning building.

**Detect:** Bucket policies allowing `s3:BypassGovernanceRetention`, missing object lock/versioning, backup keys reachable from the production IAM role. Grep backup configs for absent encryption flags (`--encrypt`, SSE-KMS) and single-region destinations.

**Bad:**
```bash
# same writable bucket, same creds, plaintext
aws s3 cp /backups/db.tar s3://app-backups/db.tar
```

**Good:**
```bash
gpg --symmetric --cipher-algo AES256 db.tar
aws s3 cp db.tar.gpg s3://vault-backups/db/ \
  --server-side-encryption aws:kms
# bucket: object lock COMPLIANCE + cross-region replication
```

**References:** CIS Control 11 (immutable backups), NIST SP 800-53 CP-9, AWS S3 Object Lock docs, CWE-311

# Backup Verification Drills (scheduled restore tests, not just backup jobs)

**MUST** run scheduled restore drills proving backups actually recover systems, with results tracked and failures escalated.

**Why:** Backups never restored are unverified guesses: truncated dumps, missing WAL segments, procedures that only work on one engineer's laptop — and ransomware crews routinely destroy backup targets too. Discovering a corrupt set during a real incident converts an outage into permanent loss.

**Detect:** Grep `restore_test`, `velero restore create`, `pg_restore` in scheduled jobs, AWS Backup restore-testing plans, drill runbooks; a backup job with no matching restore-test job is the finding. Ask for the last successful restore date and evidence: checksums, row counts, an app booting against restored data.

**References:** NIST SP 800-34, CIS Control 11, NIST CSF PR.IP-4

# Break-Glass Access Procedure

**SHOULD** define a monitored break-glass path for emergency privileged access: pre-authorized, logged, alerting on use, and reviewed within 24h.

**Why:** Without a sanctioned emergency path, responders improvise with standing admin access — which is either absent in the outage or abused permanently after it.

**Detect:** look for break-glass accounts/policies (AWS IAM break-glass role, Azure PIM emergency access) with alert-on-use and review SLA; check that emergency creds are escrowed (sealed envelope) not casually held.

**References:** Microsoft emergency access accounts, AWS break-glass role patterns, NIST 800-53 AC-2(2)

# Chaos Engineering

**MAY** run controlled failure injection in production-like environments, scoped by blast radius and abort criteria.

**Why:** Untested redundancy is assumed redundancy; failover paths quietly rot between verified drills.

**Detect:** `chaos-mesh`, `litmus`, Gremlin config, absence of game-day logs, no abort/steady-state criteria in experiment manifests.

**References:** Principles of Chaos Engineering, Netflix Chaos Monkey, AWS FIS, NIST SP 800-34 drills

# Connection Draining

**SHOULD** drain established connections at the load balancer before removing a backend from rotation.

**Why:** Abrupt backend removal mid-request severs long-poll and upload sessions, surfacing as random 502s during deploys.

**Detect:** `drain_timeout`, `idle_timeout` on Envoy/HAProxy, `notReadyBeforeDrainDelay`, missing `connectionDraining` in cloud LB config.

**References:** AWS ELB connection draining, Envoy drain documentation

# Crash-consistent volume snapshots vs logical dumps distinguished

**SHOULD** document, per datastore, whether each backup is crash-consistent (volume snapshot) or logically consistent (`pg_dump`, `mysqldump`), and use the right one per recovery scenario.

**Why:** A raw volume snapshot of a running database captures only what the host had already flushed to the volume at that instant — not the dirty pages still in page cache — so it is crash-consistent at best and the engine needs crash recovery (WAL/binlog replay) to open it. Mixing them up means discovering at restore time that the "backup" was never a valid restore point.

**Detect:** The backup matrix should state each method's consistency guarantee; volume-snapshot jobs over hot databases must pair with WAL/binlog archiving.

**Bad:**
```yaml
# snapshotting a hot Postgres PVC, no WAL archiving
backup: ebs-snapshot, volume: postgres-data
```

**Good:**
```yaml
backup: pg_basebackup + wal-archive  # restore-point capable
# volume snapshots reserved for whole-VM DR only
```

**References:** EBS/PersistentVolume snapshot consistency docs, PostgreSQL backup methods docs, NIST SP 800-34

# Daylight Saving Time

**SHOULD NOT** compute elapsed time or cron schedules by naive clock arithmetic across DST transitions; **SHOULD** test scheduled jobs and time logic across the spring-forward gap and fall-back overlap in the deployment timezone.

**Why:** Skipped and repeated local hours make jobs fire twice, never fire, or report impossible durations — a bug that hides for months and surfaces exactly at the transition.

**Detect:** Cron with fixed local hours, `timedelta(hours=1)` loops over calendar days, `TZ=America/` with `naive` datetimes, no test freezing the clock at a DST boundary (spring-forward gap, fall-back overlap) in the deployment timezone, scheduler docs silent on which timezone governs.

**References:** NIST SP 800-53 AU-8, IANA tzdb, crontab(5) NOTES on DST

# Storage Operating Degraded (Degraded RAID/Mirror) Runbook

**MUST** provide a runbook for degraded RAID/mirror states: rebuild procedure, performance limits, escalation threshold.

**Why:** A degraded mirror silently loses redundancy; the next disk failure becomes an unrecoverable array collapse.

**Detect:** `mdadm --detail` showing `degraded`, `zpool status` DEGRADED, absence of `degraded` runbook, no rebuild-priority or scrub schedule.

**References:** NIST SP 800-34, RAID recovery procedures, ZFS administration guide

# Disaster Recovery

**MUST** maintain a rehearsed recovery plan for full-site loss, with restore verified from actual backups.

**Why:** Never-restored backups are unverified files; untested DR plans fail when the real disaster arrives.

**Detect:** `dr_plan.md`, `backup_schedule` cron, absence of restore-test logs, `wal_level`/PITR disabled, offsite sync jobs without checksums.

**References:** NIST SP 800-34, ISO 22301

# DORA (financial sector resilience)

**MUST** classify critical ICT functions, test resilience (including TLPT threat-led testing), and register ICT third-party arrangements per DORA timelines.

**Why:** Financial entities failing operational-resilience tests risk forced exit from EU markets; untested backups and ICT vendors are the failure points.

**Detect:** grep for "DORA", "TLPT", "critical functions register", ICT exit plans; missing incident escalation, unregistered ICT providers.

**References:** EU Regulation 2022/2554, Commission Delegated Regulation (EU) 2024/1774 (RTS on ICT risk management), Commission Implementing Regulation (EU) 2024/2956 (ITS on the register of information), EIOPA/EBA guidance

# Error Budgets

**SHOULD** spend the gap between 100% and the SLO as a budget for risky releases, freezing changes when exhausted.

**Why:** Without a shared budget, reliability debates become endless opinion fights instead of an agreed mechanical tradeoff.

**Detect:** `error_budget` in SLO config, multi-window multi-burn-rate alert thresholds, no freeze policy on exhaustion.

**References:** Google SRE Workbook (error budgets), Prometheus multi-window multi-burn-rate alerting

# Control-Plane Quorum (etcd) Health Monitored Separately from Workloads

**MUST** monitor etcd quorum and leader health independently of application dashboards, alerting before quorum loss.

**Why:** Losing etcd quorum freezes the entire cluster's API; a workload-only dashboard misses the failure until everything is already down.

**Detect:** No etcd metrics scrape (`etcd_server_has_leader`, `etcd_server_health_failures`); no separate control-plane alert rule or runbook.

**References:** etcd monitoring docs, NIST SP 800-190 5.4, K8s HA control-plane docs

# Failover

**MUST** automatically redirect traffic to healthy replicas within the documented failover time, with the promotion path tested.

**Why:** Manual failover fails at 3 a.m.; an untested standby collapses under real load.

**Detect:** `failover_priority`, `primary`/`replica` config, no `automatic failover` in DB/LB settings, runbook-only failover docs.

**References:** AWS RDS Multi-AZ, Patroni failover, NIST SP 800-34, CWE-1049

# Graceful Shutdown

**MUST** trap SIGTERM, stop accepting new work, finish in-flight requests, then exit before the kill deadline.

**Why:** Hard-killed workers drop committed-but-unsent transactions and half-written jobs, producing data loss users blame on the service.

**Detect:** `terminationGracePeriodSeconds`, `SIGTERM` handler absent, `preStop` hook missing, `kill -9` in stop scripts.

**References:** Kubernetes termination docs, CWE-404, Google SRE Book

# Health Checks

**MUST** expose an authenticated-or-network-restricted health endpoint that verifies dependencies rather than just process liveness.

**Why:** A process that answers while its database is dead passes naive checks and keeps serving broken responses to users.

**Detect:** `GET /healthz`, `/health`, `HEALTHCHECK` in Dockerfiles, `readinessProbe` hitting only static 200 or checking process liveness instead of dependencies, and the inverse error of a `livenessProbe` wired to a DB/cache check — dependency checks in liveness kill pods during a downstream outage.

**References:** Kubernetes health checks, K8s docs, CWE-770, SRE Book

# Incident Response

**MUST** maintain a written incident response process with defined roles, escalation paths, and comms cadence, exercised annually.

**Why:** Ad-hoc response during a live outage wastes hours on coordination arguments while customer impact compounds.

**Detect:** `incident_response.md`, severity matrix, absence of paging integration, no IR tabletop logs, missing escalation contacts in runbooks.

**References:** NIST SP 800-61, SANS incident response process, ISO/IEC 27035

# Incident Severity Levels with a Designated Incident Commander

**MUST** assign a named incident commander per severity level at declaration, with coordination authority.

**Why:** Without a single decision-maker, engineers duplicate work and argue rollback timing while the outage widens.

**Detect:** severity matrix (`SEV1`–`SEV4`) in IR docs, `incident_commander` field in tickets, no commander in paging config.

**References:** NIST SP 800-61, Google SRE Workbook (incident command), ITIL incident management

# Load balancer health-check flapping detected and damped

**SHOULD** configure hysteresis on health checks — separate healthy/unhealthy thresholds, realistic timeouts, and jittered intervals — and alert on state-transition rate, not just current state.

**Why:** A single slow response ejects a healthy backend; when the ejected node's traffic overloads its siblings, they fail too, and the whole pool oscillates in a cascade. Flapping also thrashes DNS/LB control planes and hides the true failure during postmortems.

**Detect:** Review health-check configs (ALB target groups, nginx `max_fails`/`fail_timeout`, HAProxy `fall`/`rise`, Consul health checks) for threshold=1 on removal and timeouts tuned to p50 instead of p99. Query LB metrics for backend health-state transitions per minute; check whether monitoring fires on flapping patterns rather than only fully-down states.

**Bad:**
```
health_check: {interval: 2s, timeout: 1s, unhealthy_threshold: 1}
# one GC pause ejects a perfectly healthy node
```

**Good:**
```
health_check: {interval: 10s, timeout: 5s,
               unhealthy_threshold: 3, healthy_threshold: 2}
```

**References:** AWS ELB health check best practices, HAProxy tuning docs, Google SRE Book (overloading & health checks)

# Liveness vs Readiness Probes

**SHOULD NOT** wire dependency checks (DB, cache) into the liveness probe; reserve them for readiness only.

**Why:** Liveness failures kill pods during a downstream outage, turning a slowdown into a cluster-wide crash loop and thundering restart storm.

**Detect:** `livenessProbe` with `exec: pg_isready`/DB query, identical liveness and readiness endpoints, `initialDelaySeconds: 0`.

**References:** Kubernetes probe docs, CWE-770, Google SRE Workbook

# Multi-Region

**SHOULD** deploy across regions only when latency and data residency allow, with explicit region-failure semantics.

**Why:** Cross-region replication lags or split-brains; without a defined loss model, a region outage corrupts what redundancy was meant to protect.

**Detect:** `region:` keys, `global-load-balancer`, `cross-region` replication flags, DNS failover records, GDPR data-residency config.

**References:** NIST SP 800-34, AWS Well-Architected reliability pillar, GDPR Art. 44

# On-Call

**SHOULD** rotate on-call across a staffed team with bounded hours and backup responders, not one heroic engineer.

**Why:** Solo on-call burns out or sleeps through pages; one responder is itself a single point of failure for coverage.

**Detect:** PagerDuty/Opsgenie rotation config, single `oncall:` contact in runbooks, no escalation chain.

**References:** Google SRE Book (on-call), OSHA fatigue guidance, NIST SP 800-61

# Post-Incident Review Practice (blameless postmortems with tracked actions)

**MUST** hold a blameless post-incident review for every significant incident within days, with corrective actions assigned, tracked, and verified closed.

**Why:** Without structured learning the same failure repeats; blame-driven cultures hide information when it's needed most.

**Detect:** grep `postmortem`, `RCA`, `blameless`, review templates, action tickets linked to incident IDs.

**References:** NIST SP 800-61 post-incident activity, Google SRE postmortem culture, CIS Control 17

# RTO & RPO

**MUST** define a recovery time objective and recovery point objective per service, and size infrastructure to meet both.

**Why:** Without agreed targets, teams under-protect critical services and discover the mismatch only during a real outage.

**Detect:** `rto:`/`rpo:` in SLO config, backup interval vs stated RPO mismatch, no restore-time test reports.

**References:** NIST SP 800-34, ISO 22301, Google SRE Workbook

# Runbooks

**MUST** keep remediation steps for every paged alert in a version-controlled runbook a non-author can execute.

**Why:** Alerts without written procedures route to Slack archaeology at 3 a.m. when the expert is unreachable.

**Detect:** `runbooks/` directory, alert annotations linking `runbook_url`, stale `last_reviewed` dates in frontmatter.

**References:** Google SRE Workbook (running incidents), NIST SP 800-61, PagerDuty runbook practices

# Self-Healing Systems (auto-restart, auto-failover, self-repair loops)

**SHOULD** automate restart and failover only for known failure modes, keeping each repair loop bounded, observable, and rate-limited.

**Why:** Unmonitored auto-repair oscillates between nodes and masks root causes until capacity is silently exhausted.

**Detect:** review `restartPolicy`, `livenessProbe`, `auto_failover`, `recovery_loop`; check max-restart backoff and remediation alerting.

**References:** Kubernetes restartPolicy/livenessProbe, NIST SP 800-34 auto-recovery

# Single Points of Failure

**SHOULD NOT** let one component — a DNS record, a credential, one box — gate the whole service path.

**Why:** Every unreplicated dependency concentrates failure so one fault takes everything down at once.

**Detect:** one-instance StatefulSets, single `CNAME` targets, solo admin accounts, `replicas: 1`, single-node etcd/Redis without sentinel.

**References:** NIST SP 800-34, AWS Well-Architected, Google SRE Book, CWE-1049

# SLAs

**SHOULD NOT** contract externally committed availability that internal SLOs and capacity cannot demonstrably sustain.

**Why:** An SLA tighter than engineering reality triggers credits, churn, and legal exposure every time the system behaves as built.

**Detect:** SLA text vs `slo:` config mismatch, no credit policy, uptime claims without measurement source.

**References:** Google SRE Book (SLA/SLO/SLI), ISO 20000, NIST SP 800-144

# SLOs

**MUST** define measurable service level indicators with explicit error targets, wired to live dashboards.

**Why:** An unmeasured SLO is a guess; teams cannot tell degradation from noise until customers file tickets.

**Detect:** `slo:`/`sli:` in config, burn-rate alerts in Prometheus rules, absence of latency/availability metrics, dashboard-less target docs.

**References:** Google SRE Workbook (SLO chapter), Prometheus recording rules, ISO 20000

# SOAR / Security Orchestration & Automated Response

**MAY** automate containment through SOAR playbooks, with human review gates on destructive actions.

**Why:** Manual response to high-volume alerts saturates analysts while lateral movement proceeds in the queue.

**Detect:** SOAR platform config (`Shuffle`, `TheHive`, `Cortex`), playbook definitions with `auto_contain`, absence of response automation, no approval gate on isolation actions.

**References:** NIST SP 800-61, Gartner SOAR definition, MITRE ATT&CK response mitigations

# Stateless Services

**SHOULD** keep session and application state external (datastore, token) so any replica can serve any request.

**Why:** Locally stored sessions break autoscaling and failover; a killed node silently logs users out or loses their cart.

**Detect:** `session.save_path` on local disk, `JSESSIONID` sticky sessions, writes to `/tmp` or pod-local volumes, `sessionAffinity: ClientIP`.

**References:** The Twelve-Factor App (processes)

# Customer-Facing Status Page and Outage Comms Templates

**SHOULD** publish a status page and pre-approved outage templates so customers learn impact from you, not rumor.

**Why:** Silence during an outage breeds rumor; improvised messaging contradicts itself and delays reassurance.

**Detect:** status page config (`statuspage.io`, `instatus`), `comms_templates` directory, no comms owner in runbook.

**References:** NIST SP 800-61 (communications), Google SRE Workbook, Atlassian status page practices

# Sticky Sessions & Load-Balancer Affinity

**SHOULD NOT** rely on sticky sessions to make a stateful design work; if affinity is required (websockets, streaming), make it explicit, session-aware, and resilient to node loss.

**Why:** Affinity as a patch for server-side state silently breaks horizontal scaling — a rebalanced or failed node drops every "remembered" session, and scale-out multiplies the problem.

**Detect:** grep LB config for `sticky`, `affinity: cookie`, `sessionAffinity: ClientIP`; check whether session state lives in-app vs external store; test node drain behavior.

**References:** Kubernetes service sessionAffinity docs, AWS ALB stickiness docs, stateless-services issue

# Synthetic External Monitoring

**SHOULD** run synthetic probes from outside the network perimeter to catch outages, TLS problems, and defacement invisible to internal monitoring.

**Why:** Internal checks pass while the public-facing service is down or serving tampered content — the exact failure mode customers experience first.

**Detect:** grep for synthetic checkers (Pingdom, Grafana Synthetic Monitoring, CloudWatch Synthetics) hitting public URLs with content/TLS assertions, not just TCP pings.

**References:** Google SRE Book Ch.6, OWASP Testing Guide 4.0, CWE-295

# Threat Intelligence Integration

**MUST** ingest threat feeds, IOCs, and vendor advisories into ops tooling with automated matching against the estate.

**Why:** Unconsumed intelligence is unread email; a known exploited CVE sits unnoticed until it hits your stack.

**Detect:** IOC feeds in SIEM config, `threat_intel` integrations, no advisory-to-asset matching in the scanner.

**References:** NIST SP 800-150, MITRE ATT&CK, MISP threat sharing, CISA KEV catalog

