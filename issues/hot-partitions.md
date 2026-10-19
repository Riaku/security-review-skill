---
categories: [database]
domains: [data]
---

# Hot Partitions

**MUST** distribute write load across partitions or shards so no single partition absorbs a disproportionate share of traffic.

**Why:** A partition keyed on a monotonic value like today's date sends every current write to the single newest partition — same server, same WAL, same buffer pool — saturating that partition's throughput and lock contention while the older ones idle; spreading writes across machines is a separate sharding decision that Postgres partitioning does not make for you.

**Detect:** Look for shard keys built from `CURRENT_DATE`, timestamps, or auto-increment IDs used directly as the partition key; check DDL for `PARTITION BY RANGE (created_at)` with no salting and per-partition write metrics for skew.

**Bad:**
```sql
CREATE TABLE events (
    id bigserial,
    created_at timestamptz,
    payload jsonb
) PARTITION BY RANGE (created_at);
-- every insert today hits one partition
```

**Good:**
```sql
CREATE TABLE events (
    id bigserial,
    user_id bigint,
    created_at timestamptz,
    payload jsonb
) PARTITION BY RANGE (created_at);
-- Postgres allows one strategy per table: range on created_at, then hash each
-- child on user_id so a day's writes spread over N sub-partitions
CREATE TABLE events_2026_10 PARTITION OF events
    FOR VALUES FROM ('2026-10-01') TO ('2026-11-01')
    PARTITION BY HASH (user_id);
```

**References:** AWS Well-Architected hot-partition guidance, Azure Storage partition keys, Cassandra monotonic-key anti-patterns
