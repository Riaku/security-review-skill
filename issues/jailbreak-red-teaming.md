# Jailbreak Red-Teaming

**SHOULD** run recurring adversarial jailbreak testing against production prompts, logging and feeding results into the eval suite.

**Why:** Static safety guardrails decay as novel jailbreaks circulate publicly; untested systems fail the day one lands.

**Detect:** no garak/pyrit/jailbreakbench runs in CI; absence of stored jailbreak regression corpora or refusal-bypass tests.

**References:** OWASP LLM01:2025, MITRE ATLAS, NIST AI 100-3

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
