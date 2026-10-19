---
categories: [cloud-network, database, hardening-benchmarks]
domains: [data, government-compliance, infrastructure]
---

# Unauthenticated data stores exposed (Redis, Elasticsearch, MongoDB, Memcached)

**MUST** require authentication on every datastore engine and bind its listener only to the interfaces that need it (Redis `requirepass`/ACLs, MongoDB `authorization: enabled`, Elasticsearch `xpack.security.enabled`), so that reaching the port is not sufficient to read or write data.

**Why:** These engines shipped with auth off by default, and scanned-and-looted instances appear daily: Redis dumps of sessions, Elasticsearch clusters of leaked PII. An unauthenticated store on a reachable network is a breach with a countdown timer.

**Detect:** `bind`/`bind_ip` set to `0.0.0.0`; Redis without `requirepass` or ACL users, MongoDB started without `--auth` or `security.authorization: enabled`, Elasticsearch without `xpack.security.enabled`; daemons listening on a public interface.

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

**References:** CWE-306 Missing Authentication for Critical Function, OWASP A07:2021, Redis security docs, Shodan exposed-database research
