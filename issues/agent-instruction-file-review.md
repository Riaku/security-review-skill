---
categories: [ai-llm, documentation-quality]
domains: [backend, governance]
---

# Agent Instruction-File Review Surface

**MUST** code-review and CODEOWN every agent instruction file (CLAUDE.md, AGENTS.md, .cursor/rules/*.mdc, copilot-instructions.md, .gemini/styleguide.md, QWEN.md) and keep it concise — bloated instruction files are silently ignored, making unenforced policy invisible.

**Why:** These files steer all generated code in the repo; a one-line frontmatter change (e.g. `alwaysApply: true`) is a prompt-injection-from-inside-the-repo vector, and rot makes claims diverge from CI reality.

**Detect:** PRs touching instruction files without review; instruction files >500 lines or full of task-specific one-offs; divergence between instruction-file claims and actual CI config.

**References:** GitHub custom-instructions guidance (≤2 pages), Cursor rules docs (<500 lines, check into git), Anthropic "bloated CLAUDE.md gets ignored"

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [documentation-quality](../categories/documentation-quality.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
