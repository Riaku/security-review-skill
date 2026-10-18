# Runtime Threat Detection (Falco/eBPF-style workload anomaly detection)

**MUST** monitor running workloads at syscall level (Falco/eBPF) for anomalies: shells in containers, unexpected writes, suspicious spawns.

**Why:** Scanners only see what you built; attackers operate in what's running, working unnoticed inside otherwise "secure" images.

**Detect:** grep for `falco`, `tracee`, `tetragon`, `sysdig`, `ebpf` in DaemonSets/deployment YAML, custom `falco_rules.yaml` files.

**References:** MITRE ATT&CK container matrix T1610, CIS Docker/Kubernetes Benchmarks 5.x, NIST SP 800-190, Falco docs
