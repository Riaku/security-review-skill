# Agent Context-Exclusion Files

**SHOULD** maintain agent exclusion files (.cursorignore, .aiexclude, equivalent) covering secrets, credentials, and sensitive modules so they never enter agent context or indexes.

**Why:** Anything the agent can read, it can echo into code, logs, or a PR; exclusion files are the gitignore of the AI-context layer and their absence means sensitive paths are agent-reachable by default.

**Detect:** repo root lacks .cursorignore/.aiexclude while secrets/sensitive dirs are agent-reachable; index covers branches/patterns beyond the stable set; exclusion list missing recently-added sensitive paths.

**References:** Cursor .cursorignore, Gemini .aiexclude, GitHub content-exclusion controls

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
