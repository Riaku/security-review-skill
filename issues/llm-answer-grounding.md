---
categories: [ai-llm]
domains: [governance]
---

# Answer Grounding

**MUST** ground consequential answers in retrievable, attributable sources, and treat an empty retrieval result as a reason to withhold the answer rather than to generate one.

**Why:** Fluent output is not evidence: a model states a citation, a dosage, a migration step, or a legal obligation that does not exist, in the same register it uses for the ones that do. Every unsupported answer that a user acts on is the failure mode, and a refusal-focused eval suite never surfaces it.

**Detect:** answers with no citation to a retrieved chunk where retrieval was available; a prompt that tells the model to answer from its own knowledge when no documents are found; no withholding path on empty retrieval (no "insufficient sources" state, no escalation to a human); evals that score jailbreak success but never the unsupported-claim rate.

**References:** OWASP LLM09:2025, NIST AI 600-1
