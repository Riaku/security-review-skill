---
categories: [authorization-access-control]
domains: [backend]
---

# Least-Frequently-Used Permission Review (periodic entitlement pruning)

**SHOULD** periodically revoke entitlements unused over a defined window (e.g. 90 days), starting with the broadest grants.

**Why:** Unused permissions are pure attack surface: they never help legitimate work yet sit ready for any compromised account.

**Detect:** grep access-review exports for `unused_permissions`, `last_used_timestamp`, IAM Access Advisor reports.

**References:** NIST SP 800-53 AC-2(3), CIS Control 5, AWS IAM Access Advisor

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
