# hardening-benchmarks

Host, container and Kubernetes hardening baselines (CIS, STIG, kube-bench) — applies to any deployable, whether or not a compliance regime names it.

## What this category covers

This category covers default and drifting configuration of hosts, containers, clusters, and cloud accounts, and the gates that catch the drift before an attacker does. Items span published baselines and control mappings, automated benchmark scanning in CI, host and kernel hardening, cluster admission and pod security, exposed services and unauthenticated data stores, and patch cadence with provider-native cloud posture. A reviewer should expect to inspect configuration files (sshd, sysctl, daemon.json), Kubernetes manifests and admission policy, TLS endpoint settings, and the CI scan stage.

- Published baselines and control mappings — CIS Benchmarks for OS, Docker, Kubernetes, and cloud, CIS Controls implementation groups (IG1–IG3), and DISA STIG checklists.
- Automated benchmark gates — kube-bench, Lynis, and Trivy misconfig scans wired into CI with severity gates and dated exceptions.
- Host and kernel hardening — sysctl settings for source routing and redirects, kernel pointer restriction, ptrace scope, ASLR, and internet-facing SSH configuration.
- Cluster admission and pod security — Pod Security Standards, admission policy engines, seccomp, read-only root filesystems, privilege-escalation flags, and capability dropping.
- Exposure of services and data stores — default credentials, unauthenticated Redis, Elasticsearch, MongoDB, or Memcached, the kubelet port 10250, and public admin, actuator, `.env`, or `.git` endpoints.
- Patch cadence and cloud posture — remediation SLAs by severity with base-image rebuilds, plus provider-native frameworks (AWS Foundational Security Best Practices, Azure Secure Score, GCP CIS recommendations).

## What it does not cover

- [containers-k8s](../categories/containers-k8s.md) — workload design such as probes, resource requests, RBAC, and network policies belong there; the hardened configuration baseline those workloads must meet is scoped here.
- [cloud-network](../categories/cloud-network.md) — network topology, ingress, firewalls, and DNS belong there; the provider security benchmark and its continuous posture score are scoped here.
- [supply-chain](../categories/supply-chain.md) — dependency provenance, SBOMs, and signed build attestations belong there; the patching SLA for known CVEs in shipped images is scoped here.
- [secrets-crypto](../categories/secrets-crypto.md) — secret storage, rotation, and primitive choice belong there; the TLS profile and cipher suites an endpoint offers are scoped here.

## What a finding here looks like

- A kubelet with anonymous authentication enabled or `authorizationMode: AlwaysAllow`, reachable outside the control plane.
- `sshd_config` with `PermitRootLogin yes` and `PasswordAuthentication yes` on an internet-facing host.
- A pod with no seccomp profile, a writable root filesystem, or `allowPrivilegeEscalation: true`.
- An internet-reachable Redis, MongoDB, or Elasticsearch with authentication disabled.
- A TLS endpoint still negotiating RC4, 3DES, or SHA-1 MACs, or an sshd offering weak ciphers or protocol 1.
