---
categories: [correctness-pitfalls, web-api-security]
domains: [backend]
---

# Dynamic Code Evaluation of User Input (eval/exec)

**MUST NOT** pass any externally influenced string to `eval`, `exec`, `Function`, or template code execution.

**Why:** Evaluating attacker-controlled text is remote code execution — full host compromise, no sandbox assumed.

**Detect:** `eval(`, `exec(`, `new Function(`, `os.system(`, `subprocess` with `shell=True` on input, Jinja `|safe`/`Template(user_str)`.

**References:** CWE-94, CWE-95, OWASP Injection, OWASP ASVS 5.2

---

**Part of:** [correctness-pitfalls](../categories/correctness-pitfalls.md) · [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
