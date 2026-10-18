# Host Namespace Sharing (hostPath/hostPID/hostNetwork/hostIPC)

**MUST NOT** set `hostPID`, `hostNetwork`, or `hostIPC` on ordinary workloads; each flag breaks the isolation boundary between pod and node.

**Why:** Shared namespaces expose host processes, sniff node traffic, and let a pod signal or ptrace host-level daemons.

**Detect:** Pod spec keys `hostPID: true`, `hostNetwork: true`, `hostIPC: true`; DaemonSets using them without documented reason.

**References:** CIS K8s 5.2.2-5.2.4, CWE-497, MITRE ATT&CK T1611, K8s docs namespaces
