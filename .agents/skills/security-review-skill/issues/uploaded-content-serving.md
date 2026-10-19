---
categories: [web-api-security, web-client-security]
domains: [backend]
---

# Uploaded Content Serving

**MUST** serve user-uploaded content from a separate origin or object store, never execute or render it inline from the application's own origin.

**Why:** An uploaded HTML or SVG file served from your origin runs with your cookies and origin privileges, turning a file upload into stored script execution. Content inspection alone does not survive every parser differential.

**Detect:** grep upload handlers and static routes for upload directories inside the document root, inline `Content-Disposition`, and missing `X-Content-Type-Options: nosniff`; confirm uploads resolve to a distinct hostname or bucket.

**References:** OWASP File Upload Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html, CWE-434 Unrestricted Upload of File with Dangerous Type
