---
categories: [ai-llm]
domains: [governance]
---

# Cross-Model Review Diversity

**SHOULD** run the AI reviewer/critic on a different model family than the producer for security-sensitive changes — same-model review shares blind spots.

**Why:** GitHub's rubber-duck critic explicitly runs on a different model "less likely to share the same blind spots, biases, or failure modes"; a same-model reviewer tends to approve its own kind's mistakes.

**Detect:** review pipeline config shows same model for author and critic; no independent-model step for security-sensitive diffs; judgment on independence of the review chain.

**References:** GitHub Copilot rubber-duck cross-model critic, Anthropic fresh-context adversarial subagent review

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
