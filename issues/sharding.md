---
categories: [database]
domains: [data]
---

# Sharding

**MUST** choose a shard key that distributes write load evenly and keeps transactionally-related rows on the same shard; cross-shard transactions MUST be avoided by design, not discovered in production.

**Why:** A poor shard key creates hot shards that melt while others idle, and splitting related rows forces distributed transactions — where a partial commit leaves balances, inventories, and indexes permanently inconsistent.

**Detect:** Shard key reviewed against access patterns (tenant_id vs user_id vs time); queries that JOIN or transact across shards; resharding plan documented before the first shard ships; per-shard QPS/CPU variance in dashboards.

**Bad:**
```python
shard = hash(user_id) % 8
# transfers lock rows in two users' shards -> 2PC everywhere
```

**Good:**
```python
shard = hash(tenant_id) % 8   # all of a tenant's rows co-located
# cross-tenant work goes through async reconciliation
```

**References:** Vitess sharding guide, Azure sharding/catalog pattern guides, Kleppmann *DDIA* Ch. 6, CWE-662
