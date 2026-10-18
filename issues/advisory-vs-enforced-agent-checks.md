---
categories: [ai-llm, cicd-pipeline-security]
domains: [governance, infrastructure]
---

# Advisory-vs-Enforced Agent Checks

**MUST** implement every must-happen-every-time agent rule as a deterministic hook (pre-commit, post-edit lint, blocked paths, secret-scan-before-write) — not as instruction text the model may skip.

**Why:** The whole ecosystem converged on this distinction: "hooks are deterministic; CLAUDE.md is advisory" (Anthropic). Policy claimed in instruction files with no hook behind it is unenforced policy wearing a costume.

**Detect:** security rules present only in instruction-file text with no corresponding hook/CI enforcement; hook config (e.g. .claude/settings.json) empty while policy claims enforcement.

**References:** Anthropic hooks-vs-instructions guidance, Copilot CLI hooks, Cursor hooks, Codex hooks

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [governance](../domains/governance.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
