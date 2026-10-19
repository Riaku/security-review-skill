---
categories: [cloud-network, database]
domains: [data, infrastructure]
---

# Exposed Data-Service Ports

**MUST NOT** publish database, cache, search, and daemon ports (Redis 6379, Elasticsearch 9200, MongoDB 27017, Memcached 11211, Docker API 2375, Postgres 5432) outside the trusted network: no public load balancers, no `0.0.0.0/0` rules, no cloud provider public-access toggles.

**Why:** Internet-scanned services (Shodan/Censys) find published Redis, Elasticsearch, and MongoDB ports weekly; a datastore port reachable from the internet is reachable by anyone, ahead of any application-layer control.

**Detect:** scan own external IP range for 6379/9200/27017/11211/2375; grep security groups/firewall rules and Service type=LoadBalancer for data ports; check cloud provider public-access flags on managed datastores.

**References:** MITRE ATT&CK T1190, CIS Docker 2.x, Shodan exposed-database reports
