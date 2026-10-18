---
categories: [deployment-release]
domains: [infrastructure]
---

# Feature Flags

**MUST NOT** use feature flags as a substitute for access control; authorization checks belong server-side regardless of a flag's state.

**Why:** Toggling a flag off in the UI while the endpoint stays routable exposes unfinished, unauthenticated functionality to anyone who knows the URL.

**Detect:** grep flag SDK calls (`isEnabled(`, `flipper`, `launchdarkly`) wrapped around UI only while routes lack auth middleware; flags defaulting `true` in prod config.

**References:** OWASP ASVS 4.1 access control, CWE-862 missing authorization, Unleash/LaunchDarkly security guidance
