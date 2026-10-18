# Email-Template Injection

**MUST** treat user-controlled data interpolated into transactional emails as untrusted: escape HTML, strip/sanitize URLs, and never render user input as links or markup.

**Why:** Usernames or fields containing `<a href="https://phish...">` turn your trusted, DKIM-signed transactional email into a phishing vector your own domain vouches for.

**Detect:** grep mail templates for raw interpolation of user fields (`{{name}}` without escape, `|safe`, `dangerouslySetInnerHTML`); check URL fields are validated against allow-lists before rendering as links.

**References:** CWE-94 code injection in mail templates, OWASP XSS in email clients guidance

---

**Part of:** [email-security](../categories/email-security.md) · [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
