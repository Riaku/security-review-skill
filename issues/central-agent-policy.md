---
categories: [ai-llm]
domains: [backend, governance]
---

# Central Agent Policy

**SHOULD** serve AI-coding security rules from one centrally managed, versioned source instead of per-repository copies.

**Why:** Per-repo rule files drift, go stale, and can be deleted by the very agent they are meant to constrain.

**Detect:** grep for multiple committed rule files (`AGENTS.md`, `.cursor/rules`, `copilot-instructions.md`) whose contents differ, with no shared upstream reference.

**References:** Project CodeGuard, https://github.com/cosai-oasis/project-codeguard
