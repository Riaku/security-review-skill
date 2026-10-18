---
categories: [cloud-network, database]
domains: [data, infrastructure]
---

# Exposed Data-Service Ports

**MUST NOT** expose database, cache, search, and daemon ports (Redis 6379, Elasticsearch 9200, MongoDB 27017, Memcached 11211, Docker API 2375, Postgres 5432) beyond the trusted network without authentication and TLS.

**Why:** Internet-scanned services (Shodan/Censys) find unauthenticated Redis/Elasticsearch weekly — no creds needed to read or wipe the dataset.

**Detect:** scan own external IP range for 6379/9200/27017/11211/2375; grep security groups/firewall rules and Service type=LoadBalancer for data ports; check `bind`/`requirepass`/`xpack.security` settings.

**References:** MITRE ATT&CK T1190, CIS Docker 2.x, Shodan exposed-database reports
