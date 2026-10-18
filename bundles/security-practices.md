# security-practices — full checklist (19 items)

Process-level security practices (modeling, disclosure, patching).

> Generated artifact. Canonical source: `issues/<slug>.md`.

# Threat Modeling

**MUST** produce a threat model (STRIDE or attack-tree) for every new service before its first production deploy, reviewed with the owning team.

**Why:** Unmodeled trust boundaries ship as real intrusions — attackers exploit the paths nobody drew.

**Detect:** files `docs/threat-model/`, `threat-model.md`, `stride` keywords in PR templates, `threat_model` CI gate

**References:** OWASP Threat Dragon, NIST SP 800-181, OWASP ASVS V1.2

# Memory Safety: Buffer Overflow & Use-After-Free

**MUST** bound every buffer write and never dereference freed or dangling memory in unsafe languages.

**Why:** Overflows and use-after-free are classic primitives for arbitrary code execution and privilege escalation.

**Detect:** `strcpy`/`sprintf`/`memcpy` without size checks, raw `malloc`/`free` lifetimes, indexing past array length, missing bounds sanitizer.

**References:** CWE-120, CWE-416, CWE-787, CERT MEM rules

# Log Injection & Log Forging

**MUST NOT** write unsanitized user input into log lines; strip CR/LF and control characters before logging any request data.

**Why:** Injected newlines let attackers forge fake log entries or split one entry into many, poisoning the audit trail you rely on during investigations.

**Detect:** grep for user-controlled values interpolated into logger calls (`log.info("User " + username)`) without newline stripping; check for encoder/sanitizer in log appender config.

**References:** OWASP Logging Cheat Sheet, CWE-117, OWASP WSTG-INPV-009

# Patch cadence and remediation SLAs for known CVEs in production images

**MUST** rebuild and redeploy base images on a fixed cadence (weekly minimum), remediating critical CVEs within 24 hours of disclosure.

**Why:** Long-lived images accumulate known-exploitable CVEs that scanners flag forever and worms exploit within days.

**Detect:** `.trivyignore` age, `imagePullPolicy: Always`, Renovate/Dependabot config, `fixVersions` in scanner reports

**References:** CWE-1104, CISA KEV, NIST SP 800-40, OWASP A06:2021

# Cyber insurance alignment: coverage preconditions and denial clauses

**MUST NOT** let representations on insurance applications (MFA everywhere, EDR deployed, backups tested) drift from actual configuration, since denial clauses void claims on misrepresentation.

**Why:** Insurers investigate post-incident and deny payouts when stated controls are absent—leaving the breach cost entirely self-funded.

**Detect:** grep policy "warranty", "condition precedent" against live config: MFA, EDR/antivirus, offline backups, patch SLA mismatches.

**References:** ISO 27001/27017, CVE-based exclusion clauses, Marsh/Gallagher cyber underwriting guidance

# Treat LLM output as untrusted input (sanitize before HTML/SQL/shell/URL sinks)

**MUST** sanitize or parameterize every LLM output before it reaches an HTML, SQL, shell, or URL sink.

**Why:** A coerced model emitting markup or queries delivers stored XSS and injection through a path teams assume is safe.

**Detect:** model response rendered via |safe / innerHTML or concatenated into queries or subprocess args.

**References:** OWASP LLM01:2025, CWE-79, CWE-89, CWE-78

# Vulnerability disclosure program (SECURITY.md, coordinated disclosure, safe harbor)

**SHOULD** publish a SECURITY.md with a monitored intake channel, a coordinated-disclosure timeline, and safe-harbor language for good-faith researchers.

**Why:** Without a front door, findings leak to full disclosure or black markets before you can fix them.

**Detect:** `SECURITY.md` at repo root, `security.txt` in `/.well-known/`, `disclosure` / `safe harbor` keywords

**References:** ISO 29147, ISO 30111, RFC 9116, OWASP VDP Guide

# Patch management SLAs (MTTR targets by severity, exception tracking)

**MUST** define mean-time-to-remediate targets per severity (critical 7d, high 30d, medium 90d) and log every exception with owner and expiry date.

**Why:** Undated exceptions silently become permanent debt; SLA clocks make drift visible and auditable.

**Detect:** `sla` / `mttr` keys in policy docs, `waiver` / `exception` tracker files with `expires` fields

**References:** NIST SP 800-40 Rev.4, CIS Control 7, PCI DSS 6.3.3

# Independent penetration testing cadence and finding remediation tracking

**SHOULD** commission an external penetration test at least annually and after major architectural changes, with every finding tracked to closure in a ticketing system.

**Why:** Self-assessment shares the builder's blind spots; untracked findings recur across engagements.

**Detect:** `pentest` reports dated within 12 months, `remediation` tracker with finding IDs, contract/engagement records

**References:** OWASP WSTG, PTES, NIST SP 800-115, PCI DSS 11.4

# Living-off-the-Land Abuse

**MUST** monitor execution of legitimate binaries (curl, ssh, powershell, wmic, certutil, base64) for arguments and contexts inconsistent with normal operations.

**Why:** Attackers weaponize signed system tools to run malicious work, evading malware detection because nothing "bad" is ever installed.

**Detect:** grep EDR/SIEM rules for process-args telemetry on LOLBAS-listed binaries (e.g. `certutil -urlcache`, `powershell -enc`); flag hosts where these run outside admin baselines.

**References:** MITRE ATT&CK T1218 System Binary Proxy Execution, LOLBAS project, CWE-427, Atomic Red Team tests

# Attack Surface Management (continuous exposure discovery)

**MUST** continuously discover and inventory every internet-facing asset (domains, subdomains, IPs, cloud endpoints) rather than relying on a static list.

**Why:** Forgotten shadow IT and stale exposed services are the most common initial-access entry points attackers find before defenders do.

**Detect:** Certstream/subdomain enumeration output, `external-exposure.csv`, cloud security hub findings, diff of DNS zone records vs. approved inventory.

**References:** OWASP WSTG-INFO-02, CWE-1059, NIST SP 800-119, AWS Security Hub, Cloudflare for Teams

# Attack Surface Reduction (deliberate exposure minimization)

**SHOULD NOT** expose administrative interfaces, dashboards, or debug endpoints directly to the public internet without an access broker such as VPN or zero-trust gateway.

**Why:** Every unnecessary open port is a tested entry point; exposed admin panels are routinely brute-forced or exploited via known CVEs.

**Detect:** `admin`, `console`, `/debug`, `:8080`, `:9200`, `kibana`, `phpmyadmin` in public ingress or SecurityGroup rules; Terraform `ingress = 0.0.0.0/0`.

**References:** OWASP ASVS V1.3, CWE-489, NIST SP 800-53 AC-3, CIS Benchmark 5.1

# Purple Teaming (red+blue collaborative feedback loops)

**SHOULD** run structured purple-team sessions where red-team techniques are replayed against blue detections, closing each gap in both directions.

**Why:** Siloed red and blue teams optimize for scoring, not detection coverage; joint loops convert attacks into durable telemetry.

**Detect:** `purple-team` session reports, shared `detection-gap` backlog, ATT&CK coverage matrices with blue annotations

**References:** MITRE ATT&CK Evaluations, NIST SP 800-115, CISA Purple Team guidance

# Breach & Attack Simulation (adversary emulation vs controls)

**MAY** automate adversary emulation (BAS) to continuously replay known TTPs against controls, but only in environments with tested rollback and blast-radius limits.

**Why:** Point-in-time tests decay; continuous emulation catches control regressions — unbounded, it can itself cause outages.

**Detect:** BAS tool configs (SafeBreach, AttackIQ, Atomic Red Team), `atomic-red-team` in CI, simulation schedules with rollback plans

**References:** MITRE ATT&CK, Gartner BAS category, Atomic Red Team (T1059 etc.)

# Shift-Left Security (security earliest in the lifecycle)

**MUST** run SAST, dependency, and secret scanning in CI on every pull request, failing the build on high-severity findings rather than deferring them to pre-release.

**Why:** Defects caught in production cost orders of magnitude more than at commit time; late gates train teams to bypass them.

**Detect:** `.github/workflows` with `sast`/`semgrep`/`gitleaks` steps, `fail-on: high` in scanner config, pre-commit hooks

**References:** OWASP SAMM Security Testing, MS SDL, OWASP DevSecOps Maturity Model

# Secure by Design (architectural input, not a patch)

**MUST** treat security requirements as architectural inputs at design time — least privilege, defense in depth, secure defaults — not bolt-ons retrofitted after review.

**Why:** Architecture that assumes trust is unpatchable later; every bolt-on inherits the original flaw's blast radius.

**Detect:** design docs citing `least privilege` / `defense in depth`, ADRs with security sections, default-deny network policies

**References:** NIST SP 800-160, Saltzer & Schroeder principles, OWASP ASVS V1, CISA Secure by Design Pledges

# Security Champions Program (embedded advocates per team)

**SHOULD** embed a trained security champion in each engineering team, with paid time allocated, a refresh cadence, and a direct escalation line to the security group.

**Why:** A central security team cannot review everything; without funded champions, the role quietly evaporates under delivery pressure.

**Detect:** `champions` roster doc, training completion records, `office hours` schedule, per-team champion named in CODEOWNERS

**References:** OWASP SAMM Security Champions, BSIMM 11.1, Microsoft Security Champions Program

# Verification-Level Tiers (ASVS L1/L2/L3: basic / standard / privileged-app requirements)

**MUST** assign every application an ASVS baseline (L1 threat-modeled, L2 sensitive data, L3 privileged) and verify controls at that tier.

**Why:** Untiered apps get either theater-grade checks for high-risk systems or gaps that privileged attackers exploit.

**Detect:** grep for `ASVS`, `verification_level`, `baseline: L1|L2|L3` in security docs, scanner configs, requirements trackers.

**References:** OWASP ASVS 4.0.3, OWASP SAMM, NIST SP 800-53 tailoring

# Attack-Path Analysis (reachable chains from exposure to crown jewels)

**SHOULD** continuously map reachable attack paths from internet exposure and low-privilege identities to critical assets, and cut the shortest chains first.

**Why:** Individual findings look minor in isolation; it's the composed chain — public bucket to role trust to database — that actually breaches you.

**Detect:** grep for attack-path tooling: `cartography`, `bloodhound`, `peanut`, Wiz/Knossos attack paths, `reachability` graph exports, `attack_path` reports in vuln management.

**References:** MITRE ATT&CK, NIST SP 800-30 (risk assessment), BloodHound docs, CSEM attack-path analysis

