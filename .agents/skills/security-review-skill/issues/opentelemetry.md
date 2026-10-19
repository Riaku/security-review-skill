---
categories: [observability]
domains: [reliability]
---

# OpenTelemetry

**SHOULD** standardize instrumentation on OpenTelemetry SDKs and the OTLP protocol instead of one-off vendor agents.

**Why:** Fragmented telemetry leaves blind spots when vendors change pricing or an incident spans systems the ad-hoc agents never covered.

**Detect:** grep for `opentelemetry-sdk`, `otlp`, `OTEL_EXPORTER_` env vars; flag services with no instrumentation or single-vendor-only agents.

**References:** OpenTelemetry spec, OWASP Logging Cheat Sheet, NIST SP 800-137
