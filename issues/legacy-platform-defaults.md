---
categories: [mobile]
domains: [mobile]
---

# Legacy Platform Security Defaults

**MUST** set security-relevant platform defaults explicitly when supporting older runtime versions, rather than inheriting the weaker defaults those versions shipped with.

**Why:** A default that is safe on the current platform silently permits cleartext traffic, user-added CAs, or broad storage access on older versions still in the support matrix.

**Detect:** grep the manifest and build config for cleartext traffic, trust-anchor, and external-storage settings against minSdk

**References:** Google android-security-lints, https://github.com/google/android-security-lints
