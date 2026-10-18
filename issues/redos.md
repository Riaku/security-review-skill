# Regular Expression DoS (ReDoS)

**MUST NOT** run user-supplied or unbounded text against regexes containing nested quantifiers or ambiguous alternation.

**Why:** Catastrophic backtracking turns a short malicious string into exponential CPU time, freezing the request thread or worker.

**Detect:** `(a+)+`, `(a|a)*`, `(.*)*` patterns, `re.match`/`RegExp.test` on raw input, no timeout or RE2/DFA engine configured.

**References:** CWE-1333, CWE-400, OWASP ReDoS, RE2 docs
