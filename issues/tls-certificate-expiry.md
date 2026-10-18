# TLS Certificate Expiry

**MUST** Every TLS certificate serving traffic be renewed automatically before expiry, with alerting firing at least 30 days ahead of the notAfter date.

**Why:** An expired certificate breaks every HTTPS session and trains users to click through warnings; silent renewal failures routinely surface only as a customer-visible outage.

**Detect:** Check dates with `openssl s_client -servername <host> -connect <host>:443`. Flag cert-manager Certificates stuck NotReady, and hardcoded `ssl_certificate` paths in nginx/HAProxy with no renewal hook.

**Bad:**
```yaml
# nginx.conf — hand-issued cert, nobody owns renewal
server {
    listen 443 ssl;
    ssl_certificate /etc/ssl/manual-2024.pem;
}
```

**Good:**
```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
spec:
  secretName: app-tls
  renewBefore: 720h   # 30 days
  issuerRef: { name: letsencrypt-prod }
```

**References:** CWE-298, OWASP A05:2021 Security Misconfiguration, Let's Encrypt renewal docs

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
