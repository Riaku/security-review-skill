# containers-k8s

Container and Kubernetes runtime configuration.

## What this category covers

This category covers the configuration of containers and of the cluster that runs them: what a pod may touch, what identity it runs under, and how the scheduler and kubelet treat it under pressure. Member items span pod security contexts, capabilities, host mounts and namespace sharing, RBAC and admission control, probes and disruption budgets, quotas and eviction, and image construction. They also cover control-plane exposure — etcd, kubelet, and API audit logging — and syscall-level runtime detection. A reviewer should expect findings about isolation boundaries a workload can cross, and about cluster defaults that let one workload degrade or compromise another.

- Pod hardening: non-root users, dropped capabilities, seccomp, read-only root, and privilege escalation.
- Isolation boundaries: hostPath, host namespaces, runtime sockets, and privileged mode.
- Identity and authorization: service accounts, RBAC verbs, admission policy, and API audit logging.
- Control-plane and node exposure: etcd, the kubelet port, and the scope of the GitOps controller.
- Scheduling and lifecycle: probes, disruption budgets, quotas, eviction order, owner references, and finalizers.
- Image hygiene: multi-stage builds, digest pinning, and registry-outage tolerance.

## What it does not cover

- [cloud-network](../categories/cloud-network.md) — ingress, load balancers, DNS, and cloud firewall exposure belong there; this category covers segmentation inside the cluster.
- [deployment-release](../categories/deployment-release.md) — rollout strategy, artifact promotion, and rollback belong there.
- [scaling-capacity](../categories/scaling-capacity.md) — sizing, autoscaling policy, and capacity headroom belong there.

## What a finding here looks like

- A pod mounts the container runtime socket or a host path, giving a compromised container node-level control.
- A workload runs as UID 0 with default capabilities and no seccomp profile.
- An RBAC role grants `impersonate`, `bind`, or `escalate`, or broad `pods/exec`, to a non-admin subject.
- A liveness probe checks the database, so a downstream outage restarts every replica at once.
- No admission policy engine or ResourceQuota exists, so any manifest that passes review can deploy unbounded or privileged.
