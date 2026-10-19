---
categories: [security-practices, testing-strategy]
domains: [backend]
---

# Verification Path Coverage

**MUST** measure branch coverage of code that makes authentication, authorization, or signature-verification decisions and review every branch that never executes.

**Why:** A misplaced jump or duplicated cleanup branch in verification code silently accepts invalid input while line coverage stays green. Only branch-level measurement exposes the path that never runs.

**Detect:** command: `coverage run --branch` with `coverage report --show-missing` (or `gcov -b` / `llvm-cov show`) scoped to auth and signature modules; any uncovered branch in a verify function is a finding.

**References:** Apple 'goto fail' analysis, https://www.imperialviolet.org/2014/02/22/applebug.html, CWE-670 Always-Incorrect Control Flow Implementation
