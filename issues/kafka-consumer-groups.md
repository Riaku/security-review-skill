# Kafka Consumer Groups

**MUST** assign each application a distinct consumer group ID; sharing one group between services silently splits the message stream.

**Why:** Two services sharing a group each receive a disjoint partition subset, so neither sees the full event feed — silent data loss.

**Detect:** grep configs for duplicated `group.id` values across services, hardcoded shared groups, `group.instance.id` collisions.

**References:** Kafka consumer group docs, CWE-664, OWASP ASVS 6.1
