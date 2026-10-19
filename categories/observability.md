# observability

Logs, metrics, traces, profiling, alerting.

## What this category covers

This category covers the telemetry a system emits and the detection built on it: what gets recorded, whether it can be trusted and joined, and whether anyone is paged when it matters. Member items span structured logging and redaction, metrics and cardinality, distributed tracing and correlation, profiling, error tracking, and the alerting rules and routing behind them. They also cover the security-detection layer — audit trails, control-plane and data-plane access logging, beaconing, credential access, lateral movement, and threat hunting — and the health of the pipeline itself. A reviewer should expect findings about events that are missing, mutable, unattributable, or buried in noise.

- Logging: structure, levels, rotation, injection, and PII or secret redaction.
- Metrics: cardinality, latency percentiles, queue depth, and saturation forecasts.
- Tracing and profiling: context propagation, correlation IDs, flame graphs, and continuous profiling.
- Alerting: routing, fatigue, dead-man's-switch heartbeats, and job-age objectives.
- Security detection: audit trails, object-level access logs, control-plane activity, and behavioral anomalies.
- Pipeline integrity: backpressure and drop rate, plus unified SARIF ingest.

## What it does not cover

- [sre-incidents](../categories/sre-incidents.md) — on-call rotation, incident command, runbooks, and postmortems belong there; this category is the telemetry and the alert.
- [resilience](../categories/resilience.md) — the fault-tolerance behavior being measured belongs there.
- [security-practices](../categories/security-practices.md) — program-level practice such as threat modeling, disclosure, and patching belongs there.

## What a finding here looks like

- A log line records a token, password, session id, or PII field before redaction runs.
- A metric is labeled with user id, email, session token, or raw URL, so cardinality grows without bound.
- An audit-relevant event is collected but never reviewed or alerted, or is written to mutable storage.
- A scheduled job that stops running produces no alert because only failures are monitored, not absence.
- A p99 regression or queue backlog is invisible because dashboards track averages and counts.
