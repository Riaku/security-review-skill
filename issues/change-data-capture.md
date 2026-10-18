# Change Data Capture

**MUST** authenticate and encrypt every CDC connector stream (debezium, binlog, WAL slot) with least-privilege read-only database credentials.

**Why:** Unprotected replication feeds expose entire database contents, including PII, to anyone who can reach the connector port.

**Detect:** grep debezium.properties / connector JSON for `snapshot.mode=never` absent, `sslmode=disable`, hardcoded `database.password`, exposed ports 8081/5432 without TLS.

**References:** OWASP A02 Cryptographic Failures, CWE-319, OWASP Data Validation Cheat Sheet
