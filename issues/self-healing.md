# Self-Healing Systems (auto-restart, auto-failover, self-repair loops)

**MAY** automate restart and failover for known failure modes, but each repair loop MUST be bounded, observable, and rate-limited.

**Why:** Unmonitored auto-repair oscillates between nodes and masks root causes until capacity is silently exhausted.

**Detect:** review `restartPolicy`, `livenessProbe`, `auto_failover`, `recovery_loop`; check max-restart backoff and remediation alerting.

**References:** Kubernetes restartPolicy/livenessProbe, AWS REL11-BP10, NIST SP 800-34 auto-recovery, CWE-251

---

**Part of:** [resilience](../categories/resilience.md) · [sre-incidents](../categories/sre-incidents.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
