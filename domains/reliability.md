# reliability

Runtime behavior under load and failure: resilience, caching, observability, SRE.

## Detection signals

- Retry/timeout/circuit-breaker libraries
- Cache layers (redis, memcached, CDN config)
- Metrics/tracing/logging libraries (prometheus, OTel, structured loggers)
- Health endpoints, probes, autoscaling config

## Stack quick-map

- Any networked service → [resilience](../categories/resilience.md), [observability](../categories/observability.md), [sre-incidents](../categories/sre-incidents.md)
- Cache layer present → [caching](../categories/caching.md)
- Autoscaling/load-sensitive → [scaling-capacity](../categories/scaling-capacity.md)
