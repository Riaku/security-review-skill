---
categories: [authentication, cicd-pipeline-security, deployment-release]
domains: [backend, infrastructure]
---

# Default admin password, signing key and webhook auth on control planes

**MUST** replace a product's shipped default administrative password, set a unique token-signing key, and authenticate every webhook receiver before exposing a self-hosted control plane; ArgoCD's `admin` password and auto-generated `server.secretkey` are the canonical example (CWE-1188).

**Why:** ArgoCD ships with a known default admin and auto-generated signing key; an attacker who reaches the UI or webhook endpoint gains cluster-wide deploy control.

**Detect:** check `argocd-secret` for unchanged `admin.password`, default `server.secretkey`, webhook receivers without `secret`/HMAC verification, `admin.enabled: true` in values.

**References:** ArgoCD Security Guide, CWE-1188, OWASP A05:2021
