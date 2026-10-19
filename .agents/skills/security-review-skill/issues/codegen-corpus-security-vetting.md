---
categories: [ai-llm]
domains: [backend]
---

# Codegen Corpus Vetting

**MUST** vet the code corpus used to train, fine-tune, or retrieve for code generation for security-critical API misuse before it shapes generated code.

**Why:** Public examples encode wrong call sequences, and a model built or grounded on them reproduces the corpus's misuse rate across every generated call site.

**Detect:** command `semgrep --config p/security-audit` (plus crypto rules) over the corpus or retrieval index, recording the misuse rate per critical API.

**References:** GitHub code-corpus crypto misuse, https://arxiv.org/abs/2211.13498
