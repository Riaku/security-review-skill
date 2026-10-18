# Helm Hook Ordering and Failed-Hook Release Blocking

**MUST** set `hook-weight` and `hook-delete-policy` explicitly so migrations run before workloads, and treat a failed hook as a release blocker rather than a warning.

**Why:** If a DB migration hook fails but the release proceeds, new pods start against an unmigrated schema and corrupt or reject data immediately.

**Detect:** grep chart `helm.sh/hook` annotations for missing `hook-weight` ordering, absent `hook-delete-policy`, and `--no-hooks`/`--disable-hook-fail` flags in CI deploy steps.

**References:** Helm hooks docs, CWE-664 improper control of resource lifecycle, NIST SP 800-190 change control

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [deployment-release](../categories/deployment-release.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
