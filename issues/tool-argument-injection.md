# Tool / Function-Call Argument Injection

**MUST** validate and schema-check every model-generated tool argument server-side before execution; never trust the model to sanitize parameters.

**Why:** A manipulated model can emit crafted arguments that turn a benign tool into SQL, shell, or path-traversal execution.

**Detect:** tool dispatch calling exec/query with model output unchecked; missing JSON-schema validation on function-call payloads.

**References:** OWASP LLM06:2025, CWE-74, OWASP Top 10 A03
