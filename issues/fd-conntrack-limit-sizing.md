---
categories: [cloud-network, containers-k8s]
domains: [infrastructure]
---

# File descriptor and conntrack table limits sized for peak

**SHOULD** size file-descriptor limits and conntrack tables above measured peak concurrency with headroom, and alert before the ceiling is hit rather than after.

**Why:** A busy proxy hitting `ulimit -n` starts refusing connections with `EMFILE`, and a full `nf_conntrack` table silently drops new flows — both look like mysterious upstream flakiness while capacity metrics still show idle CPU.

**Detect:** Compare `ulimit -n` / `fs.file-max` and container `no-new-privileges` securityContext defaults against peak connection counts; check `net.netfilter.nf_conntrack_max` versus `nf_conntrack_count` (watch for `nf_conntrack: table full, dropping packet` in dmesg). In Kubernetes, review Pod `ulimit` inheritance, kube-proxy conntrack settings, and whether monitoring exports fd/conntrack saturation.

**Bad:**
```
# 100k concurrent proxy on default 1024 fds
$ ulimit -n
1024
```

**Good:**
```
# sized for peak + 3x headroom, alarmed at 70%
ulimit -n 65536
sysctl -w net.netfilter.nf_conntrack_max=524288
```

**References:** Netflix tuning guides, Netfilter conntrack docs, Google SRE Book (capacity monitoring), USE method
