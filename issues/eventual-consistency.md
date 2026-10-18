# Eventual Consistency

**SHOULD NOT** use eventually consistent reads for authorization, balance, or inventory decisions that gate money or access.

**Why:** A stale replica read lets a revoked user act or oversell stock during the replication lag window, an exploitable race.

**Detect:** grep for authz/balance queries hitting read replicas, `read_from=secondary`, replication-lag unchecked before decision logic, missing `session=` sticky reads.

**References:** OWASP A01 Broken Access Control, CWE-367 TOCTOU, NIST SP 800-162
