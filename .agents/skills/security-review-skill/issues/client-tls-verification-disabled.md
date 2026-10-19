---
categories: [cloud-network, secrets-crypto]
domains: [backend, infrastructure]
---

# Client-Side TLS Verification Disabled

**MUST NOT** disable server certificate or hostname verification in outbound TLS clients; every "works in dev" toggle like `verify=False` is a production man-in-the-middle hole.

**Why:** Skipping verification lets any attacker on the network path impersonate the remote service and capture credentials, tokens, or sensitive payloads that the app believes are encrypted.

**Detect:** Grep for `verify=False`, `verify: false`, `-k`/`--insecure` in curl invocations, `rejectUnauthorized: false`, `NODE_TLS_REJECT_UNAUTHORIZED=0`, custom `X509TrustManager` that returns without checking, `ssl._create_unverified_context`, `InsecureSkipVerify: true` in Go, and trust-all `HostnameVerifier` classes.

**Bad:**
```python
import requests
resp = requests.post("https://api.internal.example/token", json=payload, verify=False)
```

**Good:**
```python
import requests
resp = requests.post("https://api.internal.example/token", json=payload,
                     verify="/etc/ssl/corp-ca-bundle.pem")
```

**References:** CWE-295, CWE-299, OWASP ASVS V9.2.1, OWASP WSTG-CRYP-01
