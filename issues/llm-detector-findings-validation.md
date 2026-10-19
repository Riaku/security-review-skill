---
categories: [ai-llm]
domains: [backend]
---

# LLM Findings Need Validation

**MUST** treat findings from an LLM-based detector as candidates requiring deterministic validation before they block a merge or page a responder.

**Why:** Raw LLM detection of subtle misuse reports more than half its findings incorrectly, and a gate built on unvalidated findings teaches developers to bypass it.

**Detect:** judgment — inspect the AI-review integration and confirm findings are re-verified (rule rerun, test, or executable proof) before the required check fails.

**References:** LLM crypto-misuse detection study, https://arxiv.org/abs/2407.16576
