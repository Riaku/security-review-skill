# window.postMessage Origin Validation

**MUST** verify `event.origin` against an expected allowlist and use a target-origin argument on every `postMessage` call.

**Why:** Skipping checks lets any embedded frame or opened window read sensitive messages or inject forged ones into the app.

**Detect:** grep `addEventListener('message'`, `postMessage(` with `'*'` target, handlers lacking `event.origin` comparison or `event.source` checks.

**References:** CWE-346, OWASP A01:2021, MDN postMessage security considerations

---

**Part of:** [web-client-security](../categories/web-client-security.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)
