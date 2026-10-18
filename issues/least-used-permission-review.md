# Least-Frequently-Used Permission Review (periodic entitlement pruning)

**MAY** start with quick wins, but SHOULD run periodic reviews that revoke permissions nobody has used in a defined window (e.g. 90 days).

**Why:** Unused entitlements are pure attack surface: they never help legitimate work yet sit ready for any account that gets compromised.

**Detect:** grep access-review exports: `unused_permissions`, `last_used_timestamp`, IAM Access Advisor / GCP Policy Intelligence unused reports, entitlement-review job configs.

**References:** NIST SP 800-53 AC-2(3) (periodic review), CIS Control 5, AWS IAM Access Advisor, SOX/ISO 27001 A.5.18 review cadence
