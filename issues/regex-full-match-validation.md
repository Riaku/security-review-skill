---
categories: [web-api-security]
domains: [backend]
---

# Regex Full-Match Validation

**MUST** anchor validator patterns to the whole input, so a substring match cannot pass an allowed-format check.

**Why:** Unanchored patterns accept `valid-prefix<script>` because they match somewhere in the string. Bare alternation makes anchors apply to only one branch.

**Detect:** `re.match(`/`re.search(`/`preg_match(`/`Matcher.find()` used for validation without `^...$` or `fullmatch`; alternation lacking a wrapping group.

**References:** OpenSSF: Correctly Using Regular Expressions, https://best.openssf.org/Correctly-Using-Regular-Expressions, CWE-625
