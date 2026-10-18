# Service Mesh

**SHOULD** Where a service mesh is deployed, enforce mutual TLS in STRICT mode between sidecars and remove plaintext permissive fallbacks before production sign-off.

**Why:** A mesh left in PERMISSIVE mode still accepts plaintext, so encryption becomes optional and identity unauthenticated — an attacker inside the cluster can impersonate any service, and the mesh's own telemetry records the impostor.

**Detect:** Check Istio `PeerAuthentication`/`DestinationRule` for `mtls.mode: STRICT` versus `PERMISSIVE`/`DISABLED`. Look for namespace-wide exemptions and `excludeOutboundPorts` annotations smuggling traffic around the mesh.

**Bad:**
```yaml
kind: PeerAuthentication
spec: { mtls: { mode: PERMISSIVE } }   # plaintext still accepted
```

**Good:**
```yaml
spec:
  mtls: { mode: STRICT }
  selector: { matchLabels: { app: payments } }
```

**References:** Istio mTLS docs, NIST SP 800-207 Zero Trust, CNCF zero-trust whitepaper
