---
categories: [ai-llm]
domains: [backend]
---

# Verify The Whole Plan

**MUST** validate a multi-step agent's whole plan — tool sequence, control flow, data dependencies — against policy before the first action runs.

**Why:** Each step can be individually permitted while the composed execution violates required ordering, approval gates, or data-flow rules.

**Detect:** grep the agent runtime for a pre-execution plan check (state machine or policy evaluation over the tool-call sequence) and reject ungated destructive or spend steps.

**References:** Plan-level policy verification for agents, https://arxiv.org/abs/2609.18674
