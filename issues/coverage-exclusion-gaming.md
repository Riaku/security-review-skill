---
categories: [testing-strategy]
domains: [backend]
---

# Coverage Exclusion Gaming

**MUST NOT** reach a coverage target by excluding hard-to-test modules or lowering the threshold; publish what is excluded and why.

**Why:** The modules most often excluded are the ones carrying authorization, cryptography and money movement, so the number rises exactly as the untested risk grows and a green badge certifies the opposite of what a reader assumes.
**Detect:** read `coverage.exclude`, `.coveragerc` `omit`, Jest `coveragePathIgnorePatterns`, `/* istanbul ignore */` and `// coverage:ignore` comments, and `sonar.exclusions`; flag any auth, crypto, payment or migration module on the list while the target is being met.
**References:** Coverage.py: excluding code, https://coverage.readthedocs.io/en/latest/excluding.html, Google Testing Blog: code coverage best practices, https://testing.googleblog.com/2020/08/code-coverage-best-practices.html
