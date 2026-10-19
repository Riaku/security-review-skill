# scaling-capacity

Scaling behavior and capacity limits.

## What this category covers

This category covers how a system behaves as load grows and where its hard limits sit. Member items span capacity forecasting against peak, load testing with realistic traffic, horizontal and vertical scaling choices, autoscaling policy and ceilings, cold-start bounds, and worker-pool sizing. They also cover resource exhaustion — memory leaks, OOM behavior, disk and inode growth, quadratic work on unbounded input, storage IOPS ceilings, and replication retention filling a volume — plus tenant-level isolation and metered-spend limits. A reviewer should expect findings about a limit discovered at launch, an autoscaler that reacts to the wrong signal, or one workload that consumes capacity shared with everyone else.

- Forecasting: peak-load capacity planning and non-functional requirement traceability.
- Scaling mechanics: horizontal versus vertical, autoscaling signals and ceilings, and worker pools.
- Startup and runtime cost: cold starts, garbage collection, and memory-leak detection.
- Resource ceilings: OOM behavior, disk and inode growth, storage IOPS, and WAL retention.
- Efficiency hazards: quadratic work on unbounded input and latency-versus-throughput tradeoffs.
- Isolation and spend: per-tenant quotas, noisy-neighbor limits, and metered token budgets.

## What it does not cover

- [resilience](../categories/resilience.md) — behavior under dependency failure belongs there, not steady-state growth.
- [containers-k8s](../categories/containers-k8s.md) — the request, limit, and quota mechanics themselves belong there.
- [database](../categories/database.md) — query plans, indexing, and engine tuning belong there.

## What a finding here looks like

- Capacity is planned against average load, with no headroom for a known peak.
- An autoscaler scales on a signal that is cheap to inflate and has no maximum replica ceiling.
- A long-running service has no heap-trend monitoring, so a slow leak ends in an OOM kill at peak.
- A request path nests loops over two externally sized collections, so one payload saturates CPU.
- A storage volume is sized without benchmarking its IOPS ceiling, and saturates on launch day.
