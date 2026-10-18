# Agent Verification Loop (Executable Done-When)

**MUST** give every AI-agent coding task a runnable pass/fail verification criterion (tests, build, script-vs-fixture) wired into the task itself — otherwise the human becomes the verification loop.

**Why:** All major vendors converge on this: an agent without an executable check ships plausible-looking code indefinitely ("if you can't verify it, don't ship it" — Anthropic; "Done when" — GLM; easy-to-verify RL — Qwen).

**Detect:** agent task/plan artifacts merged with no named test/build/acceptance command; "implement X" tickets with no check; agent PRs whose CI runs no tests on the change.

**References:** Anthropic Claude Code best practices, GLM dev-pack best practice, Qwen3-Coder verification philosophy

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [testing-strategy](../categories/testing-strategy.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
