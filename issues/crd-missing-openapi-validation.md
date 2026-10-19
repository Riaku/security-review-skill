---
categories: [api-design, containers-k8s]
domains: [backend, infrastructure]
---

# CRDs Without OpenAPI Validation Schemas

**MUST** define a structural OpenAPI v3 validation schema (`spec.versions[*].schema.openAPIV3Schema`) for every CustomResourceDefinition so the API server rejects malformed objects before controllers see them.

**Why:** Schema-less CRDs admit arbitrary fields, letting a bad manifest crash controllers or smuggle input into privileged reconcile logic.

**Detect:** `kubectl get crd -o yaml` and inspect `spec.versions[*].schema.openAPIV3Schema` for `x-kubernetes-preserve-unknown-fields: true`, `additionalProperties: true`, or empty `properties` objects — for `apiextensions.k8s.io/v1` a structural schema is required, so validation is only ever absent by explicit opt-out.

**References:** Kubernetes CRD validation docs, CWE-20, K8s API conventions
