# Unsafe Merge Into Shared Runtime State

**MUST** allow-list keys before recursive merge or deep-set of untrusted input into shared, inherited, or prototype-level objects/registries.

**Why:** Poisoning shared state (JS `Object.prototype` via `__proto__` is the classic case; unsafe map/dict merge into shared config or caches is the same class) leaks attacker-controlled values to every later consumer — enabling XSS, auth bypass, and RCE.

**Detect:** grep merge/deep-set helpers fed request bodies (`merge(`, `deepSet`, `set(obj, key`); check `__proto__`/`constructor`/`prototype` key filtering; audit known-vulnerable library versions (e.g. lodash <4.17.21) and JSON.parse-then-merge flows.

**References:** CWE-1321, OWASP A08:2021, OWASP Prototype Pollution Prevention Cheat Sheet
