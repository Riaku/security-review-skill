# observability — full checklist (41 items)

Logs, metrics, traces, profiling, alerting.

> Generated artifact. Canonical source: `issues/<slug>.md`.

# Structured Logging

**MUST** emit application logs as structured JSON with consistent field names (timestamp, level, event, actor, request_id) rather than free-form text.

**Why:** Unstructured logs defeat automated search and correlation, so attackers' actions hide in noise during incident response.

**Detect:** grep for `console.log(` / `print(` in request handlers; check for logging config with `format: json` or structlog/pino/loguru setup.

**References:** OWASP Logging Cheat Sheet, CWE-1118, NIST SP 800-92

# Log Levels

**SHOULD NOT** ship production builds with debug or trace level logging enabled by default.

**Why:** Verbose levels routinely dump tokens, session payloads, and internal state that attackers read straight off log aggregators.

**Detect:** grep config for `LOG_LEVEL=debug`, `level: trace`, `logging.DEBUG`, `debug = true` in prod env files, Helm values, or Dockerfiles.

**References:** OWASP Logging Cheat Sheet, CWE-532, MASVS-STORAGE-3

# Log Rotation

**MUST** configure rotation and retention for every locally written log file so disks never fill and evidence survives long enough to investigate.

**Why:** Unrotated logs fill the volume and crash the service, while over-short retention erases the audit trail mid-incident.

**Detect:** check logrotate configs, `maxSize`/`maxBackups` in winston/pino, `--log-opt max-size` in compose, or absent rotation on file appenders.

**References:** NIST SP 800-92, CWE-400, CIS Docker 2.4

# Distributed Tracing

**MUST** propagate trace context across all service and queue boundaries so a single request is followable end to end.

**Why:** Without continuous traces, cross-service attacks (request tampering, lateral calls) fragment into unrelated spans nobody connects.

**Detect:** grep for `traceparent` / `tracestate` header propagation in HTTP clients and message producers; check tracer init covers every framework middleware.

**References:** W3C Trace Context, OWASP Testing Guide 4.2, NIST SP 800-187

# OpenTelemetry

**SHOULD** standardize instrumentation on OpenTelemetry SDKs and the OTLP protocol instead of one-off vendor agents.

**Why:** Fragmented telemetry leaves blind spots when vendors change pricing or an incident spans systems the ad-hoc agents never covered.

**Detect:** grep for `opentelemetry-sdk`, `otlp`, `OTEL_EXPORTER_` env vars; flag services with no instrumentation or single-vendor-only agents.

**References:** OpenTelemetry spec, OWASP Logging Cheat Sheet, NIST SP 800-137

# Correlation IDs

**MUST** attach a unique correlation ID to every inbound request and carry it through all downstream calls, logs, and error reports.

**Why:** Without a shared ID, reconstructing one attack's path across services means guessing by timestamps — slow, error-prone, often abandoned.

**Detect:** grep middleware for `X-Request-ID` / `request_id` generation and propagation; verify log schema includes the field on every line.

**References:** OWASP Logging Cheat Sheet, AWS Prescriptive Guidance tracing, Google SRE Book Ch.6

# Metrics Cardinality

**MUST NOT** label metrics with unbounded values like user IDs, emails, session tokens, or raw URLs.

**Why:** High-cardinality labels explode the time-series database, and attacker-crafted unique values can weaponize this into a denial-of-service against monitoring itself.

**Detect:** grep metric definitions for labels like `user=`, `email=`, `url=`, `path=` with raw request data; review Prometheus `label_replace` and histogram bucket counts.

**References:** Prometheus cardinality guidance, CWE-400, Grafana LTS high-availability docs

# p99 Latency

**SHOULD** track and alert on p99 (not just average) latency for critical endpoints and dependency calls.

**Why:** Averages hide tail latency; slow-response attacks like zip bombs, regex bombs, and resource exhaustion show up first in the p99 tail while means look healthy.

**Detect:** grep dashboards/alerts for `histogram_quantile(0.99` or `p99`; flag services whose SLOs use only mean/median latency.

**References:** Google SRE Workbook SLI chapter, CWE-400, NIST SP 800-207 zero-trust monitoring

# Alert Fatigue

**MUST NOT** page humans for alerts that are routinely ignored or auto-resolved without action.

**Why:** Operators drowning in noise stop responding entirely, so the one genuine breach notification arrives inside a wall of dismissed noise.

**Detect:** review alert manager for rules with high fire-to-ack ratio, no `runbook_url`, or silence patterns; grep for `for: 0m` thresholds and catch-all severity mappings.

**References:** Google SRE Workbook alerting chapter, PagerDuty alert fatigue guidance, NIST SP 800-61

# Error Tracking

**SHOULD** route unhandled exceptions to an error tracker (Sentry-style) with release, environment, and correlation context — while scrubbing sensitive fields before transmission.

**Why:** Silent failures hide exploitation attempts; conversely, unscrubbed error payloads ship credentials and PII to third-party trackers.

**Detect:** grep for `before_send` / `before_send` scrubbers, `Sentry.init`, and check that breadcrumbs exclude password, authorization, cookie headers.

**References:** OWASP Logging Cheat Sheet, CWE-532, Sentry security docs, Sentry `before_send` filtering

# Profiling

**MAY** run continuous CPU/heap profiling in production at low overhead to catch performance anomalies early.

**Why:** Profilers expose hot paths where resource-exhaustion attacks (ReDoS, decompression bombs) concentrate, but only if capture is already running when the incident hits.

**Detect:** grep for `py-spy`, `pprof`, `async-profiler`, `continuous profiling` in deployment manifests; verify overhead budget documented.

**References:** Google SRE Book Ch.6 monitoring, CWE-400, Datadog continuous profiling docs

# Flame Graphs

**SHOULD** make flame graphs available for CPU and allocation hot spots so performance regressions and abuse patterns are visually diagnosable.

**Why:** Attackers probing expensive endpoints look like ordinary slowness until a flame graph reveals the exact hot function being hammered.

**Detect:** check profiling pipeline outputs renderable flame graphs (pprof collapsed stacks, Speedscope JSON); verify runbooks link to them.

**References:** Brendan Gregg flame graphs, Google SRE Workbook, CWE-400

# Cost Optimization & Cost Alerting (unit-economics tracking, budget alarms, anomaly detection)

**SHOULD** Track unit economics — cost per request, per user, per pipeline run — alongside raw spend, and enable native anomaly detection so a cost surprise pages someone before the invoice does.

**Why:** Aggregate budgets miss slow-burn regressions like an N+1 query tripling per-request cost, and anomaly detection is often the first visible signal of credential abuse mining compute.

**Detect:** Check for Cost Anomaly Detection subscriptions and velocity-based thresholds. Flag teams tracking only monthly totals. Scan cost-explorer exports for idle resources: unattached EBS volumes, idle NAT gateways, oversized node pools.

**Bad:**
```
# one monthly total budget alarm at 100%; regressions invisible until overrun
```

**Good:**
```
# weekly cost/1k-requests trend + anomaly detection (daily, $50 threshold)
# routed to the owning team's channel, not just finance
```

**References:** AWS Cost Anomaly Detection docs, AWS Well-Architected Cost Optimization pillar, FinOps Framework (finops.org)

# Log Injection & Log Forging

**MUST NOT** write unsanitized user input into log lines; strip CR/LF and control characters before logging any request data.

**Why:** Injected newlines let attackers forge fake log entries or split one entry into many, poisoning the audit trail you rely on during investigations.

**Detect:** grep for user-controlled values interpolated into logger calls (`log.info("User " + username)`) without newline stripping; check for encoder/sanitizer in log appender config.

**References:** OWASP Logging Cheat Sheet, CWE-117, OWASP WSTG-INPV-009

# PII & Secrets Leakage into Application Logs

**MUST** redact passwords, tokens, API keys, and PII at the logging layer before anything reaches disk or an aggregator.

**Why:** Logs are widely readable and long-retained, making them the easiest place for attackers — and auditors — to harvest credentials and personal data.

**Detect:** grep logs and appenders for `password`, `authorization`, `id_card`, `redact`, `mask`; test by logging a known secret and checking it never appears in output.

**References:** OWASP Logging Cheat Sheet, CWE-532, CWE-200, PCI DSS 3.2.1 Req 3

# Kubernetes API Audit Logging Not Enabled

**MUST** enable the kube-apiserver audit policy with persistent, tamper-resistant shipping of audit events.

**Why:** Without API audit logs, privileged actions — secret reads, RBAC changes, pod exec — leave no trace, so cluster compromise is undetectable forensically.

**Detect:** check kube-apiserver flags `--audit-policy-file`, `--audit-log-path`; grep manifests for `audit.k8s.io/v1` Policy; verify long retention on the sink.

**References:** CIS Kubernetes 1.2.1–1.2.4, CWE-778, NIST SP 800-92, K8s docs audit-policy

# Manual kubectl apply Drift Not Detected Against Git

**SHOULD** run periodic drift detection (Flux `diff`/`check`, ArgoCD health) that alerts when live cluster state diverges from the reconciled Git revision.

**Why:** A hand-applied manifest silently overrides GitOps intent, so the next sync either reverts an emergency fix or entrenches an unauthorized change unnoticed.

**Detect:** check Flux `Kustomization` for `interval`/`retryInterval` with drift alerts, ArgoCD `syncPolicy.automated` plus `selfHeal: true`; grep for out-of-band `kubectl apply` in audit logs.

**References:** Flux drift detection docs, ArgoCD selfHeal, OWASP K8s misconfiguration, NIST SP 800-190 integrity monitoring

# Queue Depth and Consumer Lag Alerting

**MUST** page on queue depth and consumer lag thresholds so stalled processing is caught before data is lost or SLAs break.

**Why:** A stalled consumer (often from a poison message or credential expiry) silently accumulates backlog until the broker fills and producers block or messages drop.

**Detect:** grep alert rules for `rabbitmq_queue_messages_ready`, `kafka_consumergroup_lag`, `sqs ApproxAgeOfOldestMessage`; flag queues with no lag alert.

**References:** AWS SQS monitoring guide, RED/USE method, CWE-770, Google SRE Workbook

# Job Age SLO

**MUST** track age of the oldest pending job as a first-class SLO with alerting, not merely queue count or throughput.

**Why:** A backlog of 100 items averaging 1 second looks healthy while one job waits 45 minutes — count-based metrics hide tail latency entirely.

**Detect:** grep dashboards/alerts for `oldest_job_age`, `job_age_seconds`, `head_of_line_blocking`; absence of max-age alerts alongside queue-depth alerts.

**References:** Google SRE Workbook tail latency, NIST SP 800-53 AU-6, SLI/SLO practice

# Dead-man's-switch Heartbeat for Scheduled Jobs

**SHOULD** give every scheduled job a heartbeat that pages when the expected ping is missing, rather than alerting only on failure.

**Why:** A cron that never runs — disabled, deadlocked, or silently deleted — produces no error at all; only absence-of-beat reveals it.

**Detect:** grep schedulers for healthcheck pings (`healthchecks.io`, `deadman` checks, `K8s CronJob` success conditions); flag jobs with failure alerts but no liveness deadline.

**References:** Healthchecks.io dead-man pattern, Google SRE Workbook, CWE-778, K8s CronJob docs

# Slow query log captured, reviewed, and regression-tracked

**SHOULD** enable the slow query log (or `pg_stat_statements`) at an SLO-appropriate threshold, review it on a standing cadence, and treat new entrants as regressions worth a ticket.

**Why:** Slow queries are both outage-causing and attacker-friendly: an unindexed query on an auth path is a DoS lever at volume and the first domino of a connection-pool meltdown. A log nobody reads is telemetry theater.

**Detect:** Check `log_min_duration_statement` or MySQL `slow_query_log`/`long_query_time`, and whether `pg_stat_statements` is loaded. Ask for the review artifact — dashboard, weekly triage note, CI perf gate. Enabled-but-unread logs fail too.

**Bad:**
```ini
log_min_duration_statement = -1   # logging disabled
```

**Good:**
```ini
shared_preload_libraries = 'pg_stat_statements'
log_min_duration_statement = 200  # tied to p95 SLO
# weekly triage: new top queries -> tickets
```

**References:** PostgreSQL pg_stat_statements docs, MySQL slow query log docs, Google SRE Book saturation monitoring

# Disk and inode exhaustion forecasted with lead time

**MUST** forecast disk and inode consumption from historical growth rates and alert early enough (days, not hours) to act before full.

**Why:** A full disk or exhausted inode table corrupts writes and takes down every workload on the volume simultaneously, with no graceful degradation path.

**Detect:** grep monitoring for `disk_free_percent`, `inodes_free`, `predict_linear`/forecast queries in alert rules, log-rotation and cleanup cron jobs; flag alerts that fire only at >95% with no trend projection.

**References:** CWE-400, NIST SP 800-184, Google SRE monitoring four golden signals

# Crash-Loop Restart Storms Bounded and Alarmed

**SHOULD** bound restart backoff and alarm on CrashLoopBackOff so a failing pod cannot hammer the control plane or mask a persistent fault.

**Why:** Unbounded rapid restarts amplify load on kubelet and API server while the underlying error goes unnoticed until an outage.

**Detect:** No alert on `kube_pod_container_status_waiting_reason{reason="CrashLoopBackOff"}`; `restartPolicy` with no backoff ceiling or paging rule.

**References:** K8s docs backoff, kube-state-metrics CrashLoopBackOff, CWE-770, SRE alerting practices

# Log Pipeline Backpressure and Drop Rate

**MUST** monitor the log pipeline's own backlog and drop rate under load so telemetry loss is visible when it happens.

**Why:** During an attack, log volume spikes exactly when you need it most; a silently dropping pipeline destroys evidence precisely then.

**Detect:** grep pipeline metrics for `dropped_total`, `rejected_batches`, `buffer_full`, agent `out_queue` depth; verify alerts on sustained drops > 0.

**References:** NIST SP 800-92, Vector/Fluent Bit drop metrics, Google SRE Workbook, CWE-770

# Synthetic External Monitoring

**SHOULD** run synthetic probes from outside the network perimeter to catch outages, TLS problems, and defacement invisible to internal monitoring.

**Why:** Internal checks pass while the public-facing service is down or serving tampered content — the exact failure mode customers experience first.

**Detect:** grep for synthetic checkers (Pingdom, Grafana Synthetic Monitoring, CloudWatch Synthetics) hitting public URLs with content/TLS assertions, not just TCP pings.

**References:** Google SRE Book Ch.6, OWASP Testing Guide 4.0, CWE-295

# Deploy Markers on Metrics

**MUST** annotate dashboards and traces with deploy events (version, timestamp, actor) so regressions and incidents can be correlated to releases.

**Why:** Without deploy markers, every incident starts with "what changed?" guessed from memory; attackers exploiting a fresh vulnerable deploy hide behind that ambiguity.

**Detect:** grep CI/CD for annotations pushed to metrics (`deploy_event`, Grafana annotations API, `release` label on series); check dashboards show deploy lines.

**References:** Google SRE Workbook, DORA deploy frequency practices, Grafana annotations docs

# PII leakage into application logs, traces, and error reporters

**SHOULD NOT** log raw request bodies, headers, or stack traces containing PII without redaction or masking.

**Why:** Unredacted PII in logs spreads personal data into observability systems, creating unauthorized secondary processing and breach surface.

**Detect:** grep for `log.*request`, `log.*body`, `console.log(err)` without redaction; check `redact_fields`, `mask_pii`, log filter config absent.

**References:** CWE-532, OWASP A05:2021, GDPR Art. 5(1)(c), NIST SP 800-92

# SARIF-Standardized Scan Results (unified alert pipeline)

**SHOULD** emit all scanner findings in SARIF and ingest them into one dashboard, because scattered formats hide coverage gaps and duplicate triage.

**Why:** Findings in per-tool logs go unseen; a unified pipeline makes severity trends and deduplication auditable.

**Detect:** Scanners run without `--format sarif` / `output: sarif`; no upload step to code-scanning API; each tool reporting to a separate ad-hoc log file.

**References:** OWASP CI Security CS2, CWE-1053, NIST SP 800-218 PW.7, SARIF spec (OASIS), GitHub code scanning SARIF upload docs

# Threat Hunting Practice

**SHOULD** run scheduled, hypothesis-driven hunts over retained telemetry instead of waiting for alerts to fire.

**Why:** Sophisticated intruders operate below alert thresholds for weeks; only proactive searching surfaces the anomalies no rule was written for.

**Detect:** verify a documented hunt cadence, saved hunt queries (KQL/SPL/Lucene) in the SIEM, and hunt findings tracked; flag SIEM used only for alert triage.

**References:** MITRE ATT&CK D3FEND hunt guidance, NIST SP 800-150, SANS threat hunting process

# Masquerading & Homoglyph Detection

**SHOULD** detect lookalike process, service, and domain names built from homoglyphs or misspellings of trusted names (e.g. `crond` vs `cron`, `paypa1`).

**Why:** Attackers routinely disguise malware as legitimate binaries; name-similarity checks catch spoofing that hash allowlists miss entirely.

**Detect:** grep EDR/SIEM rules for homoglyph normalization, Levenshtein distance checks against known-good process lists, and lookalike domain monitoring.

**References:** MITRE ATT&CK T1036 Masquerading, T1036.008, CWE-456, Unicode homoglyphs (Trojan Source)

# Beaconing Detection

**MUST** analyze outbound connection timing for fixed-interval patterns that indicate C2 beaconing.

**Why:** Compromised hosts calling home on rigid schedules (every 60s ± jitter) are a hallmark of implant traffic that volume-based alerts never flag.

**Detect:** grep SIEM for inter-arrival variance / jitter analysis queries over flow logs; check NetFlow/Egress rules bucket connection periodicity per destination.

**References:** MITRE ATT&CK T1071, T1029 Scheduled Transfer, CWE-358, Mandiant beaconing detection guidance

# Data Exfiltration Monitoring

**SHOULD** baseline per-host and per-account egress volume and alert on anomalous outbound transfers, especially off-hours and to untrusted destinations.

**Why:** Stolen data must leave the network eventually; without egress baselines, a multi-gigabyte dump to an unknown endpoint looks like ordinary traffic.

**Detect:** grep flow-log analytics for `bytes_out` thresholds, new-destination first-seen alerts, and DB export / S3 egress alarms; verify egress paths are actually observable.

**References:** MITRE ATT&CK T1048 Exfiltration Over Alternative Protocol, T1567, CWE-200, NIST SP 800-53 AC-4

# Living-off-the-Land Abuse

**MUST** monitor execution of legitimate binaries (curl, ssh, powershell, wmic, certutil, base64) for arguments and contexts inconsistent with normal operations.

**Why:** Attackers weaponize signed system tools to run malicious work, evading malware detection because nothing "bad" is ever installed.

**Detect:** grep EDR/SIEM rules for process-args telemetry on LOLBAS-listed binaries (e.g. `certutil -urlcache`, `powershell -enc`); flag hosts where these run outside admin baselines.

**References:** MITRE ATT&CK T1218 System Binary Proxy Execution, LOLBAS project, CWE-427, Atomic Red Team tests

# Anomalous Authentication Detection (impossible travel, rare UA/IP)

**SHOULD** monitor for impossible-travel, rare user-agent, and unfamiliar-IP login patterns and trigger step-up MFA or alerting on anomalies.

**Why:** Without anomaly detection, an attacker logging in from a foreign IP with a stolen credential looks identical to the legitimate user and passes silently.

**Detect:** grep auth pipeline for absent `impossible_travel`, `geoip`, `ua_fingerprint` checks; no step-up MFA on new-device login; no alerting on geo-velocity anomalies.

**References:** NIST SP 800-63B §7.2, OWASP A07:2021, CIS Control 8.3, MITRE ATT&CK T1078

# Lateral Movement Detection (post-compromise horizontal motion in cloud/host)

**SHOULD** alert on post-compromise horizontal motion: unusual SSH/RDP hops, mass SMB enumeration, anomalous cross-account role assumption.

**Why:** Without motion alerts, dwell time stretches to months while one foothold becomes total compromise of crown jewels.

**Detect:** grep detection rules for `T1021`, `remote_services`, `admin_shares`, `pass-the-hash`, unusual-login Sigma/YARA-L rules.

**References:** MITRE ATT&CK TA0008/T1021, NIST SP 800-61, Sigma rules, GuardDuty UnauthorizedAccess

# Credential Access Detection (keylogging, token theft, credential dumping patterns)

**SHOULD** detect credential harvesting: LSASS dumps, keylogging hooks, OAuth token replay, metadata-service credential scraping.

**Why:** Stolen credentials are the leading initial-access vector; catching the theft step stops breaches identity controls alone miss.

**Detect:** grep detection content for `T1003`, `lsass`, `mimikatz`, `secretsdump`, alerts on `169.254.169.254` access, token-replay rules.

**References:** MITRE ATT&CK TA0006/T1003, NIST SP 800-63B, CWE-522, GuardDuty credential-access detections

# Runtime Threat Detection (Falco/eBPF-style workload anomaly detection)

**MUST** monitor running workloads at syscall level (Falco/eBPF) for anomalies: shells in containers, unexpected writes, suspicious spawns.

**Why:** Scanners only see what you built; attackers operate in what's running, unnoticed inside otherwise "secure" images.

**Detect:** grep `falco`, `tracee`, `tetragon`, `ebpf` in DaemonSets/deployment YAML, custom `falco_rules.yaml` files.

**References:** MITRE ATT&CK container matrix T1610, CIS Docker/K8s Benchmarks 5.x, NIST SP 800-190

# Admin Activity Review

**SHOULD** periodically review administrative actions (config changes, permission grants, data exports) against expected operations, on a defined cadence.

**Why:** Insider misuse and compromised admin accounts both hide in plain sight; unreviewed admin logs are a detection gap no amount of collection fixes.

**Detect:** check for scheduled admin-log review (CloudTrail console history, K8s audit webhook, DBA action log) with named reviewer and findings tracked; flag "logs exist but nobody reviews them".

**References:** NIST 800-53 AU-6 review, SOC2 CC7 monitoring, CIS 1.10/8.x log review

# Audit-Log Chain of Custody

**SHOULD** make audit evidence tamper-evident: append-only/WORM storage, integrity hashing or signing, and documented custody for compliance artifacts.

**Why:** Audit findings you can't prove weren't altered are worthless in court or a regulator's hands; tampering by an insider must be detectable.

**Detect:** check log destinations for immutability (S3 Object Lock, BigQuery time-travel, blockchain/hash-chained logs); verify hash/signature chain continuity; check deletion of audit logs is itself alarmed.

**References:** NIST 800-92 log management, AWS S3 Object Lock WORM, SOC2 CC4 evidence integrity

# Certificate-Issuance Monitoring

**SHOULD** alert on any certificate issued for your domains (CT-log monitoring via Certstream/CRT.sh) to detect unauthorized issuance fast.

**Why:** Rogue/mistaken certs for your domain appear in Certificate Transparency logs publicly — if you're not watching, you learn about the fake cert from an outage or a breach report.

**Detect:** check for CT-monitoring service/cron (Censys monitor, Certstream consumer, crt.sh search alerts) covering all brand domains and wildcard patterns; verify alert routing to a responder.

**References:** Certificate Transparency project (certificate-transparency.org), Censys/Certstream monitoring, Google CT policy

# Agent Session-Log Traceability

**MUST** link every agent-authored commit to its session transcript and the human who initiated it (co-author trailer, session-log URL in commit message, verified signature).

**Why:** Without the commit→session→human chain, agent work is unauditable — you cannot answer who asked for this, what context the agent saw, or who owns the outcome.

**Detect:** bot commits lacking co-author/session links; agent tooling with transcripts disabled or rotated to zero retention; no mapping from merged PR to agent run.

**References:** GitHub Copilot agent auditability (signed commits, session-log link), OpenAI Codex transcripts, DeepSeek harness session-log model

