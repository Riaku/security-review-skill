---
categories: [web-api-security]
domains: [backend]
---

# Dynamic Code Evaluation of User Input (eval/exec)

**MUST NOT** pass any externally influenced string to `eval`, `exec`, `Function`, or template code execution.

**Why:** Evaluating attacker-controlled text is remote code execution — full host compromise, no sandbox assumed.

**Detect:** `eval(`, `exec(`, `new Function(`, `compile(`/`__import__` on request data, template rendering of user strings (Jinja `|safe`, `Template(user_str)`), expression evaluators over user input.

**References:** CWE-94, CWE-95, OWASP Injection, OWASP ASVS 5.2
