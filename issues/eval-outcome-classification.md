---
categories: [ai-llm]
domains: [backend]
---

# Injection Eval Classification

**MUST** report security-eval results per pinned configuration and classify each defended attack as refused, ignored, or task-breaking, never as a bare failure rate.

**Why:** An agent that survives injection by ignoring its input is malfunctioning rather than defending, and a score that moves with the system prompt measures the configuration.

**Detect:** grep the eval harness and its report template for distinct outcome labels (refused, ignored, task-broken) and a pinned config identifier per run

**References:** Injection defence measurement study, https://arxiv.org/abs/2610.23254
