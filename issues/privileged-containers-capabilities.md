---
categories: [containers-k8s, hardening-benchmarks]
domains: [government-compliance, infrastructure]
---

# Privileged Containers and Excess Linux Capabilities

**SHOULD NOT** grant capabilities beyond the app's proven need; drop all by default and add back only what fails without them.

**Why:** Extra caps like `SYS_ADMIN` or `SYS_MODULE` approximate full privilege and enable container escape or kernel module loading.

**Detect:** `securityContext.capabilities.add` listing `SYS_ADMIN`, `NET_ADMIN`, `SYS_MODULE`; `privileged: true` without an exception record.

**References:** CIS K8s 5.2.9 (added capabilities), CAP(7), MITRE ATT&CK T1611, CWE-250
