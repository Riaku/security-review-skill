---
categories: [web-api-security]
domains: [backend]
---

# Document Processor Escape Hatches

**MUST** disable file-include, shell-escape, and external-fetch features in document and graphics processors, and allow-list the operations users may invoke.

**Why:** Any renderer that shells out or follows includes turns template injection into command execution; the escape hatch exists for convenience, not for untrusted input.

**Detect:** grep for `--shell-escape`, `--enable-write18`, `\write18`, missing `-dSAFER`, and unfiltered `\input{` passthrough in LaTeX/ImageMagick/LibreOffice invocations.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md
