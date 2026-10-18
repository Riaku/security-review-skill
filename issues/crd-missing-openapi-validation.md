---
categories: [api-design, containers-k8s]
domains: [backend, infrastructure]
---

# CRDs Without OpenAPI Validation Schemas

**MUST** define an OpenAPI v3 validation schema for every CustomResourceDefinition so the API server rejects malformed objects before controllers see them.

**Why:** Schema-less CRDs admit arbitrary fields, letting a bad manifest crash controllers or smuggle input into privileged reconcile logic.

**Detect:** `kubectl get crd -o yaml` showing empty `validation.openAPIV3Schema`; CRDs missing `x-kubernetes-*` structural markers.

**References:** Kubernetes CRD validation docs, CWE-20, K8s API conventions
