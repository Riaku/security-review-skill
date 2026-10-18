# Segregation of duties in deploy and production operations

**MAY** allow self-merge of production deploys only where compensating controls (automated policy checks, mandatory review bots) exist; otherwise require an independent approver.

**Why:** A single engineer pushing unreviewed changes to production removes the last human check before a mistake or malicious change ships.

**Detect:** check branch protection: `required_approving_review_count`, CODEOWNERS on deploy manifests, whether the same identity authors and approves releases or holds both write and deploy roles.

**References:** NIST SP 800-53 AC-5 Separation of Duties, CWE-265 Privilege Roles Conflict, OWASP ASVS V1.4, SLSA provenance requirements

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [backend](../domains/backend.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)
