# sre-incidents — full checklist (39 items)

Operational readiness: DR, incidents, SLOs, on-call.

> Generated artifact. Canonical source: `issues/<slug>.md`.

# Health Checks

**MUST** expose an authenticated-or-network-restricted health endpoint that verifies dependencies rather than just process liveness.

**Why:** A process that answers while its database is dead passes naive checks and keeps serving broken responses to users.

**Detect:** `GET /healthz`, `/health`, `HEALTHCHECK` in Dockerfiles, `livenessProbe` without DB checks, `readinessProbe` hitting only static 200.

**References:** Kubernetes health checks, K8s docs, CWE-770, SRE Book

# Liveness vs Readiness Probes

**SHOULD NOT** wire dependency checks (DB, cache) into the liveness probe; reserve them for readiness only.

**Why:** Liveness failures kill pods during a downstream outage, turning a slowdown into a cluster-wide crash loop and thundering restart storm.

**Detect:** `livenessProbe` with `exec: pg_isready`/DB query, identical liveness and readiness endpoints, `initialDelaySeconds: 0`.

**References:** Kubernetes probe docs, CWE-770, Google SRE Workbook

# Graceful Shutdown

**MUST** trap SIGTERM, stop accepting new work, finish in-flight requests, then exit before the kill deadline.

**Why:** Hard-killed workers drop committed-but-unsent transactions and half-written jobs, producing data loss users blame on the service.

**Detect:** `terminationGracePeriodSeconds`, `SIGTERM` handler absent, `preStop` hook missing, `kill -9` in stop scripts.

**References:** Kubernetes termination docs, CWE-227, Google SRE Book

# Connection Draining

**SHOULD** drain established connections at the load balancer before removing a backend from rotation.

**Why:** Abrupt backend removal mid-request severs long-poll and upload sessions, surfacing as random 502s during deploys.

**Detect:** `drain_timeout`, `idle_timeout` on Envoy/HAProxy, `notReadyBeforeDrainDelay`, missing `connectionDraining` in cloud LB config.

**References:** AWS ELB draining, Envoy drain documentation, CWE-582, NIST SP 800-178

# Stateless Services

**SHOULD** keep session and application state external (datastore, token) so any replica can serve any request.

**Why:** Locally stored sessions break autoscaling and failover; a killed node silently logs users out or loses their cart.

**Detect:** `session.save_path` on local disk, `JSESSIONID` sticky sessions, writes to `/tmp` or pod-local volumes, `sessionAffinity: ClientIP`.

**References:** The Twelve-Factor App (processes), NIST SP 800-178, CWE-384

# Failover

**MUST** automatically redirect traffic to healthy replicas within the documented failover time, with the promotion path tested.

**Why:** Manual failover fails at 3 a.m.; an untested standby collapses under real load.

**Detect:** `failover_priority`, `primary`/`replica` config, no `automatic failover` in DB/LB settings, runbook-only failover docs.

**References:** AWS RDS Multi-AZ, Patroni failover, NIST SP 800-34, CWE-1049

# Multi-Region

**SHOULD** deploy across regions only when latency and data residency allow, with explicit region-failure semantics.

**Why:** Cross-region replication lags or split-brains; without a defined loss model, a region outage corrupts what redundancy was meant to protect.

**Detect:** `region:` keys, `global-load-balancer`, `cross-region` replication flags, DNS failover records, GDPR data-residency config.

**References:** NIST SP 800-34, AWS Well-Architected reliability pillar, GDPR Art. 44

# Availability Zones

**MUST** spread replicas across at least two availability zones so one zone's failure cannot drop the service below minimum capacity.

**Why:** All replicas in one zone means a datacenter event takes down 100% of capacity despite looking available.

**Detect:** `topologySpreadConstraints`, `podAntiAffinity` on zone topology, ASG `VPCZoneIdentifier` with one subnet.

**References:** AWS Well-Architected reliability pillar, K8s topology docs, NIST SP 800-34

# Single Points of Failure

**SHOULD NOT** let one component — a DNS record, a credential, one box — gate the whole service path.

**Why:** Every unreplicated dependency concentrates failure so one fault takes everything down at once.

**Detect:** one-instance StatefulSets, single `CNAME` targets, solo admin accounts, `replicas: 1`, single-node etcd/Redis without sentinel.

**References:** NIST SP 800-34, AWS Well-Architected, Google SRE Book, CWE-1049

# Disaster Recovery

**MUST** maintain a rehearsed recovery plan for full-site loss, with restore verified from actual backups.

**Why:** Never-restored backups are unverified files; untested DR plans fail when the real disaster arrives.

**Detect:** `dr_plan.md`, `backup_schedule` cron, absence of restore-test logs, `wal_level`/PITR disabled, offsite sync jobs without checksums.

**References:** NIST SP 800-34, ISO 22301, CWE-190 (backup integrity gaps)

# RTO & RPO

**MUST** define a recovery time objective and recovery point objective per service, and size infrastructure to meet both.

**Why:** Without agreed targets, teams under-protect critical services and discover the mismatch only during a real outage.

**Detect:** `rto:`/`rpo:` in SLO config, backup interval vs stated RPO mismatch, no restore-time test reports.

**References:** NIST SP 800-34, ISO 22301, Google SRE Workbook

# SLAs

**SHOULD NOT** contract externally committed availability that internal SLOs and capacity cannot demonstrably sustain.

**Why:** An SLA looser than engineering reality triggers credits, churn, and legal exposure every time the system behaves as built.

**Detect:** SLA text vs `slo:` config mismatch, no credit policy, uptime claims without measurement source.

**References:** Google SRE Book (SLA/SLO/SLI), ISO 20000, NIST SP 800-144

# SLOs

**MUST** define measurable service level indicators with explicit error targets, wired to live dashboards.

**Why:** An unmeasured SLO is a guess; teams cannot tell degradation from noise until customers file tickets.

**Detect:** `slo:`/`sli:` in config, burn-rate alerts in Prometheus rules, absence of latency/availability metrics, dashboard-less target docs.

**References:** Google SRE Workbook (SLO chapter), Prometheus recording rules, ISO 20000

# Error Budgets

**SHOULD** spend the gap between 100% and the SLO as a budget for risky releases, freezing changes when exhausted.

**Why:** Without a shared budget, reliability debates become endless opinion fights instead of an agreed mechanical tradeoff.

**Detect:** `error_budget` in SLO config, multi-window multi-burn-rate alert thresholds, no freeze policy on exhaustion.

**References:** Google SRE Workbook (error budgets), Prometheus multi-window multi-burn-rate alerting

# Incident Response

**MUST** maintain a written incident response process with defined roles, escalation paths, and comms cadence, exercised annually.

**Why:** Ad-hoc response during a live outage wastes hours on coordination arguments while customer impact compounds.

**Detect:** `incident_response.md`, severity matrix, absence of paging integration, no IR tabletop logs, missing escalation contacts in runbooks.

**References:** NIST SP 800-61, SANS incident response process, ISO/IEC 27035

# On-Call

**SHOULD** rotate on-call across a staffed team with bounded hours and backup responders, not one heroic engineer.

**Why:** Solo on-call burns out or sleeps through pages; one responder is itself a single point of failure for coverage.

**Detect:** PagerDuty/Opsgenie rotation config, single `oncall:` contact in runbooks, no escalation chain.

**References:** Google SRE Book (on-call), OSHA fatigue guidance, NIST SP 800-61

# Runbooks

**MUST** keep remediation steps for every paged alert in a version-controlled runbook a non-author can execute.

**Why:** Alerts without written procedures route to Slack archaeology at 3 a.m. when the expert is unreachable.

**Detect:** `runbooks/` directory, alert annotations linking `runbook_url`, stale `last_reviewed` dates in frontmatter.

**References:** Google SRE Workbook (running incidents), NIST SP 800-61, PagerDuty runbook practices

# Postmortems

**SHOULD** write a blameless postmortem for every significant incident within days, with action items tracked to closure.

**Why:** Incidents without written analysis repeat; the fix lived in the responder's head and never reached the backlog.

**Detect:** `postmortems/` directory, `action_items` with owners and due dates, unresolved items past deadline.

**References:** Google SRE Book (postmortem culture), Blameless postmortem practice, NIST SP 800-61

# Chaos Engineering

**MAY** run controlled failure injection in production-like environments, scoped by blast radius and abort criteria.

**Why:** Untested redundancy is assumed redundancy; failover paths quietly rot between verified drills.

**Detect:** `chaos-mesh`, `litmus`, Gremlin config, absence of game-day logs, no abort/steady-state criteria in experiment manifests.

**References:** Principles of Chaos Engineering, Netflix Chaos Monkey, AWS FIS, NIST SP 800-34 drills

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

# DORA (financial sector resilience)

**MUST** classify critical ICT functions, test resilience (including TLPT threat-led testing), and register ICT third-party arrangements per DORA timelines.

**Why:** Financial entities failing operational-resilience tests risk forced exit from EU markets; untested backups and ICT vendors are the failure points.

**Detect:** grep for "DORA", "TLPT", "critical functions register", ICT exit plans; missing incident escalation, unregistered ICT providers.

**References:** EU Regulation 2022/2554, ESA RTS/ITS on RTS, EIOPA/EBA guidance

# Self-Healing Systems (auto-restart, auto-failover, self-repair loops)

**MAY** automate restart and failover for known failure modes, but each repair loop MUST be bounded, observable, and rate-limited.

**Why:** Unmonitored auto-repair oscillates between nodes and masks root causes until capacity is silently exhausted.

**Detect:** review `restartPolicy`, `livenessProbe`, `auto_failover`, `recovery_loop`; check max-restart backoff and remediation alerting.

**References:** Kubernetes restartPolicy/livenessProbe, AWS REL11-BP10, NIST SP 800-34 auto-recovery, CWE-251

# Dead-man's-switch Heartbeat for Scheduled Jobs

**SHOULD** give every scheduled job a heartbeat that pages when the expected ping is missing, rather than alerting only on failure.

**Why:** A cron that never runs — disabled, deadlocked, or silently deleted — produces no error at all; only absence-of-beat reveals it.

**Detect:** grep schedulers for healthcheck pings (`healthchecks.io`, `deadman` checks, `K8s CronJob` success conditions); flag jobs with failure alerts but no liveness deadline.

**References:** Healthchecks.io dead-man pattern, Google SRE Workbook, CWE-778, K8s CronJob docs

# Crash-consistent volume snapshots vs logical dumps distinguished

**SHOULD** document, per datastore, whether each backup is crash-consistent (volume snapshot) or logically consistent (`pg_dump`, `mysqldump`), and use the right one per recovery scenario.

**Why:** A raw volume snapshot of a running database captures whatever was in page cache at capture time; the engine may need crash recovery, and some configurations produce unrestorable sets. Mixing them up means discovering at restore time that the "backup" was never a valid restore point.

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

# Storage Operating Degraded (Degraded RAID/Mirror) Runbook

**MUST** provide a runbook for degraded RAID/mirror states: rebuild procedure, performance limits, escalation threshold.

**Why:** A degraded mirror silently loses redundancy; the next disk failure becomes an unrecoverable array collapse.

**Detect:** `mdadm --detail` showing `degraded`, `zpool status` DEGRADED, absence of `degraded` runbook, no rebuild-priority or scrub schedule.

**References:** NIST SP 800-34, RAID recovery procedures, ZFS administration guide, CWE-190

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

# Control-Plane Quorum (etcd) Health Monitored Separately from Workloads

**MUST** monitor etcd quorum and leader health independently of application dashboards, alerting before quorum loss.

**Why:** Losing etcd quorum freezes the entire cluster's API; a workload-only dashboard misses the failure until everything is already down.

**Detect:** No etcd metrics scrape (`etcd_server_has_leader`, `etcd_server_health_failures`); no separate control-plane alert rule or runbook.

**References:** CIS K8s 2.0, etcd monitoring docs, NIST SP 800-190 5.4, K8s HA control-plane docs

# Synthetic External Monitoring

**SHOULD** run synthetic probes from outside the network perimeter to catch outages, TLS problems, and defacement invisible to internal monitoring.

**Why:** Internal checks pass while the public-facing service is down or serving tampered content — the exact failure mode customers experience first.

**Detect:** grep for synthetic checkers (Pingdom, Grafana Synthetic Monitoring, CloudWatch Synthetics) hitting public URLs with content/TLS assertions, not just TCP pings.

**References:** Google SRE Book Ch.6, OWASP Testing Guide 4.0, CWE-295

# Incident Severity Levels with a Designated Incident Commander

**MUST** assign a named incident commander per severity level at declaration, with coordination authority.

**Why:** Without a single decision-maker, engineers duplicate work and argue rollback timing while the outage widens.

**Detect:** severity matrix (`SEV1`–`SEV4`) in IR docs, `incident_commander` field in tickets, no commander in paging config.

**References:** NIST SP 800-61, Google SRE Workbook (incident command), ITIL incident management

# Customer-Facing Status Page and Outage Comms Templates

**SHOULD** publish a status page and pre-approved outage templates so customers learn impact from you, not rumor.

**Why:** Silence during an outage breeds rumor; improvised messaging contradicts itself and delays reassurance.

**Detect:** status page config (`statuspage.io`, `instatus`), `comms_templates` directory, no comms owner in runbook.

**References:** NIST SP 800-61 (communications), Google SRE Workbook, Atlassian status page practices

# Breach notification clocks across jurisdictions

**MUST** detect and triage breaches fast enough to meet the strictest applicable notification deadline (72h GDPR, state laws).

**Why:** Missing statutory notification windows compounds breach penalties and destroys regulatory trust after an incident.

**Detect:** grep for incident response SLA timers, `notification_deadline`, `breach_clock` config; check monitoring-to-notification pipeline latency absent.

**References:** GDPR Art. 33, Cal. Civ. Code §1798.82, HIPAA Breach Rule 45 CFR 164.404, NIST SP 800-61

# SEC cybersecurity disclosure rules (public-company material incident reporting)

**MUST** disclose material cybersecurity incidents within four business days of a materiality determination via Form 8-K Item 1.05, with board-level oversight documented.

**Why:** Delayed or vague disclosure after a breach invites SEC enforcement, shareholder suits, and restatements of prior risk statements.

**Detect:** grep for "8-K", "Item 1.05", materiality assessment process; no incident-to-disclosure workflow, missing disclosure committee charter.

**References:** SEC 8-K Item 1.05 (2023), Reg S-K Item 106, SEC cyber disclosure guidance

# Threat Intelligence Integration

**MUST** ingest threat feeds, IOCs, and vendor advisories into ops tooling with automated matching against the estate.

**Why:** Unconsumed intelligence is unread email; a known exploited CVE sits unnoticed until it hits your stack.

**Detect:** IOC feeds in SIEM config, `threat_intel` integrations, no advisory-to-asset matching in the scanner.

**References:** NIST SP 800-150, MITRE ATT&CK, MISP threat sharing, CISA KEV catalog

# SOAR / Security Orchestration & Automated Response

**MAY** automate containment through SOAR playbooks, with human review gates on destructive actions.

**Why:** Manual response to high-volume alerts saturates analysts while lateral movement proceeds in the queue.

**Detect:** SOAR platform config (`Shuffle`, `TheHive`, `Cortex`), playbook definitions with `auto_contain`, absence of response automation, no approval gate on isolation actions.

**References:** NIST SP 800-61, Gartner SOAR definition, MITRE ATT&CK response mitigations

# Backup Verification Drills (scheduled restore tests, not just backup jobs)

**MUST** run scheduled restore drills proving backups actually recover systems, with results tracked and failures escalated.

**Why:** Backups never restored are unverified guesses; ransomware crews routinely destroy backup targets too.

**Detect:** grep `restore_test`, `velero restore create`, `pg_restore` in scheduled jobs, AWS Backup restore-testing plans, drill runbooks.

**References:** NIST SP 800-34, CIS Control 11, NIST CSF PR.IP-4

# Post-Incident Review Practice (blameless postmortems with tracked actions)

**MUST** hold a blameless post-incident review for every significant incident, with corrective actions assigned, tracked, and verified closed.

**Why:** Without structured learning the same failure repeats; blame-driven cultures hide information when it's needed most.

**Detect:** grep `postmortem`, `RCA`, `blameless`, review templates, action tickets linked to incident IDs.

**References:** NIST SP 800-61 post-incident activity, Google SRE postmortem culture, CIS Control 17

# Break-Glass Access Procedure

**SHOULD** define a monitored break-glass path for emergency privileged access: pre-authorized, logged, alerting on use, and reviewed within 24h.

**Why:** Without a sanctioned emergency path, responders improvise with standing admin access — which is either absent in the outage or abused permanently after it.

**Detect:** look for break-glass accounts/policies (AWS IAM break-glass role, Azure PIM emergency access) with alert-on-use and review SLA; check that emergency creds are escrowed (sealed envelope) not casually held.

**References:** Microsoft emergency access accounts, AWS break-glass role patterns, NIST 800-53 AC-2(2)

# Reconciliation Runbook

**SHOULD** maintain a tested reconciliation process between internal records and external sources (PSP settlement files, bank statements, partner reports) with discrepancy handling.

**Why:** Money systems disagree with their counterparties routinely; without a reconciliation runbook, every mismatch becomes a fire-drill, and real losses hide in the "we'll check later" pile.

**Detect:** look for reconciliation jobs comparing internal ledger vs PSP/bank files with tolerance thresholds; check discrepancy queue with owner and SLA; verify runbook covers partial settlements and currency mismatches.

**References:** Stripe reconciliation guidance, PCI-DSS 9/10 financial monitoring, payments-engineering practice guides

# DST-Transition Behavior Test

**SHOULD** test scheduled jobs and time logic across DST transitions (spring-forward gap, fall-back overlap) in the deployment timezone.

**Why:** Cron jobs silently skip or double-fire at DST boundaries; "runs every 2h" becomes 23 or 25 runs twice a year — a bug that hides for months and hits exactly when you're asleep.

**Detect:** check for tests that freeze time at DST boundaries (e.g. 2026-03-08 02:30 US), cron schedules using UTC vs local TZ, and scheduler docs stating which timezone governs; flag local-TZ cron for critical jobs.

**References:** cron DST pitfalls (crontab(5) NOTES), NTP/timezone best practices, ICU timezone docs

