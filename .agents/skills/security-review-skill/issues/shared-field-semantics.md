---
categories: [api-design]
domains: [backend]
---

# Shared Field Semantics

**MUST** document, for every field crossing a component boundary, who may write it and what each consumer interprets it to mean.

**Why:** Differential parsing turns a shared struct into a bypass: the front end validates one interpretation while the back end acts on another. Ambiguous fields are where those disagreements live.

**Detect:** Inspect the shared schema or IDL for per-field comments naming the writer and each reader's interpretation.

**References:** Orange Tsai: confusion attacks, https://blog.orange.tw/posts/2024-08-confusion-attacks-en/
