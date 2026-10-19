---
categories: [ai-llm]
domains: [backend]
---

# Setup Docs As Install Surface

**MUST** review setup instructions, requirement files, and build targets that automation executes with the same rigor as dependency manifests.

**Why:** An attacker who edits only a README or Makefile can redirect an agent to an untrusted registry or a known-vulnerable version, and the change passes review because it looks like documentation.

**Detect:** grep docs and Makefiles for install commands: `pip install`, `npm i`, `--index-url`, `-r requirements`, `curl | sh`, `go get` — check each resolves to a canonical registry and pinned version.

**References:** Agent install-time attack surface, https://arxiv.org/abs/2607.15143, OWASP Top 10 for LLM Applications: LLM03 Supply Chain
