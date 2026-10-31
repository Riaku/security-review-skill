---
categories: [correctness-pitfalls, web-api-security]
domains: [backend, frontend]
---

# Taint Survives Indirection

**MUST** follow request-controlled values through intermediate variables, wrapper accessors, helper returns, and hand-parsed substrings before calling a sink safe; a value that started at a request boundary is still tainted after it is renamed, re-wrapped, or sliced.

**Why:** A reviewer who matches the accessor to the sink in one function misses the value that arrives through a wrapper class, a helper's return, or `getQueryString().substring(...)` — the taint is discontinuous on the page and continuous at runtime, so the injection survives review.

**Detect:** Sinks fed by a variable assigned from a helper or wrapper call (`SeparateClassRequest.getTheParameter()`, map or session lookups) instead of a direct accessor; query strings and raw headers parsed with `indexOf`/`substring`/`split` into a sink argument; a sink declared safe because the variable is not named `param`.

**References:** CWE-20, OWASP Code Review Guide (https://owasp.org/www-project-code-review-guide/), OWASP A03:2021
