---
categories: [ai-llm, supply-chain]
domains: [governance, infrastructure]
---

# Model Artifact Integrity (pickle-format models)

**MUST NOT** load pickle-format model artifacts (.pkl, .pt via torch.load default) from untrusted sources; prefer safetensors or verified signed formats.

**Why:** Pickle executes arbitrary code at load time, so a malicious checkpoint is remote code execution before inference starts.

**Detect:** grep torch.load( without weights_only=True, pickle.load on model files, .pkl/.ckpt pulled from Hub without checksum/signature.

**References:** OWASP LLM03:2025, CWE-502, CWE-94

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [supply-chain](../categories/supply-chain.md) · [governance](../domains/governance.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
