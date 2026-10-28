---
categories: [database, sre-incidents]
domains: [data, reliability]
---

# Destructive Operation Targeting

**MUST** verify a target system's live role — primary or replica, production or non-production — before running any destructive or failover operation.

**Why:** Hostnames, runbooks, and habit drift out of date, and a restore or failover aimed at the wrong node destroys the copy you were relying on. The live system is the only authority on its own role.

**Detect:** command: `SELECT pg_is_in_recovery()` / `@@read_only` / cloud resource tags queried immediately before the operation, with the result recorded in the change log.

**References:** GitLab database outage postmortem, https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/
