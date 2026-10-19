---
categories: [correctness-pitfalls]
domains: [backend]
---

# Merge Conflicts

**MUST NOT** commit unresolved conflict markers or blindly pick one side when merging security-sensitive code.

**Why:** A stray `<<<<<<<` breaks the build, and a wrong-side resolution can silently drop an auth check or re-enable a patched flaw.

**Detect:** `<<<<<<<`, `=======`, `>>>>>>>` in tracked files, conflict resolved without re-running tests, security files merged without review.

**References:** OWASP ASVS 15.2, Git conflict docs
