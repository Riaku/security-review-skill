---
categories: [mobile]
domains: [mobile]
---

# Minimum Client Version

**SHOULD** enforce a minimum supported client version server-side and block older clients from sensitive operations instead of trusting them to update.

**Why:** A shipped client that cannot be forced forward is a permanent foothold for every vulnerability fixed after its release.

**Detect:** grep request middleware for a minimum-version or X-Client-Version comparison that returns an upgrade-required status

**References:** OWASP MASVS v2 (Resilience, update enforcement)
