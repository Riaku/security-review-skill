# Runtime Threat Detection (Falco/eBPF-style workload anomaly detection)

**MUST** monitor running workloads at syscall level (Falco/eBPF) for anomalies: shells in containers, unexpected writes, suspicious process spawns.

**Why:** Scanners only see what you built; attackers operate in what's running, and without runtime visibility they work unnoticed inside "secure" images.

**Detect:** grep for `falco`, `sysdig`, `tracee`, `tetragon`, `ebpf` in deployment YAML/DaemonSets, runtime-security rules files, `falco_rules.yaml` customizations.

**References:** MITRE ATT&CK container matrix (T1610), CIS Docker/Kubernetes Benchmarks 5.x, NIST SP 800-190, Falco docs
