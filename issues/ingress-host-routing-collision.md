# Ingress Host-Header / vHost Routing Collisions and TLS Passthrough Misrouting

**MUST** define explicit host matching on every Ingress rule and a catch-all default backend that returns 404/421, so an unexpected `Host` header cannot route traffic to the wrong service.

**Why:** When rules overlap or a controller falls back to its default vhost, a request aimed at `admin.example.com` can land on an unrelated backend that processes it as if trusted — and TLS passthrough makes the mismatch invisible because the outer SNI never gets re-checked inside.

**Detect:** Look for Ingress resources with empty `host:` (matches everything), duplicate hosts across namespaces, `nginx.ingress.kubernetes.io/ssl-passthrough` on shared ports without per-SNI routing, and controllers configured with a permissive default backend. Test by sending crafted `Host:` headers to the LB IP and observing which service answers.

**Bad:**
```yaml
- http:
    paths:
      - path: /            # no host: matches ANY hostname
        backend: {serviceName: payments, servicePort: 443}
```

**Good:**
```yaml
- host: payments.example.com
  http:
    paths:
      - path: /
        pathType: Prefix
        backend: {serviceName: payments, servicePort: 443}
```

**References:** CWE-441, RFC 9110 §7.2 (Host), Kubernetes Ingress docs, OWASP A01:2021

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
