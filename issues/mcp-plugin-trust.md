# Third-party MCP/plugin trust and malicious tool-description injection

**MUST** vet, pin, and sandbox third-party MCP servers and plugins; treat their tool descriptions and names as untrusted input to the model.

**Why:** A malicious tool description can instruct the agent to exfiltrate data or chain other tools harmfully.

**Detect:** MCP config pulling unpinned packages; no approved-server allowlist; tool descriptions unsanitized at registration.

**References:** OWASP LLM06:2025, MITRE ATLAS T0059, CWE-829

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [supply-chain](../categories/supply-chain.md) · [infrastructure](../domains/infrastructure.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
