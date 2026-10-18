# Agent Egress Allowlist & Proxy Control

**MUST** route coding-agent egress (model calls, MCP-over-HTTP, web fetch) through an explicit proxy/allowlist — and repo-supplied env must never control where agent traffic goes.

**Why:** DeepSeek's harness refuses to start rather than let a cloned repo set proxy vars; OpenAI uses allowlist-first domain rules where deny always wins — repo-controlled egress is an exfiltration path.

**Detect:** agent runs without managed proxy; wildcard `*` in agent network allow rules; MCP servers reaching arbitrary hosts; repo .env containing proxy settings honored by agent tooling.

**References:** DeepSeek harness proxy-refusal pattern, OpenAI Codex domain rules, GitHub agent internet firewall, Cursor fixed-destination egress

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [cloud-network](../categories/cloud-network.md) · [infrastructure](../domains/infrastructure.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
