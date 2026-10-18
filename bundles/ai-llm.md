# ai-llm — full checklist (19 items)

LLM feature security and quality.

> Generated artifact. Canonical source: `issues/<slug>.md`.

# Prompt Injection

**MUST** treat all untrusted content (user input, retrieved documents, tool output) as data, never as instructions that override system policy.

**Why:** Injected text can hijack model behavior, leaking secrets or triggering actions the operator never authorized.

**Detect:** raw user/RAG strings interpolated into f-string prompts; missing delimiters or injection test cases.

**References:** OWASP LLM01:2025, CWE-74, NIST AI 100-2

# Hallucinated Packages

**SHOULD** verify that every package name in generated or AI-assisted code actually exists and matches intent before installing.

**Why:** Attackers pre-register plausible-sounding package names that AI models invent, so blindly installing them pulls malware into the project.

**Detect:** Install logs for names absent from the registry; review AI-generated import lines against PyPI/npm search; grep manifests for near-miss spellings of popular libs.

**References:** CWE-427, Snyk "slopsquatting" research, OWASP LLM03

# Context Windows

**SHOULD** bound and trim conversation context explicitly so sensitive earlier turns are evicted rather than silently retained or truncated unpredictably.

**Why:** Unbounded context hoards PII and secrets in every replay, and overflow truncation can drop safety instructions mid-session.

**Detect:** config keys max_tokens, context_length, truncation strategy; no retention/eviction logic in history builders.

**References:** OWASP LLM10:2025, CWE-778, NIST SP 800-53 AT-4

# Evals

**MUST** run security-focused evaluation suites covering injection, data leakage, and refusal bypass before shipping or updating any model-backed feature.

**Why:** Without adversarial evals, regressions in safety behavior ship silently and are discovered by attackers first.

**Detect:** missing red-team eval datasets, no CI job matching eval|redteam|adversarial, promptfoo/garak config absent.

**References:** OWASP LLM01:2025, NIST AI RMF MEASURE, MITRE ATLAS

# Model Version Pinning

**MUST** pin exact model versions or digests rather than floating aliases like gpt-4 or latest in production configs.

**Why:** Silent upstream model swaps change safety behavior and data-handling guarantees without any code review.

**Detect:** grep model: "latest", model: gpt-4 without dated suffix; missing digest/revision fields in inference config.

**References:** OWASP LLM05:2025, CWE-1104, NIST AI RMF MANAGE

# RAG / Knowledge-Base Poisoning

**SHOULD** validate, provenance-check, and isolate ingested documents so attacker-controlled content cannot enter the retrieval index.

**Why:** Poisoned knowledge bases make malicious instructions appear as trusted retrieved context on every query.

**Detect:** ingest pipelines without source allowlists or content scanning; vector index accepting unauthenticated uploads.

**References:** OWASP LLM08:2025, CWE-506, MITRE ATLAS T0043

# Tool / Function-Call Argument Injection

**MUST** validate and schema-check every model-generated tool argument server-side before execution; never trust the model to sanitize parameters.

**Why:** A manipulated model can emit crafted arguments that turn a benign tool into SQL, shell, or path-traversal execution.

**Detect:** tool dispatch calling exec/query with model output unchecked; missing JSON-schema validation on function-call payloads.

**References:** OWASP LLM06:2025, CWE-74, OWASP Top 10 A03

# Jailbreak Red-Teaming

**SHOULD** run recurring adversarial jailbreak testing against production prompts, logging and feeding results into the eval suite.

**Why:** Static safety guardrails decay as novel jailbreaks circulate publicly; untested systems fail the day one lands.

**Detect:** no garak/pyrit/jailbreakbench runs in CI; absence of stored jailbreak regression corpora or refusal-bypass tests.

**References:** OWASP LLM01:2025, MITRE ATLAS, NIST AI 100-3

# Model Artifact Integrity (pickle-format models)

**MUST NOT** load pickle-format model artifacts (.pkl, .pt via torch.load default) from untrusted sources; prefer safetensors or verified signed formats.

**Why:** Pickle executes arbitrary code at load time, so a malicious checkpoint is remote code execution before inference starts.

**Detect:** grep torch.load( without weights_only=True, pickle.load on model files, .pkl/.ckpt pulled from Hub without checksum/signature.

**References:** OWASP LLM08:2025, CWE-502, CWE-94

# EU AI Act conformity (risk tiering, GPAI obligations, transparency and deployment deadlines)

**MUST** classify each AI system's risk tier and meet the corresponding obligations—transparency notices, conformity assessment for high-risk, GPAI documentation—before the phased enforcement deadlines.

**Why:** Systems deployed without risk classification face market withdrawal and fines up to 7% of turnover once enforcement phases begin.

**Detect:** grep for "high-risk", "GPAI", "Annex III", "conformity", "Article 50 transparency"; AI features with no risk tier or labeling.

**References:** EU AI Act 2024/1689, Annex III, GPAI Code of Practice, EU AI Office

# Treat LLM output as untrusted input (sanitize before HTML/SQL/shell/URL sinks)

**MUST** sanitize or parameterize every LLM output before it reaches an HTML, SQL, shell, or URL sink.

**Why:** A coerced model emitting markup or queries delivers stored XSS and injection through a path teams assume is safe.

**Detect:** model response rendered via |safe / innerHTML or concatenated into queries or subprocess args.

**References:** OWASP LLM01:2025, CWE-79, CWE-89, CWE-78

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

# Human-in-the-loop approval for destructive agent tool calls

**MUST** require explicit human confirmation before an autonomous agent executes destructive actions (deletes, payments, sends, deploys).

**Why:** A hijacked or hallucinating agent with unguarded write access can cause irreversible damage in a single automated chain.

**Detect:** agent tool registry lacks confirm/approval flags on destructive verbs; auto-execute=true on write-capable tools.

**References:** OWASP LLM06:2025, NIST AI RMF GOVERN 3, CWE-807

# System prompt extraction and sensitive config embedded in prompts

**SHOULD NOT** embed secrets, credentials, or proprietary logic in system prompts, since extraction via jailbreak or logging is always possible.

**Why:** Prompt contents can be coaxed out verbatim by an attacker or leaked through provider logs.

**Detect:** API keys, connection strings, or business rules literal in system prompt templates; prompt text in logs/tracing exporters.

**References:** OWASP LLM07:2025, CWE-522, CWE-200

# Third-party MCP/plugin trust and malicious tool-description injection

**MUST** vet, pin, and sandbox third-party MCP servers and plugins; treat their tool descriptions and names as untrusted input to the model.

**Why:** A malicious tool description can instruct the agent to exfiltrate data or chain other tools harmfully.

**Detect:** MCP config pulling unpinned packages; no approved-server allowlist; tool descriptions unsanitized at registration.

**References:** OWASP LLM06:2025, MITRE ATLAS T0059, CWE-829

# AI-generated code review gate before merge

**SHOULD** require human security review of AI-generated code before merge; Copilot-style output is not self-certifying.

**Why:** Models reproduce vulnerable patterns and plausible-but-broken crypto from training data at high volume and speed.

**Detect:** PRs with AI-assist labels merged without security-review approval; CI lacks a gate matching ai-generated/copilot review policy.

**References:** OWASP LLM03:2025, NIST SSDF PW.4, CWE-1157

# Embedding inversion and sensitive data in vector stores

**SHOULD NOT** embed raw sensitive documents in vector stores without assessment; embeddings can leak near-verbatim source text under inversion attacks.

**Why:** Published inversion techniques reconstruct personal and confidential content from vectors alone, defeating assumed one-way hashing.

**Detect:** vector DB ingest of unmasked PII fields; no access control on pgvector/Qdrant/Milvus collections; embeddings exported freely.

**References:** OWASP LLM02:2025, OWASP LLM08:2025, CWE-311

# Shadow AI: unsanctioned AI SaaS and embedded AI features in the stack

**MUST** inventory and govern AI features in third-party software and employee-adopted AI SaaS, since unsanctioned tools move data outside policy.

**Why:** Copilots and AI-enabled vendors quietly move code, tickets, and documents to unvetted providers.

**Detect:** network egress to openai.com/anthropic.com from unmanaged endpoints; no AI usage policy or CASB/SaaS inventory entries.

**References:** OWASP LLM09:2025, NIST AI RMF GOVERN 6, CWE-912

