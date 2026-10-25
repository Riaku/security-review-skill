# Sources & Attribution

The principal sources behind this corpus, and what each contributed. This list
is deliberately **not** exhaustive: every item carries its own `References:`
line, and those per-item citations are the authoritative record of what
supports a specific rule — together they reach more sources than are listed
here. Credit for the seed list and the taxonomy's shape comes first.

## Sources

| Source | Contributed |
|---|---|
| Original 250-item checklist by **@ghumare64 (Sahil Ghumare)** — https://x.com/ghumare64/status/2111332908657148356 | Seed list; the taxonomy's foundation |
| **Arjay McCandless — System Design Cheat Sheet** (ArjayTheDev) | CQRS, reliability patterns, long-running jobs, real-time data, write-scaling items |
| **Arjay McCandless — The Ultimate System Design Playbook** — https://www.arjaythedev.com/pdfs/system-design-guide.pdf | v11: database-workload fit, sticky sessions, priority queues/HOL blocking, durability ack policy, NFR traceability |
| https://github.com/100Psycho007/awesome-cybersecurity-for-developers | v7 mining pass |
| https://docs.github.com/en/code-security | v7: push protection, SARIF standardization, secret validity checks, malware alerts |
| https://github.com/sbilly/awesome-security | v7: ASM/ASR, purple teaming, breach simulation, shift-left, secure-by-design, champions |
| https://github.com/jassics/security-study-plan | v7 mining pass |
| https://www.okta.com (Auth0) — Essential Practices for Securing AI-Generated Code whitepaper | AI-generated-code review posture; full-stack and CI/CD security checklist alignment |
| OWASP Secure Product Design Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Secure_Product_Design_Cheat_Sheet.html | v12: fail-secure configuration, secure-by-default, defense-in-depth layering |
| CISA Secure by Design — https://www.cisa.gov/securebydesign | v12: secure-by-default shipping (MFA/logging/SSO not paywalled); memory-safety roadmap context |
| CISA Cybersecurity Best Practices — https://www.cisa.gov/topics/cybersecurity-best-practices | Zero Trust framing for `zero-trust-architecture` |
| MITRE ATT&CK — https://attack.mitre.org/ (Cloud matrix: https://attack.mitre.org/matrices/enterprise/cloud/) | `references/mitre-attack.md`: tactic→issue mapping for detection tagging and coverage review |
| https://github.com/dronezzzko/software-development-best-practices | Cross-references confirming guide coverage (API/security/language guides cited across SOURCES) |

## Guide/framework sources

| Source | Contributed |
|---|---|
| OWASP ASVS | verification-level tiers; app-sec item wording |
| OWASP WSTG | detect-methodology; conf/athz items |
| OWASP Cheat Sheet Series | prescriptive wording across items |
| MITRE CWE — https://cwe.mitre.org/ | weakness taxonomy; per-item CWE references (cited by 381 items) |
| NIST SP 800-53 Rev 5 — https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final | control references for access control, audit, integrity and crypto items (62 items) |
| CIS Benchmarks / CIS Controls — https://www.cisecurity.org/cis-benchmarks | host and platform hardening baselines (9 items) |
| PCI DSS v4.0 — https://www.pcisecuritystandards.org/ | payment-card scope, storage and transmission rules (8 items) |
| GDPR — https://gdpr-info.eu/ | privacy items: purpose limitation, data minimisation, retention (20 items) |
| ISO/IEC 27001 & 27002 | ISMS control mapping for governance items (8 items) |
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
| QA of Code guidance (Best Practice and Impact) — https://best-practice-and-impact.github.io/qa-of-code-guidance/ | v14: notebook/session leakage, git-history secret remediation, data versioning, raw-data immutability, config-example drift, test determinism, self-generated goldens, proportionate QA, dual-run equivalence, decision provenance, AI-code ownership |
| Google developer documentation style guide — https://developers.google.com/style | documentation-quality category: style consistency, README content |
| ASD-STE100 Simplified Technical English — https://asd-ste100.org | simplified-technical-english item; controlled-language references in style/inclusive doc items |
| Write the Docs style-guide guide — https://www.writethedocs.org/guide/writing/style-guides/ | DRY docs, style-guide adoption practice |
| Mailchimp Content Style Guide — https://styleguide.mailchimp.com/ | tone/clarity practice informing doc-style items |
| Stack Overflow: code comment best practices — https://stackoverflow.blog/2021/12/23/best-practices-for-writing-code-comments/ | comments-explain-why item |
| MIT CommKit: coding and comment style — https://mitcommlab.mit.edu/broad/commkit/coding-and-comment-style/ | comments-explain-why item |
| daily.dev: 10 code-commenting best practices — https://daily.dev/blog/10-code-commenting-best-practices-for-developers/ | comments-explain-why item |
| dev.to: essential guide to code commenting — https://dev.to/codebyturkan/the-essential-guide-to-code-commenting-best-practices-types-and-documentation-4e6c | comments-explain-why item |
| RFC 2119 / RFC 8174 (BCP 14) — https://www.rfc-editor.org/rfc/rfc2119.txt, https://www.rfc-editor.org/rfc/rfc8174.txt | bcp14-keyword-usage item; the skill's own normative wording standard |
| Anthropic Claude Code best practices — https://www.anthropic.com/engineering/claude-code-best-practices | v15: verification loop, hooks-vs-advisory, session-hygiene failure patterns, instruction-file bloat |
| Cursor docs (rules / agent security / Bugbot / cloud agents) — https://cursor.com/docs | v15: sandbox/run-modes, neutral-status trap, base-branch review config, .cursorignore |
| GitHub Copilot docs (code review / custom instructions / agent risks / rubber-duck) — https://docs.github.com/en/copilot | v15: agent auditability chain, cross-model critic, automations governance, instruction-file guidance |
| DeepSeek harness docs — https://deepseek-harness.github.io/deepseek-harness/en/guide/github-review | v15: webhook trust separation, repo-cannot-set-proxy fail-closed pattern |
| Qwen3-Coder — https://qwenlm.github.io/blog/qwen3-coder/ | easy-to-verify philosophy backing the agent verification loop |
| Z.ai (GLM) dev-pack best practice — https://docs.z.ai/devpack/resources/best-practice.md | v15: Goal/Context/Constraints/Done-when, session-per-task, environment-context = permission surface |
| Gemini Code Assist style guide & docs — https://cloud.google.com/gemini/docs/code-review/style-guide | review-category framing; .aiexclude exclusion pattern |
| OpenAI Codex security docs — https://developers.openai.com/codex/agent-approvals-security.md | v15: sandbox×approval matrix, two-phase secret lifecycle, cached-search injection defense |
| Amazon Q Developer docs (code reviews / severity / MCP security) — https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/code-reviews.md | six review classes; CVSS×access×effort severity matrix; MCP trust principles |
| 12-Factor App — https://12factor.net/ | v16: twelve-factor-apps, build-release-run-separation, logs-as-event-streams, one-off-admin-processes |
| Martin Fowler — Microservices (Decentralized Data Management) — https://martinfowler.com/articles/microservices.html | v16: database-per-service |
| Catio — Architecture as Code — https://www.catio.tech/blog/architecture-as-code | v16: architecture-fitness-functions (per Ford/Parsons/Kua, Building Evolutionary Architectures) |
| aquasecurity/trivy-checks — https://github.com/aquasecurity/trivy-checks | v17: management-plane-activity-alerting, object-level-data-access-logging, dedicated-service-accounts, secrets-in-launch-payloads (mined from 1,103 Rego checks / 995 AVD docs; bulk of remaining checks mapped to existing generic items) |
| ImLunaHey/project-standards — https://github.com/ImLunaHey/project-standards | v22: client-bundle secret exposure, pinned toolchain versions, coverage-exclusion gaming, review-report secret redaction (the portable slice of a stack-opinionated standards repo; stack preferences rejected) |
