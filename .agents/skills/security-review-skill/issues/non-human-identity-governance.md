---
categories: [authentication, authorization-access-control]
domains: [backend]
---

# Non-Human Identity Governance (service accounts, machine creds inventoried and scoped)

**MUST** inventory every service account, API key, and machine credential with an owner, least-privilege scope, and expiry.

**Why:** Machine identities outnumber humans 50:1 and are rarely reviewed; orphaned service accounts become attackers' favorite door.

**Detect:** grep `service_account`, `api_key`, `client_secret` inventories, orphaned-credential reports, workload-identity configs.

**References:** NIST SP 800-63B, CIS Control 6, OWASP Non-Human Identities Top 10, CSA NHI guidance
