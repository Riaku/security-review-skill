---
categories: [scaling-capacity]
domains: [reliability]
---

# Latency vs Throughput

**MUST** define separate SLOs for latency (p95/p99) and throughput, and scale on the metric that breaches first rather than a single aggregate.

**Why:** Optimizing only average throughput hides tail-latency spikes that time out clients and cascade into retry storms during peak load.

**Detect:** grep for `p99`, `histogram_quantile`, `latency_slo`, `throughput_slo` in dashboards and alert rules; absence of percentile thresholds in prometheus rules or load-test reports.

**References:** Google SRE Book SLO chapter, CWE-400, NIST SP 800-184
