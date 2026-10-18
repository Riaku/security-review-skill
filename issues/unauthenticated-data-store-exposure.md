# Unauthenticated data stores exposed (Redis, Elasticsearch, MongoDB, Memcached)

**MUST NOT** expose any datastore port (Redis, Elasticsearch, MongoDB, Memcached, etcd) to a network where untrusted clients can reach it without authentication and network-level restriction.

**Why:** These engines shipped with auth off by default, and scanned-and-looted instances appear daily: Redis dumps of sessions, Elasticsearch clusters of leaked PII. An unauthenticated store on a reachable network is a breach with a countdown timer.

**Detect:** Scan inventories for default ports (6379, 9200, 27017, 11211) bound to `0.0.0.0`; check Redis `requirepass`/ACLs, MongoDB auth, Elasticsearch `xpack.security.enabled`, and security groups opening them beyond the app tier.

**Bad:**
```yaml
kind: Service
spec:
  type: LoadBalancer        # redis straight to the internet
  ports: [{ port: 6379 }]
```

**Good:**
```yaml
spec:
  type: ClusterIP   # plus requirepass and a NetworkPolicy
---
# NetworkPolicy: apps namespace -> redis:6379 only
```

**References:** CWE-306 Missing Authentication for Critical Function, OWASP A02, Redis security docs, Shodan exposed-database research

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [database](../categories/database.md) · [hardening-benchmarks](../categories/hardening-benchmarks.md) · [data](../domains/data.md) · [infrastructure](../domains/infrastructure.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)
