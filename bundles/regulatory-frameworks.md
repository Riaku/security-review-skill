# regulatory-frameworks — full checklist (34 items)

Audit and regulatory regimes.

> Generated artifact — edit the issue files, not this one. Sources: [issues/](../issues/) · manifest: [regulatory-frameworks](../categories/regulatory-frameworks.md) · index: [SKILL.md](../SKILL.md)

# Accessibility compliance as regulatory regime (EAA, ADA/WCAG enforcement)

**SHOULD** meet WCAG 2.1 AA conformance for digital products, since the EU's EAA and US ADA litigation treat accessibility as a legal floor, not a courtesy.

**Why:** Demand letters and EAA market-surveillance actions target non-conformant interfaces; retrofitting accessibility post-launch costs multiples of building it in.

**Detect:** grep for "WCAG", "aria-", contrast ratios, keyboard handlers; missing alt text, focus management, automated axe/lighthouse a11y checks.

**References:** WCAG 2.1 AA, EN 301 549, European Accessibility Act, ADA Title III

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# AU ISM / IRAP (Australia)

**MUST** control and monitor the hosting environment per IRAP assessment scope against the Australian ISM baseline for the relevant classification level.

**Why:** Australian government workloads on unassessed cloud fail IRAP review; data residency and hosting-provider controls are checked, not assumed.

**Detect:** grep for "IRAP", "ISM", "PROTECTED", "hosting provider" in deployment docs; AU data in non-assessed regions, missing controls mapping.

**References:** Australian ISM (PSPF), IRAP (Digital Trust Framework), PSPG

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# Breach notification clocks across jurisdictions

**MUST** detect and triage breaches fast enough to meet the strictest applicable notification deadline (72h GDPR, state laws).

**Why:** Missing statutory notification windows compounds breach penalties and destroys regulatory trust after an incident.

**Detect:** grep for incident response SLA timers, `notification_deadline`, `breach_clock` config; check monitoring-to-notification pipeline latency absent.

**References:** GDPR Art. 33, Cal. Civ. Code §1798.82, HIPAA Breach Rule 45 CFR 164.404, NIST SP 800-61

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [sre-incidents](../categories/sre-incidents.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# CCPA/CPRA

**MUST** honor California consumer rights—access, deletion, opt-out of sale/sharing—within statutory deadlines across all systems holding personal information.

**Why:** The CPPA actively enforces via consumer requests and audits; a "Do Not Sell" link without backend enforcement invites per-record penalties.

**Detect:** grep for "CCPA", "Do Not Sell", "opt_out", "deletion request" handlers; missing request routing, service-provider contract clauses, GPC signal support.

**References:** CCPA/CPRA Cal. Civ. Code 1798.100+, CPPA regulations, IAPP CCPA guidance

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# Children's online privacy and age assurance (COPPA, UK Online Safety Act)

**MUST** verify user age and obtain verifiable parental consent before collecting personal data from children, and apply age-appropriate design to likely-child audiences.

**Why:** Self-declared birthdays are trivially bypassed; platforms collecting child data without verification face FTC and OfSan fines and forced redesigns.

**Detect:** grep for "age gate", "birthday only", "COPPA", "children"; no age-verification provider, data collection before consent check.

**References:** COPPA 16 CFR 312, UK Online Safety Act 2023, Age Appropriate Design Code

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# China PIPL (cross-border security assessment, separate consent, localization)

**MUST** obtain separate consent for sensitive processing and complete CAC cross-border security assessment or localization requirements before exporting Chinese personal data.

**Why:** Transferring Chinese user data abroad without CAC approval halts operations and triggers fines up to 5% of revenue plus criminal exposure.

**Detect:** grep for data flows from CN regions to overseas endpoints; missing "separate consent", CAC filing, localization config for CN deployments.

**References:** PIPL (2021), CAC Cross-Border Data Transfer Rules, GB/T 35273

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# CJIS (criminal justice data)

**MUST** apply CJIS Security Policy controls—advanced authentication, audit logging, and personnel screening—to every system touching Criminal Justice Information.

**Why:** Fingerprints, rap sheets, and criminal records flowing through unhardened systems expose sensitive justice data and disqualify agency access entirely.

**Detect:** grep for "CJIS", "ORI", "CHRI" markers; missing MFA, absent audit trails, unencrypted backup media in CJIS-scoped repos.

**References:** CJIS Security Policy v5.9, FBI CJIS Division, NIST SP 800-53

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# CMMC (defense supply chain)

**MUST** achieve the CMMC maturity level required by contract for each enclave processing FCI or CUI, with an assessed scope covering all connected vendor systems.

**Why:** Unassessed subcontractors are the classic supply-chain entry point; one compromised small vendor can expose the entire defense program.

**Detect:** grep vendor contracts/repos for "CMMC", "FCI", "CUI" scope statements; missing maturity evidence, unscoped integrations touching CUI flows.

**References:** CMMC 2.0, NIST SP 800-171, DFARS 252.204-7021

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# Common Criteria

**MAY** pursue Common Criteria evaluation (EAL level) when procuring into government or defense markets that mandate certified product assurance.

**Why:** Without an evaluated assurance level, products face procurement rejection or duplicate customer audits that stall sales for years.

**Detect:** grep product docs for "EAL", "certification ID", "TOE" scope statements; missing evaluation artifacts where tenders require CC.

**References:** Common Criteria ISO/IEC 15408, CCRA, NIAP/CCEVS

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# Cross-border data transfer mechanisms post-Schrems II

**SHOULD** use Standard Contractual Clauses with transfer impact assessments for EU data leaving adequacy-decision countries.

**Why:** Transferring EU data without valid safeguards violates GDPR Chapter V post-Schrems II, risking transfer bans and fines.

**Detect:** grep for EU data flows to non-adequate regions without SCC/TIA references; check `transfer_impact_assessment`, `scc_modules`, `adequacy` config absent.

**References:** GDPR Ch. V, Schrems II (C-311/18), EU SCC 2021/914, EDPB Recommendations 01/2020

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# Cyber insurance alignment: coverage preconditions and denial clauses

**MUST NOT** let representations on insurance applications (MFA everywhere, EDR deployed, backups tested) drift from actual configuration, since denial clauses void claims on misrepresentation.

**Why:** Insurers investigate post-incident and deny payouts when stated controls are absent—leaving the breach cost entirely self-funded.

**Detect:** grep policy "warranty", "condition precedent" against live config: MFA, EDR/antivirus, offline backups, patch SLA mismatches.

**References:** ISO 27001/27017, CVE-based exclusion clauses, Marsh/Gallagher cyber underwriting guidance

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [security-practices](../categories/security-practices.md) · [backend](../domains/backend.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# DORA (financial sector resilience)

**MUST** classify critical ICT functions, test resilience (including TLPT threat-led testing), and register ICT third-party arrangements per DORA timelines.

**Why:** Financial entities failing operational-resilience tests risk forced exit from EU markets; untested backups and ICT vendors are the failure points.

**Detect:** grep for "DORA", "TLPT", "critical functions register", ICT exit plans; missing incident escalation, unregistered ICT providers.

**References:** EU Regulation 2022/2554, ESA RTS/ITS on RTS, EIOPA/EBA guidance

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [sre-incidents](../categories/sre-incidents.md) · [government-compliance](../domains/government-compliance.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# EU AI Act conformity (risk tiering, GPAI obligations, transparency and deployment deadlines)

**MUST** classify each AI system's risk tier and meet the corresponding obligations—transparency notices, conformity assessment for high-risk, GPAI documentation—before the phased enforcement deadlines.

**Why:** Systems deployed without risk classification face market withdrawal and fines up to 7% of turnover once enforcement phases begin.

**Detect:** grep for "high-risk", "GPAI", "Annex III", "conformity", "Article 50 transparency"; AI features with no risk tier or labeling.

**References:** EU AI Act 2024/1689, Annex III, GPAI Code of Practice, EU AI Office

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# EU Cyber Resilience Act (product security lifecycle, SBOM and vulnerability handling duties)

**MUST** ship products with digital elements under a secure development lifecycle, provide an SBOM, and actively handle reported vulnerabilities for the support period.

**Why:** Unpatched connected products become botnet fodder; CRA makes manufacturers legally liable for known vulnerabilities left unfixed.

**Detect:** grep for "SBOM", "CRA", "support period", vulnerability disclosure policy; no CycloneDX/SPDX artifacts, end-of-life products with live CVEs.

**References:** EU CRA 2024/2847, ENISA SBOM guidance, ISO/IEC 30111

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [supply-chain](../categories/supply-chain.md) · [government-compliance](../domains/government-compliance.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# FedRAMP (Low/Moderate/High)

**MUST** map every cloud service consumed by the system to a FedRAMP authorization boundary at the impact level matching the data it processes, with inherited controls documented in the System Security Plan.

**Why:** Operating unauthorized cloud services inside a federal boundary voids the ATO and exposes agency data with no oversight.

**Detect:** grep IaC for AWS/Azure/GCP regions outside FedRAMP-authorized partitions; missing "fedramp", "boundary", "inherit" in compliance docs.

**References:** FedRAMP Rev5, NIST SP 800-53, FedRAMP Marketplace

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# FIPS 140-3 Validated Crypto

**MUST** perform cryptographic operations for regulated data using FIPS 140-3 validated modules rather than unaudited library implementations.

**Why:** Hand-rolled or non-validated crypto looks fine until a subtle implementation flaw breaks confidentiality with no compliance defense.

**Detect:** grep for "fips", "FIPS_MODE", openssl fips provider config; direct MD5/SHA1 usage, custom crypto, non-validated TLS libraries in regulated paths.

**References:** FIPS 140-3, CMVP validated module list, NIST SP 800-175B

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# FIPS 186 / Digital Signature Standards

**SHOULD** generate and verify digital signatures using approved algorithms (ECDSA, RSA per FIPS 186-5) with approved curves and key lengths only.

**Why:** Deprecated curves and short keys make signatures forgeable, undermining code signing, tokens, and non-repudiation guarantees.

**Detect:** grep for signature algorithm config: "RSA-1024", "DSA", "secp112", disabled curves; verify "P-256", "P-384", "RSA-2048+" in signing code.

**References:** FIPS 186-5, NIST SP 800-89, RFC 8785

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# GDPR as Regulatory Regime (enforcement posture, DPO, DPIA)

**MUST** maintain lawful basis, DPO appointment where required, and DPIAs for high-risk processing, since GDPR enforcement is complaint- and breach-driven with fines up to 4% of global turnover.

**Why:** Regulators act on data subject complaints and breach notifications; undocumented processing decisions become the fine's evidence.

**Detect:** grep for "DPIA", "DPO", "lawful basis", "Art. 6/35"; missing records of processing, consent logs, cross-border transfer clauses.

**References:** GDPR Arts. 6, 35, 37; EDPB guidelines; ICO enforcement register

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# HIPAA (health data)

**MUST** safeguard protected health information with access controls, encryption in transit, and audit logs covering every system in the HIPAA covered entity or business associate chain.

**Why:** Unlogged PHI access and plaintext transmissions drive the largest class of healthcare breaches and OCR enforcement actions.

**Detect:** grep for PHI/ePHI handling without encryption/TLS, missing audit logging, third-party analytics SDKs receiving patient data.

**References:** HIPAA Security Rule 45 CFR 164, HHS OCR guidance, NIST HIPAA Security Series

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# India DPDP Act 2023 (consent managers, data fiduciary duties)

**MUST** register consent through a Data Protection Board-consented consent manager and fulfill data fiduciary duties including breach notification and grievance redressal.

**Why:** Processing Indian personal data without compliant consent mechanisms exposes firms to penalties up to 250 crore INR once rules activate.

**Detect:** grep for "DPDP", "consent manager", "data fiduciary", grievance officer; consent captured without registered manager, no breach notification process.

**References:** DPDP Act 2023, DPDP Rules (draft), India Data Protection Board

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# ISO/IEC 27001 ISMS

**MUST** operate an information security management system with documented risk assessment, Statement of Applicability, and continual improvement cycle—not a one-time certification snapshot.

**Why:** Certifications without live risk treatment decay silently; auditors now sample actual controls against the SoA and find drift.

**Detect:** grep for "SoA", "risk register", "Clause 9/10" evidence; stale risk assessments, Annex A controls without owners or reviews.

**References:** ISO/IEC 27001:2022, ISO 27002:2022, ISO 27005

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# ITAR / EAR Export Controls

**MUST NOT** allow foreign persons or overseas infrastructure access to export-controlled technical data without a license or applicable exemption.

**Why:** Uncontrolled cloud regions or offshore contractors touching defense-related designs constitute an illegal export carrying criminal liability.

**Detect:** grep repos for "ITAR", "EAR", "export controlled" markers; code deployed to non-US regions, foreign-national access lists, public mirrors.

**References:** ITAR 22 CFR 120-130, EAR 15 CFR 730-774, DDTC

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# Brazil LGPD compliance

**SHOULD** establish a legal basis for each processing activity, appoint a data protection officer (encarregado), and honor data subject rights under LGPD timelines.

**Why:** Brazil's ANPD has moved to active enforcement; processing personal data without a stated legal basis is now directly sanctionable.

**Detect:** grep for "LGPD", "encarregado", "base legal", rights-request endpoints; missing privacy notices in pt-BR, no DPO contact published.

**References:** LGPD Lei 13.709/2018, ANPD guidelines, ANPD DSR rules

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# EU NIS2 Directive

**MUST** implement risk management, incident reporting within 24/72-hour milestones, and supply-chain security for entities in essential/important sectors.

**Why:** NIS2 makes management personally liable and fines up to 10M EUR; late incident reports compound penalties after an attack.

**Detect:** grep for "NIS2", incident response SLA docs, "24 hours"/"72 hours" reporting; missing supply-chain audits, absent vulnerability disclosure policy.

**References:** EU Directive 2022/2555, ENISA NIS2 guidance, ISO 27001 mapping

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# NIST SP 800-171 (CUI)

**MUST** protect Controlled Unclassified Information at rest and in transit with FIPS-validated encryption and enforce least-privilege access on every system storing or transmitting CUI.

**Why:** Contractors handling CUI without encryption or access scoping become the soft target for state-sponsored theft of defense-related data.

**Detect:** grep for CUI-marked storage without encryption_at_rest, unencrypted exports, shared service accounts; missing "800-171", "CUI" markings.

**References:** NIST SP 800-171 Rev3, DFARS 252.204-7012, FIPS 140-3

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# NIST SP 800-53 Controls

**MUST** implement the selected baseline's control families (AC, AU, IA, SC, SI) with each control traced to a concrete configuration artifact rather than a policy statement alone.

**Why:** Control catalogs without implementation evidence fail audits and leave real gaps like missing audit logging or weak authentication unaddressed.

**Detect:** grep for control IDs (AC-2, AU-6, IA-5) in compliance matrices without linked code/config; absent auditd, MFA, TLS enforcement settings.

**References:** NIST SP 800-53 Rev5, SP 800-53B baselines, FedRAMP

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# NIST Cybersecurity Framework (CSF)

**SHOULD** cover all five functions—Identify, Protect, Detect, Respond, Recover—with at least one measurable activity per category, so governance gaps surface before incidents do.

**Why:** Frameworks applied only as marketing checklists leave detection and response capabilities unbuilt when breaches arrive.

**Detect:** grep docs for "Identify", "Protect", "Detect", "Respond", "Recover" categories; missing SIEM, incident runbook, asset inventory artifacts.

**References:** NIST CSF 2.0, NIST SP 800-53, CIS Controls

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# NYDFS 23 NYCRR 500 (financial services cyber requirements)

**MUST** maintain a CISO program, MFA on all externally accessed systems, and report covered cyber events to DFS within 72 hours under the amended rule.

**Why:** DFS audits NY-regulated firms directly; missing MFA or late 72-hour reports produce consent orders with personal officer accountability.

**Detect:** grep for "NYDFS", "500.17", "72 hours", CISO designation; MFA gaps on VPN/admin access, no DFS reporting runbook.

**References:** 23 NYCRR 500 (amended 2023), NYDFS guidance, Part 500 FAQ

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# PCI DSS as Audit Regime (SAQ, CDE scoping)

**MUST** scope the cardholder data environment accurately and complete the correct SAQ level (or full ROC) for the actual card data flow, not the desired one.

**Why:** Under-scoped CDEs are the most common PCI failure: one stray database storing PANs drags the whole network into breach liability.

**Detect:** grep for "PAN", "cardholder", "CDE", "SAQ-" in configs; card data in logs, unsegmented networks, SAQ type mismatched to flow.

**References:** PCI DSS v4.0.1, SAQ A-D, PCI SSC scoping guidance

---

**Part of:** [payments-fraud](../categories/payments-fraud.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# Post-quantum cryptography migration plan and crypto-agility

**SHOULD** maintain a documented PQC migration plan and crypto-agile design (algorithm negotiation, centralized crypto config) so ciphers can be swapped without rewrites.

**Why:** Systems hard-coded to RSA/ECC today cannot absorb the eventual quantum break of current public-key crypto without costly emergency rework.

**Detect:** Hardcoded `RSA-2048`/`ECDH P-256` with no config indirection, absence of `ML-KEM`/`X25519` hybrid plans, TLS library pinned without upgrade path.

**References:** NIST FIPS 203/204/205, NIST IR 8547 PQC migration, NSA CNSA 2.0

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# SEC cybersecurity disclosure rules (public-company material incident reporting)

**MUST** disclose material cybersecurity incidents within four business days of a materiality determination via Form 8-K Item 1.05, with board-level oversight documented.

**Why:** Delayed or vague disclosure after a breach invites SEC enforcement, shareholder suits, and restatements of prior risk statements.

**Detect:** grep for "8-K", "Item 1.05", materiality assessment process; no incident-to-disclosure workflow, missing disclosure committee charter.

**References:** SEC 8-K Item 1.05 (2023), Reg S-K Item 106, SEC cyber disclosure guidance

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [sre-incidents](../categories/sre-incidents.md) · [government-compliance](../domains/government-compliance.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Segregation of duties in deploy and production operations

**MAY** allow self-merge of production deploys only where compensating controls (automated policy checks, mandatory review bots) exist; otherwise require an independent approver.

**Why:** A single engineer pushing unreviewed changes to production removes the last human check before a mistake or malicious change ships.

**Detect:** check branch protection: `required_approving_review_count`, CODEOWNERS on deploy manifests, whether the same identity authors and approves releases or holds both write and deploy roles.

**References:** NIST SP 800-53 AC-5 Separation of Duties, CWE-265 Privilege Roles Conflict, OWASP ASVS V1.4, SLSA provenance requirements

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [backend](../domains/backend.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# SOC 2 as Audit Regime (CCs, evidence collection)

**SHOULD** collect continuous, timestamped evidence for Trust Services Criteria (security, availability, confidentiality) rather than assembling artifacts only at audit time.

**Why:** Point-in-time evidence gathering misses control gaps during the period; auditors sample exceptions the team never noticed.

**Detect:** grep for "TSC", "CC6", "CC7" mappings; missing access review logs, change tickets, monitoring alerts as evidence; manual-only evidence folders.

**References:** AICPA TSC 2017, SOC 2 Type II, Trust Services Criteria

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# UK GDPR + Cyber Essentials / Cyber Essentials Plus

**SHOULD** pair UK GDPR data controls with Cyber Essentials' four technical controls (secure config, boundary firewalls, access control, patching), verified externally for CE+.

**Why:** UK insurers and public-sector buyers reject suppliers lacking CE; basic misconfigurations cause most breaches it targets.

**Detect:** grep for default credentials, open SSH/RDP, missing patch cadence, absent firewall rules; no "Cyber Essentials" cert or scope doc.

**References:** UK GDPR, NCSC Cyber Essentials v3.1, ICO guidance

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

