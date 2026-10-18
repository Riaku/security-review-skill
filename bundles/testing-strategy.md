# testing-strategy — full checklist (19 items)

Test pyramid, practices, and quality gates.

> Generated artifact. Canonical source: `issues/<slug>.md`.

# Unit Tests

**MUST** cover every security-relevant function (auth checks, parsers, validators) with fast isolated tests asserting both accept and reject paths.

**Why:** Untested validation logic silently passes malformed input straight into privileged code paths.

**Detect:** test files named `*_test.py`, `*.test.js` adjacent to auth/parser modules; coverage reports showing <80% on security-critical files.

**References:** OWASP ASVS V4.1, CWE-1232, NIST SP 800-218 PW.7

# Integration Tests

**SHOULD** exercise real component boundaries — database, queues, external APIs — so auth and data-flow bugs hidden by isolation surface before production.

**Why:** Mocked boundaries hide authorization bypasses and serialization errors that only appear when real services interact.

**Detect:** docker-compose.test.yml, testcontainers usage, `pytest -m integration` markers; absence of any test touching a live DB or HTTP stub.

**References:** OWASP ASVS V4.1.4, CWE-1057, NIST SP 800-218 PW.8

# End-to-End Tests

**SHOULD** drive the full user journey through a real browser or client, including login, session expiry, and privilege escalation attempts.

**Why:** Security controls that pass in isolation can fail when wired through the real UI, proxies, and session handling.

**Detect:** Playwright/Cypress/Selenium specs under `e2e/`, scenarios asserting redirect on expired token and 403 on admin routes.

**References:** OWASP ASVS V4.1.3, OWASP WSTG v4.2 (session management), NIST SP 800-115

# Contract Testing

**MUST** verify service-to-service API contracts (request/response schemas, auth headers) so a producer change cannot silently break consumer security assumptions.

**Why:** Undeclared schema drift lets unauthenticated or malformed payloads cross trust boundaries without detection.

**Detect:** Pact consumer/provider specs, OpenAPI schema validation in CI (`schemathesis`, `dredd`), missing contract checks on internal REST/gRPC services.

**References:** OWASP API Security Top 10 API2, CWE-20, NIST SP 800-218 PW.7

# Flaky Tests

**MUST NOT** retry or auto-skip security tests to silence intermittent failures; a flaky auth test is an unverified control, not a nuisance.

**Why:** Retried tests mask real race conditions in session handling and permission checks that attackers can exploit deterministically.

**Detect:** `retry=True`, `@flaky`, `pytest-rerunfailures` on security-tagged tests; CI configs with `continue-on-error` around auth suites.

**References:** OWASP ASVS V4.1.2, CWE-364 (Signal Fault), NIST SP 800-218 PW.7a

# Mocking

**SHOULD NOT** mock the component under test's own security logic (auth middleware, validators); mock only external dependencies at their network boundary.

**Why:** Mocking the guard you are supposed to be testing produces green suites that verify nothing about real enforcement.

**Detect:** mocks/stubs of auth functions in the same module's tests, `unittest.mock.patch` targeting local validators rather than outbound clients.

**References:** OWASP ASVS V4.1, CWE-453 (Insecure Default Variable), NIST SP 800-218 PW.7

# Regression Tests

**MUST** add a permanent test for every fixed security bug before merging the fix, reproducing the exact exploit condition.

**Why:** Without a pinned regression case, the vulnerability can silently return in a later refactor and ship to production.

**Detect:** security fix PRs lacking a corresponding test case; CVE IDs or advisory references absent from test names/comments (e.g. `test_cve_2024_xxx`).

**References:** OWASP ASVS V4.1.1, CWE-757, NIST SP 800-218 RV.1 (verification after remediation)

# Smoke Tests

**MAY** run a minimal post-deploy check (health endpoint, login round-trip, TLS handshake) to catch catastrophic security misconfiguration before full traffic shifts.

**Why:** A bad deploy that breaks TLS or disables auth needs seconds to detect, not a full suite run.

**Detect:** `curl -k`-free health checks, smoke stage in pipeline (`smoke.yml`, `post-deploy` job) asserting HTTPS status and auth cookie issuance.

**References:** OWASP ASVS V14.2 (config), NIST SP 800-218 PO.3, WSTG v4.2 (config management testing)

# Property-Based Testing

**SHOULD** assert invariants that must hold for all inputs — parsers never accept overlong payloads, validators reject every boundary case — rather than spot-checking examples.

**Why:** Example-based tests miss edge inputs (empty, huge, Unicode, negative) that are exactly where injection and overflow bugs live.

**Detect:** hypothesis (`@given`), fast-check (`fc.assert`), jqwik usage on parsers/validators; missing property specs on input-handling modules.

**References:** CWE-20, OWASP ASVS V5.1 (validation), NIST SP 800-218 PW.7

# Fuzzing

**SHOULD** continuously fuzz externally reachable parsers, file format handlers, and API endpoints with malformed and random inputs in CI or nightly jobs.

**Why:** Hand-written tests cannot anticipate the input shapes that trigger memory corruption or parser confusion attackers hunt for.

**Detect:** oss-fuzz targets, `atheris`/`libFuzzer`/`honggfuzz` configs, restler or schemathesis fuzz runs in CI; zero fuzz targets on C/C++ or upload handlers.

**References:** OWASP WSTG v4.2 (fuzzing), CWE-119, NIST SP 800-218 PW.8 (fuzzing), Google OSS-Fuzz

# Test-Driven Development Discipline

**SHOULD** write the failing test before the security fix, watching it go red, then minimal code to green, so the test provably guards the behavior.

**Why:** Tests written after the fix often encode the buggy behavior or skip the exact condition the exploit used.

**Detect:** commit history showing fix commits with no preceding failing-test commit; PRs where tests and fixes arrive simultaneously with no red run in CI logs.

**References:** NIST SP 800-218 PW.7 (test-first practices), OWASP BSIMM TTD-1, CWE-1140 (attempt to use cached test results)

# Code Review Practice

**MUST** require at least one independent reviewer for every change touching authentication, cryptography, or input handling, with a documented security checklist and a response SLA.

**Why:** Single-author security code ships logic errors and backdoors that a second pair of eyes reliably catches.

**Detect:** CODEOWNERS covering auth/crypto paths, PR templates with security checklist items, branch protection requiring ≥1 approval; self-merged security PRs in git log.

**References:** OWASP ASVS V1.1.4, NIST SP 800-218 PS.1 (code review), OWASP Code Review Guide v2, CWE-1068 (design/practice inconsistency)

# Linting & Static Analysis Enforced in CI (linter, type checker, SAST)

**MUST** fail the pipeline when linters, type checkers, or SAST scans report findings, not merely log them as warnings.

**Why:** Advisory-only scans are ignored at scale; vulnerable code merges unchecked because nothing blocks it.

**Detect:** Workflow steps without `--exit-code`/`fail-on-error`; `continue-on-error: true` on scan jobs; SAST action with `level: warning`; missing ruff/mypy/semgrep/codeql steps entirely.

**References:** OWASP CI Security CS2, CWE-1156, NIST SP 800-218 PW.7, GitHub Code Scanning (CodeQL) docs

# Code Fuzzing for Attack Surfaces (AFL/libFuzzer on parsers and untrusted-input paths)

**SHOULD** continuously fuzz parsers, decoders, and untrusted-input handlers with AFL/libFuzzer-style harnesses.

**Why:** Hand-written tests miss edge cases; fuzzing surfaces the memory-corruption bugs attackers actively weaponize in parsers.

**Detect:** grep for `libFuzzer`, `afl-fuzz`, `oss-fuzz`, `fuzz_targets`, `cargo-fuzz`, `atheris`, seed/corpus directories in CI.

**References:** OWASP fuzzing guidance, CWE-119/CWE-20, NIST SP 800-218 PW.8, OSS-Fuzz docs

# OpenAPI–Implementation Drift Check

**SHOULD** verify in CI that the served API matches its OpenAPI spec (request/response validation against the contract), failing on drift.

**Why:** A spec that lies is worse than no spec: consumers code against documented behavior the implementation quietly diverged from, and breaking changes ship "documented as safe."

**Detect:** check CI for contract tests (Dredd, Schemathesis, Prism, schemathesis fuzz mode), response-middleware spec validation, or oasdiff between released spec versions.

**References:** Schemathesis/Dredd docs, contract-testing practice, OWASP API Security (improper inventory)

# Automated A11y Gate in CI

**SHOULD** run automated accessibility checks (axe-core/pa11y) in CI on UI changes, failing on new violations of the target WCAG level.

**Why:** One-line accessibility checklist items change nothing; a CI gate on actual scans makes regressions visible at the PR and compounds into real WCAG compliance over time.

**Detect:** check CI for `@axe-core/playwright`, `jest-axe`, pa11y-ci configs with violation thresholds; verify scans cover key routes, not just the homepage; check manual a11y review for what automation misses (keyboard flows, screen-reader semantics).

**References:** axe-core docs, WCAG 2.2, WAI-ARIA authoring practices, EAA/Section 508 compliance guidance

# Test Determinism & Isolation

**MUST** make tests deterministic: fixed seeds for randomized tests, no shared mutable state between tests, order-independent execution.

**Why:** Nondeterministic tests silently under-verify — a security assertion that passes only in certain orders or seeds gives false confidence, and intermittent failures train teams to re-run rather than investigate.

**Detect:** check for seeded randomness in test fixtures (seed recorded/pinned), test-order randomization enabled with passing results, shared globals/singletons mutated across test files.

**References:** test-isolation practice, flaky-test prevention guidance, property-based testing seed discipline

# Self-Generated Expected Output

**MUST NOT** derive a test's expected output from the code under test (golden files generated from current implementation, assertions copied from actual run).

**Why:** A test whose expectation came from the implementation can never catch the implementation being wrong — it enshrines today's bug as tomorrow's contract, especially dangerous for security golden-hashes.

**Detect:** review golden/expected files for how they were produced (independent source vs generated-from-implementation); flag "update goldens" workflows without review of what changed and why.

**References:** testing anti-pattern literature (tautological tests), characterization-testing caveats

# Agent Verification Loop (Executable Done-When)

**MUST** give every AI-agent coding task a runnable pass/fail verification criterion (tests, build, script-vs-fixture) wired into the task itself — otherwise the human becomes the verification loop.

**Why:** All major vendors converge on this: an agent without an executable check ships plausible-looking code indefinitely ("if you can't verify it, don't ship it" — Anthropic; "Done when" — GLM; easy-to-verify RL — Qwen).

**Detect:** agent task/plan artifacts merged with no named test/build/acceptance command; "implement X" tickets with no check; agent PRs whose CI runs no tests on the change.

**References:** Anthropic Claude Code best practices, GLM dev-pack best practice, Qwen3-Coder verification philosophy

