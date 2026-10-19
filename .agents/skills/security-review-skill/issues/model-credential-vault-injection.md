---
categories: [secrets-crypto]
domains: [backend]
---

# Credentials Out Of Model Context

**MUST** keep credentials out of model context entirely: the model selects a connector identifier and a trusted boundary injects the secret.

**Why:** A secret pasted into a prompt enters a data pipeline that persists it in history, logs, memory, and generated code, and prompt injection turns that disclosure into action.

**Detect:** grep prompts, system messages, and tool schemas for interpolated `api_key`, `token`, `Bearer `, `password`; confirm tool handlers resolve credentials from a vault server-side.

**References:** Vault-mediated credential execution for agents, https://arxiv.org/abs/2609.33371
