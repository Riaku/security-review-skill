---
categories: [messaging-async]
domains: [data]
---

# Distinct consumer group per service on partitioned streams

**MUST** give each independent service its own consumer group on a partitioned message stream; sharing one group between services silently splits the feed, so neither receives every event (Kafka consumer group IDs are the common case).

**Why:** Two services sharing a group each receive a disjoint partition subset, so neither sees the full event feed — silent data loss.

**Detect:** grep configs for duplicated `group.id` values across services, hardcoded shared groups, `group.instance.id` collisions.

**References:** Kafka consumer group docs, CWE-664, OWASP ASVS 6.1
