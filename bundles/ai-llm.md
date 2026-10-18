# ai-llm — full checklist (31 items)

LLM feature security and quality.

> Generated artifact — edit the issue files, not this one. Sources: [issues/](../issues/) · manifest: [ai-llm](../categories/ai-llm.md) · index: [SKILL.md](../SKILL.md)

# Advisory-vs-Enforced Agent Checks

**MUST** implement every must-happen-every-time agent rule as a deterministic hook (pre-commit, post-edit lint, blocked paths, secret-scan-before-write) — not as instruction text the model may skip.

**Why:** The whole ecosystem converged on this distinction: "hooks are deterministic; CLAUDE.md is advisory" (Anthropic). Policy claimed in instruction files with no hook behind it is unenforced policy wearing a costume.

**Detect:** security rules present only in instruction-file text with no corresponding hook/CI enforcement; hook config (e.g. .claude/settings.json) empty while policy claims enforcement.

**References:** Anthropic hooks-vs-instructions guidance, Copilot CLI hooks, Cursor hooks, Codex hooks

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [governance](../domains/governance.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Agent Context-Exclusion Files

**SHOULD** maintain agent exclusion files (.cursorignore, .aiexclude, equivalent) covering secrets, credentials, and sensitive modules so they never enter agent context or indexes.

**Why:** Anything the agent can read, it can echo into code, logs, or a PR; exclusion files are the gitignore of the AI-context layer and their absence means sensitive paths are agent-reachable by default.

**Detect:** repo root lacks .cursorignore/.aiexclude while secrets/sensitive dirs are agent-reachable; index covers branches/patterns beyond the stable set; exclusion list missing recently-added sensitive paths.

**References:** Cursor .cursorignore, Gemini .aiexclude, GitHub content-exclusion controls

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Agent Egress Allowlist & Proxy Control

**MUST** route coding-agent egress (model calls, MCP-over-HTTP, web fetch) through an explicit proxy/allowlist — and repo-supplied env must never control where agent traffic goes.

**Why:** Some agent harnesses refuse to start rather than honor repo-controlled proxy settings, and vendors ship allowlist-first egress where deny wins — repo-controlled egress is an exfiltration path.

**Detect:** agent runs without managed proxy; wildcard `*` in agent network allow rules; MCP servers reaching arbitrary hosts; repo .env containing proxy settings honored by agent tooling.

**References:** OpenAI Codex domain rules, Anthropic agent network controls, vendor agent egress allowlists

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [cloud-network](../categories/cloud-network.md) · [governance](../domains/governance.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Human-in-the-loop approval for destructive agent tool calls

**MUST** require explicit human confirmation before an autonomous agent executes destructive actions (deletes, payments, sends, deploys).

**Why:** A hijacked or hallucinating agent with unguarded write access can cause irreversible damage in a single automated chain.

**Detect:** agent tool registry lacks confirm/approval flags on destructive verbs; auto-execute=true on write-capable tools.

**References:** OWASP LLM06:2025, NIST AI RMF GOVERN 3, CWE-807

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Agent Instruction-File Review Surface

**MUST** code-review and CODEOWN every agent instruction file (CLAUDE.md, AGENTS.md, .cursor/rules/*.mdc, copilot-instructions.md, .gemini/styleguide.md, QWEN.md) and keep it concise — bloated instruction files are silently ignored, making unenforced policy invisible.

**Why:** These files steer all generated code in the repo; a one-line frontmatter change (e.g. `alwaysApply: true`) is a prompt-injection-from-inside-the-repo vector, and rot makes claims diverge from CI reality.

**Detect:** PRs touching instruction files without review; instruction files >500 lines or full of task-specific one-offs; divergence between instruction-file claims and actual CI config.

**References:** GitHub custom-instructions guidance (≤2 pages), Cursor rules docs (<500 lines, check into git), Anthropic "bloated CLAUDE.md gets ignored"

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [documentation-quality](../categories/documentation-quality.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Agent Session Hygiene

**SHOULD** run one session per task, clear context after two failed corrections, and push broad exploration to subagents — mixed-task or polluted sessions degrade output and retain stale secrets/instructions.

**Why:** Anthropic names the failure patterns (kitchen-sink session, correct-over-and-over, infinite unscoped exploration); GLM codifies session-per-task — stale context silently biases every later generation and can leak prior-task secrets into new code.

**Detect:** judgment on session transcripts: unrelated tasks per session, >2 correction loops in one session, unscoped "investigate everything" runs in the main context.

**References:** Anthropic named failure patterns, GLM session-management guidance, Cursor cloud-agent session practice

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Agent Session-Log Traceability

**MUST** link every agent-authored commit to its session transcript and the human who initiated it (co-author trailer, session-log URL in commit message, verified signature).

**Why:** Without the commit→session→human chain, agent work is unauditable — you cannot answer who asked for this, what context the agent saw, or who owns the outcome.

**Detect:** bot commits lacking co-author/session links; agent tooling with transcripts disabled or rotated to zero retention; no mapping from merged PR to agent run.

**References:** GitHub Copilot agent auditability (signed commits, session-log link), OpenAI Codex transcripts, DeepSeek harness session-log model

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [observability](../categories/observability.md) · [governance](../domains/governance.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Agent Verification Loop (Executable Done-When)

**MUST** give every AI-agent coding task a runnable pass/fail verification criterion (tests, build, script-vs-fixture) wired into the task itself — otherwise the human becomes the verification loop.

**Why:** Industry practice converges on this: an agent without an executable check ships plausible-looking code indefinitely.

**Detect:** agent task/plan artifacts merged with no named test/build/acceptance command; "implement X" tickets with no check; agent PRs whose CI runs no tests on the change.

**References:** Anthropic Claude Code best practices, vendor coding-agent verification guidance

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [testing-strategy](../categories/testing-strategy.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# AI-Code Ownership Policy

**MUST** hold a named human accountable for every merged AI-generated change — no unreviewed AI output — and maintain team skill on owned code rather than letting understanding decay.

**Why:** Merge gates alone don't prevent deskilling: teams that stop understanding their own code lose the ability to review, debug, and secure it — the accountability must be a policy, not just a pipeline step.

**Detect:** judgment on documented policy artifacts: AI-use guidelines naming accountable owners, review requirements that don't weaken for AI-authored PRs, evidence reviewers can explain the code they approve.

**References:** AI-generated-code review companion, deskilling research (METR/Anthropic findings), engineering-ownership practice

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# AI-generated code review gate before merge

**SHOULD** require human security review of AI-generated code before merge; Copilot-style output is not self-certifying.

**Why:** Models reproduce vulnerable patterns and plausible-but-broken crypto from training data at high volume and speed.

**Detect:** PRs with AI-assist labels merged without security-review approval; CI lacks a gate matching ai-generated/copilot review policy.

**References:** OWASP LLM03:2025, NIST SSDF PW.4, CWE-1157

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [governance](../domains/governance.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Coding-Agent Sandbox & Permission-Mode Review

**MUST** review how coding agents are configured: OS-level sandbox on, writes workspace-scoped, network off by default, approval policy enforced — and flag bypass flags (`--yolo`, `dangerously-*`, `bypassPermissions`, `approval=never`).

**Why:** The agent's technical reach, not its instructions, is the real boundary; full-access modes inside a dev container let a malicious repo exfiltrate everything reachable, including the agent's own credentials.

**Detect:** grep agent configs for `--yolo`, `dangerously-bypass`, `sandbox_mode = "danger-full-access"`, `approval_policy = "never"`, `bypassPermissions`; check for OS-enforced sandbox vs advisory-only policy.

**References:** OpenAI Codex approvals/security model, Anthropic /sandbox + permissions, Cursor Run Modes ("best-effort, not a hard boundary")

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [security-practices](../categories/security-practices.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Context Windows

**SHOULD** bound and trim conversation context explicitly so sensitive earlier turns are evicted rather than silently retained or truncated unpredictably.

**Why:** Unbounded context hoards PII and secrets in every replay, and overflow truncation can drop safety instructions mid-session.

**Detect:** config keys max_tokens, context_length, truncation strategy; no retention/eviction logic in history builders.

**References:** OWASP LLM10:2025, CWE-778, NIST SP 800-53 AT-4

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Cross-Model Review Diversity

**SHOULD** run the AI reviewer/critic on a different model family than the producer for security-sensitive changes — same-model review shares blind spots.

**Why:** Some vendors run the reviewer/critic on a different model family, on the theory it is less likely to share the same blind spots, biases, or failure modes; a same-model reviewer tends to approve its own kind's mistakes.

**Detect:** review pipeline config shows same model for author and critic; no independent-model step for security-sensitive diffs; judgment on independence of the review chain.

**References:** vendor cross-model review practice, Anthropic fresh-context adversarial subagent review

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Embedding inversion and sensitive data in vector stores

**SHOULD NOT** embed raw sensitive documents in vector stores without assessment; embeddings can leak near-verbatim source text under inversion attacks.

**Why:** Published inversion techniques reconstruct personal and confidential content from vectors alone, defeating assumed one-way hashing.

**Detect:** vector DB ingest of unmasked PII fields; no access control on pgvector/Qdrant/Milvus collections; embeddings exported freely.

**References:** OWASP LLM02:2025, OWASP LLM08:2025, CWE-311

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# EU AI Act conformity (risk tiering, GPAI obligations, transparency and deployment deadlines)

**MUST** classify each AI system's risk tier and meet the corresponding obligations—transparency notices, conformity assessment for high-risk, GPAI documentation—before the phased enforcement deadlines.

**Why:** Systems deployed without risk classification face market withdrawal and fines up to 7% of turnover once enforcement phases begin.

**Detect:** grep for "high-risk", "GPAI", "Annex III", "conformity", "Article 50 transparency"; AI features with no risk tier or labeling.

**References:** EU AI Act 2024/1689, Annex III, GPAI Code of Practice, EU AI Office

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# Evals

**MUST** run security-focused evaluation suites covering injection, data leakage, and refusal bypass before shipping or updating any model-backed feature.

**Why:** Without adversarial evals, regressions in safety behavior ship silently and are discovered by attackers first.

**Detect:** missing red-team eval datasets, no CI job matching eval|redteam|adversarial, promptfoo/garak config absent.

**References:** OWASP LLM01:2025, NIST AI RMF MEASURE, MITRE ATLAS

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Hallucinated Packages

**SHOULD** verify that every package name in generated or AI-assisted code actually exists and matches intent before installing.

**Why:** Attackers pre-register plausible-sounding package names that AI models invent, so blindly installing them pulls malware into the project.

**Detect:** Install logs for names absent from the registry; review AI-generated import lines against PyPI/npm search; grep manifests for near-miss spellings of popular libs.

**References:** CWE-427, Snyk "slopsquatting" research, OWASP LLM03

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [supply-chain](../categories/supply-chain.md) · [governance](../domains/governance.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Jailbreak Red-Teaming

**SHOULD** run recurring adversarial jailbreak testing against production prompts, logging and feeding results into the eval suite.

**Why:** Static safety guardrails decay as novel jailbreaks circulate publicly; untested systems fail the day one lands.

**Detect:** no garak/pyrit/jailbreakbench runs in CI; absence of stored jailbreak regression corpora or refusal-bypass tests.

**References:** OWASP LLM01:2025, MITRE ATLAS, NIST AI 100-3

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# PII redaction and DPAs before sending data to third-party LLM APIs

**MUST** redact or tokenize PII and execute a DPA with the provider before payloads leave the trust boundary.

**Why:** Personal data reaching an external model API may be logged, retained, or trained on beyond compliance scope.

**Detect:** outbound LLM calls without redaction middleware; missing DPA or zero-retention agreement in vendor records.

**References:** GDPR Art. 28, OWASP LLM02:2025, NIST Privacy Framework

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [compliance-privacy](../categories/compliance-privacy.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Denial-of-wallet: unbounded LLM token spend per user/tenant

**MUST** enforce per-user and per-tenant token budgets, rate limits, and alerting on LLM API spend.

**Why:** A scripted attacker or runaway agent loop can burn thousands of dollars in tokens within hours on a metered API.

**Detect:** no rate_limit, max_tokens, or budget keys on LLM gateway routes; provider usage alerts not configured.

**References:** OWASP LLM10:2025, CWE-770, CWE-400

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [scaling-capacity](../categories/scaling-capacity.md) · [governance](../domains/governance.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Treat LLM output as untrusted input (sanitize before HTML/SQL/shell/URL sinks)

**MUST** sanitize or parameterize every LLM output before it reaches an HTML, SQL, shell, or URL sink.

**Why:** A coerced model emitting markup or queries delivers stored XSS and injection through a path teams assume is safe.

**Detect:** model response rendered via |safe / innerHTML or concatenated into queries or subprocess args.

**References:** OWASP LLM01:2025, CWE-79, CWE-89, CWE-78

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [security-practices](../categories/security-practices.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Third-party MCP/plugin trust and malicious tool-description injection

**MUST** vet, pin, and sandbox third-party MCP servers and plugins; treat their tool descriptions and names as untrusted input to the model.

**Why:** A malicious tool description can instruct the agent to exfiltrate data or chain other tools harmfully.

**Detect:** MCP config pulling unpinned packages; no approved-server allowlist; tool descriptions unsanitized at registration.

**References:** OWASP LLM06:2025, MITRE ATLAS, CWE-829

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [supply-chain](../categories/supply-chain.md) · [governance](../domains/governance.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Model Artifact Integrity (pickle-format models)

**MUST NOT** load pickle-format model artifacts (.pkl, .pt via torch.load default) from untrusted sources; prefer safetensors or verified signed formats.

**Why:** Pickle executes arbitrary code at load time, so a malicious checkpoint is remote code execution before inference starts.

**Detect:** grep torch.load( without weights_only=True, pickle.load on model files, .pkl/.ckpt pulled from Hub without checksum/signature.

**References:** OWASP LLM03:2025, CWE-502, CWE-94

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [supply-chain](../categories/supply-chain.md) · [governance](../domains/governance.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Model Version Pinning

**MUST** pin exact model versions or digests rather than floating aliases like gpt-4 or latest in production configs.

**Why:** Silent upstream model swaps change safety behavior and data-handling guarantees without any code review.

**Detect:** grep model: "latest", model: gpt-4 without dated suffix; missing digest/revision fields in inference config.

**References:** OWASP LLM05:2025, CWE-1104, NIST AI RMF MANAGE

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Prompt Injection

**MUST** treat all untrusted content (user input, retrieved documents, tool output) as data, never as instructions that override system policy.

**Why:** Injected text can hijack model behavior, leaking secrets or triggering actions the operator never authorized.

**Detect:** raw user/RAG strings interpolated into f-string prompts; missing delimiters or injection test cases.

**References:** OWASP LLM01:2025, CWE-74, NIST AI 100-2

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# RAG / Knowledge-Base Poisoning

**SHOULD** validate, provenance-check, and isolate ingested documents so attacker-controlled content cannot enter the retrieval index.

**Why:** Poisoned knowledge bases make malicious instructions appear as trusted retrieved context on every query.

**Detect:** ingest pipelines without source allowlists or content scanning; vector index accepting unauthenticated uploads.

**References:** OWASP LLM04:2025, CWE-506, MITRE ATLAS

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Review-Bot Neutral-Status Trap

**MUST** verify that AI review gates actually fail on unresolved findings — a required status that reports neutral/success while findings remain open does not block merges.

**Why:** Cursor documents this explicitly (findings default to neutral; you must enable fail-on-unresolved); GitHub Copilot defaults to "Comment" not "Approve" — teams often believe they have an AI gate they don't have.

**Detect:** branch protection requiring a bot check whose conclusion set lacks failure-on-findings; severity thresholds set above real risk; review config where unresolved ≠ failed.

**References:** Cursor Bugbot status semantics, GitHub Copilot review default-Comment behavior, Gemini severity-threshold filtering

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [governance](../domains/governance.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Shadow AI: unsanctioned AI SaaS and embedded AI features in the stack

**MUST** inventory and govern AI features in third-party software and employee-adopted AI SaaS, since unsanctioned tools move data outside policy.

**Why:** Copilots and AI-enabled vendors quietly move code, tickets, and documents to unvetted providers.

**Detect:** network egress to openai.com/anthropic.com from unmanaged endpoints; no AI usage policy or CASB/SaaS inventory entries.

**References:** OWASP LLM09:2025, NIST AI RMF GOVERN 6, CWE-912

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [compliance-privacy](../categories/compliance-privacy.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# System prompt extraction and sensitive config embedded in prompts

**SHOULD NOT** embed secrets, credentials, or proprietary logic in system prompts, since extraction via jailbreak or logging is always possible.

**Why:** Prompt contents can be coaxed out verbatim by an attacker or leaked through provider logs.

**Detect:** API keys, connection strings, or business rules literal in system prompt templates; prompt text in logs/tracing exporters.

**References:** OWASP LLM07:2025, CWE-522, CWE-200

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Tool / Function-Call Argument Injection

**MUST** validate and schema-check every model-generated tool argument server-side before execution; never trust the model to sanitize parameters.

**Why:** A manipulated model can emit crafted arguments that turn a benign tool into SQL, shell, or path-traversal execution.

**Detect:** tool dispatch calling exec/query with model output unchecked; missing JSON-schema validation on function-call payloads.

**References:** OWASP LLM06:2025, CWE-74, OWASP Top 10 A03

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Unattended-Agent Automation Governance

**MUST** govern scheduled/event-triggered agents (cron, webhook) with: attribution to the automation creator, minimal tool surface per automation, trigger trust controls (signed webhooks, ignore non-trusted events), and preserved downstream human approval.

**Why:** Unattended agents run with no human per task — GitHub documents a dedicated automations-risk section; DeepSeek's review harness gives inbound webhook auth ZERO outbound authority by design.

**Detect:** automations with broad tool grants or opt-in to untrusted-user events; webhook endpoints accepting unsigned payloads; no owner attribution per automation; agent can merge/approve its own output.

**References:** GitHub Copilot automations risks-and-mitigations, DeepSeek harness webhook model, Cursor Automations docs

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [governance](../domains/governance.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

