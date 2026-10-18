---
categories: [ai-llm, observability]
domains: [governance, reliability]
---

# Agent Session-Log Traceability

**MUST** link every agent-authored commit to its session transcript and the human who initiated it (co-author trailer, session-log URL in commit message, verified signature).

**Why:** Without the commit→session→human chain, agent work is unauditable — you cannot answer who asked for this, what context the agent saw, or who owns the outcome.

**Detect:** bot commits lacking co-author/session links; agent tooling with transcripts disabled or rotated to zero retention; no mapping from merged PR to agent run.

**References:** GitHub Copilot agent auditability (signed commits, session-log link), OpenAI Codex transcripts, DeepSeek harness session-log model
