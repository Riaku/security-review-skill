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
| https://www.okta.com (Auth0) — Essential Practices for Securing AI-Generated Code whitepaper (fetched, PDF) | v12: AI-code review posture; full-stack/CI-CD security checklist cross-check (no new gaps beyond existing ai-llm items) |
| OWASP Secure Product Design Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Secure_Product_Design_Cheat_Sheet.html | v12: fail-secure configuration, secure-by-default, defense-in-depth layering |
| CISA Secure by Design — https://www.cisa.gov/securebydesign | v12: secure-by-default shipping (MFA/logging/SSO not paywalled); memory-safety roadmap context |
| CISA Cybersecurity Best Practices — https://www.cisa.gov/topics/cybersecurity-best-practices | Zero Trust + secure-by-design pointers (no new items beyond above) |
| MITRE ATT&CK — https://attack.mitre.org/ (Cloud matrix: https://attack.mitre.org/matrices/enterprise/cloud/) | `references/mitre-attack.md`: tactic→issue mapping for detection tagging and coverage review |
| https://github.com/dronezzzko/software-development-best-practices | Link index only (curated pointers to guides already cited); no checklist content mined |
| Microsoft modern practices / SMB cybersecurity pages (microsoft.com) | Marketing/landing pages — no substantive checklist content mined; nothing sourced |

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
