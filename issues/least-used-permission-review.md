# Least-Frequently-Used Permission Review (periodic entitlement pruning)

**MAY** begin with quick wins, but SHOULD periodically revoke entitlements unused over a defined window (e.g. 90 days).

**Why:** Unused permissions are pure attack surface: they never help legitimate work yet sit ready for any compromised account.

**Detect:** grep access-review exports for `unused_permissions`, `last_used_timestamp`, IAM Access Advisor / GCP unused-service reports, entitlement-review jobs.

**References:** NIST SP 800-53 AC-2(3), CIS Control 5, AWS IAM Access Advisor, ISO 27001 A.5.18 review cadence
