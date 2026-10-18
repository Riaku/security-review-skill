# NodePort / LoadBalancer Accidentally Exposing Internal Services

**SHOULD NOT** publish admin dashboards, databases, or metrics endpoints via NodePort or an internet-facing LoadBalancer; internal services stay internal unless a reviewed ingress explicitly fronts them.

**Why:** A `type: NodePort` service opens a 30000-32767 port on every node's public IP, and a defaulted `LoadBalancer` scope often lands on the open internet — exposing unauthenticated UIs that were designed for cluster-internal access only.

**Detect:** Audit manifests for `type: NodePort`, `type: LoadBalancer` without `loadBalancerSourceRanges` or `service.beta.kubernetes.io/aws-load-balancer-internal: "true"`, and Helm values overriding service type. Live check: `kubectl get svc -A | grep -E 'NodePort|LoadBalancer'`, then probe the node ports externally. Flag `/metrics`, `/actuator`, dashboard UIs surfacing this way.

**Bad:**
```yaml
spec:
  type: NodePort        # admin UI now on every node's public IP:31234
  ports: [{port: 8080, targetPort: 8080}]
```

**Good:**
```yaml
spec:
  type: ClusterIP   # expose only via authenticated Ingress with TLS
```

**References:** CWE-284, CIS Kubernetes 5.2.2, OWASP Kubernetes Top 10, AWS LB isolation docs
