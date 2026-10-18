# AI-generated code review gate before merge

**SHOULD** require human security review of AI-generated code before merge; Copilot-style output is not self-certifying.

**Why:** Models reproduce vulnerable patterns and plausible-but-broken crypto from training data at high volume and speed.

**Detect:** PRs with AI-assist labels merged without security-review approval; CI lacks a gate matching ai-generated/copilot review policy.

**References:** OWASP LLM03:2025, NIST SSDF PW.4, CWE-1157

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [infrastructure](../domains/infrastructure.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
