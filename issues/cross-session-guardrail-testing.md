---
categories: [ai-llm]
domains: [backend]
---

# Cross-Session Guardrail Testing

**MUST** test agent guardrails against attacks spread across multiple sessions, since per-message checks see only a harmless fragment of the payload.

**Why:** A per-session filter that judges each message in isolation never sees the aggregate, so a workflow assembled across sessions passes every check.

**Detect:** inspect the guardrail test corpus for multi-session scenarios that accumulate or launder state between conversations.

**References:** CSTM-Bench (arXiv 2604.21131), https://arxiv.org/abs/2604.21131
