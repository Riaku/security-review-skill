# Service Mesh / Service-to-Service mTLS (identity for internal traffic)

**SHOULD** enforce mutual TLS between internal services so east-west traffic carries identity, not network-location trust.

**Why:** A flat internal network lets whoever breaches one service impersonate any other and sniff cleartext credentials.

**Detect:** grep mesh configs: `mtls.mode: STRICT`, `PeerAuthentication`, `security.istio.io`, Linkerd/Consul `tls: ENABLE`, mesh policy manifests.

**References:** NIST SP 800-207 Zero Trust, Istio mTLS docs, CIS Kubernetes Benchmark 5.x, CWE-319
