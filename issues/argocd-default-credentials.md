# ArgoCD-Specific: Default Admin Password, JWT Signing Key, Webhook Auth

**MUST** replace ArgoCD's default `admin` password, set a unique `server.signingkey`, and authenticate all webhook receivers before exposing the API.

**Why:** ArgoCD ships with a known default admin and auto-generated signing key; an attacker who reaches the UI or webhook endpoint gains cluster-wide deploy control.

**Detect:** check `argocd-secret` for unchanged `admin.password`, default `server.signingkey`, webhook receivers without `secret`/HMAC verification, `admin.enabled: true` in values.

**References:** ArgoCD Security Guide, CWE-1188, CVE-2023-22482, OWASP A05:2021

---

**Part of:** [authentication](../categories/authentication.md) · [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [deployment-release](../categories/deployment-release.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
