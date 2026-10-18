# Rollbacks

**MUST** be rehearsed, one-command operations whose database migrations are backward-compatible or paired with tested down-migrations.

**Why:** An irreversible schema change pins a broken release in production because rolling back the app would corrupt data, extending outage duration.

**Detect:** grep migration folders for down scripts missing or marked irreversible; check deploy manifests for `revisionHistoryLimit` and `kubectl rollout undo` runbook presence.

**References:** NIST SP 800-34 contingency planning, Fowler Parallel Change, CWE-581 group authorization failure on rollback state

---

**Part of:** [deployment-release](../categories/deployment-release.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
