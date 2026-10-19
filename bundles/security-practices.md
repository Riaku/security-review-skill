# security-practices — full checklist (74 items)

Process-level security practices (modeling, disclosure, patching).

> Generated artifact — edit the issue files, not this one. Manifest: [categories/security-practices.md](../categories/security-practices.md) · Index: [SKILL.md](../SKILL.md)

# Abuse Cases Per Feature

**SHOULD** write an abuse case for every user-facing feature, naming the attacker goal, the abused flow, and the control that stops it.

**Why:** User stories describe intended behavior; the gap between that and what an attacker can make the system do is the bug backlog.

**Detect:** grep feature specs and PRDs for `abuse` or `misuse`; a feature directory with no abuse case is the finding.

**References:** OWASP Abuse Case Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet.html

# Admin Activity Review

**SHOULD** periodically review administrative actions (config changes, permission grants, data exports) against expected operations, on a defined cadence.

**Why:** Insider misuse and compromised admin accounts both hide in plain sight; unreviewed admin logs are a detection gap no amount of collection fixes.

**Detect:** check for scheduled admin-log review (CloudTrail console history, K8s audit webhook, DBA action log) with named reviewer and findings tracked; flag "logs exist but nobody reviews them".

**References:** NIST 800-53 AU-6 review, SOC2 CC7 monitoring, CIS 8.11 (Conduct Audit Log Reviews)

# Advisory Scope Precision

**MUST** publish each security advisory with affected version ranges, vulnerable usage patterns, fixed versions, mitigations, and a CVE identifier.

**Why:** A vague advisory leaves consumers unable to decide whether they are affected, so the fix never ships. Precision is what turns disclosure into protection.

**Detect:** Advisory files and CHANGELOG entries carrying `Affected versions`, `Fixed in`, `CVE-20` - flag any advisory missing one of the three.

**References:** OpenSSF Concise Guide for Developing More Secure Software, https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Concise-Guide-for-Developing-More-Secure-Software.md, ISO/IEC 29147 Vulnerability disclosure, ISO/IEC 30111 Vulnerability handling processes

# AI Halt Authority

**MUST** define in advance who may halt development or deployment of a system judged unacceptably risky, and the procedure for doing so.

**Why:** Without a pre-committed stop path, sunk-cost pressure keeps a risky system shipping while the decision is deferred to whoever objects loudest.

**Detect:** find the governance document naming the stop authority, the trigger criteria, and the last time the path was exercised.

**References:** NIST AI 600-1 GV-1.3-007, https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf

# Architecture Doc & ADR Coverage

**SHOULD** maintain a current architecture overview (components, data flow, trust boundaries) plus ADRs for settled design decisions, kept in the repo.

**Why:** Without a current overview, every reviewer and new engineer rebuilds the mental model from code — and without ADRs, settled decisions get re-litigated endlessly or silently violated by people who never knew they were settled.

**Detect:** check for architecture doc with a diagram covering current components (compare against actual services/dirs); check docs/adr/ (or equivalent) exists with dated, numbered records; flag overview last-updated far behind structural changes.

**References:** C4 model, ADR practice (Nygard)

# Artifact Evidence for Claims

**SHOULD** credit a security practice only when its artifact exists in the repository, such as a fuzz target, a test, or a gate config, never from a README claim.

**Why:** Claims drift while artifacts do not, and a check that names the signal proving each practice is both automatable and honest.

**Detect:** grep LLVMFuzzerTestOneInput, func Fuzz, import atheris for a fuzzing claim; repeat with the artifact each other claim implies

**References:** OpenSSF Scorecard, https://github.com/ossf/scorecard

# Asset Criticality Inventory

**MUST** record every asset with a criticality and sensitivity classification that drives its protection and review priority.

**Why:** Without classification every asset gets the same default treatment, and the systems that matter are protected by accident. Criticality is what makes prioritization possible.

**Detect:** Inspect the asset register: each entry has an owner, a criticality tier and a data-sensitivity label.

**References:** NCSC Definitive Architecture View, https://www.ncsc.gov.uk/collection/operational-technology/definitive-architecture-view

# Attack-Path Analysis (reachable chains from exposure to crown jewels)

**SHOULD** continuously map reachable attack paths from internet exposure and low-privilege identities to critical assets, cutting shortest chains first.

**Why:** Findings look minor in isolation; it's the composed chain — public bucket to role trust to database — that actually breaches you.

**Detect:** grep `cartography`, `bloodhound`, `attack_path` reports, reachability graph exports.

**References:** MITRE ATT&CK, NIST SP 800-30, BloodHound docs

# Attack Surface Management (continuous exposure discovery)

**MUST** continuously discover and inventory every internet-facing asset (domains, subdomains, IPs, cloud endpoints) rather than relying on a static list.

**Why:** Forgotten shadow IT and stale exposed services are the most common initial-access entry points attackers find before defenders do.

**Detect:** Certstream/subdomain enumeration output, `external-exposure.csv`, cloud security hub findings, diff of DNS zone records vs. approved inventory.

**References:** OWASP WSTG-INFO-02, NIST SP 800-53 RA-5/CM-8, AWS Security Hub, Cloudflare One

# Attack Surface Reduction (deliberate exposure minimization)

**SHOULD NOT** expose administrative interfaces, dashboards, or debug endpoints directly to the public internet without an access broker such as VPN or zero-trust gateway.

**Why:** Every unnecessary open port is a tested entry point; exposed admin panels are routinely brute-forced or exploited via known CVEs.

**Detect:** `admin`, `console`, `/debug`, `:8080`, `:9200`, `kibana`, `phpmyadmin` in public ingress or SecurityGroup rules; Terraform `ingress = 0.0.0.0/0`.

**References:** OWASP ASVS V1.14, CWE-489, NIST SP 800-53 AC-3, CIS Benchmark 5.1

# Banned API Build Enforcement

**MUST** enforce banned-function lists mechanically at build time so forbidden calls fail compilation or lint rather than review.

**Why:** Review attention is finite and memory is worse; a dangerous call that only a reviewer might catch survives until the day it does not.

**Detect:** Banned-API analyzer rules wired into the build (DevSkim rules, CodeQL custom queries); re-add a banned call and confirm CI fails.

**References:** DevSkim, https://github.com/microsoft/DevSkim, SAFECode Fundamental Practices v3 (2018), https://safecode.org/wp-content/uploads/2018/03/SAFECode_Fundamental_Practices_for_Secure_Software_Development_March_2018.pdf

# Breach & Attack Simulation (adversary emulation vs controls)

**MAY** automate adversary emulation (BAS) to continuously replay known TTPs against controls, but only in environments with tested rollback and blast-radius limits.

**Why:** Point-in-time tests decay; continuous emulation catches control regressions — unbounded, it can itself cause outages.

**Detect:** BAS tool configs (SafeBreach, AttackIQ, Atomic Red Team), `atomic-red-team` in CI, simulation schedules with rollback plans

**References:** MITRE ATT&CK, Gartner BAS category, Atomic Red Team (T1059 etc.)

# Break-Glass Access Procedure

**SHOULD** define a monitored break-glass path for emergency privileged access: pre-authorized, logged, alerting on use, and reviewed within 24h.

**Why:** Without a sanctioned emergency path, responders improvise with standing admin access — which is either absent in the outage or abused permanently after it.

**Detect:** look for break-glass accounts/policies (AWS IAM break-glass role, Azure PIM emergency access) with alert-on-use and review SLA; check that emergency creds are escrowed (sealed envelope) not casually held.

**References:** Microsoft emergency access accounts, AWS break-glass role patterns, NIST 800-53 AC-2(2)

# Eliminate Vulnerability Classes

**SHOULD** prefer a mechanism that eliminates a whole defect class over repeated point fixes when findings concentrate in that class.

**Why:** Removing the class turns many independent bugs into one solved problem, while point fixes leave the next instance to be discovered in production.

**Detect:** judgment: the defect trend by class across recent releases — whether one class keeps returning after repeated fixes

**References:** Anderson, Security Engineering 1st ed., ch.23, https://www.cl.cam.ac.uk/~rja14/book.html

# Coding-Agent Sandbox & Permission-Mode Review

**MUST** review how coding agents are configured: OS-level sandbox on, writes workspace-scoped, network off by default, approval policy enforced — and flag bypass flags (`--yolo`, `dangerously-*`, `bypassPermissions`, `approval=never`).

**Why:** The agent's technical reach, not its instructions, is the real boundary; full-access modes inside a dev container let a malicious repo exfiltrate everything reachable, including the agent's own credentials.

**Detect:** grep agent configs for `--yolo`, `dangerously-bypass`, `sandbox_mode = "danger-full-access"`, `approval_policy = "never"`, `bypassPermissions`; check for OS-enforced sandbox vs advisory-only policy.

**References:** OpenAI Codex approvals/security model, Anthropic /sandbox + permissions, Cursor Run Modes ("best-effort, not a hard boundary")

# Compensating Controls for Unpatchable Systems

**MUST** maintain pre-engineered compensating controls — network isolation, feature disablement, hardened access — for components that cannot be patched on the vendor's schedule.

**Why:** Most known-exploited vulnerabilities affect systems that cannot be patched in place, and few vendors ship workarounds, so the mitigation has to exist before the incident.

**Detect:** judgment: the compensating-control runbook entry for each unpatchable component

**References:** I Can't Patch My OT Systems!, https://arxiv.org/abs/2510.06951, CISA KEV catalog, https://www.cisa.gov/known-exploited-vulnerabilities-catalog

# Complementary SAST Engines

**SHOULD** run more than one static-analysis engine and use their combined findings to direct human security review.

**Why:** A single engine misses whole bug classes, and its clean result is read as proof of safety. Different engines fail on different patterns.

**Detect:** CI runs at least two independent analyzers (for example semgrep plus CodeQL) and routes both SARIF outputs into one triage queue.

**References:** arXiv:2407.12241, https://arxiv.org/abs/2407.12241

# Control Effectiveness Testing

**MUST** test that each security control actually fires — lockout, filter rule, report endpoint, alert route — not merely that it is configured.

**Why:** A control deployed with a typo looks identical to a working one in a configuration review. Only a negative test that should trigger it proves the path is live.

**Detect:** command: an automated control test suite (for example a `pytest tests/security/test_controls.py` job or an active scanner run against staging) that triggers each control and asserts the block or alert.

**References:** OWASP Web Security Testing Guide, NIST SP 800-53 CA-8

# Cyber insurance alignment: coverage preconditions and denial clauses

**MUST NOT** let representations on insurance applications (MFA everywhere, EDR deployed, backups tested) drift from actual configuration, since denial clauses void claims on misrepresentation.

**Why:** Insurers investigate post-incident and deny payouts when stated controls are absent—leaving the breach cost entirely self-funded.

**Detect:** grep policy "warranty", "condition precedent" against live config: MFA, EDR/antivirus, offline backups, patch SLA mismatches.

**References:** ISO 27001/27017, CVE-based exclusion clauses, Marsh/Gallagher cyber underwriting guidance

# Dangerous Functionality Inventory

**MUST** maintain a reviewed inventory of dangerous functionality - untrusted deserialization, raw binary parsing, dynamic code execution, direct memory access - and isolate it.

**Why:** These operations are code execution by design, so the only durable control is knowing where they are and keeping them few, sandboxed and separately reviewed.

**Detect:** `eval(`, `exec(`, `pickle.loads`, `yaml.load(`, `mmap(`, `ctypes.` and FFI entry points, cross-checked against the dangerous-functionality inventory.

**References:** OWASP ASVS V15 Secure Coding and Architecture, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x24-V15-Secure-Coding-and-Architecture.md

# Decision-Record Provenance

**SHOULD** keep decision artifacts (assumption logs, decision records/ADRs) alongside the outputs and code they govern: who decided what, when, on what evidence.

**Why:** Months later, nobody can distinguish a deliberate assumption from an oversight — and future reviewers re-litigate settled choices or trust stale ones without provenance.

**Detect:** judgment on presence of decision/assumption records near consequential logic and outputs (ADRs in docs/adr, assumption logs in analysis projects), with dates and authors.

**References:** ADR practice (Nygard)

# Defense-in-Depth Layering

**SHOULD** protect each asset with multiple independent control layers (network, app, data, runtime) so no single failure exposes it; layers must be independent, not correlated.

**Why:** Every control fails eventually — a bypassed WAF, a missed CVE, a phished credential. Correlated layers (all bypassed by the same trick) are one layer wearing a trench coat.

**Detect:** map each crown-jewel asset to its control stack; flag assets protected by a single layer; check layer independence (e.g. WAF + app validation + DB authz vs WAF-only; secrets not readable by the same principal that reaches the app).

**References:** OWASP Secure Product Design Cheat Sheet, NIST SP 800-53 defense-in-depth, CISA Secure by Design

# Eliminate Hazard First

**MUST** remove the hazardous capability first, then reduce exposure by design, and only then add protective controls.

**Why:** A control wrapping a dangerous feature is a promise to configure it correctly forever. Deleting the feature removes the failure class instead of managing it.

**Detect:** For each high-risk finding, check the chosen fix against the alternatives in order: remove, redesign, then control.

**References:** NIST SP 800-160v1r1, https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-160v1r1.pdf

# Embargo Artifact Silence

**MUST** keep every artifact silent during a disclosure embargo: commit messages, branch names, release notes and CI job output.

**Why:** The advisory text is the last place a leak appears. A descriptive commit message or public CI log tells attackers what to exploit before a fix ships.

**Detect:** `git log --oneline` and branch names in the embargo window matching `CVE-`, `vuln`, `security fix` before the advisory is public.

**References:** Eclipse CSI Security Handbook: Embargoes, https://github.com/eclipse-csi/security-handbook/blob/main/docs/vulnerabilities/embargoes.md

# Exploit-Class Weighted Investment

**SHOULD** weight defensive and review effort toward the weakness classes that dominate real exploitation, such as memory-lifetime and parser bugs.

**Why:** Equal attention across all weakness classes spends most of the budget on bugs nobody weaponizes. Exploited-in-the-wild data shows a small set of classes recurring.

**Detect:** Rank open findings and review focus areas by CWE, then compare the top classes with the Project Zero exploited-in-the-wild list; the review plan stating where effort goes is the artifact.

**References:** Google Project Zero: 0days in the wild, https://googleprojectzero.github.io/0days-in-the-wild/rca.html

# Prioritize By Exploitation

**MUST** prioritize remediation by observed exploitation and exposure, treating severity scores as an impact input rather than the ranking.

**Why:** Severity classifiers perform near chance at predicting real exploitation, so severity-ranked backlogs spend effort on findings nobody is using.

**Detect:** command join scanner findings with EPSS and the KEV catalog (`trivy --format json` plus EPSS lookup) and sort by exploitation signal times exposure.

**References:** CVSS versus exploitation-prioritization measurement, https://arxiv.org/abs/2603.12450, CISA KEV Catalog, https://www.cisa.gov/known-exploited-vulnerabilities-catalog

# Exploitation-Based Prioritization

**MUST** prioritize remediation by evidence of active exploitation and override severity-score ordering when a finding appears in a known-exploited catalog.

**Why:** Score-ordered queues leave exploited vulnerabilities unpatched while pristine high-severity findings absorb the attention.

**Detect:** grep the dependency and patch policy for a known-exploited feed and a shorter deadline for those entries than for severity-only findings.

**References:** CISA Known Exploited Vulnerabilities Catalog, https://www.cisa.gov/known-exploited-vulnerabilities-catalog

# Fail-Secure Configuration

**MUST** design components to fail in a secure state: auth failures deny access, TLS verification failures abort the connection, policy engine outages block rather than allow, and partial initialization never exposes privileged surfaces.

**Why:** Fail-open is the silent killer — an auth service timeout that defaults to "allowed" or a verifier that skips on error turns an outage into a breach window.

**Detect:** grep for `except: pass` / default-allow branches around authz and TLS verify calls; check `failOpen: false` on admission webhooks, `ssl_verify` defaults, circuit-breaker fallback behavior on security checks.

**References:** OWASP Secure Product Design Cheat Sheet (fail securely), NIST SP 800-162 fail-closed guidance

# Severity from Instance Attributes

**MUST** rate a finding by the concrete instance — data reachable, identifier predictability, read versus write — rather than by vulnerability class alone.

**Why:** One class spans trivial to critical depending on what the specific object exposes, so class-level severity both inflates reports and buries real criticals.

**Detect:** judgment: the finding record — whether severity cites reachable data and identifier entropy

**References:** Bugcrowd Vulnerability Rating Taxonomy, https://github.com/bugcrowd/vulnerability-rating-taxonomy

# Fix the Bug Class

**SHOULD** close a fixed vulnerability as a class, adding a mechanical check that fails on the same pattern elsewhere.

**Why:** The same weakness usually recurs in sibling handlers; fixing only the reported instance leaves the rest exploitable and unreported.

**Detect:** judgment: the fix commit — whether it adds a lint/semgrep rule or shared helper, or only patches one call site.

**References:** CWE Top 25 (2024), https://cwe.mitre.org/top25/archive/2024/2024_cwe_top25.html, NIST SP 800-218 SSDF, https://csrc.nist.gov/pubs/sp/800/218/final

# Guidelines Backed by Rules

**SHOULD** pair every written security guideline with an automated rule in the repository and a severity that routes findings to the right reviewer.

**Why:** Guidelines without enforcement decay into folklore, while rules without guidance produce findings developers cannot act on.

**Detect:** grep the security guideline document and the linter configs, and list guidelines with no corresponding rule id.

**References:** GitLab Secure Coding Guidelines, https://docs.gitlab.com/development/secure_coding_guidelines/

# Independent AI Assessment

**MUST** have risk assessments and red-team exercises for an AI system performed by assessors who did not build it.

**Why:** Builders grade their own work against the threats they already thought of, so self-assessment certifies the system's blind spots.

**Detect:** compare the assessment report's authors and reviewers against commit authorship and the team roster for the model or feature.

**References:** NIST AI 600-1 MEASURE 1.3, https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf

# Input Entry Point Inventory

**MUST** enumerate every data-entry point — network, IPC, files, deep links, clipboard, background sync — and validate each as an untrusted boundary.

**Why:** Teams validate the HTTP API and forget the deep link, the shared file, or the IPC message, each of which reaches the same privileged code. An unlisted entry point never gets reviewed.

**Detect:** judgment: the data-flow diagram or threat model — every entry point listed with its parser, validation, and trust level, cross-checked against platform entry declarations in the app manifest.

**References:** OWASP MASVS-CODE-4 (input validation), https://github.com/OWASP/masvs/blob/master/controls/MASVS-CODE-4.md, OWASP Threat Modeling

# Insider and Control-Plane Threats

**MUST** model authorized-but-malicious insiders, colluding parties, and build or control-plane compromise as first-class threats, not as edge cases.

**Why:** Modern stacks have no defensible perimeter and privileged authority spread across contractors, vendors, and automation, so the actors the model ignores are the ones that succeed.

**Detect:** Read the threat model's actor list and confirm insider, third-party, and CI/control-plane attackers each have modelled paths.

**References:** TRACE threat modelling (arXiv 2606.22214), https://arxiv.org/abs/2606.22214

# Isolate the Security Core

**MUST** isolate the code that must always be correct into a small, separately owned component with its own review and tests.

**Why:** High assurance is only achievable for code small enough to audit exhaustively; authorization smeared across services makes every service part of the trusted base.

**Detect:** judgment: the auth/authz module and its callers — list every service that makes its own trust decision instead of delegating to the core.

**References:** Saltzer & Schroeder, The Protection of Information in Computer Systems (1975), https://web.archive.org/web/2023/https://dl.acm.org/doi/10.1145/359545.359563

# Design Out Exploited Flaws

**MUST** design out any vulnerability with confirmed in-the-wild exploitation rather than accepting a compensating control.

**Why:** Active exploitation means an adversary has already solved the mitigation problem, so the compensating control is a speed bump in front of a working exploit.

**Detect:** command match SBOM findings against the CISA KEV catalog (`grype` output joined with the KEV list) and fail on matches without a removal plan.

**References:** CISA Known Exploited Vulnerabilities Catalog, https://www.cisa.gov/known-exploited-vulnerabilities-catalog, FDA premarket cybersecurity guidance (design out KEV-listed vulnerabilities), https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cybersecurity-medical-devices-quality-system-considerations-and-content-premarket-submissions

# Legacy Asset Compensating Controls

**MUST** place compensating controls at the boundary of any asset that cannot adopt current authentication or cryptography, and record the accepted gap.

**Why:** Extended-lifecycle devices outlive the primitives around them, so exposure has to be absorbed by segmentation and monitoring rather than by the device.

**Detect:** Take the asset inventory's end-of-support entries and confirm each has a named boundary control and an owner.

**References:** NCSC Operational Technology collection, https://www.ncsc.gov.uk/collection/operational-technology

# Living-off-the-Land Abuse

**MUST** monitor execution of legitimate binaries (curl, ssh, powershell, wmic, certutil, base64) for arguments and contexts inconsistent with normal operations.

**Why:** Attackers weaponize signed system tools to run malicious work, evading malware detection because nothing "bad" is ever installed.

**Detect:** grep EDR/SIEM rules for process-args telemetry on LOLBAS-listed binaries (e.g. `certutil -urlcache`, `powershell -enc`); flag hosts where these run outside admin baselines.

**References:** MITRE ATT&CK T1218 System Binary Proxy Execution, LOLBAS project, CWE-427, Atomic Red Team tests

# Treat LLM output as untrusted input (sanitize before HTML/SQL/shell/URL sinks)

**MUST** sanitize or parameterize every LLM output before it reaches an HTML, SQL, shell, or URL sink.

**Why:** A coerced model emitting markup or queries delivers stored XSS and injection through a path teams assume is safe.

**Detect:** model response rendered via |safe / innerHTML or concatenated into queries or subprocess args.

**References:** OWASP LLM05:2025, CWE-79, CWE-89, CWE-78

# Malware Scan Untrusted Files

**MUST** scan files received from untrusted sources for malware before storing, serving, or processing them further.

**Why:** The application becomes a distribution channel: it stores the payload, serves it from its own origin, and hands it to internal processors.

**Detect:** clamscan on the upload quarantine path; check the upload pipeline for a scan step before the file is promoted.

**References:** OWASP ASVS v5.0 V5, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x14-V5-File-Handling.md, CWE-509

# Memory Safety: Buffer Overflow & Use-After-Free

**MUST** bound every buffer write and never dereference freed or dangling memory in unsafe languages.

**Why:** Overflows and use-after-free are classic primitives for arbitrary code execution and privilege escalation.

**Detect:** `strcpy`/`sprintf`/`memcpy` without size checks, raw `malloc`/`free` lifetimes, indexing past array length, missing bounds sanitizer.

**References:** CWE-120, CWE-416, CWE-787, CERT MEM rules

# No Opt-In Security Controls

**MUST** enable security controls by default on every path, requiring an explicit recorded exception to disable one for a caller.

**Why:** A control that each developer must remember to invoke is absent wherever someone forgot, which is exactly where the exploit lands.

**Detect:** grep security helpers gated on a default-false flag or optional parameter (strict=False, verify=False, enable_xss=false)

**References:** Linux kernel self-protection, https://kernel.org/doc/html/latest/security/self-protection.html

# Admin Tasks as One-Off Processes from the Release

**SHOULD** run admin and maintenance tasks (migrations, REPLs, one-time scripts) as one-off processes from the same released code, config, and dependency isolation — committed to the repo — rather than ad-hoc scripts executed against production out-of-band.

**Why:** Out-of-band admin access (manual `psql` into prod, hand-copied scripts, SSH one-offs) is unauditable, drifts from the released code's assumptions, and is the classic vector for irreversible mistakes. Running the same image as a scoped one-off Job keeps credentials, code version, and audit trail aligned.

**Detect:** runbooks showing manual DB/console access instead of `kubectl job` or release-hook migrations; admin scripts not present in the repo; production mutations with no corresponding committed task definition.

**References:** 12factor.net/admin-processes, OWASP Logging Cheat Sheet (audit of admin actions), Kubernetes Jobs pattern

# Patch management SLAs (MTTR targets by severity, exception tracking)

**MUST** define mean-time-to-remediate targets per severity (critical 24h, high 30d, medium 90d) covering both application dependencies and the base images of shipped artifacts, rebuilding and redeploying those images on a fixed cadence (weekly minimum) so long-lived images do not accumulate known-exploitable CVEs, and log every exception with owner and expiry date.

**Why:** Undated exceptions silently become permanent debt; SLA clocks make drift visible and auditable.

**Detect:** `sla` / `mttr` keys in policy docs, `waiver` / `exception` tracker files with `expires` fields; `.trivyignore` age, `imagePullPolicy: Always`, Renovate/Dependabot config, `fixVersions` in scanner reports

**References:** NIST SP 800-40 Rev. 4, CIS Control 7, PCI DSS 6.3.3, CWE-1104, CISA KEV, OWASP A06:2021

# Independent penetration testing cadence and finding remediation tracking

**SHOULD** commission an external penetration test at least annually and after major architectural changes, with every finding tracked to closure in a ticketing system.

**Why:** Self-assessment shares the builder's blind spots; untracked findings recur across engagements.

**Detect:** `pentest` reports dated within 12 months, `remediation` tracker with finding IDs, contract/engagement records

**References:** OWASP WSTG, PTES, NIST SP 800-115, PCI DSS 11.4

# Privileged-Action Attribution

**MUST** ensure every privileged action is attributable to a named individual — no shared admin accounts, no service-account interactive use.

**Why:** Shared root/admin credentials destroy non-repudiation; when an incident happens, "admin did it" is not an answer.

**Detect:** grep for shared `admin`/`root` logins in auth logs config, team password vaults for infra creds, kubectl exec under shared identities; check SSO with per-user identity to admin planes.

**References:** NIST SP 800-53 AC-6/IA-2, SOX ITGC segregation of duties, CIS 5.4 no shared administrator accounts

# Proportionate QA Tiering

**SHOULD** match review/QA rigor to the risk tier of what's being changed: critical-path and high-impact components get deep review, dual verification, and testing; throwaway work gets proportionate scrutiny.

**Why:** Uniform maximum rigor exhausts reviewers into rubber-stamping; uniform minimum rigor misses disasters. Both failure modes come from never assigning a risk tier in the first place.

**Detect:** judgment on whether a documented risk tier / QA plan exists and matches the component's actual criticality (user impact, data sensitivity, money movement).

**References:** OWASP SAMM, risk-based testing practice

# Purple Teaming (red+blue collaborative feedback loops)

**SHOULD** run structured purple-team sessions where red-team techniques are replayed against blue detections, closing each gap in both directions.

**Why:** Siloed red and blue teams optimize for scoring, not detection coverage; joint loops convert attacks into durable telemetry.

**Detect:** `purple-team` session reports, shared `detection-gap` backlog, ATT&CK coverage matrices with blue annotations

**References:** MITRE ATT&CK Evaluations, NIST SP 800-115, CISA Purple Team guidance

# Remove Unused Attack Surface

**MUST** remove routes, listener ports, and integrations that no current client, test, or job uses, rather than leaving them deployed and reachable.

**Why:** Capability nobody maintains is capability nobody patches, and a reachable route is exploitable whether or not a UI links to it.

**Detect:** grep route tables and container/service port definitions for paths with no caller in the UI, SDK, or tests, and integrations whose credentials remain live; confirm from outside the host that the port or route is not reachable.

**References:** OWASP Attack Surface Analysis Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Attack_Surface_Analysis_Cheat_Sheet.html, NCSC Secure Development Principles, https://www.ncsc.gov.uk/collection/developers-collection/principles

# Sandbox Untrusted Code

**MUST** run plugins, user scripts, and third-party extensions with no ambient authority: no filesystem, network, or credentials unless explicitly granted.

**Why:** Third-party code runs with the host process's identity, so one malicious plugin has exactly the access the service has.

**Detect:** grep plugin and eval loaders (`vm.runInNewContext` presented as a sandbox, `importlib`, `eval`, dynamic `require`) for filesystem, network, and env access in the same context.

**References:** Node.js security guidance, https://nodejs.org/en/about/security, OWASP Deserialization Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html

# Declared Scan Suppressions

**MUST** record every scanner suppression as a scoped, justified, expiring declaration naming the rule and the non-exploitability argument.

**Why:** Inline ignores and blanket exclude files accumulate silently until the gate passes for reasons nobody can reconstruct.

**Detect:** grep for `# nosec`, `// nolint`, `.trivyignore`, `--exclude`, and scanner `ignore` entries; require an adjacent justification and expiry.

**References:** OpenSSF OSPS Baseline: suppressed findings must be declared, https://www.bestpractices.dev/en/criteria

# Secure by Default Shipping

**MUST** ship products secure out-of-the-box: MFA, logging, and SSO available at no extra cost and enabled (or one-click) on first run — never paywalled or buried as advanced features.

**Why:** CISA's Secure by Design finding: the security burden has been pushed onto consumers because vendors ship insecure defaults; most customers never harden what they buy.

**Detect:** review default config of the shipped product: are MFA/logging/encrypted transport on by default? Is any baseline security control gated behind paid tiers or manual hardening docs?

**References:** CISA Secure by Design whitepaper & Pledge, OWASP Secure Product Design Cheat Sheet

# Secure by Design (architectural input, not a patch)

**MUST** treat security requirements as architectural inputs at design time — least privilege, defense in depth, secure defaults — not bolt-ons retrofitted after review.

**Why:** Architecture that assumes trust is unpatchable later; every bolt-on inherits the original flaw's blast radius.

**Detect:** design docs citing `least privilege` / `defense in depth`, ADRs with security sections, default-deny network policies

**References:** NIST SP 800-160, Saltzer & Schroeder principles, OWASP ASVS V1, CISA Secure by Design Pledges

# Secure Development Attestation

**SHOULD** retain signed, per-release evidence that the documented secure-development practices were followed, in a form a customer can verify.

**Why:** Procurement increasingly asks for attestation rather than a questionnaire, and evidence invented after the fact is worthless. Unsigned claims of practice cannot be distinguished from aspiration.

**Detect:** judgment: the release artifacts — a signed attestation or provenance bundle per version, mapped to the practices it claims and retrievable by version.

**References:** CISA Secure Software Development Attestation Form, https://www.cisa.gov/resources-tools/resources/secure-software-development-attestation-form, NIST SP 800-218 (SSDF)

# Security Baseline Procurement

**MUST** state a minimum security baseline in the request for proposal and the contract so supplier controls are agreed before delivery.

**Why:** Security requirements discovered after delivery become renegotiation, and the cheapest resolution is an exception. Stating them at procurement makes the baseline a condition of the deal.

**Detect:** judgment: the RFP, the contract security schedule, and the supplier self-assessment — whether the same testable baseline appears in all three.

**References:** MVSP (Minimum Viable Secure Product), https://mvsp.dev, NIST SP 800-161 supply chain risk management

# Security Champions Program (embedded advocates per team)

**SHOULD** embed a trained security champion in each engineering team, with paid time allocated, a refresh cadence, and a direct escalation line to the security group.

**Why:** A central security team cannot review everything; without funded champions, the role quietly evaporates under delivery pressure.

**Detect:** `champions` roster doc, training completion records, `office hours` schedule, per-team champion named in CODEOWNERS

**References:** OWASP SAMM Security Champions, BSIMM satellite, Microsoft Security Champions Program

# Security Is Cross-Cutting

**MUST** review every call site of an access-control decision in the change, not only the module that appears to own it.

**Why:** Access control and auth logic scatter through the codebase and interleave, so a review confined to the security package misses most of the code that decides access.

**Detect:** judgment — trace each security feature's call sites and integration glue (`authorize`, `can?`, `has_permission`, policy checks) across the diff, not only the security module.

**References:** Mining security features as cross-cutting concerns, https://arxiv.org/abs/2610.06132

# Security Program Metrics

**SHOULD** track findings by lifecycle phase, remediation-SLA adherence, and review coverage as standing metrics, not one-off reports.

**Why:** Without trend data the program cannot show that shift-left happened, and interest and funding decay back to the previous baseline.

**Detect:** Read the tracker's last four quarters and confirm a findings-by-phase series and an SLA-adherence series both exist.

**References:** OWASP Security Culture, https://owasp.github.io/www-project-security-culture/stable/

# Security Properties Decomposition

**MUST** analyze and document confidentiality, integrity and peer authentication as separate properties rather than one undifferentiated security goal.

**Why:** A single 'is it secure' goal cannot be tested or attributed to a mechanism. Named properties each get their own threat, mechanism and failure mode.

**Detect:** Inspect the design doc: each property has a stated mechanism and a stated failure condition.

**References:** RFC 3552, https://www.rfc-editor.org/rfc/rfc3552.txt

# Explicit Security Requirements in Specs

**MUST** state security behavior as explicitly and traceably as functional behavior in the specification that drives implementation or generation.

**Why:** A spec that describes function explicitly and security implicitly yields code that satisfies the visible requirements while dropping authorization and validation.

**Detect:** judgment: the spec — for each entity, a named requirement covering access, input validation, and failure behavior

**References:** SDD security benchmark, https://arxiv.org/abs/2606.00167

# Specialist Reviewer Routing

**MUST** route changes touching security, privacy, or concurrency to a reviewer qualified in that domain instead of approving on trust.

**Why:** A generalist reviewer cannot tell a subtle authorization flaw from style, so approval becomes a formality that transfers the risk to users. Named ownership makes expertise a precondition of merge.

**Detect:** grep CODEOWNERS and branch-protection rules for security-sensitive paths (auth, crypto, payments, migrations) owned by a named team; unowned paths are the finding.

**References:** Google engineering practices: what to look for in a code review, https://github.com/google/eng-practices/blob/master/review/reviewer/looking-for.md

# Structured Security Requirements

**MUST** track each security requirement as a structured record linked to its implementation and verification, not as prose in a document.

**Why:** Prose requirements cannot be queried, traced to code, or counted at audit time, so they rot silently. Structured records keep every requirement visible until it is verified.

**Detect:** Inspect the requirements store: each requirement has an ID, an owner, a link to implementing code and a verification artifact.

**References:** SAFECode Fundamental Practices for Secure Software Development v3 (2018), https://safecode.org/wp-content/uploads/2018/03/SAFECode_Fundamental_Practices_for_Secure_Software_Development_March_2018.pdf

# Subproject Strictness Floor

**MUST** enforce security requirements in every subproject at least as strictly as the primary codebase.

**Why:** The weakest subproject sets the project's real posture, and auxiliary repositories typically skip the gates the main one enforces.

**Detect:** command compare required checks and scanner config across repos (`gh api repos/{owner}/{repo}/branches/main/protection`, CI config diff) and flag any subset.

**References:** OpenSSF OSPS Baseline: subproject security requirements, https://www.bestpractices.dev/en/criteria

# Threat Model From Code

**MUST** derive the threat model from the code and architecture definition and regenerate it in CI so the document cannot drift from the system.

**Why:** Hand-maintained models and annotation-based mitigation labels decay silently, so the document keeps claiming controls the code no longer implements.

**Detect:** git log -1 --format=%cd -- threatmodel/ compared with the last commit touching the described components; a stale regeneration date fails

**References:** OWASP pytm, https://github.com/OWASP/pytm

# Threat Modeling

**MUST** produce a threat model (STRIDE or attack-tree) for every new service before its first production deploy, reviewed with the owning team.

**Why:** Unmodeled trust boundaries ship as real intrusions — attackers exploit the paths nobody drew.

**Detect:** files `docs/threat-model/`, `threat-model.md`, `stride` keywords in PR templates, `threat_model` CI gate

**References:** OWASP Threat Dragon, NIST SP 800-154, OWASP ASVS V1.2

# Threat-to-Test Traceability

**MUST** map each identified threat to an attack-pattern identifier and to the requirement or test that would catch it.

**Why:** A threat list that stops at description produces no evidence anything was addressed. Linking each threat to a test closes the loop and exposes unmitigated rows.

**Detect:** Inspect the threat-model table: every row has a threat, an attack-pattern ID, a mitigation requirement and a verification artifact.

**References:** OWASP Cornucopia, https://cornucopia.owasp.org/about/

# Tool Evaluation on Own Corpus

**SHOULD** evaluate security-analysis tools on a hand-built corpus of known-bad and known-good cases before trusting them in the pipeline.

**Why:** Vendor benchmarks measure the vendor's test set, not your code. A fixed local corpus shows what a tool misses in your languages and frameworks.

**Detect:** Inspect the benchmark repository: versioned cases with expected findings and a recorded per-tool result.

**References:** arXiv:2503.09433, https://arxiv.org/abs/2503.09433

# Out-of-Scope Threat Disclosure

**MUST** state explicitly which threats the design does not address, alongside the ones it mitigates.

**Why:** A security section that lists only mitigated threats invites deployment in contexts the design never covered, with no compensating control.

**Detect:** Read the threat model's security section and confirm a named out-of-scope list exists next to the mitigations.

**References:** NCSC Protocol Design Principles, https://www.ncsc.gov.uk/sites/default/files/2026-06/Protocol-Design-Principles.pdf

# Usable Security Controls

**SHOULD** verify that each security control fits the workflow it constrains, because a control users must fight gets replaced by informal workarounds that void it.

**Why:** Controls that add friction are routed around, and the workaround is invisible to the audit that counts the control as deployed.

**Detect:** judgment: the workflow around the control — what the fastest compliant path costs the user

**References:** Anderson, Security Engineering 1st ed., ch.23, https://www.cl.cam.ac.uk/~rja14/book.html

# Verification-Level Tiers (ASVS L1/L2/L3: basic / standard / privileged-app requirements)

**MUST** assign each app an ASVS tier (L1 basic, L2 sensitive data, L3 privileged) and verify controls at that level.

**Why:** Untiered apps get theater-grade checks on high-risk systems, leaving privileged-function gaps attackers exploit directly.

**Detect:** grep `ASVS`, `verification_level`, `baseline: L1|L2|L3` in security docs, scanner configs, requirement trackers.

**References:** OWASP ASVS 5.0, OWASP SAMM, NIST SP 800-53 control tailoring

# Verification Path Coverage

**MUST** measure branch coverage of code that makes authentication, authorization, or signature-verification decisions and review every branch that never executes.

**Why:** A misplaced jump or duplicated cleanup branch in verification code silently accepts invalid input while line coverage stays green. Only branch-level measurement exposes the path that never runs.

**Detect:** command: `coverage run --branch` with `coverage report --show-missing` (or `gcov -b` / `llvm-cov show`) scoped to auth and signature modules; any uncovered branch in a verify function is a finding.

**References:** Apple 'goto fail' analysis, https://www.imperialviolet.org/2014/02/22/applebug.html, CWE-670 Always-Incorrect Control Flow Implementation

# Vetted Implementations Over Bespoke Code

**SHOULD** implement authentication, authorization, parsing, and encoding with maintained, widely reviewed libraries rather than bespoke code.

**Why:** Shared implementations meet their failure modes earlier and are fixed once for everyone; a bespoke variant ships its first bug to production.

**Detect:** grep for hand-rolled crypto, base64, JWT, or auth helpers defined in-repo instead of a maintained library

**References:** OWASP Go Secure Coding Practices, https://github.com/OWASP/Go-SCP

# Vulnerability disclosure program (SECURITY.md, coordinated disclosure, safe harbor)

**SHOULD** publish a SECURITY.md with a monitored intake channel, a coordinated-disclosure timeline, and safe-harbor language for good-faith researchers.

**Why:** Without a front door, findings leak to full disclosure or black markets before you can fix them.

**Detect:** `SECURITY.md` at repo root, `security.txt` in `/.well-known/`, `disclosure` / `safe harbor` keywords

**References:** ISO 29147, ISO 30111, RFC 9116, OWASP VDP Guide

# Zero Trust Architecture

**SHOULD** verify every request explicitly regardless of network location — no implicit trust for internal networks, device posture checked, per-request authorization, least-privilege service identity.

**Why:** Perimeter-based trust collapses the moment one host is compromised; zero trust contains blast radius by treating every call as coming from an attacker until proven otherwise.

**Detect:** look for mTLS everywhere / service mesh, identity-aware proxies (BeyondCorp-style), absence of "trusted internal network" CIDR allow-lists as sole authz, continuous session validation rather than once-at-connect.

**References:** NIST SP 800-207 Zero Trust Architecture, CISA Zero Trust Maturity Model

