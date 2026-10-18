---
categories: [containers-k8s, hardening-benchmarks]
domains: [government-compliance, infrastructure]
---

# Kubelet Port Protection (10250 AuthN/AuthZ, Anonymous Access)

**MUST NOT** allow anonymous authentication on kubelet port 10250; enable Webhook authorization and firewall the port to control-plane only.

**Why:** An open kubelet API exposes exec, logs, and running-config, letting an attacker run commands in any pod on the node.

**Detect:** `anonymousAuth: true` or `authorizationMode: AlwaysAllow` in kubelet config; 10250 reachable from arbitrary CIDRs; 10255 read-only port open.

**References:** CIS K8s 4.2.1-4.2.3, CWE-306, MITRE ATT&CK T1610, K8s kubelet auth docs

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [hardening-benchmarks](../categories/hardening-benchmarks.md) · [government-compliance](../domains/government-compliance.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
