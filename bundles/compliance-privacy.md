# compliance-privacy — full checklist (34 items)

Privacy operations and data protection in code.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/compliance-privacy.md](../categories/compliance-privacy.md) · Index: [SKILL.md](../SKILL.md)

# Audit Logs

**MUST** record security-relevant events (auth, access, privilege changes) with tamper-evident integrity and retention aligned to policy; **SHOULD** keep compliance-relevant audit evidence on append-only/WORM storage with integrity hashing or signing and documented custody, so insider tampering is detectable.

**Why:** Missing or mutable audit trails prevent incident reconstruction and violate compliance requirements for non-repudiation.

**Detect:** grep for auth/access handlers missing audit calls; check `audit_log`, `log_event`, HMAC signing, retention config absent; check log destinations for immutability (S3 Object Lock, BigQuery time-travel, hash-chained logs), verify hash/signature chain continuity, and confirm audit-log deletion is itself alarmed.

**References:** CWE-778, NIST SP 800-92, AWS S3 Object Lock WORM, SOC 2 CC7.2/CC4, PCI DSS 10.2

# Breach notification clocks across jurisdictions

**MUST** detect and triage breaches fast enough to meet the strictest applicable notification deadline (72h GDPR, state laws).

**Why:** Missing statutory notification windows compounds breach penalties and destroys regulatory trust after an incident.

**Detect:** grep for incident response SLA timers, `notification_deadline`, `breach_clock` config; check monitoring-to-notification pipeline latency absent.

**References:** GDPR Art. 33, Cal. Civ. Code §1798.82, HIPAA Breach Rule 45 CFR 164.404, NIST SP 800-61

# CCPA/CPRA

**MUST** honor California consumer rights—access, deletion, opt-out of sale/sharing—within statutory deadlines across all systems holding personal information.

**Why:** The CPPA actively enforces via consumer requests and audits; a "Do Not Sell" link without backend enforcement invites per-record penalties.

**Detect:** grep for "CCPA", "Do Not Sell", "opt_out", "deletion request" handlers; missing request routing, service-provider contract clauses, GPC signal support.

**References:** CCPA/CPRA Cal. Civ. Code 1798.100+, CPPA regulations, IAPP CCPA guidance

# Children's online privacy and age assurance (COPPA, UK Online Safety Act)

**MUST** obtain verifiable parental consent before collecting personal data from under-13 US users (COPPA, 16 CFR 312), and where UK users are likely to be children apply the age-appropriate design code and use age verification or age estimation that is highly effective at determining whether a user is a child (Online Safety Act 2023 s.12(6)).

**Why:** Self-declared birthdays are trivially bypassed; platforms collecting child data without verification face FTC, Ofcom, and ICO fines and forced redesigns.

**Detect:** grep for "age gate", "birthday only", "COPPA", "children"; no age-verification provider, data collection before consent check.

**References:** COPPA 16 CFR 312, UK Online Safety Act 2023, Age Appropriate Design Code

# China PIPL (cross-border security assessment, separate consent, localization)

**MUST** use one of PIPL Art. 38's transfer mechanisms (CAC security assessment, CAC standard-contract filing, or PI-protection certification) where the Art. 40 thresholds apply, obtain separate consent for sensitive PI (Art. 29) and for the cross-border transfer (Art. 39), and localise within China where Art. 40 applies.

**Why:** Transferring Chinese user data abroad without CAC approval halts operations and triggers fines up to 5% of revenue plus criminal exposure.

**Detect:** grep for data flows from CN regions to overseas endpoints; missing "separate consent", CAC filing, localization config for CN deployments.

**References:** PIPL (2021), CAC Cross-Border Data Transfer Rules, GB/T 35273

# Cookie Consent

**SHOULD** block non-essential cookies until explicit user consent is obtained, with granular category controls.

**Why:** Setting tracking cookies before consent violates ePrivacy Directive and GDPR, exposing sites to regulatory fines and user distrust.

**Detect:** grep for analytics/advertising cookie initialization before consent check; inspect `CookieConsent`, `googleAnalytics`, `fbq` calls preceding consent gate.

**References:** ePrivacy Directive Art. 5(3), GDPR Recital 30, IAB TCF v2.3

# Cross-border data transfer mechanisms post-Schrems II

**SHOULD** use Standard Contractual Clauses with a documented transfer impact assessment for EU/EEA personal data transferred to a country without an adequacy decision.

**Why:** Transferring EU data without valid safeguards violates GDPR Chapter V post-Schrems II, risking transfer bans and fines.

**Detect:** grep for EU data flows to non-adequate regions without SCC/TIA references; check `transfer_impact_assessment`, `scc_modules`, `adequacy` config absent.

**References:** GDPR Ch. V, Schrems II (C-311/18), EU SCC 2021/914, EDPB Recommendations 01/2020

# Data Classification & Labeling (PII/confidential tagged at rest and in pipelines)

**SHOULD** tag PII and confidential data at creation and carry labels through storage and ETL so downstream controls act on them.

**Why:** Ungoverned data spreads into logs, analytics, and backups unnoticed, turning a small leak into a regulatory breach.

**Detect:** grep `data_classification`, `pii_tagging`, Macie sensitive-data jobs, dbt `pii: true` tags.

**References:** NIST SP 800-122, GDPR Art. 4/32

# Data Residency

**MUST** store and process data within the geographic boundaries mandated by applicable regulation or customer contract.

**Why:** Storing data in unauthorized jurisdictions violates sovereignty laws and can trigger regulatory enforcement or contract breach.

**Detect:** grep for region/zone config in storage, compute, CDN settings; check `data_residency`, `region_constraint`, `geo_fence` keys absent or misconfigured.

**References:** GDPR Ch. V, Russian 152-FZ, China PIPL Art. 40, ISO 27018

# Data Retention, Erasure & Tenant Offboarding Purge

**MUST** automatically delete personal data when its retention period expires or a deletion request arrives, and propagate and verify the deletion across every secondary copy: search indexes, caches, analytics, replicas, export buckets, and backups; a departing tenant's data **MUST** be purged from primary stores, replicas, caches, search indexes, analytics, backups policy, and third-party processors, with verification and attestation evidence that the purge completed.

**Why:** Hoarding data beyond its purpose violates GDPR/CCPA erasure obligations and enlarges the breach blast radius — you cannot leak what you no longer hold. Offboarded tenant data lingering in a warehouse layer or search index is the same breach waiting to be discovered, and "we deleted the account" rarely means everything.

**Detect:** Grep for retention jobs (`DELETE ... WHERE created_at < ...`), tombstone/outbox patterns feeding replicas, and whether deletion covers search indexes and backup expiry; map the erasure workflow against a datastore inventory and require every store to have a verified delete-by-user step. A delete endpoint touching only the primary table is a gap. For offboarding, review the tenant purge runbook and code against the actual datastore inventory, look for orphaned tenant rows (`SELECT tenant_id ... GROUP BY` compared with the active-tenant set), and confirm a purge verification/attestation step exists.

**Bad:**
```python
@app.delete("/users/{id}")
def delete_user(id):
    db.users.delete(id)   # analytics replica keeps the row
```

**Good:**
```python
db.users.mark_deleted(id)          # tombstone
outbox.publish("user.deleted", id) # replicas, index, cache
```

**References:** GDPR Art. 17 Right to Erasure (and Art. 19 notification), CCPA deletion, NIST SP 800-53 SI-12 / AU-11, ISO 27018, SOC 2 CC6, OWASP Multi-Tenant Security Cheat Sheet

# DSAR Fulfillment (GDPR access/deletion requests)

**MUST** provide a verified mechanism to retrieve and erase all personal data for a data subject within one month of request (extendable by two further months for complex requests), including a machine-readable export (JSON/CSV) of the data the subject provided and that is processed on consent or contract (GDPR Art. 20).

**Why:** Inability to fulfill DSARs violates GDPR Articles 15/17 and invites regulatory enforcement and subject complaints.

**Detect:** grep for missing DSAR endpoints or deletion jobs; check `dsar`, `right_to_erasure`, `data_export` handlers, SLA timers absent; review export coverage against the datastore inventory (the Art. 20 export must cover provided data while the Art. 15 response covers activity/logs/derived records) and confirm the self-service export is access-controlled.

**References:** GDPR Art. 15, GDPR Art. 17, GDPR Art. 20 (portability), GDPR Art. 12(3), ISO 27701 §9, DSAR platform docs

# Excessive Data Exposure in API Serialization

**MUST NOT** serialize whole ORM/model objects to API responses; project an explicit DTO containing only intended fields.

**Why:** Returning full models leaks password hashes, internal IDs, and PII that the UI never asked for but every caller now receives.

**Detect:** `jsonify(user)` / `resp.json(model)` patterns; serializers without field allowlists; `password`/`ssn` keys in response bodies.

**References:** OWASP API3:2023, CWE-213

# GDPR

**MUST** process personal data of EU residents only under a documented lawful basis, with data minimization enforced at collection, and maintain the accountability artifacts regulators expect: DPO appointment where required (Art. 37), DPIAs for high-risk processing (Art. 35), and records of processing.

**Why:** Unlawful processing exposes organizations to fines up to 4% of global annual turnover under GDPR Article 83 — and enforcement is complaint- and breach-driven, so undocumented processing decisions become the fine's evidence.

**Detect:** grep for personal data fields collected without consent flags; check privacy policy config, `lawful_basis`, `consent_required` keys absent from data models; missing DPIAs, DPO designation, records of processing, consent logs, cross-border transfer clauses.

**References:** GDPR Arts. 5, 6, 35, 37, 83; ISO 27701; EDPB guidelines; ICO enforcement register

# HIPAA (health data)

**MUST** safeguard protected health information with access controls, encryption in transit, and audit logs covering every system in the HIPAA covered entity or business associate chain.

**Why:** Unlogged PHI access and plaintext transmissions drive the largest class of healthcare breaches and OCR enforcement actions.

**Detect:** grep for PHI/ePHI handling without encryption/TLS, missing audit logging, third-party analytics SDKs receiving patient data.

**References:** HIPAA Security Rule 45 CFR 164, HHS OCR guidance, NIST HIPAA Security Series

# India DPDP Act 2023 (consent managers, data fiduciary duties)

**MUST** honour consent given, managed, reviewed, or withdrawn through a Consent Manager registered with the Data Protection Board of India, and fulfill data fiduciary duties including breach notification and grievance redressal.

**Why:** Processing Indian personal data without compliant consent mechanisms exposes firms to penalties up to 250 crore INR once rules activate.

**Detect:** grep for "DPDP", "consent manager", "data fiduciary", grievance officer; consent captured without registered manager, no breach notification process.

**References:** DPDP Act 2023, DPDP Rules 2025, India Data Protection Board

# Joiner-mover-leaver access revocation (offboarding and role change hygiene)

**MUST** revoke all access within a defined SLA (24h) on termination, and re-evaluate entitlements on every internal transfer — movers are as risky as leavers.

**Why:** Stale accounts are the top initial-access vector in breaches; role changes silently accumulate permissions nobody removes.

**Detect:** audit exports comparing HR roster to IdP groups; grep for active accounts with no recent login, local admin accounts outside SSO, orphaned SSH keys and API tokens.

**References:** NIST SP 800-53 AC-2(j) account monitoring, CWE-287, OWASP A07:2021, Cloud Security Alliance JML guidance

# Brazil LGPD compliance

**SHOULD** establish a legal basis for each processing activity, appoint a data protection officer (encarregado), and honor data subject rights under LGPD timelines.

**Why:** Brazil's ANPD has moved to active enforcement; processing personal data without a stated legal basis is now directly sanctionable.

**Detect:** grep for "LGPD", "encarregado", "base legal", rights-request endpoints; missing privacy notices in pt-BR, no DPO contact published.

**References:** LGPD Lei 13.709/2018, ANPD guidelines, ANPD DSR rules

# Litigation Hold Capability

**SHOULD** be able to suspend retention/deletion policies on demand for legal preservation (litigation hold) across all data stores and logs.

**Why:** Automated retention deletion that can't be paused becomes spoliation of evidence; legal needs a kill-switch on the shredder.

**Detect:** review retention jobs for a hold flag respected at deletion time; check backup lifecycle, log rotation, and SaaS retention can be frozen per custodian/case; verify hold procedure is documented and tested.

**References:** EDRM (edrm.net), FRCP 37(e), NIST SP 800-53 SI-12/AU-11, legal hold vendor docs (Exterro, Relativity)

# PII redaction and DPAs before sending data to third-party LLM APIs

**MUST** redact or tokenize PII and execute a DPA with the provider before payloads leave the trust boundary.

**Why:** Personal data reaching an external model API may be logged, retained, or trained on beyond compliance scope.

**Detect:** outbound LLM calls without redaction middleware; missing DPA or zero-retention agreement in vendor records.

**References:** GDPR Art. 28, OWASP LLM02:2025, NIST Privacy Framework

# Interactive-Session Artifact Leakage

**MUST NOT** commit interactive-session artifacts (notebooks with executed outputs, REPL dumps, workspace snapshots) that embed the actual data processed during the session.

**Why:** Executed notebooks persist every row/chart they touched inside the committed file — sensitive data ships silently with code review, forks, and clones, invisible to diff tools that show only code.

**Detect:** grep tracked notebook/JSON files for embedded result payloads (`"outputs"`, base64 blobs, table rows); check for output-stripping pre-commit hooks or CI checks on committed notebooks.

**References:** Jupyter notebook security best practices, nbstripout/ClearOutputPreprocessor tooling

# NYDFS 23 NYCRR 500 (financial services cyber requirements)

**MUST** maintain a CISO program, MFA on all externally accessed systems, and report covered cyber events to DFS within 72 hours under the amended rule.

**Why:** DFS audits NY-regulated firms directly; missing MFA or late 72-hour reports produce consent orders with personal officer accountability.

**Detect:** grep for "NYDFS", "500.17", "72 hours", CISO designation; MFA gaps on VPN/admin access, no DFS reporting runbook.

**References:** 23 NYCRR 500 (amended 2023), NYDFS guidance, Part 500 FAQ

# Object-Level Data Access Logging

**SHOULD** enable data-plane (object/bucket-level) read and write logging on object storage holding sensitive data, not just control-plane API logging — management-plane logs record who created the bucket, but never who read the objects inside it.

**Why:** Object stores default to control-plane-only logging; a bulk exfiltration of customer records via thousands of `GetObject` calls is invisible until data-plane logging is turned on — after the incident. Compliance regimes (PCI, HIPAA, GDPR access-record duties) and forensic timelines both hinge on per-object access records that control-plane logs simply do not contain.

**Detect:** S3 server access logging or CloudTrail data events (`ReadOnly`/`WriteOnly` for the bucket prefix) enabled; GCS bucket audit configuration with `DATA_READ`/`DATA_WRITE` enabled; Azure Storage diagnostic settings including Read/Write/DELETE operations. Flag buckets with lifecycle policies but no data-event logging, and flag logging enabled only at management-event scope.

**References:** AWS S3 data events / server access logging docs, GCP Cloud Storage audit logging, Azure Storage diagnostics, CIS AWS 3.x (logging), aquasecurity/trivy-checks storage logging rules

# PCI DSS

**MUST NOT** store sensitive authentication data (full track, CVV, PIN block) after authorization completes.

**Why:** Retaining cardholder authentication data massively expands breach impact and violates contractual obligations with card brands.

**Detect:** grep for `cvv`, `track_data`, `pin_block` persisted post-auth; check database schemas, logs, and backups for prohibited fields.

**References:** PCI DSS 3.2.1 Req 3.2, PCI DSS 4.0 Req 3.3.1, CWE-312

# PII Handling

**SHOULD NOT** transmit or store unencrypted personally identifiable information outside designated secure stores.

**Why:** Unencrypted PII in transit or at rest enables mass identity theft and triggers mandatory breach disclosure obligations.

**Detect:** grep for SSN, email, phone fields serialized without encryption; check TLS enforcement, `encrypt_pii`, field-level encryption config keys.

**References:** CWE-311, CWE-312, NIST SP 800-122, GDPR Art. 32

# PII Propagation & Warehouse Lineage

**SHOULD** track where PII flows through warehouse layers (raw→staging→marts→exports) with lineage, and enforce classification at each hop.

**Why:** PII copied into analytics tables, temp datasets, and BI exports silently multiplies copies beyond the retention and access controls that protect the source.

**Detect:** review lineage tooling (OpenLineage, dbt lineage, DataHub/Collibra) for PII-tagged datasets; sample staging/mart tables for unclassified columns containing emails/ids; check export destinations inherit classification.

**References:** OpenLineage spec, GDPR Art. 5(1)(c) data minimisation, Snowflake/BigQuery data-classification docs

# PII & Secrets Leakage into Application Logs

**MUST** redact passwords, tokens, API keys, and PII at the logging layer before anything reaches disk or an aggregator.

**Why:** Logs are widely readable and long-retained, making them the easiest place for attackers — and auditors — to harvest credentials and personal data; unredacted request bodies, headers, and stack traces spread PII into traces and error-reporters as secondary sinks.

**Detect:** Grep logs and appenders for `password`, `authorization`, `id_card`, `redact`, `mask`; grep for `log.*request`, `log.*body`, `console.log(err)` without redaction and missing `redact_fields`/`mask_pii` filter config. Test by logging a known secret and checking it never appears in logs, traces, or error-reporter payloads.

**References:** OWASP Logging Cheat Sheet, CWE-532, CWE-200, PCI DSS 3.2.1 Req 3, GDPR Art. 5(1)(c), NIST SP 800-92

# Privileged access management: JIT access, break-glass, session recording

**SHOULD** issue privileged access just-in-time with expiry and approval, and record break-glass sessions for review.

**Why:** Standing admin credentials are always in an attacker's blast radius; JIT shrinks the window and recordings make misuse provable.

**Detect:** grep for long-lived admin API keys, shared root SSH access, `sudo` without logging; check PAM tool coverage, session-recording config, break-glass runbook existence.

**References:** NIST SP 800-53 AC-6(1)(2)(9) least privilege + JIT, CWE-250, OWASP A07:2021 Identification and Authentication Failures

# Privileged-Action Attribution

**MUST** ensure every privileged action is attributable to a named individual — no shared admin accounts, no service-account interactive use.

**Why:** Shared root/admin credentials destroy non-repudiation; when an incident happens, "admin did it" is not an answer.

**Detect:** grep for shared `admin`/`root` logins in auth logs config, team password vaults for infra creds, kubectl exec under shared identities; check SSO with per-user identity to admin planes.

**References:** NIST SP 800-53 AC-6/IA-2, SOX ITGC segregation of duties, CIS 5.4 no shared administrator accounts

# Anonymization vs pseudonymization and re-identification risk in shared datasets

**MUST NOT** describe a dataset as anonymous unless re-identification is infeasible with auxiliary data; pseudonymized data — reversible keys, stable IDs — remains personal data under GDPR.

**Why:** Substituting user IDs is not anonymization. Linking "anonymized" exports against public sources (voter rolls, breach dumps, location traces) routinely re-identifies people, as the Netflix Prize showed.

**Detect:** Review shared exports for stable identifiers and quasi-identifiers (birth date + ZIP + gender), and whether k-anonymity or differential privacy was applied. Check whether the agreement's claimed classification matches custody of the mapping table.

**Bad:**
```python
export = df[["user_id", "zip", "dob", "purchase"]]  # "anonymous"
# join zip+dob against voter file -> names
```

**Good:**
```python
export = anonymize(df, k=20,
    generalize={"dob": "year", "zip": "5->3"})
# or differential-privacy aggregates, not row-level release
```

**References:** GDPR Recital 26 (anonymised vs pseudonymised), NIST SP 800-188 De-Identifying Datasets, Narayanan & Shmatikov

# Serverless Execution Environment Reuse Leaking Data Across Invocations

**MUST NOT** cache per-request data — customer records, tokens, decrypted keys — in module-level or global mutable state of a serverless function, because warm containers are shared by later, possibly different, invocations.

**Why:** Lambda and friends reuse a warmed container across tenants' requests when concurrency allows; a global populated during request A can be read during request B, producing cross-customer data disclosure that only appears under load.

**Detect:** In Lambda/Cloud Function/Cloud Run code, flag module-scope dicts, lists, or connection objects that store request-derived values (`current_user = None` at top level then assigned inside the handler), memoized decryption caches keyed loosely, and background threads outliving the handler. Contrast with connection pools (acceptable) versus data caches (not).

**Bad:**
```python
cached_profile = None          # module scope, survives invocations
def handler(event, ctx):
    global cached_profile
    cached_profile = fetch_profile(event["user_id"])
    return {"sso": cached_profile["email"]}
```

**Good:**
```python
def handler(event, ctx):
    profile = fetch_profile(event["user_id"])   # request-local only
    return {"sso": profile["email"]}
```

**References:** CWE-459, AWS Lambda execution environment reuse docs, OWASP Serverless Top 10 S3:2017 (Sensitive Data Exposure)

# Shadow AI: unsanctioned AI SaaS and embedded AI features in the stack

**MUST** inventory and govern AI features in third-party software and employee-adopted AI SaaS, since unsanctioned tools move data outside policy.

**Why:** Copilots and AI-enabled vendors quietly move code, tickets, and documents to unvetted providers.

**Detect:** network egress to openai.com/anthropic.com from unmanaged endpoints; no AI usage policy or CASB/SaaS inventory entries.

**References:** OWASP LLM03:2025, NIST AI RMF GOVERN 6, CWE-912

# SOC 2 as Audit Regime (CCs, evidence collection)

**SHOULD** collect continuous, timestamped evidence for Trust Services Criteria (security, availability, confidentiality) rather than assembling artifacts only at audit time.

**Why:** Point-in-time evidence gathering misses control gaps during the period; auditors sample exceptions the team never noticed.

**Detect:** grep for "TSC", "CC6", "CC7" mappings; missing access review logs, change tickets, monitoring alerts as evidence; manual-only evidence folders.

**References:** AICPA TSC 2017, SOC 2 Type II, Trust Services Criteria

# Software Licenses

**MUST** track third-party dependency licenses and enforce policy against incompatible or copyleft terms in proprietary distributions.

**Why:** Unlicensed or GPL-contaminated code in shipped products creates legal liability, forced open-sourcing, and distribution injunctions.

**Detect:** grep dependency manifests for `GPL`, `AGPL`, `UNLICENSED`; check license scanner config, `allowed_licenses`, `license_policy` files absent.

**References:** SPDX License List, GPL v2/v3, AGPL v3, OWASP Dependency-Check

# Vendor/third-party risk management and subprocessor registers

**MUST** vet critical suppliers at onboarding and re-review their security posture on a fixed cadence.
**SHOULD** maintain a current register of every vendor and its subprocessors with review dates, data access scope, and breach-notification terms.

**Why:** Breaches frequently originate downstream; without a register you cannot assess exposure or notify affected parties when a vendor falls. A single compromised or negligent vendor becomes your breach: SolarWinds showed one upstream can poison thousands of downstream users.

**Detect:** Missing vendor register doc or spreadsheet; SaaS admin lists without subprocessor pages checked; contracts lacking breach-notification SLA clauses; no `vendor_risk`/`supplier_assessment`/`C-SCRM` records in third-party inventories, due-diligence records, or SBOM ingestion configs.

**References:** NIST SP 800-161, NIST SSDF (SP 800-218), SOC 2 CC9.2, GDPR Art. 28, ISO 27036

