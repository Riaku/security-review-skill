---
categories: [deployment-release, secrets-crypto]
domains: [backend, infrastructure]
---

# Plaintext Secrets in Helm values Files and Rendered Manifests

**MUST NOT** commit plaintext secrets in `values.yaml` or render them into manifests; reference ExternalSecret/SealedSecret objects or inject at deploy time instead.

**Why:** Values files and `helm get values` output are readable by anyone with repo or release access, leaking credentials through charts and CI artifacts.

**Detect:** `password:`, `apiKey:`, `token:` literals in `values*.yaml`, `helm get values` output containing credentials, missing `existingSecret` references.

**References:** OWASP ASVS V6.4.1, CWE-312, Helm security best practices, Bitnami `existingSecret` pattern
