---
categories: [ai-llm]
domains: [backend]
---

# Agent Output Trust Per Hop

**MUST** re-validate agent output at every downstream consumer instead of trusting the upstream agent's check.

**Why:** An agent that reads attacker content, acts on it, and writes output other agents consume spreads harm with no vulnerable code anywhere.

**Detect:** grep inter-agent handoffs for output forwarded to another agent or a sink without re-validation at the consumer (`messages.append(tool_result)`, `publish(agent_output)`).

**References:** Agentic runtime threat analysis, https://arxiv.org/abs/2602.19555, OWASP Top 10 for LLM Applications: LLM01 Prompt Injection
