---
categories: [hardening-benchmarks]
domains: [government-compliance, infrastructure]
---

# SSH Hardening

**MUST NOT** permit root login or password authentication on internet-facing SSH; keys only, with `PermitRootLogin no`, `PasswordAuthentication no`, and modern MACs/ciphers.

**Why:** Password-auth SSH is brute-forced at scale; root login hands attackers the highest-privilege account the moment one credential leaks.

**Detect:** grep `sshd_config` and `sshd_config.d/*` for `PermitRootLogin yes`, `PasswordAuthentication yes`, `Protocol 1`, weak `Ciphers`/`MACs`.

**References:** CIS Distro Benchmark sec. 5, CWE-287, NIST SP 800-123, Mozilla Open SSH config
