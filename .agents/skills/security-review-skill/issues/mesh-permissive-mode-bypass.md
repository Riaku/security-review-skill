---
categories: [authentication, cloud-network]
domains: [backend, infrastructure]
---

# Service Mesh Permissive mTLS and Direct-Pod-IP Bypass

**MUST NOT** treat permissive-mode mTLS as an access-control boundary; enforce STRICT mTLS per namespace and pair it with NetworkPolicies that block plaintext direct-pod-IP access.
**SHOULD** Where a service mesh is deployed, enforce mutual TLS in STRICT mode between sidecars and remove plaintext permissive fallbacks before production sign-off.

**Why:** Permissive mode accepts both meshed (mTLS) and raw plaintext traffic, so an attacker inside the cluster — or a compromised pod — simply bypasses the sidecar by dialing the pod IP on the plaintext port, and any authorization policy keyed on peer identity silently fails open for that path.

**Detect:** Check PeerAuthentication `mtls.mode: PERMISSIVE` (or mesh-wide default), AuthorizationPolicies that allow when principal is empty, CNI/network policies that don't restrict pod ports to sidecar traffic only, and services reachable on `podIP:port` in egress tests. Verify destination rules route through the service, not resolved pod endpoints. Also check `PeerAuthentication`/`DestinationRule` for `mtls.mode: STRICT` versus `PERMISSIVE`/`DISABLED`, and look for namespace-wide exemptions and `excludeOutboundPorts` annotations smuggling traffic around the mesh.

**Bad:**
```yaml
mtls:
  mode: PERMISSIVE   # plaintext to podIP:8080 still accepted
```

**Good:**
```yaml
mtls:
  mode: STRICT
# plus NetworkPolicy restricting the port to the mesh sidecar
```

**References:** Istio security docs (permissive mTLS caveats), Istio mTLS docs, NIST SP 800-207 Zero Trust, CNCF zero-trust whitepaper, OWASP Kubernetes Top 10, CWE-300
