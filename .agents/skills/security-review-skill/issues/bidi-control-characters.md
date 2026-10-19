---
categories: [correctness-pitfalls]
domains: [backend]
---

# Bidirectional Control Characters

**MUST** reject bidirectional override and zero-width characters in source, templates, and configuration, failing CI when a file contains them.

**Why:** Direction-override and invisible glyphs let a reviewer see one order of tokens while the compiler or browser executes another.

**Detect:** eslint-plugin-security detect-bidi-characters, or grep -rP '[\x{202A}-\x{202E}\x{2066}-\x{2069}]'

**References:** eslint-plugin-security, https://github.com/eslint-community/eslint-plugin-security, Trojan Source, https://trojansource.codes
