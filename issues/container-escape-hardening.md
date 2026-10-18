# Container Escape Hardening

**MUST** minimize syscall surface (seccomp profiles, no unmasked dangerous syscalls, read-only rootfs) so a compromised container cannot break out to the host.

**Why:** Kernel exploits and permissive seccomp/unconfined profiles turn one broken container into full node compromise — the classic escape path Falco and Tracee alert on.

**Detect:** grep manifests for `seccompProfile`, `unconfined`, `unmasked`, `privileged: true`, `CAP_SYS_*`; run `docker run` escape test suites (e.g. cdve).

**References:** CIS Docker 5.3, MITRE ATT&CK T1611, Pod Security Standards restricted
