# Self-Healing Systems (auto-restart, auto-failover, self-repair loops)

**SHOULD** automate restart and failover only for known failure modes, keeping each repair loop bounded, observable, and rate-limited.

**Why:** Unmonitored auto-repair oscillates between nodes and masks root causes until capacity is silently exhausted.

**Detect:** review `restartPolicy`, `livenessProbe`, `auto_failover`, `recovery_loop`; check max-restart backoff and remediation alerting.

**References:** Kubernetes restartPolicy/livenessProbe, NIST SP 800-34 auto-recovery