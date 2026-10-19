---
categories: [resilience]
domains: [reliability]
---

# Graceful Degradation

**SHOULD** define a fallback per dependency so optional features shed instead of failing the whole request when a non-critical service is down.

**Why:** One optional enrichment service erroring should cost features, not the whole request.

**Detect:** grep `fallback`, `default_value`, cached-response fallbacks, per-dependency feature flags.

**References:** Netflix fallback patterns, Google SRE Book graceful degradation
