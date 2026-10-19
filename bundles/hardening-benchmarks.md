# hardening-benchmarks — full checklist (17 items)

CIS/STIG-style configuration baselines.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/hardening-benchmarks.md](../categories/hardening-benchmarks.md) · Index: [SKILL.md](../SKILL.md)

# No Admission Policy Engine (Pod Security Standards / Gatekeeper / Kyverno)

**MUST** run an admission policy engine enforcing Pod Security Standards or equivalent custom policy at cluster scope.

**Why:** Without admission control, any YAML that passes review can deploy privileged or unsegmented workloads; policy drift goes unchecked.

**Detect:** No ValidatingWebhookConfiguration for gatekeeper/kyverno; namespaces missing `pod-security.kubernetes.io/enforce` labels.

**References:** CIS K8s 5.2, K8s Pod Security Admission, OWASP Kubernetes Top 10 K04

# Benchmark Scanning in CI (kube-bench, Lynis, Trivy misconfig)

**SHOULD** run kube-bench, Lynis, or Trivy misconfig scans in CI on every image and host config change, failing the pipeline on high-severity findings.

**Why:** Hardening drifts silently after deploy; without automated benchmark gates, regressions ship unnoticed until an attacker exploits them.

**Detect:** Check `.github/workflows/*` or Jenkinsfile for `kube-bench`, `lynis audit`, `trivy config`, `trivy image --scanners misconfig` steps and severity gates.

**References:** CIS Benchmarks, NIST SP 800-53 CM-6, DevSecOps, CWE-1188

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
- run: kube-bench --json | jq '[.Controls[].tests[].results[] | select(.status=="FAIL")]'
# failures fail the build unless matched to a registered exception
```

**References:** CIS Benchmarks (cisecurity.org), CIS Kubernetes Benchmark, CIS Docker Benchmark, DISA STIGs

# CIS Controls (IG1–IG3)

**SHOULD** map security controls to CIS Controls v8 implementation groups, with IG1 as the baseline for every asset and IG2/IG3 layered by risk tier.

**Why:** Without implementation-group mapping, small teams skip the highest-yield safeguards (asset inventory, access control, patching) while chasing low-priority items.

**Detect:** Search docs/policies for `CIS Controls`, `IG1`, `safeguard 4.1`-style citations; check whether asset inventory and MFA controls are evidenced.

**References:** CIS Controls v8 IG1-IG3, NIST CSF, ISO 27001 Annex A

# CIS Docker Benchmark

**MUST** align container host and daemon configuration with the current CIS Docker Benchmark sections 2 (daemon) and 5 (runtime), including `daemon.json` settings, before production deployment.

**Why:** Unhardened Docker defaults expose the socket, permissive logging, and root containers that turn one compromised image into full host takeover.

**Detect:** grep daemon.json for `userns-remap`, `log-driver`, `live-restore`; check `/var/run/docker.sock` permissions and `--privileged` in compose files.

**References:** CIS Docker Benchmark v1.6.0, CIS Controls v8, NIST SP 800-190

# Cloud Provider Security Benchmarks (AWS Foundations / Azure / GCP CIS)

**SHOULD** The provider's own framework — AWS Foundational Security Best Practices, Azure Secure Score, GCP CIS recommendations — be continuously evaluated in the native tool rather than spot-checked by hand.

**Why:** Provider frameworks catch platform-specific misconfigurations generic hardening misses: live root keys, audit logging off, IAM users with `*:*`, unencrypted snapshots — each a documented incident pattern.

**Detect:** Confirm Security Hub standards / Defender for Cloud cover every account and subscription, not just the primary one. Check for findings aged past 30 days with no owner and member accounts silently excluded from the aggregator.

**Bad:**
```
# Security Hub enabled in one region of one account; 14 others unmonitored
```

**Good:**
```hcl
# org-wide aggregation: standards enabled per member account via StackSets,
# findings exported to SIEM with an SLA on high severity
```

**References:** AWS Foundational Security Best Practices standard, CIS AWS Foundations Benchmark, Microsoft Defender for Cloud, GCP Security Command Center

# Default & Weak Credentials in Shipped Software

**MUST NOT** ship software with default usernames/passwords or demo accounts enabled in production; force credential change on first login.

**Why:** Scanners sweep the internet for known default credentials (admin/admin, root/toor) and compromise unmodified deployments within minutes of exposure.

**Detect:** grep configs/seed files for `admin:admin`, `changeme`, `default_password`, hardcoded credentials in Docker images, demo accounts in fixtures shipped to prod.

**References:** CWE-1188, OWASP A05:2021, CIS Control 4.7, NIST SP 800-63B

# DISA STIG Hardening

**SHOULD** apply DISA STIG checklists to systems handling regulated or government-adjacent data, documenting every deviation with a documented mitigation.

**Why:** STIG gaps show auditors unmitigated known vulnerabilities; unreviewed deviations become compliance findings and exploitable defaults left in place.

**Detect:** Look for STIG checklist files, `stig`/`STIG` annotations in Ansible or Puppet roles, and `openscap-scanner` profiles referencing `disa_stig`.

**References:** DISA STIG, NIST SP 800-70, CIS Controls v8 IG2, SCAP/OSCAL

# Kernel/Sysctl Hardening

**MUST** disable source routing, redirect sends, and proxy ARP, and enable `kernel.kptr_restrict=2`, `kernel.yama.ptrace_scope=1`, and ASLR system-wide via sysctl.

**Why:** Default kernel settings leak kernel pointers, allow ptrace of other processes, and permit packet spoofing that aids lateral movement and local privilege escalation.

**Detect:** grep `/etc/sysctl.conf` and `/etc/sysctl.d/*.conf` for `kptr_restrict`, `ptrace_scope`, `rp_filter`, `accept_redirects`, `randomize_va_space`.

**References:** CIS Distro Benchmark sec. 3, CWE-1188, NIST SP 800-123, CWE-200

# Kubelet Port Protection (10250 AuthN/AuthZ, Anonymous Access)

**MUST NOT** allow anonymous authentication on kubelet port 10250; enable Webhook authorization and firewall the port to control-plane only.

**Why:** An open kubelet API exposes exec, logs, and running-config, letting an attacker run commands in any pod on the node.

**Detect:** `anonymousAuth: true` or `authorizationMode: AlwaysAllow` in kubelet config; 10250 reachable from arbitrary CIDRs; 10255 read-only port open.

**References:** CIS K8s 4.2.1-4.2.3, CWE-306, MITRE ATT&CK T1610, K8s kubelet auth docs

# Patch cadence and remediation SLAs for known CVEs in production images

**MUST** rebuild and redeploy base images on a fixed cadence (weekly minimum), remediating critical CVEs within 24 hours of disclosure.

**Why:** Long-lived images accumulate known-exploitable CVEs that scanners flag forever and worms exploit within days.

**Detect:** `.trivyignore` age, `imagePullPolicy: Always`, Renovate/Dependabot config, `fixVersions` in scanner reports

**References:** CWE-1104, CISA KEV, NIST SP 800-40 Rev. 4, OWASP A06:2021

# Pod Security Standards: seccomp, readOnlyRootFilesystem, allowPrivilegeEscalation

**MUST** apply `RuntimeDefault` seccomp, `readOnlyRootFilesystem: true`, and `allowPrivilegeEscalation: false` on all pod security contexts.

**Why:** Permissive security contexts let exploits persist writes to the container root and escalate via setuid binaries; unconfined or unmasked syscall surfaces turn one broken container into full node compromise — the classic escape path Falco and Tracee alert on.

**Detect:** Pod YAML missing `securityContext.seccompProfile`, `readOnlyRootFilesystem`, or showing `allowPrivilegeEscalation: true`; grep manifests for `unconfined`, `unmasked`, `CAP_SYS_*`; run container escape test suites (e.g. cdve).

**References:** CIS K8s 5.2.1-5.2.8, K8s Pod Security Standards restricted, CWE-250, MITRE ATT&CK T1611, CIS Docker 5.3

# Privileged Containers and Excess Linux Capabilities

**SHOULD NOT** grant capabilities beyond the app's proven need; drop all by default and add back only what fails without them.

**Why:** Extra caps like `SYS_ADMIN` or `SYS_MODULE` approximate full privilege and enable container escape or kernel module loading.

**Detect:** `securityContext.capabilities.add` listing `SYS_ADMIN`, `NET_ADMIN`, `SYS_MODULE`; `privileged: true` without an exception record.

**References:** CIS K8s 1.24 5.2.9 (added capabilities), CAP(7), MITRE ATT&CK T1611, CWE-250

# Sensitive endpoint exposure (actuator, /admin, .git, .env, debug routes, dashboards)

**MUST NOT** Expose admin panels, actuator endpoints, `.git`/`.env` files, or dashboards publicly; gate them behind auth.

**Why:** Leaked `.env` and `.git` hand attackers credentials and full source directly.

**Detect:** Reachable `/actuator`, `/admin`, `/.git/HEAD`, `/.env`, `/server-status`, `/metrics` without auth.

**References:** OWASP A05:2021, CWE-538, CWE-200, OWASP WSTG-CONF-05

# SSH Hardening

**MUST NOT** permit root login or password authentication on internet-facing SSH; keys only, with `PermitRootLogin no`, `PasswordAuthentication no`, and modern MACs/ciphers.

**Why:** Password-auth SSH is brute-forced at scale; root login hands attackers the highest-privilege account the moment one credential leaks.

**Detect:** grep `sshd_config` and `sshd_config.d/*` for `PermitRootLogin yes`, `PasswordAuthentication yes`, `Protocol 1`, weak `Ciphers`/`MACs`.

**References:** CIS Distro Benchmark sec. 5, CWE-287, NIST SP 800-123, Mozilla Open SSH config

# TLS/ Cipher Suite Hardening (Mozilla profiles, disable legacy)

**MUST** Terminating endpoints offer only modern suites per the Mozilla Intermediate (or Modern) profile, and MUST NOT negotiate RC4, 3DES, SHA-1 MACs, export, or anonymous suites.

**Why:** Legacy ciphers carry known breaks — Sweet32 against 3DES, Lucky13 against CBC, total break of RC4 — so one enabled weak suite lets an on-path attacker force the connection down to a level they can decrypt.

**Detect:** Probe with `nmap --script ssl-enum-ciphers -p 443 host` or SSL Labs. Grep nginx `ssl_ciphers`, Java `jdk.tls.disabledAlgorithms`, and LB security policies for `RC4`, `3DES`, `MD5`, `NULL`. Verify TLS 1.2+ with AEAD preference.

**Bad:**
```nginx
ssl_ciphers "ALL:eNULL:RC4:3DES:+HIGH";   # everything and the kitchen sink
```

**Good:**
```nginx
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-ECDSA-CHACHA20-POLY1305;
ssl_protocols TLSv1.2 TLSv1.3;
```

**References:** Mozilla Server-Side TLS (Intermediate profile), RFC 8446, CWE-326 Inadequate Encryption Strength

# Unauthenticated data stores exposed (Redis, Elasticsearch, MongoDB, Memcached)

**MUST** require authentication on every datastore engine and bind its listener only to the interfaces that need it (Redis `requirepass`/ACLs, MongoDB `authorization: enabled`, Elasticsearch `xpack.security.enabled`), so that reaching the port is not sufficient to read or write data.

**Why:** These engines shipped with auth off by default, and scanned-and-looted instances appear daily: Redis dumps of sessions, Elasticsearch clusters of leaked PII. An unauthenticated store on a reachable network is a breach with a countdown timer.

**Detect:** `bind`/`bind_ip` set to `0.0.0.0`; Redis without `requirepass` or ACL users, MongoDB started without `--auth` or `security.authorization: enabled`, Elasticsearch without `xpack.security.enabled`; daemons listening on a public interface.

**Bad:**
```yaml
kind: Service
spec:
  type: LoadBalancer        # redis straight to the internet
  ports: [{ port: 6379 }]
```

**Good:**
```yaml
spec:
  type: ClusterIP   # plus requirepass and a NetworkPolicy
---
# NetworkPolicy: apps namespace -> redis:6379 only
```

**References:** CWE-306 Missing Authentication for Critical Function, OWASP A07:2021, Redis security docs, Shodan exposed-database research

