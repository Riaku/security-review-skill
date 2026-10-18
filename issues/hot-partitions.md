---
categories: [database]
domains: [data]
---

# Hot Partitions

**MUST** distribute write load across partitions or shards so no single partition absorbs a disproportionate share of traffic.

**Why:** A partition keyed on a monotonic value like today's date concentrates all current writes on one node, throttling throughput and amplifying the blast radius of a single-node failure while the rest of the cluster idles.

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
    shard smallint,
    created_at timestamptz,
    payload jsonb
) PARTITION BY HASH (shard), RANGE (created_at);
-- shard = hash(user_id) % N spreads writes
```

**References:** AWS Well-Architected hot-partition guidance, Azure Storage partition keys, Cassandra monotonic-key anti-patterns
