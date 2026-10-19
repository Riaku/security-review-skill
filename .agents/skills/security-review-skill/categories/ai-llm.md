# ai-llm

LLM feature security and quality.

## What this category covers

This category covers the security, privacy, and governance problems that appear once an LLM feature, autonomous coding agent, or retrieval pipeline enters a stack. Items span prompt and retrieval trust boundaries, untrusted model output reaching downstream sinks, coding-agent and unattended-agent authority, the model and agent supply chain, data handling for embeddings and prompts, and the security evaluations and review gates that catch regressions. A reviewer should expect to see prompt construction, tool and function-call dispatch, RAG ingest pipelines, agent and sandbox configuration, and CI review and verification wiring. Findings here sit on the model-facing trust boundary rather than in general application security.

- Prompt and retrieval trust boundaries — prompt injection and knowledge-base poisoning, with retrieved or tool-supplied content treated as data.
- Untrusted model output — sanitizing LLM output and function-call arguments before HTML, SQL, shell, or URL sinks.
- Coding-agent and autonomous-agent governance — sandbox and permission modes, human approval for destructive tools, egress allowlists, context-exclusion files, session hygiene and traceability, and unattended-automation controls.
- Model and agent supply chain — model version pinning, pickle-format artifact integrity, hallucinated package names, and third-party MCP/plugin trust.
- Data handling for model features — embedding inversion, secrets in system prompts, context-window bounds, and redaction before third-party LLM APIs.
- Evaluation and review discipline — security evaluation suites, jailbreak red-teaming, cross-model review diversity, AI-generated-code review gates, and review bots that fail on unresolved findings.

## What it does not cover

- [security-practices](../categories/security-practices.md) — repository-wide secure design, threat modeling, and defense-in-depth belong there; prompt and tool trust boundaries and agent authority are scoped here.
- [supply-chain](../categories/supply-chain.md) — dependency lockfiles, image scanning, and build provenance belong there; model artifacts, hallucinated packages, and MCP/plugin trust are scoped here.
- [cicd-pipeline-security](../categories/cicd-pipeline-security.md) — runner isolation, branch protection, and CI policy gates belong there; how coding agents are sandboxed and passed through a merge gate is scoped here.
- [compliance-privacy](../categories/compliance-privacy.md) — lawful basis, retention, and data-subject rights belong there; embedding inversion and system-prompt secret exposure are scoped here.

## What a finding here looks like

- Untrusted user or retrieved text concatenated into a prompt with no delimiter, so injected instructions override system policy.
- Model-generated output or tool arguments passed to an HTML, SQL, shell, or URL sink without sanitization or schema validation.
- A coding agent running with a bypass permission mode (`--yolo`, `dangerously-*`, `approval=never`) or a wildcard egress rule.
- A model checkpoint loaded via `torch.load()` or `pickle.load()` from an unverified source.
- No per-user or per-tenant token budget or spend alert on an LLM gateway, so a runaway loop burns metered spend.
