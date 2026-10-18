# Dedicated Service Accounts per Workload

**SHOULD NOT** run workloads under the `default` Kubernetes service account; each workload **SHOULD** declare a dedicated `serviceAccountName` scoped to exactly the API access it needs.

**Why:** The default SA is shared by every pod that doesn't override it, so any IAM or RBAC grant made for one workload silently applies to all of them, and audit logs cannot attribute an API call to the workload that made it. Dedicated identities are the prerequisite for least-privilege cloud IAM (IRSA/workload identity), per-workload RBAC, and meaningful `automountServiceAccountToken` control.

**Detect:** `spec.serviceAccountName` absent or `default` in Deployments/Pods/StatefulSets; `default` SA bound to any Role/ClusterRole beyond the baseline; IAM roles (e.g. EKS IRSA annotations) attached to workloads running as `default`. Policy engines: Kyverno `require-dedicated-service-accounts` / a equivalent admission rule.

**References:** CIS Kubernetes 5.1.4 (minimize default SA admission), K8s service accounts docs, EKS IRSA / GKE Workload Identity guidance, aquasecurity/trivy-checks KSV010–KSV012
