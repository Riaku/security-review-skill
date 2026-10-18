# Sources & Attribution

Every external source this skill's content was derived from, with what it
contributed. Kept current as new sources are mined.

## User-provided sources

| Source | Contributed |
|---|---|
| Original 250-item checklist by **@ghumare64 (Sahil Ghumare)** — https://x.com/ghumare64/status/2111332908657148356 | Seed list; the taxonomy's foundation |
| **Arjay McCandless — System Design Cheat Sheet** (ArjayTheDev) | CQRS, reliability patterns, long-running jobs, real-time data, write-scaling items |
| **Arjay McCandless — The Ultimate System Design Playbook** — https://www.arjaythedev.com/pdfs/system-design-guide.pdf | v11: database-workload fit, sticky sessions, priority queues/HOL blocking, durability ack policy, NFR traceability |
| https://github.com/100Psycho007/awesome-cybersecurity-for-developers | v7 mining pass |
| https://docs.github.com/en/code-security | v7: push protection, SARIF standardization, secret validity checks, malware alerts |
| https://github.com/sbilly/awesome-security | v7: ASM/ASR, purple teaming, breach simulation, shift-left, secure-by-design, champions |
| https://github.com/jassics/security-study-plan | v7 mining pass |
| https://www.splunk.com/.../threat-hunters-cookbook.pdf | **Gated — could not be fetched.** Threat-hunting items (threat-hunting, beaconing, masquerading, exfiltration, LtL) were authored from general knowledge of the discipline, not from this PDF |
| https://www.sonarsource.com/.../sonarqube (paid-search link) | SonarQube listed in `references/tooling.md`; no checklist content mined (marketing page) |
| https://github.com/Anof-cyber/Application-Security | **Unusable — no readable README at time of mining.** Nothing sourced |

## Guide/framework sources (proposed by agent, approved by user)

| Source | Contributed |
|---|---|
| OWASP ASVS | verification-level tiers; app-sec item wording |
| OWASP WSTG | detect-methodology; conf/athz items |
| OWASP Cheat Sheet Series | prescriptive wording across items |
| SANS Top 25 Most Dangerous Software Errors | correctness-pitfalls severity weighting |
| NIST SP 800-161r1 | supply-chain risk management |
| SLSA (slsa.dev) | build provenance, hermetic builds |
| OpenSSF Scorecard | repo-hygiene items (branch protection, pinned actions, fuzzing) |
| MITRE ATT&CK (incl. Cloud matrix) | lateral movement, credential access, container escape, masquerading |
| AWS Well-Architected Security Pillar | cloud-network / deployment items |
| Salesforce policy_sentry | IAM least-privilege, dangerous-policy items |
| Prowler | CSPM detect patterns |
| open-guides/og-aws | backup/ops gotchas |
| danluu post-mortem collection (github.com/danluu/post-mortems) | incident-review items |
| CNCF Cloud Native Security Whitepaper (cncf/tag-security) | lifecycle-domain framing |
| Google Search Central + web.dev (CWV, Lighthouse docs) | seo-web-quality category |
| Vendor platform docs (Cloudflare, Vercel, GitHub Pages, Fly.io, Azure, GCP) | `references/platform-hosting.md` surfaces |

## Pattern sources

| Source | Contributed |
|---|---|
| Matt Pocock's `grilling` skill — https://github.com/mattpocock/skills (skills/productivity/grilling) | `references/tree-traversal.md` frontier/rounds model |
| Agent Skills specification — https://agentskills.io/specification | repo structure, progressive disclosure |

## User-provided content (not external)

- System-design additions from user's screenshots (reads/writes split, reliability, long-running jobs, real-time, scale-writes)
- Engineering-practice additions (O(n²)/nested loops, TDD, circuit breakers, rate limiting, idempotency, CI/CD, exception handling, cost/observability alerting)
- Compliance direction (CIS, STIG, FedRAMP, and related government/regulatory regimes)
