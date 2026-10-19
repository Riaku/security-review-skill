---
categories: [ai-llm]
domains: [backend, governance]
---

# Security Guidance in Generation

**MUST** seed code-generation context — templates, rules files, and scaffolds — with the security standard the output must satisfy, not only scan the output afterwards.

**Why:** Generators without the requirement in context reproduce the same insecure defaults every time, and post-hoc scanning then arguments with the tool instead of the template.

**Detect:** grep the scaffold and agent-rules files for references to the project's security baseline, and check whether generated IaC is scanned against the same baseline.

**References:** Ansible security smells in LLM-generated IaC (arXiv 2608.24962), https://arxiv.org/abs/2608.24962
