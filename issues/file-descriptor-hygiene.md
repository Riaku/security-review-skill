---
categories: [correctness-pitfalls]
domains: [backend]
---

# File Descriptor Hygiene

**MUST** open every descriptor that carries secrets or privileged handles close-on-exec, so spawned child processes cannot inherit them.

**Why:** An inherited descriptor is a live handle to a secret in a process that was never granted it, and it survives long after the request that opened it.

**Detect:** grep `open(`, `socket(`, `os.Open`, `FileStream` for missing `O_CLOEXEC`/`FD_CLOEXEC`/close-on-exec, prioritising descriptors for key material, database sockets and log files; flag subprocess spawns that inherit the full descriptor table.

**References:** SEI CERT C Coding Standard, https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard
