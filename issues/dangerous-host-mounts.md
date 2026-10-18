# Dangerous Host Mounts: docker.sock, hostPath, Privileged Pods

**MUST NOT** mount host paths such as `/`, `/etc`, or the container runtime socket into untrusted workloads, and MUST NOT mark pods privileged without documented justification.

**Why:** A hostPath or privileged pod is effectively node root access; one compromised app owns the machine and every co-located secret.

**Detect:** `hostPath` volumes pointing at `/etc`, `/proc`, `/var/run/docker.sock`; `privileged: true` in pod manifests.

**References:** CIS K8s 5.2.4, 5.2.5, CWE-668, OWASP K8s PS4, MITRE ATT&CK T1611
