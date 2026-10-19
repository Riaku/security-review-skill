# security-practices

Process-level security practices (modeling, disclosure, patching).

## What this category covers

This category covers the organizational and process controls around a system rather than a single line of code: how threats are found before release, how exposure is minimized and continuously inventoried, how code ships secure by default, and how findings and incidents are handled afterward. The items span design-time practice (threat modeling, secure by design, defense in depth, zero trust, fail-secure configuration, secure-by-default shipping), verification and assurance (attack-path analysis, breach and attack simulation, purple teaming, penetration-testing cadence, verification-level tiers), and operational security (patch-management timelines, attack-surface management and reduction, abuse of legitimate system binaries, admin activity review, privileged-action attribution, break-glass procedure). They also cover documentation and provenance (architecture docs and ADRs, decision records kept with the code they govern), program structure (security champions, vulnerability disclosure), and specific process exposures such as untrusted LLM output and coding-agent permissions. Expect findings about a control that exists on paper but not in practice, or a process gap with no owner.

- Design-time practice: threat modeling, secure by design, defense in depth, zero trust, and fail-secure defaults.
- Assurance and testing: attack-path analysis, breach and attack simulation, purple teaming, penetration-testing cadence, and verification tiers.
- Operational security: patch-management timelines, attack-surface management and reduction, abuse of legitimate system binaries, admin activity review, privileged-action attribution, and break-glass access.
- Documentation and provenance: architecture overviews and ADRs, and decision records that stay with the code they govern.
- Program and response: security champions, vulnerability disclosure, cyber-insurance alignment, coding-agent sandboxing, and untrusted LLM output.
- Risk-proportionate process: QA and review rigor tiered to the impact of the change, and one-off admin tasks run from the released artifact.

## What it does not cover

- [testing-strategy](../categories/testing-strategy.md) — the automated tests and CI gates that verify controls belong there.
- [authorization-access-control](../categories/authorization-access-control.md) — concrete access-control mechanisms belong there rather than the program that governs them.
- [compliance-privacy](../categories/compliance-privacy.md) — specific regulatory obligations and privacy handling belong there.
- [web-api-security](../categories/web-api-security.md) — the concrete application-layer attack surface belongs there rather than the process around it.

## What a finding here looks like

- A service in production with no threat model covering its trust boundaries.
- A critical dependency CVE left past the stated remediation target, with the exception unlogged and unowned.
- An administrative action that cannot be attributed to a named individual because it ran under a shared account.
- A base image that keeps shipping known-exploitable CVEs because nothing rebuilds and redeploys it.
- A published disclosure policy with no monitored intake channel behind it.
