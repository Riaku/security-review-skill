---
categories: [distributed-systems]
domains: [data]
---

# Bloom Filters

**MAY** use Bloom filters as a fast pre-check, but MUST NOT treat a positive match as authoritative since false positives are inherent.

**Why:** Trusting a Bloom hit as truth admits items that were never present, bypassing denylists or corrupting existence-based security decisions.

**Detect:** grep for bloom/`guava BloomFilter`/`BitSet` gating authz or dedup without a backing store confirmation on positive, missing `expectedFpp`/`fpp` sizing config.

**References:** Bloom 1970 paper, CWE-364 Signal Error, RedisBloom false-positive docs
