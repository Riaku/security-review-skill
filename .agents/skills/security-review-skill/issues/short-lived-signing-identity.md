---
categories: [supply-chain]
domains: [infrastructure]
---

# Short-Lived Signing Identity

**MUST** sign artifacts with short-lived credentials bound to a verified workload identity rather than long-lived static keys.

**Why:** A static signing key is a permanent impersonation token: whoever steals it signs as you forever. Minutes-scale certificates leave almost no window.

**Detect:** Keyless `cosign sign` with an OIDC-issued Fulcio certificate; flag long-lived `cosign.key` or GPG keys held in CI secrets.

**References:** Sigstore Fulcio, https://github.com/sigstore/fulcio
