---
categories: [deployment-release]
domains: [infrastructure]
---

# Dev Endpoints in Shipped Artifacts

**MUST NOT** ship release artifacts containing debug endpoints, internal hostnames, private IP addresses, or test-only administrative screens.

**Why:** Anyone who unpacks the artifact can read those strings and reach internal infrastructure the release was never meant to expose.

**Detect:** strings on the release binary or package, then grep for RFC1918 addresses, .internal hostnames, and /debug paths

**References:** Google android-security-lints, https://github.com/google/android-security-lints
