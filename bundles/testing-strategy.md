# testing-strategy — full checklist (34 items)

Test pyramid, practices, and quality gates.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/testing-strategy.md](../categories/testing-strategy.md) · Index: [SKILL.md](../SKILL.md)

# Agent Verification Loop (Executable Done-When)

**MUST** give every AI-agent coding task a runnable pass/fail verification criterion (tests, build, script-vs-fixture) wired into the task itself — otherwise the human becomes the verification loop.

**Why:** Industry practice converges on this: an agent without an executable check ships plausible-looking code indefinitely.

**Detect:** agent task/plan artifacts merged with no named test/build/acceptance command; "implement X" tickets with no check; agent PRs whose CI runs no tests on the change.

**References:** Anthropic Claude Code best practices, vendor coding-agent verification guidance

# Architecture Fitness Functions in CI

**SHOULD** encode architectural constraints (dependency direction and depth, layering rules, latency budgets, secrets-only-via-secrets-layer) as executable checks that run in CI on every change, not as documentation reviewed once.

**Why:** ADRs record that a boundary was decided; fitness functions keep it from eroding over the next 200 commits. Unenforced architectural rules drift silently until they fail at scale, and a stated boundary with no automated check is indistinguishable from no boundary.

**Detect:** presence of ArchUnit, import-linter, dependency-cruiser, or custom structural validators wired into CI config; absence of any automated structural check is the finding.

**References:** catio.tech/blog/architecture-as-code, Ford/Parsons/Kua "Building Evolutionary Architectures" (fitness functions)

# Test From the Attacker's View

**MUST** test the deployed system end to end against attacker paths, not only per-unit happy paths inside the code.

**Why:** Most exploitable flaws live in the seams between middleware, routing, and services, and unit tests mock exactly those seams away.

**Detect:** run an authenticated black-box pass (`zap-baseline.py -r report.html <url>` or the OWASP WSTG checklist) against a deployed environment in CI or pre-release.

**References:** OWASP Web Security Testing Guide, https://owasp.org/www-project-web-security-testing-guide/

# Authorization Test Matrix

**MUST** test authorization as a matrix of actors against actions and objects, including cross-user, cross-tenant, and expired-role denials.

**Why:** Functional tests exercise the happy owner path; authorization bugs live in the pairs nobody wrote a test for.

**Detect:** grep the test suite for each endpoint's owner case only, and for absent `403`/`forbidden` assertions against a second user or tenant.

**References:** OWASP Authorization Regression Testing Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Regression_Testing_Cheat_Sheet.html

# Automated A11y Gate in CI

**SHOULD** run automated accessibility checks (axe-core/pa11y) in CI on UI changes, failing on new violations of the target WCAG level.

**Why:** One-line accessibility checklist items change nothing; a CI gate on actual scans makes regressions visible at the PR and compounds into real WCAG compliance over time.

**Detect:** check CI for `@axe-core/playwright`, `jest-axe`, pa11y-ci configs with violation thresholds; verify scans cover key routes, not just the homepage; check manual a11y review for what automation misses (keyboard flows, screen-reader semantics).

**References:** axe-core docs, WCAG 2.2, WAI-ARIA authoring practices, EAA/Section 508 compliance guidance

# Code Review Practice

**MUST** require at least one independent reviewer for every change touching authentication, cryptography, or input handling, with a documented security checklist and a response SLA.

**Why:** Single-author security code ships logic errors and backdoors that a second pair of eyes reliably catches.

**Detect:** CODEOWNERS covering auth/crypto paths, PR templates with security checklist items, branch protection requiring ≥1 approval; self-merged security PRs in git log.

**References:** OWASP ASVS V1.1.7, NIST SP 800-218 (SSDF) (code review), OWASP Code Review Guide v2, CWE-1068 (Inconsistency Between Implementation and Documented Design)

# Concurrency Stress Testing

**SHOULD** exercise concurrent code with interleaving and stress tests that reproduce races, not only sequential unit tests.

**Why:** Races do not reproduce on the happy path; they reproduce under real interleaving, usually first in production.

**Detect:** a stress target that fires the same handler or critical section from many goroutines/threads with randomized scheduling and repeats, wired into CI; a bare `go test -race` run belongs to sanitizers-in-ci.

**References:** Software Engineering at Google, ch. 20, https://abseil.io/resources/swe-book/html/ch20.html

# Contract Testing

**MUST** verify service-to-service API contracts (request/response schemas, auth headers) so a producer change cannot silently break consumer security assumptions.

**Why:** Undeclared schema drift lets unauthenticated or malformed payloads cross trust boundaries without detection.

**Detect:** Pact consumer/provider specs, OpenAPI schema validation in CI (`schemathesis`, `dredd`), missing contract checks on internal REST/gRPC services.

**References:** OWASP API Security Top 10 API10:2023 (Unsafe Consumption of APIs), CWE-20, NIST SP 800-218 (SSDF)

# Control Effectiveness Testing

**MUST** test that each security control actually fires — lockout, filter rule, report endpoint, alert route — not merely that it is configured.

**Why:** A control deployed with a typo looks identical to a working one in a configuration review. Only a negative test that should trigger it proves the path is live.

**Detect:** command: an automated control test suite (for example a `pytest tests/security/test_controls.py` job or an active scanner run against staging) that triggers each control and asserts the block or alert.

**References:** OWASP Web Security Testing Guide, NIST SP 800-53 CA-8

# End-to-End Tests

**SHOULD** drive the full user journey through a real browser or client, including login, session expiry, and privilege escalation attempts.

**Why:** Security controls that pass in isolation can fail when wired through the real UI, proxies, and session handling.

**Detect:** Playwright/Cypress/Selenium specs under `e2e/`, scenarios asserting redirect on expired token and 403 on admin routes.

**References:** OWASP ASVS V4.1.3, OWASP WSTG v4.2 (session management), NIST SP 800-115

# Verify Fixes Beyond The Finding

**MUST** verify a security fix by re-running the full scanner set plus a behavioral exploit test, never by the disappearance of one finding.

**Why:** A change can silence the named check while leaving sibling findings, breaking behavior, or missing the security intent entirely.

**Detect:** command re-run every configured scanner and the exploit test for the class, then diff the complete result set before and after the fix.

**References:** TerraProbe repair verification, https://arxiv.org/abs/2606.26590

# Flaky Tests

**MUST NOT** retry or auto-skip security tests to silence intermittent failures; a flaky auth test is an unverified control, not a nuisance.

**Why:** Retried tests mask real race conditions in session handling and permission checks that attackers can exploit deterministically.

**Detect:** `retry=True`, `@flaky`, `pytest-rerunfailures` on security-tagged tests; CI configs with `continue-on-error` around auth suites.

**References:** OWASP ASVS V1.1.1, CWE-362, NIST SP 800-218 (SSDF)

# Fuzzing

**SHOULD** continuously fuzz externally reachable parsers, file format handlers, and API endpoints with malformed and random inputs in CI or nightly jobs.

**Why:** Hand-written tests cannot anticipate the input shapes that trigger memory corruption or parser confusion attackers hunt for; fuzzing surfaces the memory-corruption bugs attackers actively weaponize in parsers.

**Detect:** oss-fuzz targets, `atheris`/`libFuzzer`/`honggfuzz`/AFL configs, `fuzz_targets` declarations and seed/corpus directories, `cargo-fuzz`, restler or schemathesis fuzz runs in CI; zero fuzz targets on C/C++ or upload handlers.

**References:** OWASP WSTG v4.2 (fuzzing), CWE-119, NIST SP 800-218 (SSDF) (fuzzing), Google OSS-Fuzz

# Integration Tests

**SHOULD** exercise real component boundaries — database, queues, external APIs — so auth and data-flow bugs hidden by isolation surface before production.

**Why:** Mocked boundaries hide authorization bypasses and serialization errors that only appear when real services interact.

**Detect:** docker-compose.test.yml, testcontainers usage, `pytest -m integration` markers; absence of any test touching a live DB or HTTP stub.

**References:** OWASP ASVS V1.1.1, CWE-1057, NIST SP 800-218 (SSDF)

# Linting & Static Analysis Enforced in CI (linter, type checker, SAST)

**MUST** fail the pipeline when linters, type checkers, or SAST scans report findings, not merely log them as warnings.

**Why:** Advisory-only scans are ignored at scale; vulnerable code merges unchecked because nothing blocks it, and defects caught in production cost orders of magnitude more than at commit time.

**Detect:** Workflow steps without `--exit-code`/`fail-on-error`; `continue-on-error: true` on scan jobs; SAST action with `level: warning`; missing ruff/mypy/semgrep/codeql steps entirely; pre-commit hooks running the same checks earliest in the lifecycle.

**References:** NIST SP 800-218 (SSDF), GitHub Code Scanning (CodeQL) docs, OWASP SAMM Security Testing, OWASP DevSecOps Maturity Model

# Mocking

**SHOULD NOT** mock the component under test's own security logic (auth middleware, validators); mock only external dependencies at their network boundary.

**Why:** Mocking the guard you are supposed to be testing produces green suites that verify nothing about real enforcement.

**Detect:** mocks/stubs of auth functions in the same module's tests, `unittest.mock.patch` targeting local validators rather than outbound clients.

**References:** OWASP ASVS V4.1, CWE-453 (Insecure Default Variable), NIST SP 800-218 (SSDF)

# Negative Test Coverage

**MUST** include negative tests asserting that unauthorized, malformed, and out-of-policy operations fail, not only that valid operations succeed.

**Why:** A suite that tests only the happy path passes just as loudly when an authorization check is deleted. Negative tests are what make 'merge if green' a meaningful gate.

**Detect:** grep test suites for assertions on 401/403/400 paths, `pytest.raises`, and `expect(...).toThrow`; modules with only success-path cases are the finding.

**References:** GitLab secure coding guidelines, https://docs.gitlab.com/development/secure_coding_guidelines/, OpenSSF Concise Guide for Developing More Secure Software, https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Concise-Guide-for-Developing-More-Secure-Software.md

# OpenAPI–Implementation Drift Check

**SHOULD** verify in CI that the served API matches its OpenAPI spec (request/response validation against the contract), failing on drift.

**Why:** A spec that lies is worse than no spec: consumers code against documented behavior the implementation quietly diverged from, and breaking changes ship "documented as safe."

**Detect:** check CI for contract tests (Dredd, Schemathesis, Prism, schemathesis fuzz mode), response-middleware spec validation, or oasdiff between released spec versions.

**References:** Schemathesis/Dredd docs, contract-testing practice, OWASP API Security (improper inventory)

# Property-Based Testing

**SHOULD** assert invariants that must hold for all inputs — parsers never accept overlong payloads, validators reject every boundary case — rather than spot-checking examples.

**Why:** Example-based tests miss edge inputs (empty, huge, Unicode, negative) that are exactly where injection and overflow bugs live.

**Detect:** hypothesis (`@given`), fast-check (`fc.assert`), jqwik usage on parsers/validators; missing property specs on input-handling modules.

**References:** CWE-20, OWASP ASVS V5.1 (validation), NIST SP 800-218 (SSDF)

# Regression Tests

**MUST** add a permanent test for every fixed security bug before merging the fix, reproducing the exact exploit condition.

**Why:** Without a pinned regression case, the vulnerability can silently return in a later refactor and ship to production.

**Detect:** security fix PRs lacking a corresponding test case; CVE IDs or advisory references absent from test names/comments (e.g. `test_cve_2024_xxx`).

**References:** OWASP ASVS V1.1.1, NIST SP 800-218 (SSDF) (verification after remediation)

# Sanitizers in CI

**MUST** build and test memory-unsafe code that parses untrusted input with address, undefined-behaviour, and thread sanitizers in CI.

**Why:** Sanitizers turn latent memory and concurrency bugs into loud, reproducible CI failures instead of remote code execution in production.

**Detect:** two CI jobs: `-fsanitize=address,undefined` and a separate `-fsanitize=thread` (MSan where the runtime allows), each running the parser test suite; a single combined flag set is a bug in the pipeline, not a passing gate.

**References:** OWASP C-Based Toolchain Hardening Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/C-Based_Toolchain_Hardening_Cheat_Sheet.html

# Negative Control for Security Scanners

**MUST** validate each security scanner against a fixture with a known finding before trusting a clean result on real code.

**Why:** A scanner that crashes, misconfigures, or skips its target reports no findings, which is indistinguishable from a clean codebase.

**Detect:** run the scanner in CI against a seeded vulnerable fixture and assert the expected finding is reported

**References:** Trail of Bits Testing Handbook, https://github.com/trailofbits/testing-handbook, AppSec Guide, https://appsec.guide/

# Security Re-Check on Fixes

**MUST** re-run the security review and security tests over the area any bug fix touches, including code that was not security-relevant before.

**Why:** Fixes to previously safe code routinely introduce new vulnerabilities, and fix discussion rarely mentions security, so an unreviewed fix is an unreviewed change to the attack surface.

**Detect:** `git show --stat` on the fix commit, then confirm the changed paths are covered by a security test; a conventional-commit 'fix:' prefix is a filter, not the evidence

**References:** Mozilla security-regression study, https://arxiv.org/abs/2207.01942

# Seeded-Defect Review Calibration

**SHOULD** seed a known number of defects into a review round and use the detection ratio to estimate how many unknown defects remain.

**Why:** A review that finds nothing is indistinguishable from a review that missed everything unless its sensitivity has been measured.

**Detect:** judgment: the last calibration exercise's found-versus-seeded table and the residual estimate it implies

**References:** Anderson, Security Engineering 1st ed., ch.23, https://www.cl.cam.ac.uk/~rja14/book.html

# Self-Generated Expected Output

**MUST NOT** derive a test's expected output from the code under test (golden files generated from current implementation, assertions copied from actual run).

**Why:** A test whose expectation came from the implementation can never catch the implementation being wrong — it enshrines today's bug as tomorrow's contract, especially dangerous for security golden-hashes.

**Detect:** review golden/expected files for how they were produced (independent source vs generated-from-implementation); flag "update goldens" workflows without review of what changed and why.

**References:** testing anti-pattern literature (tautological tests), characterization-testing caveats

# Smoke Tests

**MAY** run a minimal post-deploy check (health endpoint, login round-trip, TLS handshake) to catch catastrophic security misconfiguration before full traffic shifts.

**Why:** A bad deploy that breaks TLS or disables auth needs seconds to detect, not a full suite run.

**Detect:** `curl -k`-free health checks, smoke stage in pipeline (`smoke.yml`, `post-deploy` job) asserting HTTPS status and auth cookie issuance.

**References:** OWASP ASVS V14.1 (build and deploy), NIST SP 800-218 (SSDF), WSTG v4.2 (configuration testing)

# Static Gate Not Sufficient

**MUST NOT** treat a clean static-analysis run as evidence that input-dependent paths are secure.

**Why:** Vulnerabilities that depend on adversarial input, execution context, or chaining evade static checks while remaining exploitable.

**Detect:** command run the dynamic or exploit suite for the changed surface (`schemathesis`, `zap-baseline`, PoC tests) alongside the static gate.

**References:** Static-pass / dynamic-fail gap, https://arxiv.org/abs/2609.10762

# Structured Fuzz Harness

**SHOULD** derive typed, structured inputs from the fuzz bytes so each harness reaches the parser's real code paths instead of one shallow entry point.

**Why:** Coverage is decided by harness design: a harness that never decodes its input exercises almost none of the parsing logic it claims to fuzz.

**Detect:** each fuzz target body: targets that forward raw bytes without constructing the format's typed message have no structured coverage

**References:** Trail of Bits Testing Handbook, https://github.com/trailofbits/testing-handbook

# Test-Driven Development Discipline

**SHOULD** write the failing test before the security fix, watching it go red, then minimal code to green, so the test provably guards the behavior.

**Why:** Tests written after the fix often encode the buggy behavior or skip the exact condition the exploit used.

**Detect:** commit history showing fix commits with no preceding failing-test commit; PRs where tests and fixes arrive simultaneously with no red run in CI logs.

**References:** NIST SP 800-218 (SSDF)

# Test Determinism & Isolation

**MUST** make tests deterministic: fixed seeds for randomized tests, no shared mutable state between tests, order-independent execution.

**Why:** Nondeterministic tests silently under-verify — a security assertion that passes only in certain orders or seeds gives false confidence, and intermittent failures train teams to re-run rather than investigate.

**Detect:** check for seeded randomness in test fixtures (seed recorded/pinned), test-order randomization enabled with passing results, shared globals/singletons mutated across test files.

**References:** test-isolation practice, flaky-test prevention guidance, property-based testing seed discipline

# Test Fixture Data Hygiene

**MUST NOT** place production personal data, live credentials, or real customer records in test fixtures, examples, or seed data.

**Why:** Fixtures are copied into repositories, CI logs, and image layers with none of the controls that protect the production store. Once committed, the exposure is permanent and unrevokable.

**Detect:** grep fixture, seed, and example files for real-looking addresses and account numbers plus live key prefixes (`AKIA`, `sk_live_`, `ghp_`); confirm generators or synthetic data are used instead.

**References:** OWASP User Privacy Protection Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html, CWE-312 Cleartext Storage of Sensitive Information

# Tooling Security Gap Measurement

**MUST** re-measure each adopted code-generation tool's security pass rate on your own tasks, rather than inferring safety from functional gains or release notes.

**Why:** Functional improvement and security improvement diverge per model family, so yesterday's measurement is the only evidence you have about today's tool.

**Detect:** run the same security test suite per tool version and diff the pass rate across releases.

**References:** Longitudinal functionality-security gap study (arXiv 2610.08240), https://arxiv.org/abs/2610.08240

# Unit Tests

**MUST** cover every security-relevant function (auth checks, parsers, validators) with fast isolated tests asserting both accept and reject paths.

**Why:** Untested validation logic silently passes malformed input straight into privileged code paths.

**Detect:** test files named `*_test.py`, `*.test.js` adjacent to auth/parser modules; coverage reports showing <80% on security-critical files.

**References:** OWASP ASVS V1.1.1, NIST SP 800-218 (SSDF)

# Verification Path Coverage

**MUST** measure branch coverage of code that makes authentication, authorization, or signature-verification decisions and review every branch that never executes.

**Why:** A misplaced jump or duplicated cleanup branch in verification code silently accepts invalid input while line coverage stays green. Only branch-level measurement exposes the path that never runs.

**Detect:** command: `coverage run --branch` with `coverage report --show-missing` (or `gcov -b` / `llvm-cov show`) scoped to auth and signature modules; any uncovered branch in a verify function is a finding.

**References:** Apple 'goto fail' analysis, https://www.imperialviolet.org/2014/02/22/applebug.html, CWE-670 Always-Incorrect Control Flow Implementation

