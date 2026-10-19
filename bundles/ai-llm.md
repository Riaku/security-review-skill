# ai-llm — full checklist (57 items)

LLM feature security and quality.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/ai-llm.md](../categories/ai-llm.md) · Index: [SKILL.md](../SKILL.md)

# Adversarial Issue Descriptions

**MUST** treat issue and bug-report text that triggers automated code changes as untrusted input, and test the fixer with adversarially written issues.

**Why:** Whoever can author the work order can steer an auto-fixer toward code that passes the tests while removing a control.

**Detect:** grep for issue-triggered automation (`on: issues`, auto-fix labels, `@agent fix` handlers) and confirm each has an adversarial-description test case.

**References:** SWEADV (arXiv 2609.15963), https://arxiv.org/abs/2609.15963

# Advisory-vs-Enforced Agent Checks

**MUST** implement every must-happen-every-time agent rule as a deterministic hook (pre-commit, post-edit lint, blocked paths, secret-scan-before-write) — not as instruction text the model may skip.

**Why:** The whole ecosystem converged on this distinction: "hooks are deterministic; CLAUDE.md is advisory" (Anthropic). Policy claimed in instruction files with no hook behind it is unenforced policy wearing a costume.

**Detect:** security rules present only in instruction-file text with no corresponding hook/CI enforcement; hook config (e.g. .claude/settings.json) empty while policy claims enforcement.

**References:** Anthropic hooks-vs-instructions guidance, Copilot CLI hooks, Cursor hooks, Codex hooks

# Agent Approval Atomicity

**MUST** check and consume an approval atomically immediately before execution, requiring fresh approval when the target or parameters change.

**Why:** Approval followed by substitution is a time-of-check/time-of-use hole: the human approves one action and the agent executes another. Single-use approval bound to the exact arguments closes it.

**Detect:** grep approval stores for `get` then `execute` without an atomic consume, and for approvals keyed on tool name rather than a hash of the exact arguments.

**References:** OWASP AI Agent Security Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html, CWE-367 Time-of-check Time-of-use Race Condition

# Agent Auth Strength Parity

**MUST NOT** let an automated agent reach privileged operations through weaker authentication than a human would need for the same operation.

**Why:** An agent holding broad permissions behind a static key is a privilege escalator: attack the weaker credential, inherit the stronger authority.

**Detect:** compare the agent's credential type against the operations in its tool manifest; a long-lived API key or unauthenticated local socket reaching admin actions is the finding.

**References:** NIST SP 800-207 §5.7, https://doi.org/10.6028/NIST.SP.800-207, NIST SP 800-53 IA-5

# Agent Context-Exclusion Files

**SHOULD** maintain agent exclusion files (.cursorignore, .aiexclude, equivalent) covering secrets, credentials, and sensitive modules so they never enter agent context or indexes.

**Why:** Anything the agent can read, it can echo into code, logs, or a PR; exclusion files are the gitignore of the AI-context layer and their absence means sensitive paths are agent-reachable by default.

**Detect:** repo root lacks .cursorignore/.aiexclude while secrets/sensitive dirs are agent-reachable; index covers branches/patterns beyond the stable set; exclusion list missing recently-added sensitive paths.

**References:** Cursor .cursorignore, Gemini .aiexclude, GitHub content-exclusion controls

# Agent Egress Allowlist & Proxy Control

**MUST** route coding-agent egress (model calls, MCP-over-HTTP, web fetch) through an explicit proxy/allowlist — and repo-supplied env must never control where agent traffic goes.

**Why:** Some agent harnesses refuse to start rather than honor repo-controlled proxy settings, and vendors ship allowlist-first egress where deny wins — repo-controlled egress is an exfiltration path.

**Detect:** agent runs without managed proxy; wildcard `*` in agent network allow rules; MCP servers reaching arbitrary hosts; repo .env containing proxy settings honored by agent tooling.

**References:** OpenAI Codex domain rules, Anthropic agent network controls, vendor agent egress allowlists

# Human-in-the-loop approval for destructive agent tool calls

**MUST** require explicit human confirmation before an autonomous agent executes destructive actions (deletes, payments, sends, deploys).

**Why:** A hijacked or hallucinating agent with unguarded write access can cause irreversible damage in a single automated chain.

**Detect:** agent tool registry lacks confirm/approval flags on destructive verbs; auto-execute=true on write-capable tools.

**References:** OWASP LLM06:2025, NIST AI RMF GOVERN 3.2, CWE-807

# Agent Instruction-File Review Surface

**MUST** code-review and CODEOWN every agent instruction file (CLAUDE.md, AGENTS.md, .cursor/rules/*.mdc, copilot-instructions.md, .gemini/styleguide.md, QWEN.md) and keep it concise — bloated instruction files are silently ignored, making unenforced policy invisible.

**Why:** These files steer all generated code in the repo; a one-line frontmatter change (e.g. `alwaysApply: true`) is a prompt-injection-from-inside-the-repo vector, and rot makes claims diverge from CI reality.

**Detect:** PRs touching instruction files without review; instruction files >500 lines or full of task-specific one-offs; divergence between instruction-file claims and actual CI config.

**References:** GitHub custom-instructions guidance (≤2 pages), Cursor rules docs (<500 lines, check into git), Anthropic "bloated CLAUDE.md gets ignored"

# Agent Memory Isolation

**MUST** namespace agent memory per user and session so no stored context can enter another user's prompt.

**Why:** A shared store carries one user's data and instructions into another user's context: a data leak and a persistent injection channel that outlives the session that planted it.

**Detect:** grep memory and vector-store reads/writes for a user or session namespace/partition key; global collection names with no tenant field, and retrieval filtered only by similarity, are the finding.

**References:** OWASP AI Agent Security Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html, OWASP Top 10 for LLM Applications (LLM01 prompt injection)

# Agent Output Trust Per Hop

**MUST** re-validate agent output at every downstream consumer instead of trusting the upstream agent's check.

**Why:** An agent that reads attacker content, acts on it, and writes output other agents consume spreads harm with no vulnerable code anywhere.

**Detect:** grep inter-agent handoffs for output forwarded to another agent or a sink without re-validation at the consumer (`messages.append(tool_result)`, `publish(agent_output)`).

**References:** Agentic runtime threat analysis, https://arxiv.org/abs/2602.19555, OWASP Top 10 for LLM Applications: LLM01 Prompt Injection

# Verify The Whole Plan

**MUST** validate a multi-step agent's whole plan — tool sequence, control flow, data dependencies — against policy before the first action runs.

**Why:** Each step can be individually permitted while the composed execution violates required ordering, approval gates, or data-flow rules.

**Detect:** grep the agent runtime for a pre-execution plan check (state machine or policy evaluation over the tool-call sequence) and reject ungated destructive or spend steps.

**References:** Plan-level policy verification for agents, https://arxiv.org/abs/2609.18674

# Agent Session Hygiene

**SHOULD** run one session per task, clear context after two failed corrections, and push broad exploration to subagents — mixed-task or polluted sessions degrade output and retain stale secrets/instructions.

**Why:** Anthropic names the failure patterns (kitchen-sink session, correct-over-and-over, infinite unscoped exploration); GLM codifies session-per-task — stale context silently biases every later generation and can leak prior-task secrets into new code.

**Detect:** judgment on session transcripts: unrelated tasks per session, >2 correction loops in one session, unscoped "investigate everything" runs in the main context.

**References:** Anthropic named failure patterns, GLM session-management guidance, Cursor cloud-agent session practice

# Agent Session-Log Traceability

**MUST** link every agent-authored commit to its session transcript and the human who initiated it (co-author trailer, session-log URL in commit message, verified signature).

**Why:** Without the commit→session→human chain, agent work is unauditable — you cannot answer who asked for this, what context the agent saw, or who owns the outcome.

**Detect:** bot commits lacking co-author/session links; agent tooling with transcripts disabled or rotated to zero retention; no mapping from merged PR to agent run.

**References:** GitHub Copilot agent auditability (signed commits, session-log link), OpenAI Codex transcripts, DeepSeek harness session-log model

# Setup Docs As Install Surface

**MUST** review setup instructions, requirement files, and build targets that automation executes with the same rigor as dependency manifests.

**Why:** An attacker who edits only a README or Makefile can redirect an agent to an untrusted registry or a known-vulnerable version, and the change passes review because it looks like documentation.

**Detect:** grep docs and Makefiles for install commands: `pip install`, `npm i`, `--index-url`, `-r requirements`, `curl | sh`, `go get` — check each resolves to a canonical registry and pinned version.

**References:** Agent install-time attack surface, https://arxiv.org/abs/2607.15143, OWASP Top 10 for LLM Applications: LLM03 Supply Chain

# Agent Tool Authorization

**MUST** enforce authorization for agent tool execution outside the agent's own decision context, never from a flag the agent sets for itself.

**Why:** Anything inside the model's context is attacker-influenceable through prompt injection, including an 'approved' flag. Enforcement must live in the component that actually executes the call.

**Detect:** grep tool-execution code for approval checks that read agent-supplied arguments, prompt state, or model output instead of a server-side authorization decision.

**References:** OWASP AI Agent Security Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html, OWASP Top 10 for LLM Applications (LLM06 excessive agency)

# Per-Call Tool Authorization

**MUST** authorize each model-initiated tool call against its concrete arguments — scope, recipient, amount, tenant — at execution time, denying by default when no rule matches.

**Why:** A capability gate only proves the agent can reach a tool, never that this recipient, amount, or record is permitted, so a steered argument turns a legitimate tool into a confused deputy.

**Detect:** grep tool dispatch that forwards model-supplied arguments straight to handlers (`tools[name](**args)`, `execute_tool(`, `function_call.arguments`) with no per-call policy check.

**References:** ScopeGate agent authorization study, https://arxiv.org/abs/2606.28679, OWASP Top 10 for LLM Applications: LLM06 Excessive Agency

# Agent Verification Loop (Executable Done-When)

**MUST** give every AI-agent coding task a runnable pass/fail verification criterion (tests, build, script-vs-fixture) wired into the task itself — otherwise the human becomes the verification loop.

**Why:** Industry practice converges on this: an agent without an executable check ships plausible-looking code indefinitely.

**Detect:** agent task/plan artifacts merged with no named test/build/acceptance command; "implement X" tickets with no check; agent PRs whose CI runs no tests on the change.

**References:** Anthropic Claude Code best practices, vendor coding-agent verification guidance

# AI-Code Ownership Policy

**MUST** hold a named human accountable for every merged AI-generated change — no unreviewed AI output — and maintain team skill on owned code rather than letting understanding decay.

**Why:** Merge gates alone don't prevent deskilling: teams that stop understanding their own code lose the ability to review, debug, and secure it — the accountability must be a policy, not just a pipeline step.

**Detect:** judgment on documented policy artifacts: AI-use guidelines naming accountable owners, review requirements that don't weaken for AI-authored PRs, evidence reviewers can explain the code they approve.

**References:** AI-generated-code review companion, deskilling research (METR/Anthropic findings), engineering-ownership practice

# AI-generated code review gate before merge

**SHOULD** require human security review of AI-generated code before merge; Copilot-style output is not self-certifying.

**Why:** Models reproduce vulnerable patterns and plausible-but-broken crypto from training data at high volume and speed.

**Detect:** PRs with AI-assist labels merged without security-review approval; CI lacks a gate matching ai-generated/copilot review policy.

**References:** OWASP LLM05:2025, NIST SSDF PW.7

# AI Halt Authority

**MUST** define in advance who may halt development or deployment of a system judged unacceptably risky, and the procedure for doing so.

**Why:** Without a pre-committed stop path, sunk-cost pressure keeps a risky system shipping while the decision is deferred to whoever objects loudest.

**Detect:** find the governance document naming the stop authority, the trigger criteria, and the last time the path was exercised.

**References:** NIST AI 600-1 GV-1.3-007, https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf

# AI Third-Party Components

**MUST** inventory third-party datasets, pre-trained models, plugins, and hosted model APIs, recording their downstream impact and a contingency plan for failure.

**Why:** Errors and compromises in procured models or data propagate silently into every downstream output, and an uninventoried component cannot be rotated or recalled.

**Detect:** grep for unpinned model and dataset loads (`from_pretrained(`, `hf_hub_download`, dataset URLs, plugin registries) and check each appears in the component inventory with a digest.

**References:** NIST AI 600-1 GOVERN 6.1, https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf

# Approval Claims Verified at Source

**MUST** verify any approval, ticket, or exception cited inside untrusted content against the source system's record before acting on it.

**Why:** An injection can claim pre-approval in a pull-request body or issue comment, and downstream reviewers then cite the fabricated authority as if it were evidence.

**Detect:** grep review automation for approval read from pull_request.body, comment.body, or a file in the diff rather than a ticketing or IdP API call

**References:** Agentic CI/CD attack study, https://arxiv.org/abs/2607.19267

# Approval Validity Horizon

**MUST** attach an expiry to every approval or guardrail verdict and re-check it immediately before the action executes.

**Why:** State changes between check and actuation, so an approval correct at decision time can authorize an action the current state forbids.

**Detect:** grep approval objects for `expires_at` / `valid_until` and confirm the executor re-reads state or refuses stale verdicts before the side effect.

**References:** Approved-too-late guardrail staleness, https://arxiv.org/abs/2608.26306, CWE-367 (TOCTOU)

# Capability Envelope Documentation

**MUST** document each model-backed feature's knowledge limits, tested validity range, and intended human oversight, and surface them where decisions are made.

**Why:** Undocumented capability boundaries invite over-trust, and over-trust is the exploit: users act on output outside the range where it was ever validated.

**Detect:** read the feature's model card or docs for stated limits, tested scope, and oversight expectations, then check whether the UI repeats them.

**References:** NIST AI 600-1 MAP 2.2, https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf

# Central Agent Policy

**SHOULD** serve AI-coding security rules from one centrally managed, versioned source instead of per-repository copies.

**Why:** Per-repo rule files drift, go stale, and can be deleted by the very agent they are meant to constrain.

**Detect:** grep for multiple committed rule files (`AGENTS.md`, `.cursor/rules`, `copilot-instructions.md`) whose contents differ, with no shared upstream reference.

**References:** Project CodeGuard, https://github.com/cosai-oasis/project-codeguard

# Codegen Corpus Vetting

**MUST** vet the code corpus used to train, fine-tune, or retrieve for code generation for security-critical API misuse before it shapes generated code.

**Why:** Public examples encode wrong call sequences, and a model built or grounded on them reproduces the corpus's misuse rate across every generated call site.

**Detect:** command `semgrep --config p/security-audit` (plus crypto rules) over the corpus or retrieval index, recording the misuse rate per critical API.

**References:** GitHub code-corpus crypto misuse, https://arxiv.org/abs/2211.13498

# Coding-Agent Sandbox & Permission-Mode Review

**MUST** review how coding agents are configured: OS-level sandbox on, writes workspace-scoped, network off by default, approval policy enforced — and flag bypass flags (`--yolo`, `dangerously-*`, `bypassPermissions`, `approval=never`).

**Why:** The agent's technical reach, not its instructions, is the real boundary; full-access modes inside a dev container let a malicious repo exfiltrate everything reachable, including the agent's own credentials.

**Detect:** grep agent configs for `--yolo`, `dangerously-bypass`, `sandbox_mode = "danger-full-access"`, `approval_policy = "never"`, `bypassPermissions`; check for OS-enforced sandbox vs advisory-only policy.

**References:** OpenAI Codex approvals/security model, Anthropic /sandbox + permissions, Cursor Run Modes ("best-effort, not a hard boundary")

# Context Windows

**SHOULD** bound and trim conversation context explicitly so sensitive earlier turns are evicted rather than silently retained or truncated unpredictably.

**Why:** Unbounded context hoards PII and secrets in every replay, and overflow truncation can drop safety instructions mid-session.

**Detect:** config keys max_tokens, context_length, truncation strategy; no retention/eviction logic in history builders.

**References:** OWASP LLM10:2025, CWE-778, NIST SP 800-53 SC-4 (Information in Shared System Resources)

# Cross-Model Review Diversity

**SHOULD** run the AI reviewer/critic on a different model family than the producer for security-sensitive changes — same-model review shares blind spots.

**Why:** Some vendors run the reviewer/critic on a different model family, on the theory it is less likely to share the same blind spots, biases, or failure modes; a same-model reviewer tends to approve its own kind's mistakes.

**Detect:** review pipeline config shows same model for author and critic; no independent-model step for security-sensitive diffs; judgment on independence of the review chain.

**References:** vendor cross-model review practice, Anthropic fresh-context adversarial subagent review

# Cross-Session Guardrail Testing

**MUST** test agent guardrails against attacks spread across multiple sessions, since per-message checks see only a harmless fragment of the payload.

**Why:** A per-session filter that judges each message in isolation never sees the aggregate, so a workflow assembled across sessions passes every check.

**Detect:** inspect the guardrail test corpus for multi-session scenarios that accumulate or launder state between conversations.

**References:** CSTM-Bench (arXiv 2604.21131), https://arxiv.org/abs/2604.21131

# Embedding inversion and sensitive data in vector stores

**SHOULD NOT** embed raw sensitive documents in vector stores without assessment; embeddings can leak near-verbatim source text under inversion attacks.

**Why:** Published inversion techniques reconstruct personal and confidential content from vectors alone, defeating assumed one-way hashing.

**Detect:** vector DB ingest of unmasked PII fields; no access control on pgvector/Qdrant/Milvus collections; embeddings exported freely.

**References:** OWASP LLM02:2025, OWASP LLM08:2025, CWE-311

# EU AI Act conformity (risk tiering, GPAI obligations, transparency and deployment deadlines)

**MUST** classify each AI system's risk tier and meet the corresponding obligations—transparency notices, conformity assessment for high-risk, GPAI documentation—before the phased enforcement deadlines.

**Why:** Systems deployed without risk classification face market withdrawal and administrative fines of up to EUR 15M or 3% of worldwide turnover (Art. 99(4)); prohibited practices carry up to EUR 35M or 7% (Art. 99(3)).

**Detect:** grep for "high-risk", "GPAI", "Annex III", "conformity", "Article 50 transparency"; AI features with no risk tier or labeling.

**References:** EU AI Act 2024/1689, Annex III, GPAI Code of Practice, EU AI Office

# Injection Eval Classification

**MUST** report security-eval results per pinned configuration and classify each defended attack as refused, ignored, or task-breaking, never as a bare failure rate.

**Why:** An agent that survives injection by ignoring its input is malfunctioning rather than defending, and a score that moves with the system prompt measures the configuration.

**Detect:** grep the eval harness and its report template for distinct outcome labels (refused, ignored, task-broken) and a pinned config identifier per run

**References:** Injection defence measurement study, https://arxiv.org/abs/2610.23254

# Security Evals & Jailbreak Red-Teaming

**MUST** run security-focused evaluation suites covering injection, data leakage, and refusal bypass before shipping or updating any model-backed feature; **SHOULD** also run recurring adversarial jailbreak testing against production prompts, logging and feeding the results back into that suite.

**Why:** Without adversarial evals, regressions in safety behavior ship silently and are discovered by attackers first; static safety guardrails decay as novel jailbreaks circulate publicly, so an untested system fails the day one lands.

**Detect:** missing red-team eval datasets, no CI job matching eval|redteam|adversarial, promptfoo/garak config absent; no garak/pyrit/jailbreakbench runs in CI, and no stored jailbreak regression corpora or refusal-bypass tests.

**References:** OWASP LLM01:2025, NIST AI RMF MEASURE, MITRE ATLAS, NIST AI 100-2e2023

# Hallucinated Packages

**SHOULD** verify that every package name in generated or AI-assisted code actually exists and matches intent before installing.

**Why:** Attackers pre-register plausible-sounding package names that AI models invent, so blindly installing them pulls malware into the project.

**Detect:** Install logs for names absent from the registry; review AI-generated import lines against PyPI/npm search; grep manifests for near-miss spellings of popular libs.

**References:** CWE-427, Snyk "slopsquatting" research, OWASP LLM03

# Independent AI Assessment

**MUST** have risk assessments and red-team exercises for an AI system performed by assessors who did not build it.

**Why:** Builders grade their own work against the threats they already thought of, so self-assessment certifies the system's blind spots.

**Detect:** compare the assessment report's authors and reviewers against commit authorship and the team roster for the model or feature.

**References:** NIST AI 600-1 MEASURE 1.3, https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf

# PII redaction and DPAs before sending data to third-party LLM APIs

**MUST** redact or tokenize PII and execute a DPA with the provider before payloads leave the trust boundary.

**Why:** Personal data reaching an external model API may be logged, retained, or trained on beyond compliance scope.

**Detect:** outbound LLM calls without redaction middleware; missing DPA or zero-retention agreement in vendor records.

**References:** GDPR Art. 28, OWASP LLM02:2025, NIST Privacy Framework

# Denial-of-wallet: unbounded LLM token spend per user/tenant

**MUST** enforce per-user and per-tenant token budgets, rate limits, and alerting on LLM API spend.

**Why:** A scripted attacker or runaway agent loop can burn thousands of dollars in tokens within hours on a metered API.

**Detect:** no rate_limit, max_tokens, or budget keys on LLM gateway routes; provider usage alerts not configured.

**References:** OWASP LLM10:2025, CWE-770, CWE-400

# LLM Findings Need Validation

**MUST** treat findings from an LLM-based detector as candidates requiring deterministic validation before they block a merge or page a responder.

**Why:** Raw LLM detection of subtle misuse reports more than half its findings incorrectly, and a gate built on unvalidated findings teaches developers to bypass it.

**Detect:** judgment — inspect the AI-review integration and confirm findings are re-verified (rule rerun, test, or executable proof) before the required check fails.

**References:** LLM crypto-misuse detection study, https://arxiv.org/abs/2407.16576

# Treat LLM output as untrusted input (sanitize before HTML/SQL/shell/URL sinks)

**MUST** sanitize or parameterize every LLM output before it reaches an HTML, SQL, shell, or URL sink.

**Why:** A coerced model emitting markup or queries delivers stored XSS and injection through a path teams assume is safe.

**Detect:** model response rendered via |safe / innerHTML or concatenated into queries or subprocess args.

**References:** OWASP LLM05:2025, CWE-79, CWE-89, CWE-78

# Third-party MCP/plugin trust and malicious tool-description injection

**MUST** vet, pin, and sandbox third-party MCP servers and plugins; treat their tool descriptions and names as untrusted input to the model.

**Why:** A malicious tool description can instruct the agent to exfiltrate data or chain other tools harmfully.

**Detect:** MCP config pulling unpinned packages; no approved-server allowlist; tool descriptions unsanitized at registration.

**References:** OWASP LLM03:2025, MITRE ATLAS, CWE-829

# Model Artifact Integrity (pickle-format models)

**MUST NOT** load pickle-format model artifacts (.pkl, .pt via torch.load default) from untrusted sources; prefer safetensors or verified signed formats.

**Why:** Pickle executes arbitrary code at load time, so a malicious checkpoint is remote code execution before inference starts.

**Detect:** grep torch.load( without weights_only=True, pickle.load on model files, .pkl/.ckpt pulled from Hub without checksum/signature.

**References:** OWASP LLM03:2025, CWE-502, CWE-94

# Model Version Pinning

**MUST** pin exact model versions or digests rather than floating aliases like gpt-4 or latest in production configs.

**Why:** Silent upstream model swaps change safety behavior and data-handling guarantees without any code review.

**Detect:** grep model: "latest", model: gpt-4 without dated suffix; missing digest/revision fields in inference config.

**References:** OWASP LLM03:2025, CWE-1104, NIST AI RMF MANAGE

# Output Filters Are Bypassable

**MUST NOT** treat output filtering or refusal lists as a security boundary; enforce the real control before the harmful action or data sink.

**Why:** Pattern-matched output controls fail against novel, less explicit inputs, so a filter designed as the last line becomes no line at all.

**Detect:** locate where the guardrail sits relative to the tool call, query, or response sink, and whether anything else blocks the harmful action.

**References:** NIST AI 600-1 §2.3, https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf

# Prompt Injection

**MUST** treat all untrusted content (user input, retrieved documents, tool output) as data, never as instructions that override system policy.

**Why:** Injected text can hijack model behavior, leaking secrets or triggering actions the operator never authorized.

**Detect:** raw user/RAG strings interpolated into f-string prompts; missing delimiters or injection test cases.

**References:** OWASP LLM01:2025, CWE-74, NIST AI 100-2

# Provenance Trust Lattice

**SHOULD** attach provenance labels to model inputs and enforce that lower-trust content cannot influence higher-trust decisions.

**Why:** Heuristic filters are bypassed routinely; a structural non-interference rule makes provenance a checkable property instead of a judgment call.

**Detect:** grep the pipeline for trust labels (`trust_level`, `source_trust`, `provenance`) and for a policy check that blocks rather than logs cross-level influence.

**References:** Cryptographic input provenance for LLM pipelines, https://arxiv.org/abs/2508.09288

# RAG / Knowledge-Base Poisoning

**SHOULD** validate, provenance-check, and isolate ingested documents so attacker-controlled content cannot enter the retrieval index.

**Why:** Poisoned knowledge bases make malicious instructions appear as trusted retrieved context on every query.

**Detect:** ingest pipelines without source allowlists or content scanning; vector index accepting unauthenticated uploads.

**References:** OWASP LLM04:2025, CWE-506, MITRE ATLAS

# Review-Bot Neutral-Status Trap

**MUST** verify that AI review gates actually fail on unresolved findings — a required status that reports neutral/success while findings remain open does not block merges.

**Why:** Cursor documents this explicitly (findings default to neutral; you must enable fail-on-unresolved); GitHub Copilot defaults to "Comment" not "Approve" — teams often believe they have an AI gate they don't have.

**Detect:** branch protection requiring a bot check whose conclusion set lacks failure-on-findings; severity thresholds set above real risk; review config where unresolved ≠ failed.

**References:** Cursor Bugbot status semantics, GitHub Copilot review default-Comment behavior, Gemini severity-threshold filtering

# Security Guidance in Generation

**MUST** seed code-generation context — templates, rules files, and scaffolds — with the security standard the output must satisfy, not only scan the output afterwards.

**Why:** Generators without the requirement in context reproduce the same insecure defaults every time, and post-hoc scanning then arguments with the tool instead of the template.

**Detect:** grep the scaffold and agent-rules files for references to the project's security baseline, and check whether generated IaC is scanned against the same baseline.

**References:** Ansible security smells in LLM-generated IaC (arXiv 2608.24962), https://arxiv.org/abs/2608.24962

# Shadow AI: unsanctioned AI SaaS and embedded AI features in the stack

**MUST** inventory and govern AI features in third-party software and employee-adopted AI SaaS, since unsanctioned tools move data outside policy.

**Why:** Copilots and AI-enabled vendors quietly move code, tickets, and documents to unvetted providers.

**Detect:** network egress to openai.com/anthropic.com from unmanaged endpoints; no AI usage policy or CASB/SaaS inventory entries.

**References:** OWASP LLM03:2025, NIST AI RMF GOVERN 6, CWE-912

# Synthetic Data Memorisation Checks

**MUST NOT** treat synthetic records as non-personal until memorisation and nearest-neighbour tests show they cannot reproduce real individuals from the training set.

**Why:** Generative models emit training rows verbatim or near-verbatim for rare records, so a synthetic release can leak the very individuals it was generated to protect.

**Detect:** command: run a distance-to-closest-training-record test and a membership-inference check (`sdmetrics`, `synthcity`, or an explicit overlap count) before release; flag exports shipped with no test result recorded.

**References:** NIST SP 800-188 De-Identifying Government Datasets, https://csrc.nist.gov/pubs/sp/800/188/final, Shokri et al., Membership Inference Attacks Against Machine Learning Models, https://arxiv.org/abs/1610.05820, Carlini et al., Extracting Training Data from Large Language Models, https://arxiv.org/abs/2012.07805

# System prompt extraction and sensitive config embedded in prompts

**SHOULD NOT** embed secrets, credentials, or proprietary logic in system prompts, since extraction via jailbreak or logging is always possible.

**Why:** Prompt contents can be coaxed out verbatim by an attacker or leaked through provider logs.

**Detect:** API keys, connection strings, or business rules literal in system prompt templates; prompt text in logs/tracing exporters.

**References:** OWASP LLM07:2025, CWE-522, CWE-200

# Tool / Function-Call Argument Injection

**MUST** validate and schema-check every model-generated tool argument server-side before execution; never trust the model to sanitize parameters.

**Why:** A manipulated model can emit crafted arguments that turn a benign tool into SQL, shell, or path-traversal execution.

**Detect:** tool dispatch calling exec/query with model output unchecked; missing JSON-schema validation on function-call payloads.

**References:** OWASP LLM06:2025, CWE-74, OWASP Top 10 A03

# Tooling Security Gap Measurement

**MUST** re-measure each adopted code-generation tool's security pass rate on your own tasks, rather than inferring safety from functional gains or release notes.

**Why:** Functional improvement and security improvement diverge per model family, so yesterday's measurement is the only evidence you have about today's tool.

**Detect:** run the same security test suite per tool version and diff the pass rate across releases.

**References:** Longitudinal functionality-security gap study (arXiv 2610.08240), https://arxiv.org/abs/2610.08240

# Training Data Reconstruction

**SHOULD** keep records under restricted access out of training sets for any model that callers outside that restriction can query.

**Why:** Model access alone supports reconstruction of training records, so serving a model trained on sensitive data hands over a sampling oracle for it.

**Detect:** Inspect each deployed model's training-data manifest against its exposure tier, and flag models trained on identifiable records that untrusted callers can query.

**References:** SoK on data reconstruction (arXiv 2506.07888), https://arxiv.org/abs/2506.07888

# Training Data Trust Boundary

**MUST** treat corpora that train, tune, or configure a decision component as untrusted input with their own provenance, validation, and write access control.

**Why:** Whoever can write the corpus shapes the component's behavior without touching code, and the effect survives review because the model carries the payload.

**Detect:** grep the training and tuning pipeline for dataset reads without a pinned digest or source provenance (`read_csv("http`, `load_dataset(`, `s3://` paths without version IDs).

**References:** OWASP ML Top 10: ML02 Data Poisoning, https://github.com/OWASP/www-project-machine-learning-security-top-10/tree/master/docs

# Unattended-Agent Automation Governance

**MUST** govern scheduled/event-triggered agents (cron, webhook) with: attribution to the automation creator, minimal tool surface per automation, trigger trust controls (signed webhooks, ignore non-trusted events), and preserved downstream human approval.

**Why:** Unattended agents run with no human per task, so every capability they hold is reachable from whatever triggers them; an automation must not inherit outbound authority from an inbound webhook or schedule it does not control.

**Detect:** automations with broad tool grants or opt-in to untrusted-user events; webhook endpoints accepting unsigned payloads; no owner attribution per automation; agent can merge/approve its own output.

**References:** GitHub Copilot coding agent risks and mitigations, OWASP LLM06:2025 Excessive Agency, NIST SP 800-53 AC-6

