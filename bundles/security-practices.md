# security-practices — full checklist (30 items)

Process-level security practices (modeling, disclosure, patching).

> Generated artifact — edit the issue files, not this one. Manifest: [categories/security-practices.md](../categories/security-practices.md) · Index: [SKILL.md](../SKILL.md)

# Admin Activity Review

**SHOULD** periodically review administrative actions (config changes, permission grants, data exports) against expected operations, on a defined cadence.

**Why:** Insider misuse and compromised admin accounts both hide in plain sight; unreviewed admin logs are a detection gap no amount of collection fixes.

**Detect:** check for scheduled admin-log review (CloudTrail console history, K8s audit webhook, DBA action log) with named reviewer and findings tracked; flag "logs exist but nobody reviews them".

**References:** NIST 800-53 AU-6 review, SOC2 CC7 monitoring, CIS 1.10/8.x log review

# Architecture Doc & ADR Coverage

**SHOULD** maintain a current architecture overview (components, data flow, trust boundaries) plus ADRs for settled design decisions, kept in the repo.

**Why:** Without a current overview, every reviewer and new engineer rebuilds the mental model from code — and without ADRs, settled decisions get re-litigated endlessly or silently violated by people who never knew they were settled.

**Detect:** check for architecture doc with a diagram covering current components (compare against actual services/dirs); check docs/adr/ (or equivalent) exists with dated, numbered records; flag overview last-updated far behind structural changes.

**References:** C4 model, ADR practice (Nygard)

# Attack-Path Analysis (reachable chains from exposure to crown jewels)

**SHOULD** continuously map reachable attack paths from internet exposure and low-privilege identities to critical assets, cutting shortest chains first.

**Why:** Findings look minor in isolation; it's the composed chain — public bucket to role trust to database — that actually breaches you.

**Detect:** grep `cartography`, `bloodhound`, `attack_path` reports, reachability graph exports.

**References:** MITRE ATT&CK, NIST SP 800-30, BloodHound docs

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

# Coding-Agent Sandbox & Permission-Mode Review

**MUST** review how coding agents are configured: OS-level sandbox on, writes workspace-scoped, network off by default, approval policy enforced — and flag bypass flags (`--yolo`, `dangerously-*`, `bypassPermissions`, `approval=never`).

**Why:** The agent's technical reach, not its instructions, is the real boundary; full-access modes inside a dev container let a malicious repo exfiltrate everything reachable, including the agent's own credentials.

**Detect:** grep agent configs for `--yolo`, `dangerously-bypass`, `sandbox_mode = "danger-full-access"`, `approval_policy = "never"`, `bypassPermissions`; check for OS-enforced sandbox vs advisory-only policy.

**References:** OpenAI Codex approvals/security model, Anthropic /sandbox + permissions, Cursor Run Modes ("best-effort, not a hard boundary")

# Cyber insurance alignment: coverage preconditions and denial clauses

**MUST NOT** let representations on insurance applications (MFA everywhere, EDR deployed, backups tested) drift from actual configuration, since denial clauses void claims on misrepresentation.

**Why:** Insurers investigate post-incident and deny payouts when stated controls are absent—leaving the breach cost entirely self-funded.

**Detect:** grep policy "warranty", "condition precedent" against live config: MFA, EDR/antivirus, offline backups, patch SLA mismatches.

**References:** ISO 27001/27017, CVE-based exclusion clauses, Marsh/Gallagher cyber underwriting guidance

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

# Fail-Secure Configuration

**MUST** design components to fail in a secure state: auth failures deny access, TLS verification failures abort the connection, policy engine outages block rather than allow, and partial initialization never exposes privileged surfaces.

**Why:** Fail-open is the silent killer — an auth service timeout that defaults to "allowed" or a verifier that skips on error turns an outage into a breach window.

**Detect:** grep for `except: pass` / default-allow branches around authz and TLS verify calls; check `failOpen: false` on admission webhooks, `ssl_verify` defaults, circuit-breaker fallback behavior on security checks.

**References:** OWASP Secure Product Design Cheat Sheet (fail securely), NIST SP 800-162 fail-closed guidance

# Living-off-the-Land Abuse

**MUST** monitor execution of legitimate binaries (curl, ssh, powershell, wmic, certutil, base64) for arguments and contexts inconsistent with normal operations.

**Why:** Attackers weaponize signed system tools to run malicious work, evading malware detection because nothing "bad" is ever installed.

**Detect:** grep EDR/SIEM rules for process-args telemetry on LOLBAS-listed binaries (e.g. `certutil -urlcache`, `powershell -enc`); flag hosts where these run outside admin baselines.

**References:** MITRE ATT&CK T1218 System Binary Proxy Execution, LOLBAS project, CWE-427, Atomic Red Team tests

# Treat LLM output as untrusted input (sanitize before HTML/SQL/shell/URL sinks)

**MUST** sanitize or parameterize every LLM output before it reaches an HTML, SQL, shell, or URL sink.

**Why:** A coerced model emitting markup or queries delivers stored XSS and injection through a path teams assume is safe.

**Detect:** model response rendered via |safe / innerHTML or concatenated into queries or subprocess args.

**References:** OWASP LLM01:2025, CWE-79, CWE-89, CWE-78

# Log Injection & Log Forging

**MUST NOT** write unsanitized user input into log lines; strip CR/LF and control characters before logging any request data.

**Why:** Injected newlines let attackers forge fake log entries or split one entry into many, poisoning the audit trail you rely on during investigations.

**Detect:** grep for user-controlled values interpolated into logger calls (`log.info("User " + username)`) without newline stripping; check for encoder/sanitizer in log appender config.

**References:** OWASP Logging Cheat Sheet, CWE-117

# Memory Safety: Buffer Overflow & Use-After-Free

**MUST** bound every buffer write and never dereference freed or dangling memory in unsafe languages.

**Why:** Overflows and use-after-free are classic primitives for arbitrary code execution and privilege escalation.

**Detect:** `strcpy`/`sprintf`/`memcpy` without size checks, raw `malloc`/`free` lifetimes, indexing past array length, missing bounds sanitizer.

**References:** CWE-120, CWE-416, CWE-787, CERT MEM rules

# Admin Tasks as One-Off Processes from the Release

**SHOULD** run admin and maintenance tasks (migrations, REPLs, one-time scripts) as one-off processes from the same released code, config, and dependency isolation — committed to the repo — rather than ad-hoc scripts executed against production out-of-band.

**Why:** Out-of-band admin access (manual `psql` into prod, hand-copied scripts, SSH one-offs) is unauditable, drifts from the released code's assumptions, and is the classic vector for irreversible mistakes. Running the same image as a scoped one-off Job keeps credentials, code version, and audit trail aligned.

**Detect:** runbooks showing manual DB/console access instead of `kubectl job` or release-hook migrations; admin scripts not present in the repo; production mutations with no corresponding committed task definition.

**References:** 12factor.net/admin-processes, OWASP Logging Cheat Sheet (audit of admin actions), Kubernetes Jobs pattern

# Patch cadence and remediation SLAs for known CVEs in production images

**MUST** rebuild and redeploy base images on a fixed cadence (weekly minimum), remediating critical CVEs within 24 hours of disclosure.

**Why:** Long-lived images accumulate known-exploitable CVEs that scanners flag forever and worms exploit within days.

**Detect:** `.trivyignore` age, `imagePullPolicy: Always`, Renovate/Dependabot config, `fixVersions` in scanner reports

**References:** CWE-1104, CISA KEV, NIST SP 800-40, OWASP A06:2021

# Patch management SLAs (MTTR targets by severity, exception tracking)

**MUST** define mean-time-to-remediate targets per severity (critical 24h, high 30d, medium 90d) and log every exception with owner and expiry date.

**Why:** Undated exceptions silently become permanent debt; SLA clocks make drift visible and auditable.

**Detect:** `sla` / `mttr` keys in policy docs, `waiver` / `exception` tracker files with `expires` fields

**References:** NIST SP 800-40 Rev.4, CIS Control 7, PCI DSS 6.3.3

# Independent penetration testing cadence and finding remediation tracking

**SHOULD** commission an external penetration test at least annually and after major architectural changes, with every finding tracked to closure in a ticketing system.

**Why:** Self-assessment shares the builder's blind spots; untracked findings recur across engagements.

**Detect:** `pentest` reports dated within 12 months, `remediation` tracker with finding IDs, contract/engagement records

**References:** OWASP WSTG, PTES, NIST SP 800-115, PCI DSS 11.4

# Privileged-Action Attribution

**MUST** ensure every privileged action is attributable to a named individual — no shared admin accounts, no service-account interactive use.

**Why:** Shared root/admin credentials destroy non-repudiation; when an incident happens, "admin did it" is not an answer.

**Detect:** grep for shared `admin`/`root` logins in auth logs config, team password vaults for infra creds, kubectl exec under shared identities; check SSO with per-user identity to admin planes.

**References:** NIST 800-53 AC-6/IA-2, SOX ITGC segregation of duties, CIS 1.5 no shared accounts

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

# Security Champions Program (embedded advocates per team)

**SHOULD** embed a trained security champion in each engineering team, with paid time allocated, a refresh cadence, and a direct escalation line to the security group.

**Why:** A central security team cannot review everything; without funded champions, the role quietly evaporates under delivery pressure.

**Detect:** `champions` roster doc, training completion records, `office hours` schedule, per-team champion named in CODEOWNERS

**References:** OWASP SAMM Security Champions, BSIMM satellite, Microsoft Security Champions Program

# Threat Modeling

**MUST** produce a threat model (STRIDE or attack-tree) for every new service before its first production deploy, reviewed with the owning team.

**Why:** Unmodeled trust boundaries ship as real intrusions — attackers exploit the paths nobody drew.

**Detect:** files `docs/threat-model/`, `threat-model.md`, `stride` keywords in PR templates, `threat_model` CI gate

**References:** OWASP Threat Dragon, NIST SP 800-181, OWASP ASVS V1.2

# Verification-Level Tiers (ASVS L1/L2/L3: basic / standard / privileged-app requirements)

**MUST** assign each app an ASVS tier (L1 basic, L2 sensitive data, L3 privileged) and verify controls at that level.

**Why:** Untiered apps get theater-grade checks on high-risk systems, leaving privileged-function gaps attackers exploit directly.

**Detect:** grep `ASVS`, `verification_level`, `baseline: L1|L2|L3` in security docs, scanner configs, requirement trackers.

**References:** OWASP ASVS 4.0.3, OWASP SAMM, NIST SP 800-53 control tailoring

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

