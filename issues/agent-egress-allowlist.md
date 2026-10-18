---
categories: [ai-llm, cloud-network]
domains: [governance, infrastructure]
---

# Agent Egress Allowlist & Proxy Control

**MUST** route coding-agent egress (model calls, MCP-over-HTTP, web fetch) through an explicit proxy/allowlist — and repo-supplied env must never control where agent traffic goes.

**Why:** Some agent harnesses refuse to start rather than honor repo-controlled proxy settings, and vendors ship allowlist-first egress where deny wins — repo-controlled egress is an exfiltration path.

**Detect:** agent runs without managed proxy; wildcard `*` in agent network allow rules; MCP servers reaching arbitrary hosts; repo .env containing proxy settings honored by agent tooling.

**References:** OpenAI Codex domain rules, Anthropic agent network controls, vendor agent egress allowlists

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [cloud-network](../categories/cloud-network.md) · [governance](../domains/governance.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
