---
categories: [web-api-security]
domains: [backend]
---

# CSV Formula Injection

**MUST** prefix-escape any exported field whose first character is `=`, `+`, `-`, `@`, tab, or CR, following RFC 4180 quoting.

**Why:** A username beginning with `=` executes as a formula when the export is opened in a spreadsheet, giving code execution on the reviewer's machine.

**Detect:** grep export code (`to_csv`, `csv.writer`, `CsvWriter`) for a field-prefix check (`'=`, `"="`, `startswith` guard) and for raw `join(',')` serialization.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md, RFC 4180 (CSV format)
