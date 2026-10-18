# Path Traversal

**MUST NOT** Use user input directly in file paths; resolve and confirm the result stays inside the base directory.

**Why:** `../` sequences escape the sandbox to read configs, keys, and source off the host.

**Detect:** `open(` / `send_file` with request params; `os.path.join(base, user_input)` without post-resolve prefix check.

**References:** OWASP A03:2021, CWE-22, OWASP Path Traversal guide

---

**Part of:** [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
