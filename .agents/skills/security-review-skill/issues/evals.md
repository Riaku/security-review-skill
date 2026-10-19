---
categories: [ai-llm]
domains: [governance]
---

# Security Evals & Jailbreak Red-Teaming

**MUST** run security-focused evaluation suites covering injection, data leakage, and refusal bypass before shipping or updating any model-backed feature; **SHOULD** also run recurring adversarial jailbreak testing against production prompts, logging and feeding the results back into that suite.

**Why:** Without adversarial evals, regressions in safety behavior ship silently and are discovered by attackers first; static safety guardrails decay as novel jailbreaks circulate publicly, so an untested system fails the day one lands.

**Detect:** missing red-team eval datasets, no CI job matching eval|redteam|adversarial, promptfoo/garak config absent; no garak/pyrit/jailbreakbench runs in CI, and no stored jailbreak regression corpora or refusal-bypass tests.

**References:** OWASP LLM01:2025, NIST AI RMF MEASURE, MITRE ATLAS, NIST AI 100-2e2023
