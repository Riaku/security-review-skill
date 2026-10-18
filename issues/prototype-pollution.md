# Prototype Pollution

**MUST** validate and reject `__proto__`, `constructor`, and `prototype` keys before recursive merge or deep-set operations on untrusted input.

**Why:** Polluted `Object.prototype` leaks attacker-controlled properties app-wide, enabling XSS, auth bypass, and RCE in Node.

**Detect:** grep `__proto__`, `merge(`, `deepSet`, `set(obj, key` in utils; check lodash versions <4.17.21 and JSON.parse-then-merge flows.

**References:** CWE-1321, OWASP A08:2021, OWASP Prototype Pollution Prevention Cheat Sheet
