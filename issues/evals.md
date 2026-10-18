# Evals

**MUST** run security-focused evaluation suites covering injection, data leakage, and refusal bypass before shipping or updating any model-backed feature.

**Why:** Without adversarial evals, regressions in safety behavior ship silently and are discovered by attackers first.

**Detect:** missing red-team eval datasets, no CI job matching eval|redteam|adversarial, promptfoo/garak config absent.

**References:** OWASP LLM01:2025, NIST AI RMF MEASURE, MITRE ATLAS
