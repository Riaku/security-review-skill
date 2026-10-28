# regulatory-frameworks

Audit and regulatory regimes.

## What this category covers

This category covers whether the systems a reviewer sees map to the audit, certification, and statutory regimes that govern them, with evidence attached. Items span control catalogues and management systems, data-protection statutes and cross-border transfer, sector and financial regimes, government and defense authorization, cryptographic and product standards, and adjacent obligations such as export controls, accessibility, and AI regulation. A reviewer should expect to find control IDs, boundary and scope documents, incident-reporting clocks, and the configuration artifacts that are supposed to satisfy each control.

- Control catalogues and management systems — NIST SP 800-53, the NIST CSF, and ISO/IEC 27001 ISMS controls traced to configuration evidence.
- Data-protection statutes and cross-border transfer — GDPR, CCPA/CPRA, LGPD, China PIPL, India DPDP, HIPAA, children's privacy, and SCC or TIA transfer mechanisms.
- Sector and financial regimes — PCI DSS, NYDFS 23 NYCRR 500, DORA, NIS2, CJIS, SEC material-incident disclosure, and cyber-insurance preconditions.
- Government, cloud, and defense authorization — FedRAMP boundaries, CMMC levels, NIST SP 800-171 CUI handling, Australian ISM and IRAP, and Common Criteria evaluation.
- Cryptographic and product standards — FIPS 140-3 validated modules, FIPS 186 signature algorithms, post-quantum migration plans, and the EU Cyber Resilience Act's SBOM and vulnerability-handling duties.
- Adjacent statutory obligations — EU AI Act risk tiering, ITAR and EAR export controls, accessibility conformance (WCAG, EAA, ADA), segregation of duties, and UK GDPR with Cyber Essentials.
- Consumer commerce and marketing statutes — CAN-SPAM email content duties, negative-option renewal disclosure (ROSCA and state auto-renew laws), and DMCA designated-agent registration for services hosting user uploads.

## What it does not cover

- [compliance-privacy](../categories/compliance-privacy.md) — how privacy obligations are implemented in code (data-subject rights, retention, residency, redaction) belongs there; the audit and certification regimes those implementations satisfy are scoped here.
- [hardening-benchmarks](../categories/hardening-benchmarks.md) — technical configuration baselines (CIS, STIG, sysctl, SSH, TLS) belong there; the control catalogues and certifications that cite them are scoped here.
- [payments-fraud](../categories/payments-fraud.md) — payment-flow mechanics, ledger integrity, and retry deduplication belong there; the PCI DSS and financial-sector regimes are scoped here.
- [ai-llm](../categories/ai-llm.md) — prompt safety, agent authority, and model supply chain belong there; EU AI Act risk tiering and conformity obligations are scoped here.

## What a finding here looks like

- A control ID cited in a compliance matrix with no linked code, configuration, or evidence artifact behind it.
- A service inside an authorization boundary processing data above its authorized impact level, or running outside the authorized partition entirely.
- An AI feature in production with no assigned risk tier, transparency notice, or GPAI documentation.
- A control warranted to a cyber insurer (MFA everywhere, EDR deployed, offline backups tested) that is absent from live configuration.
- Export-controlled technical data reachable by foreign-national personnel or deployed to a non-US region without a license or exemption.
- A user-upload feature launched with no registered DMCA agent and no notice-and-takedown workflow.
