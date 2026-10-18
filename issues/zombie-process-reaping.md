---
categories: [containers-k8s, correctness-pitfalls]
domains: [backend, infrastructure]
---

# Zombie Process Reaping Handled in Container PID 1

**MUST** ensure the container's PID 1 reaps orphaned child processes, via an init system (tini/dumb-init) or a reaping-aware entrypoint.

**Why:** A non-reaping PID 1 lets zombies accumulate until the PID limit is hit, blocking new process spawns and stalling the container.

**Detect:** Container PID 1 is a shell or app without `--reaping`; `docker top`/`ps` shows defunct `<defunct>` entries; no tini/dumb-init in image.

**References:** CIS Docker 5.x, CWE-459, tini/dumb-init docs, Kubernetes init container patterns

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [correctness-pitfalls](../categories/correctness-pitfalls.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
