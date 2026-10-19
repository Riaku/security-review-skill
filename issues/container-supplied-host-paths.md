---
categories: [containers-k8s]
domains: [infrastructure]
---

# Container Paths On The Host

**MUST** canonicalize and confine every container-supplied path before a host-side operation resolves it.

**Why:** Privileged host-to-container interactions resolve paths chosen inside the container, so a crafted path redirects a host operation across the isolation boundary.

**Detect:** grep daemon and plugin code for host operations on container-provided paths without clean-plus-prefix confinement (`os.Open(hostPath + req.Path)`, unvalidated `mount --bind` source).

**References:** Bulkhead container path resolution, https://arxiv.org/abs/2607.12723, CWE-22 (Path Traversal)
