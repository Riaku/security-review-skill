---
categories: [ai-llm]
domains: [governance]
---

# Cross-Model Review Diversity

**SHOULD** run the AI reviewer/critic on a different model family than the producer for security-sensitive changes — same-model review shares blind spots.

**Why:** Some vendors run the reviewer/critic on a different model family, on the theory it is less likely to share the same blind spots, biases, or failure modes; a same-model reviewer tends to approve its own kind's mistakes.

**Detect:** review pipeline config shows same model for author and critic; no independent-model step for security-sensitive diffs; judgment on independence of the review chain.

**References:** vendor cross-model review practice, Anthropic fresh-context adversarial subagent review

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
