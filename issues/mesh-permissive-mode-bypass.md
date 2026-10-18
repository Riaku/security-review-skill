# Service Mesh Permissive mTLS and Direct-Pod-IP Bypass

**MUST NOT** treat permissive-mode mTLS as an access-control boundary; enforce STRICT mTLS per namespace and pair it with NetworkPolicies that block plaintext direct-pod-IP access.

**Why:** Permissive mode accepts both meshed (mTLS) and raw plaintext traffic, so an attacker inside the cluster — or a compromised pod — simply bypasses the sidecar by dialing the pod IP on the plaintext port, and any authorization policy keyed on peer identity silently fails open for that path.

**Detect:** Check PeerAuthentication `mtls.mode: PERMISSIVE` (or mesh-wide default), AuthorizationPolicies that allow when principal is empty, CNI/network policies that don't restrict pod ports to sidecar traffic only, and services reachable on `podIP:port` in egress tests. Verify destination rules route through the service, not resolved pod endpoints.

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

**References:** Istio security docs (permissive mTLS caveats), OWASP Kubernetes Top 10, CWE-300

---

**Part of:** [authentication](../categories/authentication.md) · [cloud-network](../categories/cloud-network.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
