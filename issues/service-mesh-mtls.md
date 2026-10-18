# Service Mesh / Service-to-Service mTLS (identity for internal traffic)

**SHOULD** enforce mutual TLS between internal services so east-west traffic is authenticated and encrypted, not trusted by network location alone.

**Why:** Flat internal networks let an attacker who breaches one service impersonate any other and sniff credentials in cleartext.

**Detect:** grep mesh configs: `mtls.mode: STRICT`, `PeerAuthentication`, `apiVersion: security.istio.io`, `tls: mode: ENABLE` in Linkerd/Consul configs, mesh policy manifests.

**References:** NIST SP 800-207 Zero Trust, Istio mTLS docs, CIS Kubernetes Benchmark 5.x, CWE-319 (cleartext transmission)
