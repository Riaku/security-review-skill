# Docker-in-Docker / Privileged Build Steps in CI

**SHOULD** replace privileged Docker-in-Docker with rootless or daemonless builders (BuildKit, Kaniko, Buildah) since `privileged: true` grants the container host-level control.

**Why:** A privileged build container can escape to the runner host and capture every credential and workload on it.

**Detect:** Grep workflows for `privileged: true`, `docker:dind` images, or volume mounts of `/var/run/docker.sock` into build jobs.

**References:** OWASP Docker DS01, CWE-250, NIST SP 800-218 PW.5, Kaniko and BuildKit rootless docs, GitLab CI best practices
