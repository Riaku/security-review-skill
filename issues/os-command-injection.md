# OS Command Injection (CWE-78)

**MUST NOT** Pass user input into shell commands; invoke programs with argument arrays, no shell interpolation.

**Why:** `;`, `|`, and backticks turn an argument into arbitrary command execution.

**Detect:** `os.system`, `subprocess` with `shell=True`, `Runtime.exec`, `$()`/backticks in built command strings.

**References:** CWE-78, OWASP A03:2021, OWASP Command Injection guidance

---

**Part of:** [correctness-pitfalls](../categories/correctness-pitfalls.md) · [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
