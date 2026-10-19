---
categories: [observability]
domains: [infrastructure]
---

# Gateway Payload Logging

**MUST** disable full request and response payload logging unless redaction and a bounded retention window are enforced.

**Why:** Trace features capture credentials and personal data into log sinks that are far more widely readable than the systems they instrument.

**Detect:** grep gateway and proxy IaC for payload or trace logging enabled (`data_trace_enabled`, `xray_tracing_enabled`, `field_level_logs`, `logging_level: full`) without redaction config.

**References:** Checkov IaC policy catalogue, https://github.com/bridgecrewio/checkov
