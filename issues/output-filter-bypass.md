---
categories: [ai-llm]
domains: [backend]
---

# Output Filters Are Bypassable

**MUST NOT** treat output filtering or refusal lists as a security boundary; enforce the real control before the harmful action or data sink.

**Why:** Pattern-matched output controls fail against novel, less explicit inputs, so a filter designed as the last line becomes no line at all.

**Detect:** locate where the guardrail sits relative to the tool call, query, or response sink, and whether anything else blocks the harmful action.

**References:** OWASP LLM05:2025 Improper Output Handling, NIST AI 600-1 §2.3, https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
