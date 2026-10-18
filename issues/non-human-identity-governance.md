# Non-Human Identity Governance (service accounts, machine creds inventoried and scoped)

**MUST** inventory every service account, API key, and machine credential, assign an owner, and scope each to least privilege with expiry.

**Why:** Machine identities typically outnumber humans 50:1 and are rarely reviewed — orphaned service accounts become the attacker's favorite door.

**Detect:** grep for `service_account`, `api_key`, `client_secret` inventories, IAM user-vs-role audits, Vault identity listings, `orphaned_credentials` reports, workload-identity configs.

**References:** NIST SP 800-63B, CIS Control 6, OWASP Non-Human Identities Top 10, Cloud Security Alliance NHI guidance
