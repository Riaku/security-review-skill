# Partition Keys

**SHOULD** choose partition keys with high cardinality and even distribution; low-cardinality or null keys hot-spot a single partition.

**Why:** A skewed key (e.g. tenant ID of one giant customer) overloads one broker and consumer while others idle, degrading throughput and latency SLOs.

**Detect:** grep producer code for `key=`, `partition_key`, constant or nullable keys; check broker metrics for per-partition byte imbalance.

**References:** Kafka partitioning docs, CWE-400, NIST SP 800-53 SC-5
