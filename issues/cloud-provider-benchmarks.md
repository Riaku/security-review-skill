# Cloud Provider Security Benchmarks (AWS Foundations / Azure / GCP CIS)

**SHOULD** The provider's own framework — AWS Foundational Security Best Practices, Azure Secure Score, GCP CIS recommendations — be continuously evaluated in the native tool rather than spot-checked by hand.

**Why:** Provider frameworks catch platform-specific misconfigurations generic hardening misses: live root keys, audit logging off, IAM users with `*:*`, unencrypted snapshots — each a documented incident pattern.

**Detect:** Confirm Security Hub standards / Defender for Cloud cover every account and subscription, not just the primary one. Check for findings aged past 30 days with no owner and member accounts silently excluded from the aggregator.

**Bad:**
```
# Security Hub enabled in one region of one account; 14 others unmonitored
```

**Good:**
```hcl
# org-wide aggregation: standards enabled per member account via StackSets,
# findings exported to SIEM with an SLA on high severity
```

**References:** AWS Foundational Security Best Practices standard, CIS AWS Foundations Benchmark, Microsoft Defender for Cloud, GCP Security Command Center

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [hardening-benchmarks](../categories/hardening-benchmarks.md) · [infrastructure](../domains/infrastructure.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)
