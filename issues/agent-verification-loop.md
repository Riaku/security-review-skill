---
categories: [ai-llm, testing-strategy]
domains: [backend, governance]
---

# Agent Verification Loop (Executable Done-When)

**MUST** give every AI-agent coding task a runnable pass/fail verification criterion (tests, build, script-vs-fixture) wired into the task itself — otherwise the human becomes the verification loop.

**Why:** Industry practice converges on this: an agent without an executable check ships plausible-looking code indefinitely.

**Detect:** agent task/plan artifacts merged with no named test/build/acceptance command; "implement X" tickets with no check; agent PRs whose CI runs no tests on the change.

**References:** Anthropic Claude Code best practices, vendor coding-agent verification guidance

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [testing-strategy](../categories/testing-strategy.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
