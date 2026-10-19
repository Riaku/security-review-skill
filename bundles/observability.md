# observability — full checklist (57 items)

Logs, metrics, traces, profiling, alerting.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/observability.md](../categories/observability.md) · Index: [SKILL.md](../SKILL.md)

# Admin Activity Review

**SHOULD** periodically review administrative actions (config changes, permission grants, data exports) against expected operations, on a defined cadence.

**Why:** Insider misuse and compromised admin accounts both hide in plain sight; unreviewed admin logs are a detection gap no amount of collection fixes.

**Detect:** check for scheduled admin-log review (CloudTrail console history, K8s audit webhook, DBA action log) with named reviewer and findings tracked; flag "logs exist but nobody reviews them".

**References:** NIST 800-53 AU-6 review, SOC2 CC7 monitoring, CIS 8.11 (Conduct Audit Log Reviews)

# Agent Session-Log Traceability

**MUST** link every agent-authored commit to its session transcript and the human who initiated it (co-author trailer, session-log URL in commit message, verified signature).

**Why:** Without the commit→session→human chain, agent work is unauditable — you cannot answer who asked for this, what context the agent saw, or who owns the outcome.

**Detect:** bot commits lacking co-author/session links; agent tooling with transcripts disabled or rotated to zero retention; no mapping from merged PR to agent run.

**References:** GitHub Copilot agent auditability (signed commits, session-log link), OpenAI Codex transcripts, DeepSeek harness session-log model

# Verify The Alert Channel

**MUST** monitor the delivery path of security alerts and keep it outside the control of the component being monitored.

**Why:** A guardrail that fires into a broken or suppressible channel is indistinguishable from one that never fires, and the gap appears only during the incident.

**Detect:** command schedule a synthetic alert (`amtool alert add`, Alertmanager test alert) with an expected-receipt check and an alert when receipt is missing.

**References:** Agentic AI Top 10: AAI012 Checker-out-of-the-Loop, https://github.com/precize/Agentic-AI-Top10-Vulnerability

# Alert Fatigue

**MUST NOT** page humans for alerts that are routinely ignored or auto-resolved without action.

**Why:** Operators drowning in noise stop responding entirely, so the one genuine breach notification arrives inside a wall of dismissed noise.

**Detect:** review alert manager for rules with high fire-to-ack ratio, no `runbook_url`, or silence patterns; grep for `for: 0m` thresholds and catch-all severity mappings.

**References:** Google SRE Workbook alerting chapter, PagerDuty alert fatigue guidance, NIST SP 800-61

# Anomalous Authentication Detection (impossible travel, rare UA/IP)

**SHOULD** monitor for impossible-travel, rare user-agent, and unfamiliar-IP login patterns and trigger step-up MFA or alerting on anomalies.

**Why:** Without anomaly detection, an attacker logging in from a foreign IP with a stolen credential looks identical to the legitimate user and passes silently.

**Detect:** grep auth pipeline for absent `impossible_travel`, `geoip`, `ua_fingerprint` checks; no step-up MFA on new-device login; no alerting on geo-velocity anomalies.

**References:** OWASP A07:2021, CIS Control 8.3, MITRE ATT&CK T1078

# Application-Level Active Defense

**SHOULD** aggregate misuse signals across endpoints — repeated authorization failures, malformed structures, out-of-order steps — and respond rather than only logging each event.

**Why:** Per-endpoint validation lets an attacker probe the whole application without ever tripping a control, and the owner learns nothing until the breach.

**Detect:** grep for alerting or throttling keyed on aggregated 403/422 rates and workflow-order violations, not only per-route rate limits.

**References:** OWASP WSTG Business Logic Testing, https://github.com/OWASP/wstg/tree/master/document/4-Web_Application_Security_Testing

# Audit-First State Changes

**MUST** write the audit record in the same transaction as the state change, so neither commits without the other.

**Why:** A change that lands without its record leaves the audit trail asserting a world that is no longer true, and no later reconciliation can recover it.

**Detect:** grep state-changing handlers and deploy scripts for an audit write outside the same transaction, or after the mutation returns.

**References:** Audit-first rollback semantics (arXiv 2609.00406), https://arxiv.org/abs/2609.00406

# Audit Logs

**MUST** record security-relevant events (auth, access, privilege changes) with tamper-evident integrity and retention aligned to policy; **SHOULD** keep compliance-relevant audit evidence on append-only/WORM storage with integrity hashing or signing and documented custody, so insider tampering is detectable.

**Why:** Missing or mutable audit trails prevent incident reconstruction and violate compliance requirements for non-repudiation.

**Detect:** grep for auth/access handlers missing audit calls; check `audit_log`, `log_event`, HMAC signing, retention config absent; check log destinations for immutability (S3 Object Lock, BigQuery time-travel, hash-chained logs), verify hash/signature chain continuity, and confirm audit-log deletion is itself alarmed.

**References:** CWE-778, NIST SP 800-92, AWS S3 Object Lock WORM, SOC 2 CC7.2/CC4, PCI DSS 10.2

# Action-to-Audit Divergence Checks

**MUST** test each class of divergence between an executed action and its audit record before treating the log as evidence of what happened.

**Why:** Aggregate logging records what the system claims happened, not whether it matched the approval; action-without-approval, approval-without-action, silent failure logged as success, and wrong-target execution each need their own structural check.

**Detect:** judgment: the audit design and the checker wired to each of the four divergence classes

**References:** Architectural Obsolescence of Unhardened Agentic-AI Runtimes, https://arxiv.org/abs/2605.01740

# Beaconing Detection

**MUST** analyze outbound connection timing for fixed-interval patterns that indicate C2 beaconing.

**Why:** Compromised hosts calling home on rigid schedules (every 60s ± jitter) are a hallmark of implant traffic that volume-based alerts never flag.

**Detect:** grep SIEM for inter-arrival variance / jitter analysis queries over flow logs; check NetFlow/Egress rules bucket connection periodicity per destination.

**References:** MITRE ATT&CK T1071, T1029 Scheduled Transfer, CWE-358, Mandiant beaconing detection guidance

# Certificate-Issuance Monitoring

**SHOULD** alert on any certificate issued for your domains (CT-log monitoring via Certstream/CRT.sh) to detect unauthorized issuance fast.

**Why:** Rogue/mistaken certs for your domain appear in Certificate Transparency logs publicly — if you're not watching, you learn about the fake cert from an outage or a breach report.

**Detect:** check for CT-monitoring service/cron (Censys monitor, Certstream consumer, crt.sh search alerts) covering all brand domains and wildcard patterns; verify alert routing to a responder.

**References:** Certificate Transparency project (certificate-transparency.org), Censys/Certstream monitoring, Google CT policy

# Correlation IDs

**MUST** attach a unique correlation ID to every inbound request and carry it through all downstream calls, logs, and error reports.

**Why:** Without a shared ID, reconstructing one attack's path across services means guessing by timestamps — slow, error-prone, often abandoned.

**Detect:** grep middleware for `X-Request-ID` / `request_id` generation and propagation; verify log schema includes the field on every line.

**References:** OWASP Logging Cheat Sheet, AWS Prescriptive Guidance tracing, Google SRE Book Ch.6

# Cost Optimization & Cost Alerting (unit-economics tracking, budget alarms, anomaly detection)

**MUST** budget alarms exist at account and per-project level, wired to a channel someone actually reads, with thresholds low enough to catch a runaway resource before it becomes a five-figure month.
**SHOULD** track unit economics — cost per request, per user, per pipeline run — alongside raw spend, and enable native anomaly detection so a cost surprise pages someone before the invoice does.

**Why:** Compromised keys, crypto-mining spin-ups, and retry-storm Lambda loops all manifest first as a billing spike; teams without alarms discover them at invoice time, weeks after the abuse started. Aggregate budgets miss slow-burn regressions like an N+1 query tripling per-request cost, and anomaly detection is often the first visible signal of credential abuse mining compute.

**Detect:** Check IaC for AWS Budgets / GCP Budget Alerts / Azure Cost Management exports — absence is the finding. Verify recipients are distribution lists, not one departing engineer, and that daily-velocity checks exist alongside monthly totals. Check for Cost Anomaly Detection subscriptions and velocity-based thresholds. Flag teams tracking only monthly totals. Scan cost-explorer exports for idle resources: unattached EBS volumes, idle NAT gateways, oversized node pools.

**Bad:**
```
# no budgets defined at all; first signal is the month-end invoice: $41,000
# one monthly total budget alarm at 100%; regressions invisible until overrun
```

**Good:**
```
# weekly cost/1k-requests trend + anomaly detection (daily, $50 threshold)
# routed to the owning team's channel, not just finance
# plus account/per-project aws_budgets_budget at a low threshold -> ops-alerts@corp distribution list
```

**References:** AWS Budgets docs, GCP Budget alerts, CIS AWS Foundations 4.x, OWASP A09:2021 Logging & Monitoring Failures, AWS Cost Anomaly Detection docs, AWS Well-Architected Cost Optimization pillar, FinOps Framework (finops.org)

# Crash-Loop Restart Storms Bounded and Alarmed

**SHOULD** bound a crash-looping workload's blast radius (restart deadline, quota, node-level backoff tuning where available) and alarm on CrashLoopBackOff so a failing pod cannot hammer the control plane or mask a persistent fault.

**Why:** Unbounded rapid restarts amplify load on kubelet and API server while the underlying error goes unnoticed until an outage.

**Detect:** No alert on `kube_pod_container_status_waiting_reason{reason="CrashLoopBackOff"}` and no paging rule for it; no `activeDeadlineSeconds` or quota bounding an endlessly restarting workload (`restartPolicy` accepts only `Always`/`OnFailure`/`Never` and carries no backoff ceiling).

**References:** K8s docs backoff, kube-state-metrics CrashLoopBackOff, CWE-770, SRE alerting practices

# Credential Access Detection (keylogging, token theft, credential dumping patterns)

**SHOULD** detect credential harvesting: LSASS dumps, keylogging hooks, OAuth token replay, metadata-service credential scraping.

**Why:** Stolen credentials are the leading initial-access vector; catching the theft step stops breaches identity controls alone miss.

**Detect:** grep detection content for `T1003`, `lsass`, `mimikatz`, `secretsdump`, alerts on `169.254.169.254` access, token-replay rules.

**References:** MITRE ATT&CK TA0006/T1003, NIST SP 800-63B, CWE-522, GuardDuty credential-access detections

# Data Exfiltration Monitoring

**SHOULD** baseline per-host and per-account egress volume and alert on anomalous outbound transfers, especially off-hours and to untrusted destinations.

**Why:** Stolen data must leave the network eventually; without egress baselines, a multi-gigabyte dump to an unknown endpoint looks like ordinary traffic.

**Detect:** grep flow-log analytics for `bytes_out` thresholds, new-destination first-seen alerts, and DB export / S3 egress alarms; verify egress paths are actually observable.

**References:** MITRE ATT&CK T1048 Exfiltration Over Alternative Protocol, T1567, CWE-200, NIST SP 800-53 AC-4

# Deploy Markers on Metrics

**MUST** annotate dashboards and traces with deploy events (version, timestamp, actor) so regressions and incidents can be correlated to releases.

**Why:** Without deploy markers, every incident starts with "what changed?" guessed from memory; attackers exploiting a fresh vulnerable deploy hide behind that ambiguity.

**Detect:** grep CI/CD for annotations pushed to metrics (`deploy_event`, Grafana annotations API, `release` label on series); check dashboards show deploy lines.

**References:** Google SRE Workbook, DORA deploy frequency practices, Grafana annotations docs

# Detection Log-Source Liveness

**MUST** verify that every deployed detection rule's declared log source is actually arriving, and alert on rules that have received no events.

**Why:** A rule whose index or channel is never populated is a control that silently does not exist while counting as deployed coverage.

**Detect:** query the backend for the newest event per log source (tstats latest(_time) by index, or SELECT max(ts) GROUP BY source) and compare with each rule's logsource

**References:** deadair, https://github.com/alephnull-sh/deadair

# Detection Rule FP Profile

**SHOULD** record each detection rule's maturity status and its known false-positive profile inside the rule, and review both whenever the rule changes.

**Why:** An undeclared false-positive rate is discovered by analysts at 3am, and the rule is then disabled or ignored wholesale.

**Detect:** grep for falsepositives: and status: fields in every rule file, and compare declared profile against alert volume per rule

**References:** Sigma rule schema, https://github.com/SigmaHQ/sigma

# Disk and inode exhaustion forecasted with lead time

**MUST** forecast disk and inode consumption from historical growth rates and alert early enough (days, not hours) to act before full.

**Why:** A full disk or exhausted inode table corrupts writes and takes down every workload on the volume simultaneously, with no graceful degradation path.

**Detect:** grep monitoring for `disk_free_percent`, `inodes_free`, `predict_linear`/forecast queries in alert rules, log-rotation and cleanup cron jobs; flag alerts that fire only at >95% with no trend projection.

**References:** CWE-400, NIST SP 800-184, Google SRE monitoring four golden signals

# Distributed Tracing

**MUST** propagate trace context across all service and queue boundaries so a single request is followable end to end.

**Why:** Without continuous traces, cross-service attacks (request tampering, lateral calls) fragment into unrelated spans nobody connects.

**Detect:** grep for `traceparent` / `tracestate` header propagation in HTTP clients and message producers; check tracer init covers every framework middleware.

**References:** W3C Trace Context, OpenTelemetry documentation

# Error Tracking

**SHOULD** route unhandled exceptions to an error tracker (Sentry-style) with release, environment, and correlation context — while scrubbing sensitive fields before transmission.

**Why:** Silent failures hide exploitation attempts; conversely, unscrubbed error payloads ship credentials and PII to third-party trackers.

**Detect:** grep for `before_send` scrubbers, `Sentry.init`, and check that breadcrumbs exclude password, authorization, cookie headers.

**References:** OWASP Logging Cheat Sheet, CWE-532, Sentry security docs, Sentry `before_send` filtering

# Flame Graphs

**SHOULD** make flame graphs available for CPU and allocation hot spots so performance regressions and abuse patterns are visually diagnosable.

**Why:** Attackers probing expensive endpoints look like ordinary slowness until a flame graph reveals the exact hot function being hammered.

**Detect:** check profiling pipeline outputs renderable flame graphs (pprof collapsed stacks, Speedscope JSON); verify runbooks link to them.

**References:** Brendan Gregg flame graphs, Google SRE Workbook, CWE-400

# Gateway Payload Logging

**MUST** disable full request and response payload logging unless redaction and a bounded retention window are enforced.

**Why:** Trace features capture credentials and personal data into log sinks that are far more widely readable than the systems they instrument.

**Detect:** grep gateway and proxy IaC for payload or trace logging enabled (`data_trace_enabled`, `xray_tracing_enabled`, `field_level_logs`, `logging_level: full`) without redaction config.

**References:** Checkov IaC policy catalogue, https://github.com/bridgecrewio/checkov

# Infrastructure Drift Detection (live state vs IaC and GitOps reconciliation)

**MUST** continuously diff live infrastructure against IaC definitions and alert on unauthorized manual changes; **SHOULD** also run periodic drift detection on the GitOps path (Flux `diff`/`check`, ArgoCD health) that alerts when live cluster state diverges from the reconciled Git revision.

**Why:** A hand-applied manifest silently overrides GitOps intent, so the next sync either reverts an emergency fix or entrenches an unauthorized change unnoticed; console-clicked changes bypass review and become invisible holes — an undocumented open security group never gets fixed.

**Detect:** grep `terraform plan -detailed-exitcode` cron jobs, Driftctl, AWS Config drift rules, `kubectl diff -f`; check Flux `Kustomization` for `interval`/`retryInterval` with drift alerts, ArgoCD `syncPolicy.automated` plus `selfHeal: true`; grep for out-of-band `kubectl apply` in audit logs.

**References:** Flux drift detection docs, ArgoCD selfHeal, OWASP K8s misconfiguration, NIST SP 800-190 integrity monitoring, NIST SP 800-53 CM-3/CM-6, CIS Control 2, Terraform drift docs

# Dead-man's-switch Heartbeat for Scheduled Jobs

**SHOULD** give every scheduled job a heartbeat that pages when the expected ping is missing, rather than alerting only on failure.

**Why:** A cron that never runs — disabled, deadlocked, or silently deleted — produces no error at all; only absence-of-beat reveals it.

**Detect:** grep schedulers for healthcheck pings (`healthchecks.io`, `deadman` checks, `K8s CronJob` success conditions); flag jobs with failure alerts but no liveness deadline.

**References:** Healthchecks.io dead-man pattern, Google SRE Workbook, CWE-778, K8s CronJob docs

# Job Age SLO

**MUST** track age of the oldest pending job as a first-class SLO with alerting, not merely queue count or throughput.

**Why:** A backlog of 100 items averaging 1 second looks healthy while one job waits 45 minutes — count-based metrics hide tail latency entirely.

**Detect:** grep dashboards/alerts for `oldest_job_age`, `job_age_seconds`, `head_of_line_blocking`; absence of max-age alerts alongside queue-depth alerts.

**References:** Google SRE Workbook tail latency, NIST SP 800-53 AU-6, SLI/SLO practice

# Kubernetes API Audit Logging Not Enabled

**MUST** enable the kube-apiserver audit policy with persistent, tamper-resistant shipping of audit events.

**Why:** Without API audit logs, privileged actions — secret reads, RBAC changes, pod exec — leave no trace, so cluster compromise is undetectable forensically.

**Detect:** check kube-apiserver flags `--audit-policy-file`, `--audit-log-path`; grep manifests for `audit.k8s.io/v1` Policy; verify long retention on the sink.

**References:** CIS Kubernetes Benchmark 1.2.x (API-server audit settings: --audit-policy-file, --audit-log-path, rotation and retention), CWE-778, NIST SP 800-92, K8s docs audit-policy

# Key Use Logging

**MUST** log every use of a key-management key with caller identity, operation, and target resource.

**Why:** Key use without an audit trail hides both misuse and the blast radius of a stolen credential. The log is the only record separating a legitimate decrypt from an exfiltration.

**Detect:** grep key-management client wrappers for audit emission on encrypt, decrypt, and sign calls; flag direct key-service calls that bypass the wrapper.

**References:** OWASP Proactive Controls C9, https://github.com/OWASP/www-project-proactive-controls, NIST SP 800-57 key management

# Lateral Movement Detection (post-compromise horizontal motion in cloud/host)

**SHOULD** alert on post-compromise horizontal motion: unusual SSH/RDP hops, mass SMB enumeration, anomalous cross-account role assumption.

**Why:** Without motion alerts, dwell time stretches to months while one foothold becomes total compromise of crown jewels.

**Detect:** grep detection rules for `T1021`, `remote_services`, `admin_shares`, `pass-the-hash`, unusual-login Sigma/YARA-L rules.

**References:** MITRE ATT&CK TA0008/T1021, NIST SP 800-61, Sigma rules, GuardDuty UnauthorizedAccess

# Living-off-the-Land Abuse

**MUST** monitor execution of legitimate binaries (curl, ssh, powershell, wmic, certutil, base64) for arguments and contexts inconsistent with normal operations.

**Why:** Attackers weaponize signed system tools to run malicious work, evading malware detection because nothing "bad" is ever installed.

**Detect:** grep EDR/SIEM rules for process-args telemetry on LOLBAS-listed binaries (e.g. `certutil -urlcache`, `powershell -enc`); flag hosts where these run outside admin baselines.

**References:** MITRE ATT&CK T1218 System Binary Proxy Execution, LOLBAS project, CWE-427, Atomic Red Team tests

# Log Destination Inventory

**MUST** keep a log inventory of what each layer logs, its destination, retention, and access, and emit only to documented destinations.

**Why:** An undocumented sink moves sensitive data outside the retention and access regime, and no later investigation can say where it went.

**Detect:** grep logger configuration (`handlers`, `appenders`, `syslog:`, `outputs`) and compare every destination against the inventory document.

**References:** OWASP ASVS v5.0 V16.2.3, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md

# Log Injection & Log Forging

**MUST NOT** write unsanitized user input into log lines; strip CR/LF and control characters before logging any request data.

**Why:** Injected newlines let attackers forge fake log entries or split one entry into many, poisoning the audit trail you rely on during investigations.

**Detect:** grep for user-controlled values interpolated into logger calls (`log.info("User " + username)`) without newline stripping; check for encoder/sanitizer in log appender config.

**References:** OWASP Logging Cheat Sheet, CWE-117

# Log Levels

**SHOULD NOT** ship production builds with debug or trace level logging enabled by default.

**Why:** Verbose levels routinely dump tokens, session payloads, and internal state that attackers read straight off log aggregators.

**Detect:** grep config for `LOG_LEVEL=debug`, `level: trace`, `logging.DEBUG`, `debug = true` in prod env files, Helm values, or Dockerfiles.

**References:** OWASP Logging Cheat Sheet, CWE-532, MASVS-STORAGE-3

# Log Pipeline Backpressure and Drop Rate

**MUST** monitor the log pipeline's own backlog and drop rate under load so telemetry loss is visible when it happens.

**Why:** During an attack, log volume spikes exactly when you need it most; a silently dropping pipeline destroys evidence precisely then.

**Detect:** grep pipeline metrics for `dropped_total`, `rejected_batches`, `buffer_full`, agent `out_queue` depth; verify alerts on sustained drops > 0.

**References:** NIST SP 800-92, Vector/Fluent Bit drop metrics, Google SRE Workbook, CWE-770

# Log Rotation

**MUST** configure rotation and retention for every log file a process writes on a host or VM (in containers, rotate at the node or collector instead, never in-pod) so disks never fill and evidence survives long enough to investigate.

**Why:** Unrotated logs fill the volume and crash the service, while over-short retention erases the audit trail mid-incident.

**Detect:** check logrotate configs, `maxSize`/`maxBackups` in winston/pino, `--log-opt max-size` in compose, or absent rotation on file appenders.

**References:** NIST SP 800-92, CWE-400, CIS Docker 2.4

# Logs as Event Streams

**SHOULD** write the log stream unbuffered to stdout/stderr and leave routing, aggregation, and retention to the execution environment; **SHOULD NOT** write or manage logfiles from inside a container.

**Why:** App-managed logfiles inside containers silently fill ephemeral storage (triggering node eviction), lose evidence on restart (breaking incident forensics), and bypass the centralized pipeline where PII-scrubbing and retention policy live.

**Detect:** log file paths or rotating file handlers in app config inside containerized deploys; missing stdout logger configuration; container logs empty despite active logging code.

**References:** 12factor.net/logs, OWASP Logging Cheat Sheet, Kubernetes logging best practices

# Management-Plane Activity Alerting

**MUST** route cloud control-plane audit streams (CloudTrail, Azure Activity Log, GCP Cloud Audit Logs) into real-time metric filters and alarms so privileged API activity — root/console usage, security-group and firewall changes, IAM policy modifications, key deletion — pages a human within minutes instead of waiting for a periodic log review.

**Why:** Audit logs that only get read quarterly turn a live intrusion into a post-mortem; attackers mutate security groups and IAM grants in hours, and the provider's control-plane API leaves no trace in workload telemetry. Alerting is the difference between catching a stolen-credential session mid-flight and discovering it next quarter.

**Detect:** CloudTrail configured with CloudWatch metric filters + alarms (or equivalent GuardDuty/Activity Log alert rules) covering: root account usage, `AuthorizeSecurityGroupIngress` widening, `iam:Put*Policy`/`Attach*Policy`, console login failures burst, KMS key scheduling-for-deletion; absence of any alarm wired to the audit stream is the finding. Distinguish from `admin-activity-review` (periodic human review) — this item requires automated real-time alerting.

**References:** CIS AWS 3.x (CloudTrail processing & alerting), AWS CloudTrail best practices, Azure Activity Log alert guidance, aquasecurity/trivy-checks AWS CloudTrail alert rules

# Masquerading & Homoglyph Detection

**SHOULD** detect lookalike process, service, and domain names built from homoglyphs or misspellings of trusted names (e.g. `crond` vs `cron`, `paypa1`).

**Why:** Attackers routinely disguise malware as legitimate binaries; name-similarity checks catch spoofing that hash allowlists miss entirely.

**Detect:** grep EDR/SIEM rules for homoglyph normalization, Levenshtein distance checks against known-good process lists, and lookalike domain monitoring.

**References:** MITRE ATT&CK T1036 Masquerading, T1036.008, CWE-456, Unicode homoglyphs (Trojan Source)

# Metrics Cardinality

**MUST NOT** label metrics with unbounded values like user IDs, emails, session tokens, or raw URLs.

**Why:** High-cardinality labels explode the time-series database, and attacker-crafted unique values can weaponize this into a denial-of-service against monitoring itself.

**Detect:** grep metric definitions for labels like `user=`, `email=`, `url=`, `path=` with raw request data; review Prometheus `label_replace` and histogram bucket counts.

**References:** Prometheus cardinality guidance, CWE-400

# Object-Level Data Access Logging

**SHOULD** enable data-plane (object/bucket-level) read and write logging on object storage holding sensitive data, not just control-plane API logging — management-plane logs record who created the bucket, but never who read the objects inside it.

**Why:** Object stores default to control-plane-only logging; a bulk exfiltration of customer records via thousands of `GetObject` calls is invisible until data-plane logging is turned on — after the incident. Compliance regimes (PCI, HIPAA, GDPR access-record duties) and forensic timelines both hinge on per-object access records that control-plane logs simply do not contain.

**Detect:** S3 server access logging or CloudTrail data events (`ReadOnly`/`WriteOnly` for the bucket prefix) enabled; GCS bucket audit configuration with `DATA_READ`/`DATA_WRITE` enabled; Azure Storage diagnostic settings including Read/Write/DELETE operations. Flag buckets with lifecycle policies but no data-event logging, and flag logging enabled only at management-event scope.

**References:** AWS S3 data events / server access logging docs, GCP Cloud Storage audit logging, Azure Storage diagnostics, CIS AWS 3.x (logging), aquasecurity/trivy-checks storage logging rules

# Off-Box Log Shipping

**MUST** ship logs to a logically separate system in near real time so a compromised host cannot erase the record of its own activity.

**Why:** Local logs are the first artifact an intruder edits, and forensic value depends on the record already existing outside the blast radius.

**Detect:** grep for local-only logging (`FileHandler`, a `/var/log` volume, no forwarder sidecar) on services that emit security events.

**References:** OWASP ASVS v5.0 V16.4.3, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md, NIST SP 800-92

# OpenTelemetry

**SHOULD** standardize instrumentation on OpenTelemetry SDKs and the OTLP protocol instead of one-off vendor agents.

**Why:** Fragmented telemetry leaves blind spots when vendors change pricing or an incident spans systems the ad-hoc agents never covered.

**Detect:** grep for `opentelemetry-sdk`, `otlp`, `OTEL_EXPORTER_` env vars; flag services with no instrumentation or single-vendor-only agents.

**References:** OpenTelemetry spec, OWASP Logging Cheat Sheet, NIST SP 800-137

# p99 Latency

**SHOULD** track and alert on p99 (not just average) latency for critical endpoints and dependency calls.

**Why:** Averages hide tail latency; slow-response attacks like zip bombs, regex bombs, and resource exhaustion show up first in the p99 tail while means look healthy.

**Detect:** grep dashboards/alerts for `histogram_quantile(0.99` or `p99`; flag services whose SLOs use only mean/median latency.

**References:** Google SRE Workbook SLI chapter, CWE-400, NIST SP 800-207 zero-trust monitoring

# PII & Secrets Leakage into Application Logs

**MUST** redact passwords, tokens, API keys, and PII at the logging layer before anything reaches disk or an aggregator.

**Why:** Logs are widely readable and long-retained, making them the easiest place for attackers — and auditors — to harvest credentials and personal data; unredacted request bodies, headers, and stack traces spread PII into traces and error-reporters as secondary sinks.

**Detect:** Grep logs and appenders for `password`, `authorization`, `id_card`, `redact`, `mask`; grep for `log.*request`, `log.*body`, `console.log(err)` without redaction and missing `redact_fields`/`mask_pii` filter config. Test by logging a known secret and checking it never appears in logs, traces, or error-reporter payloads.

**References:** OWASP Logging Cheat Sheet, CWE-532, CWE-200, PCI DSS 3.2.1 Req 3, GDPR Art. 5(1)(c), NIST SP 800-92

# Portable Detection Rules

**MUST** author detection logic in a vendor-neutral, machine-readable rule format that compiles to each backend's query dialect, keeping native queries out of the source of truth.

**Why:** Detection knowledge locked in one query dialect cannot be peer-reviewed, tested elsewhere, or migrated without rewriting the entire detection program.

**Detect:** grep rule files for native query syntax (index=, sourcetype=, EventID) where a neutral schema (logsource, detection, selection) is expected

**References:** Sigma, https://github.com/SigmaHQ/sigma, Agent Threat Rules, https://github.com/Agent-Threat-Rule/agent-threat-rules

# Profiling

**MAY** run continuous CPU/heap profiling in production at low overhead to catch performance anomalies early.

**Why:** Profilers expose hot paths where resource-exhaustion attacks (ReDoS, decompression bombs) concentrate, but only if capture is already running when the incident hits.

**Detect:** grep for `py-spy`, `pprof`, `async-profiler`, `continuous profiling` in deployment manifests; verify overhead budget documented.

**References:** Google SRE Book Ch.6 monitoring, CWE-400, Datadog continuous profiling docs

# Queue Depth and Consumer Lag Alerting

**MUST** page on queue depth and consumer lag thresholds so stalled processing is caught before data is lost or SLAs break.

**Why:** A stalled consumer (often from a poison message or credential expiry) silently accumulates backlog until the broker fills and producers block or messages drop.

**Detect:** grep alert rules for `rabbitmq_queue_messages_ready`, `kafka_consumergroup_lag`, `sqs ApproxAgeOfOldestMessage`; flag queues with no lag alert.

**References:** AWS SQS monitoring guide, RED/USE method, CWE-770, Google SRE Workbook

# Rejected Input Logging

**SHOULD** log server-side-only security anomalies: rejected out-of-range values, attempts to change non-modifiable fields, and access-control denials.

**Why:** These events are invisible to the client and are the earliest signal of tampering, enumeration, or a broken authorization rule. Without them an attack looks like ordinary traffic.

**Detect:** grep validation and authorization middleware for log calls on rejection paths; flag handlers that return an error without recording principal, route, and rejected value.

**References:** OWASP Proactive Controls C9 (implement logging), https://github.com/OWASP/www-project-proactive-controls, OWASP Logging Cheat Sheet

# Runtime Threat Detection (Falco/eBPF-style workload anomaly detection)

**MUST** monitor running workloads at syscall level (Falco/eBPF) for anomalies: shells in containers, unexpected writes, suspicious spawns.

**Why:** Scanners only see what you built; attackers operate in what's running, unnoticed inside otherwise "secure" images.

**Detect:** grep `falco`, `tracee`, `tetragon`, `ebpf` in DaemonSets/deployment YAML, custom `falco_rules.yaml` files.

**References:** MITRE ATT&CK container matrix T1610, CIS Docker/K8s Benchmarks 5.x, NIST SP 800-190

# SARIF-Standardized Scan Results (unified alert pipeline)

**SHOULD** emit all scanner findings in SARIF and ingest them into one dashboard, because scattered formats hide coverage gaps and duplicate triage.

**Why:** Findings in per-tool logs go unseen; a unified pipeline makes severity trends and deduplication auditable.

**Detect:** Scanners run without `--format sarif` / `output: sarif`; no upload step to code-scanning API; each tool reporting to a separate ad-hoc log file.

**References:** NIST SP 800-218 (SSDF), SARIF spec (OASIS), GitHub code scanning SARIF upload docs

# Security Telemetry Access Control

**MUST** restrict security telemetry, network maps, and policy exports to dedicated administrator accounts, since they describe where the valuable assets are.

**Why:** The map of the defences is reconnaissance: policy stores reveal which accounts are worth compromising and monitoring data reveals what is watched.

**Detect:** kubectl auth can-i --list -n monitoring --as=<subject>; compare with the admin-only group that should be the sole reader.

**References:** NIST SP 800-207 §5.5, https://doi.org/10.6028/NIST.SP.800-207, NIST SP 800-53 AC-6

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

# Stable Rule Identifiers

**MUST** give every detection rule an immutable identifier under a versioned rule schema, keeping severity, category, and owner in separate mutable metadata fields.

**Why:** Rules are cited by incident reports and dashboards, so reassigned or meaning-laden identifiers break references and turn wrong the moment classification changes.

**Detect:** grep -h '^id:' rules/*.yml | sort | uniq -d  (duplicate or reassigned IDs), plus a schema-version field in each rule header

**References:** Agent Threat Rules, https://github.com/Agent-Threat-Rule/agent-threat-rules

# Structured Logging

**MUST** emit application logs as structured JSON with consistent field names (timestamp, level, event, actor, request_id) rather than free-form text.

**Why:** Unstructured logs defeat automated search and correlation, so attackers' actions hide in noise during incident response.

**Detect:** grep for `console.log(` / `print(` in request handlers; check for logging config with `format: json` or structlog/pino/loguru setup.

**References:** OWASP Logging Cheat Sheet, CWE-1118, NIST SP 800-92

# Synthetic External Monitoring

**SHOULD** run synthetic probes from outside the network perimeter to catch outages, TLS problems, and defacement invisible to internal monitoring.

**Why:** Internal checks pass while the public-facing service is down or serving tampered content — the exact failure mode customers experience first.

**Detect:** grep for synthetic checkers (Pingdom, Grafana Synthetic Monitoring, CloudWatch Synthetics) hitting public URLs with content/TLS assertions, not just TCP pings.

**References:** Google SRE Book Ch.6, OWASP Testing Guide 4.0, CWE-295

# Threat Hunting Practice

**SHOULD** run scheduled, hypothesis-driven hunts over retained telemetry instead of waiting for alerts to fire.

**Why:** Sophisticated intruders operate below alert thresholds for weeks; only proactive searching surfaces the anomalies no rule was written for.

**Detect:** verify a documented hunt cadence, saved hunt queries (KQL/SPL/Lucene) in the SIEM, and hunt findings tracked; flag SIEM used only for alert triage.

**References:** MITRE ATT&CK D3FEND hunt guidance, NIST SP 800-150, SANS threat hunting process

