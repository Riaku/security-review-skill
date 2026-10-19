---
categories: [correctness-pitfalls]
domains: [backend]
---

# Constant Format Strings

**MUST NOT** pass untrusted data as a format string to printf-style, logging, or template formatting functions.

**Why:** A user-controlled format string reads and writes memory through `%n`/`%s`, and the same mistake in loggers corrupts output.

**Detect:** grep `printf(`, `syslog(`, `fprintf(`, `fmt.Fprintf(w, <var>` and `String.format(<var>` where the first argument is not a string literal.

**References:** CWE Top 25, https://cwe.mitre.org/top25/, SEI CERT C Coding Standard (FIO30-C), https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard
