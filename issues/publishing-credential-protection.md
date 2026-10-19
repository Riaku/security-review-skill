---
categories: [supply-chain]
domains: [infrastructure]
---

# Publishing Credential Protection

**MUST** keep package-publishing tokens and release signing keys in a protected, short-lived publishing environment, never as long-lived repository secrets.

**Why:** An attacker who can publish as you never needs to breach your build: long-lived publish tokens are the usual entry point, and a forged release reaches every consumer through the channel they already trust.

**Detect:** grep CI and repository config for `NPM_TOKEN`, `TWINE_PASSWORD`, `CARGO_REGISTRY_TOKEN`, and long-lived registry tokens; check that publishing runs from a protected environment with short-lived or trusted-publisher credentials.

**References:** SLSA v1.0 requirements, https://slsa.dev/spec/v1.0/requirements, NIST SP 800-218 (SSDF) PS.2
