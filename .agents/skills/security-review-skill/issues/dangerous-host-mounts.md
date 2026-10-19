---
categories: [containers-k8s]
domains: [infrastructure]
---

# Dangerous Host Mounts: docker.sock, hostPath, Privileged Pods

**MUST NOT** mount host paths such as `/`, `/etc`, or the container runtime socket into untrusted workloads, and MUST NOT mark pods privileged without documented justification.

**Why:** A hostPath or privileged pod is effectively node root access; one compromised app owns the machine and every co-located secret — and runtime-socket access grants the full container-control API, trivially equivalent to root on the node.

**Detect:** `hostPath` volumes pointing at `/etc`, `/proc`, `/var/run/docker.sock`; volume mounts of `containerd.sock` or `crio.sock`; env `DOCKER_HOST` pointing at a mounted socket path; `privileged: true` in pod manifests. Remedy: scoped socket proxy or a dedicated agent instead of raw socket exposure.

**References:** CIS K8s 5.2.4, 5.2.5, CWE-668, OWASP K8s PS4, MITRE ATT&CK T1611, CIS Docker 2.4, NIST SP 800-190 4.4
