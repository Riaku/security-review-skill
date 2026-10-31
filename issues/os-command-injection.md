---
categories: [web-api-security]
domains: [backend]
---

# OS Command Injection (CWE-78)

**MUST NOT** Pass user input into shell commands; invoke programs with argument arrays, no shell interpolation, and keep request data out of the environment of a child process that expands variables.

**Why:** `;`, `|`, and backticks turn an argument into arbitrary command execution, and a tainted environment variable is the same injection when the child expands `$VAR`/`%VAR%` or runs a shell wrapper.

**Detect:** `os.system`, `subprocess` with `shell=True`, `Runtime.exec`, `$()`/backticks in built command strings; `Runtime.exec(String[], String[] envp)` or `ProcessBuilder.environment().put(...)` carrying request values into a command that expands them.

**References:** CWE-78, OWASP A03:2021, OWASP Command Injection guidance
