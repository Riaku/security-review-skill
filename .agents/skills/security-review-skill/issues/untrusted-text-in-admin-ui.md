---
categories: [web-client-security]
domains: [frontend]
---

# Untrusted Text in Admin UI

**MUST** mark user-supplied text wherever it appears in privileged review, approval, or system-message surfaces so it cannot be mistaken for system output.

**Why:** A file named "Payment Approved - Finance System" deceives a human approver with no script execution and no technical exploit at all.

**Detect:** grep admin and approval templates for user-controlled fields (filenames, display names, subjects) rendered in the same style as system labels.

**References:** OWASP WSTG Business Logic Testing, https://github.com/OWASP/wstg/tree/master/document/4-Web_Application_Security_Testing
