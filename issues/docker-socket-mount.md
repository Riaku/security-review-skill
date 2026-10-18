# Docker Socket Mounted into Containers

**MUST NOT** expose `/var/run/docker.sock` (or containerd/CRI-O sockets) to application containers; use a scoped proxy or dedicated agent instead.

**Why:** Socket access grants full container-control API, which is trivially equivalent to root on the node and defeats every other control.

**Detect:** Volume mounts of `docker.sock`, `containerd.sock`, or `crio.sock`; env `DOCKER_HOST` pointing at a mounted socket path.

**References:** CIS Docker 2.4, CWE-732, OWASP Top10 A05, NIST SP 800-190 4.4
