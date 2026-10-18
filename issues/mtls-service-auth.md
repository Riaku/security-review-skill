# mTLS / Service-to-Service Authentication

**SHOULD** Internal service-to-service calls authenticate with short-lived client certificates rather than shared API keys or network-location trust.

**Why:** "It's inside the VPC so it's fine" collapses the moment one workload is compromised: shared keys leak in env files and logs and identify no caller, while per-workload certs give cryptographic identity that expires before reuse.

**Detect:** Look for SPIFFE/SPIRE or cert-manager `Certificate` with `usages: [client auth]`. Grep for peers authenticated only by IP allowlist or a fleet-wide `INTERNAL_API_KEY`. Check cert lifetimes (hours, not years) and automated rotation.

**Bad:**
```python
# one key for every caller, checked by every callee
if request.headers["X-Internal-Key"] == env("INTERNAL_API_KEY"): ok()
```

**Good:**
```python
peer = verify_client_cert(request, ca=trust_bundle)   # SPIFFE ID per workload
if peer.spiffe_id in allowed_callers[endpoint]: ok()
```

**References:** SPIFFE/SPIRE docs, NIST SP 800-207 Zero Trust, Istio identity & certificate docs
