---
categories: [distributed-systems]
domains: [data]
---

# Bloom Filters

**MAY** use Bloom filters as a fast pre-check, but MUST NOT treat a positive match as authoritative since false positives are inherent.

**Why:** A Bloom hit means "maybe present": treating it as truth over-blocks denylisted lookups and silently admits never-seen items in allowlist or dedup checks. Only a negative is definitive (`BF.EXISTS` returns 1 for "may exist", 0 for "definitely does not exist"), so positives must be confirmed against the backing store.

**Detect:** grep for bloom/`guava BloomFilter`/`BitSet` gating authz or dedup without a backing store confirmation on positive, missing `expectedInsertions`/`fpp` (Guava) or `ERROR`/`CAPACITY` (RedisBloom) sizing.

**References:** Bloom 1970 paper, RedisBloom false-positive docs
