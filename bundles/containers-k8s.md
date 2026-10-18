# containers-k8s — full checklist (44 items)

Container and Kubernetes runtime configuration.

> Generated artifact. Canonical source: `issues/<slug>.md`.

# Liveness vs Readiness Probes

**SHOULD NOT** wire dependency checks (DB, cache) into the liveness probe; reserve them for readiness only.

**Why:** Liveness failures kill pods during a downstream outage, turning a slowdown into a cluster-wide crash loop and thundering restart storm.

**Detect:** `livenessProbe` with `exec: pg_isready`/DB query, identical liveness and readiness endpoints, `initialDelaySeconds: 0`.

**References:** Kubernetes probe docs, CWE-770, Google SRE Workbook

# Multi-Stage Builds

**MUST** build images with multi-stage Dockerfiles so compilers, headers, and build caches never ship in the final stage.

**Why:** Single-stage images carry toolchains that widen the attack surface and make CVE triage impossible against runtime-only needs.

**Detect:** Dockerfile lacking a second `FROM` line; `gcc`, `make`, `-dev` packages or `/root/.cache` present in final image layers.

**References:** CIS Docker Benchmark (image build), NIST SP 800-190 4.2

# Non-Root Containers

**MUST NOT** run container processes as UID 0; every image declares a `USER` with a numeric non-zero ID.

**Why:** Root inside a container that escapes or mounts host paths becomes root on the node, bypassing most isolation assumptions.

**Detect:** `USER root`, missing `USER` directive in Dockerfile; runtime `id -u` equals 0; `runAsNonRoot: false` in pod specs.

**References:** CIS Docker 4.1, CIS K8s 5.2.6, CWE-250, OWASP K8s PSA runAsNonRoot

# Resource Requests & Limits

**SHOULD** set explicit CPU/memory requests and limits on every container so one workload cannot starve the node or the scheduler cannot place blindly.

**Why:** Unbounded containers trigger noisy-neighbor degradation and OOM kills of unrelated pods under memory pressure.

**Detect:** Pod/Deployment YAML missing `resources.requests` or `resources.limits`; LimitRange absent in namespace.

**References:** CIS K8s 5.2.1, NIST SP 800-190 5.3, CWE-770, K8s docs resource-management

# Pod Disruption Budgets

**SHOULD** define a PodDisruptionBudget for every highly-available workload so voluntary drains never take down all replicas at once.

**Why:** Without a budget, node upgrades or scale-downs can evict every replica simultaneously, causing an avoidable availability outage.

**Detect:** Deployments with `replicas > 1` and no matching `PodDisruptionBudget` kind; `minAvailable`/`maxUnavailable` unset cluster-wide.

**References:** K8s docs poddisruptionbudgets, SRE Workbook availability practices, NIST SP 800-190 5.4

# Kubernetes RBAC & NetworkPolicies

**MUST** bind least-privilege RBAC roles and enforce default-deny NetworkPolicies per namespace instead of flat open cluster networking.

**Why:** Cluster-admin bindings and absent network segmentation let any compromised pod read secrets or laterally reach every service.

**Detect:** `ClusterRoleBinding` to `cluster-admin` for app serviceaccounts; no `NetworkPolicy` with `podSelector` matching all ingress in namespace.

**References:** CIS K8s 5.1, RBAC Least Privilege, CWE-284, OWASP Kubernetes Top 10 K03/K07

# CIS Benchmarks (OS/container/k8s/cloud)

**MUST** Every OS image, container base, Kubernetes cluster, and cloud account be baselined against the applicable CIS Benchmark, with deviations recorded as explicit, time-boxed exceptions rather than silent drift.

**Why:** CIS Benchmarks encode thousands of reviewed hardening decisions; skipping them means rediscovering — as a breach — the weak SSH config or unlogged audit trail that was already solved and documented.

**Detect:** Run `kube-bench`, `lynis`, or ScoutSuite and diff against a documented exception list. Check CI for a benchmark stage on built images; flag exceptions with no owner or expiry date.

**Bad:**
```
# "we hardened it last year" — no automated check, drift unknown
```

**Good:**
```yaml
# CI job on every image build + weekly cluster scan
- run: kube-bench --json | jq '[.NodeResults[].Tests[] | select(.failures>0)]'
# failures fail the build unless matched to a registered exception
```

**References:** CIS Benchmarks (cisecurity.org), CIS Kubernetes Benchmark, CIS Docker Benchmark, DISA STIGs

# CIS Docker Benchmark

**MUST** align container host and daemon configuration with the current CIS Docker Benchmark sections 2 (daemon) and 5 (runtime), including `daemon.json` settings, before production deployment.

**Why:** Unhardened Docker defaults expose the socket, permissive logging, and root containers that turn one compromised image into full host takeover.

**Detect:** grep daemon.json for `userns-remap`, `log-driver`, `live-restore`; check `/var/run/docker.sock` permissions and `--privileged` in compose files.

**References:** CIS Docker Benchmark v1.6.0, CIS Controls v8, NIST SP 800-190

# Pod Security Standards: seccomp, readOnlyRootFilesystem, allowPrivilegeEscalation

**MUST** apply `RuntimeDefault` seccomp, `readOnlyRootFilesystem: true`, and `allowPrivilegeEscalation: false` on all pod security contexts.

**Why:** Permissive security contexts let exploits persist writes to the container root and escalate via setuid binaries; unconfined or unmasked syscall surfaces turn one broken container into full node compromise — the classic escape path Falco and Tracee alert on.

**Detect:** Pod YAML missing `securityContext.seccompProfile`, `readOnlyRootFilesystem`, or showing `allowPrivilegeEscalation: true`; grep manifests for `unconfined`, `unmasked`, `CAP_SYS_*`; run container escape test suites (e.g. cdve).

**References:** CIS K8s 5.2.1-5.2.8, K8s Pod Security Standards restricted, CWE-250, MITRE ATT&CK T1611, CIS Docker 5.3

# Dangerous Host Mounts: docker.sock, hostPath, Privileged Pods

**MUST NOT** mount host paths such as `/`, `/etc`, or the container runtime socket into untrusted workloads, and MUST NOT mark pods privileged without documented justification.

**Why:** A hostPath or privileged pod is effectively node root access; one compromised app owns the machine and every co-located secret — and runtime-socket access grants the full container-control API, trivially equivalent to root on the node.

**Detect:** `hostPath` volumes pointing at `/etc`, `/proc`, `/var/run/docker.sock`; volume mounts of `containerd.sock` or `crio.sock`; env `DOCKER_HOST` pointing at a mounted socket path; `privileged: true` in pod manifests. Remedy: scoped socket proxy or a dedicated agent instead of raw socket exposure.

**References:** CIS K8s 5.2.4, 5.2.5, CWE-668, OWASP K8s PS4, MITRE ATT&CK T1611, CIS Docker 2.4, NIST SP 800-190 4.4

# Privileged Containers and Excess Linux Capabilities

**SHOULD NOT** grant capabilities beyond the app's proven need; drop all by default and add back only what fails without them.

**Why:** Extra caps like `SYS_ADMIN` or `SYS_MODULE` approximate full privilege and enable container escape or kernel module loading.

**Detect:** `securityContext.capabilities.add` listing `SYS_ADMIN`, `NET_ADMIN`, `SYS_MODULE`; `privileged: true` without an exception record.

**References:** CIS K8s 5.2.7, CAP(7), MITRE ATT&CK T1611, CWE-250

# Host Namespace Sharing (hostPath/hostPID/hostNetwork/hostIPC)

**MUST NOT** set `hostPID`, `hostNetwork`, or `hostIPC` on ordinary workloads; each flag breaks the isolation boundary between pod and node.

**Why:** Shared namespaces expose host processes, sniff node traffic, and let a pod signal or ptrace host-level daemons.

**Detect:** Pod spec keys `hostPID: true`, `hostNetwork: true`, `hostIPC: true`; DaemonSets using them without documented reason.

**References:** CIS K8s 5.2.2-5.2.4, CWE-497, MITRE ATT&CK T1611, K8s docs namespaces

# Auto-Mounted Service Account Tokens in Pods That Don't Need the API

**SHOULD** set `automountServiceAccountToken: false` on pods and serviceaccounts that never call the Kubernetes API.

**Why:** An unnecessary mounted token is a standing credential an attacker with any file-read bug can use against the API server.

**Detect:** Pod specs without `automountServiceAccountToken: false`; mounted path `/var/run/secrets/kubernetes.io/serviceaccount` in non-API workloads.

**References:** CIS K8s 5.1.5, CWE-522, OWASP Kubernetes Top 10 K06, NIST SP 800-190 5.2

# K8s RBAC Escalation via impersonate/bind/escalate Verbs

**MUST NOT** grant `impersonate`, `bind`, or `escalate` verbs to non-admin subjects; each is a direct path to cluster-admin.

**Why:** `bind` lets a user attach cluster-admin to themselves, `impersonate` borrows any identity, `escalate` upgrades any role — self-grant with no audit trail of intent.

**Detect:** `kubectl auth can-i --list` and grep ClusterRole YAML for `impersonate`, `bind`, `escalate` in verbs; flag RoleBindings to ClusterRole admin.

**References:** RBAC: The Bad Parts (Kubernetes blog), CWE-269, MITRE ATT&CK T1098.001, NIST SP 800-190

# Cloud Metadata Endpoint Credential Theft (IMDS / 169.254.169.254)

**MUST** treat the link-metadata range (`169.254.169.254/32`, GCE `metadata.google.internal`, Azure `169.254.169.254/metadata`) as hostile territory: block it at the network layer from any workload that processes user-supplied URLs.

**Why:** Reaching the metadata service from a compromised or SSRF-able workload hands the attacker the node's IAM credentials verbatim — no exploitation needed, just a GET — and any single missing layer in the chain (v1-tolerant instance, open egress, string-only URL filter) completes the attack.

**Detect:** In SSRF filters, confirm the blocklist covers link-local, loopback, and cloud-specific IPs and is applied after DNS resolution, not on the raw string; test filters with decimal (`2852039166`), IPv6-mapped, and DNS-rebind forms. Check Kubernetes `hostAliases`, egress NetworkPolicies denying `169.254.169.254`, iptables/ip sets on nodes, container `hostNetwork` settings that sidestep pod-level blocks, and proxy configurations that allow CONNECT to it. On instances, verify `HttpTokens=required` plus `HttpPutResponseHopLimit=1` on launch templates. Search code for hardcoded `169.254.169.254` outside legitimate credential-fetching libraries.

**Bad:**
```python
url = user_input
if "localhost" not in url:      # trivially bypassed by decimal/hex IP forms
    requests.get(url)
```

**Good:**
```
# egress deny at the pod network boundary
ipset -A blacklist 169.254.169.254
iptables -A FORWARD -m set --match-set blacklist dst -j DROP
```

**References:** CWE-200, AWS IMDSv2 bulletin, GCP metadata protection docs, OWASP SSRF Prevention Cheat Sheet, CIS AWS 5.6/5.7

# No Admission Policy Engine (Pod Security Standards / Gatekeeper / Kyverno)

**MUST** run an admission policy engine enforcing Pod Security Standards or equivalent custom policy at cluster scope.

**Why:** Without admission control, any YAML that passes review can deploy privileged or unsegmented workloads; policy drift goes unchecked.

**Detect:** No ValidatingWebhookConfiguration for gatekeeper/kyverno; namespaces missing `pod-security.kubernetes.io/enforce` labels.

**References:** CIS K8s 5.2, K8s Pod Security Admission, OWASP Kubernetes Top 10 K04, NIST SP 800-190 5.4

# Admission Webhook failurePolicy:Fail Deadlock and TLS Misconfig

**SHOULD** set `failurePolicy: Fail` only where the webhook is highly available, with valid TLS certs and namespace exclusions for its own namespace.

**Why:** A failing fail-closed webhook blocks all API writes cluster-wide; bad TLS makes every admission request error the same way.

**Detect:** ValidatingWebhookConfiguration with `failurePolicy: Fail` and no `namespaceSelector` excluding kube-system/webhook ns; expired or self-signed `caBundle`.

**References:** CIS K8s 5.2, K8s docs admission-webhook, CWE-1041, SRE postmortem patterns

# etcd Exposure and Missing etcd Encryption

**MUST** restrict etcd (2379/2380) to control-plane peers and enable encryption at rest for all stored Secrets.

**Why:** etcd holds every secret in plaintext by default; a reachable or unencrypted datastore dumps the cluster's entire credential set.

**Detect:** etcd client port reachable off-node; kube-apiserver missing `--encryption-provider-config`; no EncryptionConfiguration resource.

**References:** CIS K8s 2.0, 3.2.1, CWE-311, NIST SP 800-190 5.2, K8s encryption-at-rest docs

# Kubelet Port Protection (10250 AuthN/AuthZ, Anonymous Access)

**MUST NOT** allow anonymous authentication on kubelet port 10250; enable Webhook authorization and firewall the port to control-plane only.

**Why:** An open kubelet API exposes exec, logs, and running-config, letting an attacker run commands in any pod on the node.

**Detect:** `anonymousAuth: true` or `authorizationMode: AlwaysAllow` in kubelet config; 10250 reachable from arbitrary CIDRs; 10255 read-only port open.

**References:** CIS K8s 4.2.1-4.2.3, CWE-306, MITRE ATT&CK T1610, K8s kubelet auth docs

# Kubernetes API Audit Logging Not Enabled

**MUST** enable the kube-apiserver audit policy with persistent, tamper-resistant shipping of audit events.

**Why:** Without API audit logs, privileged actions — secret reads, RBAC changes, pod exec — leave no trace, so cluster compromise is undetectable forensically.

**Detect:** check kube-apiserver flags `--audit-policy-file`, `--audit-log-path`; grep manifests for `audit.k8s.io/v1` Policy; verify long retention on the sink.

**References:** CIS Kubernetes 1.2.1–1.2.4, CWE-778, NIST SP 800-92, K8s docs audit-policy

# Mutable Image Tags (latest) Instead of Digest Pinning

**SHOULD** reference images by immutable digest (`@sha256:`) rather than floating tags like `latest` in production manifests.

**Why:** A retagged or compromised `latest` silently changes what deploys, defeating rollback and supply-chain review.

**Detect:** Image fields ending in `:latest` or bare repo names; absence of `@sha256:` digest in Deployment/Pod specs.

**References:** CIS Docker 4.5, NIST SP 800-190 4.4, OWASP A08 Software Supply Chain, CWE-829

# Admission Enforcement of Signed Images (Verify, Not Just Sign)

**MUST** enforce signature verification at admission so unsigned or wrongly-signed images are rejected before they ever schedule.

**Why:** Signing without enforcement is decoration: an attacker pushes an unsigned image and the cluster runs it happily because nothing checks.

**Detect:** ClusterPolicy `cosigned` / `verify-images` with `match` on all registries; absence of kyverno/admission-controller verify rules; `--image-verification` disabled in k3s config.

**References:** SLSA L4, Sigstore, NSA Kubernetes Hardening Guide, CIS K8s 5.4

# Docker-in-Docker / Privileged Build Steps in CI

**SHOULD** replace privileged Docker-in-Docker with rootless or daemonless builders (BuildKit, Kaniko, Buildah) since `privileged: true` grants the container host-level control.

**Why:** A privileged build container can escape to the runner host and capture every credential and workload on it.

**Detect:** Grep workflows for `privileged: true`, `docker:dind` images, or volume mounts of `/var/run/docker.sock` into build jobs.

**References:** OWASP Docker DS01, CWE-250, NIST SP 800-218 (SSDF), Kaniko and BuildKit rootless docs, GitLab CI best practices

# Helm Hook Ordering and Failed-Hook Release Blocking

**MUST** set `hook-weight` and `hook-delete-policy` explicitly so migrations run before workloads, and treat a failed hook as a release blocker rather than a warning.

**Why:** If a DB migration hook fails but the release proceeds, new pods start against an unmigrated schema and corrupt or reject data immediately.

**Detect:** grep chart `helm.sh/hook` annotations for missing `hook-weight` ordering, absent `hook-delete-policy`, and `--no-hooks`/`--disable-hook-fail` flags in CI deploy steps.

**References:** Helm hooks docs, CWE-664 improper control of resource lifecycle, NIST SP 800-190 change control

# Operator Finalizer Leaks Blocking Resource Deletion

**MUST** ensure operators remove their finalizers on owned resources even when reconciliation errors, so deletion never hangs indefinitely.

**Why:** A leaked finalizer leaves resources stuck in Terminating, blocking namespace deletion and cascading cleanup failures across the cluster.

**Detect:** Resources with `metadata.finalizers` referencing an operator whose controller is down; namespace stuck `Terminating` with lingering finalizers.

**References:** K8s docs finalizers, etcd garbage collection, CWE-404, operator-sdk finalizer patterns

# Missing ownerReferences Causing Orphaned Managed Resources

**SHOULD** set `ownerReferences` on every resource a controller creates so cascading deletion reclaims them automatically.

**Why:** Orphaned resources accumulate invisibly, leaking quotas, secrets, and network policies after their parent is gone.

**Detect:** Created resources lacking `metadata.ownerReferences`; garbage collector cannot trace children; orphan count grows over time.

**References:** K8s docs garbage collection, ownerReferences, CWE-404, operator-sdk ownership patterns

# CRDs Without OpenAPI Validation Schemas

**MUST** define an OpenAPI v3 validation schema for every CustomResourceDefinition so the API server rejects malformed objects before controllers see them.

**Why:** Schema-less CRDs admit arbitrary fields, letting a bad manifest crash controllers or smuggle input into privileged reconcile logic.

**Detect:** `kubectl get crd -o yaml` showing empty `validation.openAPIV3Schema`; CRDs missing `x-kubernetes-*` structural markers.

**References:** Kubernetes CRD validation docs, CWE-20, K8s API conventions

# GitOps Controller Running as cluster-admin

**SHOULD** scope GitOps controllers (Flux, ArgoCD) to least-privilege per-namespace roles instead of the blanket `cluster-admin` ClusterRoleBinding.

**Why:** A compromised repo, PR, or controller CVE becomes instant full-cluster takeover when the sync engine holds cluster-admin.

**Detect:** grep deploy manifests for `cluster-admin` bound to `system:serviceaccount:flux-system` / `argocd`; check ClusterRoleBinding subjects and reconciliation scopes.

**References:** OWASP A05 Security Misconfiguration, CWE-250 Execution with Unnecessary Privileges, ArgoCD security docs, NIST SP 800-190

# PersistentVolume Reclaim Policy and NFS root_squash Data Exposure

**MUST** set PersistentVolume `persistentReclaimPolicy` deliberately (Retain for data-bearing volumes) and enable `root_squash` on NFS exports.

**Why:** A careless Delete policy destroys data on release, while NFS without root_squash lets any pod's root read and write the export.

**Detect:** PVs with `persistentVolumeReclaimPolicy: Delete` on stateful data; NFS export options missing `root_squash` in `/etc/exports` or provisioner config.

**References:** CIS K8s 5.2.3, NFS man root_squash, CWE-284, NIST SP 800-190 5.3

# Missing ResourceQuota / LimitRange Allowing Namespace Exhaustion

**SHOULD** apply ResourceQuota and LimitRange to every tenant namespace so one team cannot consume the whole cluster's compute.

**Why:** Without quotas, a runaway or malicious workload exhausts shared CPU/memory, degrading every other namespace on the cluster.

**Detect:** Namespaces with no `ResourceQuota` or `LimitRange` objects; tenant namespaces sharing unbounded node pools.

**References:** CIS K8s 5.2.1, K8s quotas/limitranges docs, CWE-770, NIST SP 800-190 5.3

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

# ConfigMap Hot-Reload Assumption for Environment Variables

**MUST NOT** rely on environment-variable-injected ConfigMaps updating at runtime; env vars are fixed at container start, so mount files or restart the pod.

**Why:** Teams assume config changes propagate live, then ship with stale credentials or feature flags after a ConfigMap update.

**Detect:** `envFrom: configMapRef` where the app expects live updates; no checksum annotation or rollout trigger on ConfigMap change.

**References:** K8s docs configmap env immutability, CWE-676, Bitnami/Flux config-reload patterns

# exec/attach/debug RBAC Verbs Are Root-in-Pod Equivalent

**MUST NOT** grant `pods/exec`, `pods/attach`, or `pods/debug` broadly; restrict them to named break-glass groups with audit.

**Why:** exec into a pod bypasses every app-layer control — anyone with the verb reads secrets, env vars, and tokens as the workload's user.

**Detect:** grep ClusterRole/Role YAML for `exec`, `attach`, `debug` verbs on `pods`/`pods/exec`; check who can `kubectl exec` via `kubectl auth can-i create pods/exec --as=...`.

**References:** Kubernetes RBAC docs, CWE-269, MITRE ATT&CK T1611 Escape to Host, NIST SP 800-190

# File descriptor and conntrack table limits sized for peak

**SHOULD** size file-descriptor limits and conntrack tables above measured peak concurrency with headroom, and alert before the ceiling is hit rather than after.

**Why:** A busy proxy hitting `ulimit -n` starts refusing connections with `EMFILE`, and a full `nf_conntrack` table silently drops new flows — both look like mysterious upstream flakiness while capacity metrics still show idle CPU.

**Detect:** Compare `ulimit -n` / `fs.file-max` and container `no-new-privileges` securityContext defaults against peak connection counts; check `net.netfilter.nf_conntrack_max` versus `nf_conntrack_count` (watch for `nf_conntrack: table full, dropping packet` in dmesg). In Kubernetes, review Pod `ulimit` inheritance, kube-proxy conntrack settings, and whether monitoring exports fd/conntrack saturation.

**Bad:**
```
# 100k concurrent proxy on default 1024 fds
$ ulimit -n
1024
```

**Good:**
```
# sized for peak + 3x headroom, alarmed at 70%
ulimit -n 65536
sysctl -w net.netfilter.nf_conntrack_max=524288
```

**References:** Netflix tuning guides, Netfilter conntrack docs, Google SRE Book (capacity monitoring), USE method

# Node Disk/Memory Pressure Eviction Behavior Understood

**SHOULD** document and test how kubelet evicts pods under DiskPressure/MemoryPressure, ordering QoS classes and PDBs correctly.

**Why:** Unexpected eviction ordering can kill stateful or critical pods first, turning a disk-full event into a data-loss outage.

**Detect:** No eviction-threshold config in kubelet; no alerts on `nodefs.available`/`memory.available`; QoS classes unset on critical workloads.

**References:** K8s docs eviction, kubelet resource-pressure evictions, CWE-770, SRE Workbook capacity practices

# Control-Plane Quorum (etcd) Health Monitored Separately from Workloads

**MUST** monitor etcd quorum and leader health independently of application dashboards, alerting before quorum loss.

**Why:** Losing etcd quorum freezes the entire cluster's API; a workload-only dashboard misses the failure until everything is already down.

**Detect:** No etcd metrics scrape (`etcd_server_has_leader`, `etcd_server_health_failures`); no separate control-plane alert rule or runbook.

**References:** CIS K8s 2.0, etcd monitoring docs, NIST SP 800-190 5.4, K8s HA control-plane docs

# Crash-Loop Restart Storms Bounded and Alarmed

**SHOULD** bound restart backoff and alarm on CrashLoopBackOff so a failing pod cannot hammer the control plane or mask a persistent fault.

**Why:** Unbounded rapid restarts amplify load on kubelet and API server while the underlying error goes unnoticed until an outage.

**Detect:** No alert on `kube_pod_container_status_waiting_reason{reason="CrashLoopBackOff"}`; `restartPolicy` with no backoff ceiling or paging rule.

**References:** K8s docs backoff, kube-state-metrics CrashLoopBackOff, CWE-770, SRE alerting practices

# Zombie Process Reaping Handled in Container PID 1

**MUST** ensure the container's PID 1 reaps orphaned child processes, via an init system (tini/dumb-init) or a reaping-aware entrypoint.

**Why:** A non-reaping PID 1 lets zombies accumulate until the PID limit is hit, blocking new process spawns and stalling the container.

**Detect:** Container PID 1 is a shell or app without `--reaping`; `docker top`/`ps` shows defunct `<defunct>` entries; no tini/dumb-init in image.

**References:** CIS Docker 5.x, CWE-459, tini/dumb-init docs, Kubernetes init container patterns

# Registry Outage Tolerated via Cached/Pinned Images

**SHOULD** keep images cached on nodes and pinned by digest so a registry outage does not block scheduling or restarts.

**Why:** If a pod must pull during a registry outage, rescheduling and rollouts stall, turning a third-party outage into a cluster outage.

**Detect:** No `imagePullPolicy: IfNotPresent`/`Never` with pre-pulled images; no local registry mirror or pull-through cache configured.

**References:** K8s docs imagePullPolicy, NIST SP 800-190 4.4, Harbor/Docker registry mirror docs, OWASP A08

# Noisy-neighbor isolation between tenants/workloads

**MUST** enforce per-tenant or per-workload resource quotas (CPU, memory, I/O, connection rate) so one tenant's burst cannot degrade others sharing the host.

**Why:** Without isolation, a single abusive or misbehaving tenant saturates shared CPU, disk I/O, or network, violating SLAs for everyone co-located.

**Detect:** grep for `ResourceQuota`, `LimitRange`, `CPUShares`/`cpu_weight`, `blkio`/`IOClass`, per-tenant `rate_limit` in gateway config; flag shared pools with no per-tenant caps.

**References:** OWASP ASVS 14.2, CWE-770, Kubernetes QoS/ResourceQuota docs

# Immutable Infrastructure (no SSH-and-patch; replace, don't mutate)

**SHOULD NOT** patch running servers over SSH; rebuild and redeploy images so every host matches a known, auditable template.

**Why:** Hand-mutated snowflake hosts hide drift from hardening baselines and can't be trusted or reproduced during incidents.

**Detect:** grep SSH-to-prod patch runbooks vs image pipelines: Packer bake jobs, launch-template updates, `strategy: Recreate`.

**References:** NIST SP 800-53 CM-2/CM-6, CIS Control 2

# Runtime Threat Detection (Falco/eBPF-style workload anomaly detection)

**MUST** monitor running workloads at syscall level (Falco/eBPF) for anomalies: shells in containers, unexpected writes, suspicious spawns.

**Why:** Scanners only see what you built; attackers operate in what's running, unnoticed inside otherwise "secure" images.

**Detect:** grep `falco`, `tracee`, `tetragon`, `ebpf` in DaemonSets/deployment YAML, custom `falco_rules.yaml` files.

**References:** MITRE ATT&CK container matrix T1610, CIS Docker/K8s Benchmarks 5.x, NIST SP 800-190

# Egress Control (outbound traffic allow-listed; exfil paths narrowed)

**SHOULD** restrict outbound traffic to an explicit allow-list so compromised hosts cannot freely phone home or exfiltrate.

**Why:** Default-open egress is the exfiltration highway: malware, reverse shells, and data staging all reach arbitrary endpoints.

**Detect:** grep `NetworkPolicy` egress rules, `egress gateway`, proxy allow-lists, `default-deny` outbound rules.

**References:** NIST SP 800-207 Zero Trust, CIS Control 12, MITRE ATT&CK TA0011

# Dedicated Service Accounts per Workload

**SHOULD NOT** run workloads under the `default` Kubernetes service account; each workload should declare a dedicated `serviceAccountName` scoped to exactly the API access it needs.

**Why:** The default SA is shared by every pod that doesn't override it, so any IAM or RBAC grant made for one workload silently applies to all of them, and audit logs cannot attribute an API call to the workload that made it. Dedicated identities are the prerequisite for least-privilege cloud IAM (IRSA/workload identity), per-workload RBAC, and meaningful `automountServiceAccountToken` control.

**Detect:** `spec.serviceAccountName` absent or `default` in Deployments/Pods/StatefulSets; `default` SA bound to any Role/ClusterRole beyond the baseline; IAM roles (e.g. EKS IRSA annotations) attached to workloads running as `default`. Policy engines: Kyverno `require-dedicated-service-accounts` / a equivalent admission rule.

**References:** CIS Kubernetes 5.1.4 (minimize default SA admission), K8s service accounts docs, EKS IRSA / GKE Workload Identity guidance, aquasecurity/trivy-checks KSV010–KSV012

