# CIS Docker Benchmark

**MUST** align container host and daemon configuration with the current CIS Docker Benchmark sections 2 (daemon), 5 (runtime), and 18 (daemon.json) before production deployment.

**Why:** Unhardened Docker defaults expose the socket, permissive logging, and root containers that turn one compromised image into full host takeover.

**Detect:** grep daemon.json for `userns-remap`, `log-driver`, `live-restore`; check `/var/run/docker.sock` permissions and `--privileged` in compose files.

**References:** CIS Docker Benchmark v1.6.0, CIS Controls v8, NIST SP 800-190
