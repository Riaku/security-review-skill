---
categories: [hardening-benchmarks]
domains: [government-compliance]
---

# Kernel/Sysctl Hardening

**MUST** disable source routing, redirect sends, and proxy ARP, and enable `kernel.kptr_restrict=2`, `kernel.yama.ptrace_scope=1`, and ASLR system-wide via sysctl.

**Why:** Default kernel settings leak kernel pointers, allow ptrace of other processes, and permit packet spoofing that aids lateral movement and local privilege escalation.

**Detect:** grep `/etc/sysctl.conf` and `/etc/sysctl.d/*.conf` for `kptr_restrict`, `ptrace_scope`, `rp_filter`, `accept_redirects`, `randomize_va_space`.

**References:** CIS Distro Benchmark sec. 3, CWE-1188, NIST SP 800-123, CWE-200
