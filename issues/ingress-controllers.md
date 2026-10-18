# Ingress Controllers

**MUST** Treat the ingress controller as a high-value attack surface: run it least-privileged, patch on the vendor's security cadence, and never expose admin or metrics ports publicly.

**Why:** Ingress controllers parse attacker-controlled headers and hostnames at the edge; annotation-injection CVEs in NGINX Ingress have yielded cluster-admin, so broad RBAC plus a wildcard host turns one bug into total cluster compromise.

**Detect:** Review the controller's ClusterRole for wildcards and secret-read access. Grep Ingress resources for `server-snippet`/`configuration-snippet` annotations accepted from untrusted namespaces; check for `host: "*"` catch-alls and exposed `:10254` metrics.

**Bad:**
```yaml
# any namespace can inject arbitrary nginx config via annotation
metadata:
  annotations:
    "nginx.ingress.kubernetes.io/server-snippet": "..."
```

**Good:**
```yaml
# controller args: snippets disabled, annotation allowlist enforced,
# --watch-namespace scoped, metrics cluster-internal only
```

**References:** CVE-2021-25742, OWASP A03:2021 Injection, Kubernetes ingress security docs

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
