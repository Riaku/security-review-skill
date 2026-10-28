# reliability

Runtime behavior under load and failure: resilience, caching, observability, SRE.

## Detection signals

- Retry/timeout/circuit-breaker libraries
- Cache layers (redis, memcached, CDN config)
- Metrics/tracing/logging libraries (prometheus, OTel, structured loggers)
- Health endpoints, probes, autoscaling config
- Any deployable service (Dockerfile, deploy manifest, server entrypoint) — this
  domain reviews missing telemetry and resilience, so the absence of retry or
  metrics libraries is a reason to include it, not to skip it

## Stack quick-map

- Any networked service → resilience, observability, sre-incidents
- Deploy manifest or Dockerfile present → deployment-release, containers-k8s
- Cache layer present → caching
- Autoscaling/load-sensitive → scaling-capacity
