# testing-strategy

Test pyramid, practices, and quality gates.

## What this category covers

This category covers how a codebase proves its behavior before and after merge: the layers of test, the properties each layer must actually assert, and the gates that block a bad change. The items span the test pyramid (unit, integration, end-to-end, smoke) and its sharp edges: flaky tests, determinism and isolation, stubbing only external dependencies, and expected outputs that are not derived from the implementation. They also cover techniques that guard security behavior — test-first discipline for fixes, a regression test per fixed bug, property-based and fuzz testing, contract testing, accessibility gates — and the CI checks that enforce them, including linting and static analysis, architecture fitness functions, and spec-to-implementation drift. Expect findings about a control that nothing actually verifies: a test that mocks the very check it claims to test, a suite that can pass against a broken implementation, or a gate that only warns.

- Test layers and coverage: unit tests for security-relevant functions, integration tests at real boundaries, end-to-end journeys, and smoke checks.
- Test quality: flaky-test discipline, determinism and isolation, stubbing only external dependencies, and assertions not derived from the implementation.
- Behavior-guarding techniques: test-first fixes, regression tests per bug, property-based testing, fuzz testing, and contract testing.
- CI gates: linting and static analysis, architecture fitness functions, accessibility checks, and spec-to-implementation drift.
- Automated-change verification: runnable pass-or-fail criteria wired into agent-assisted work.

## What it does not cover

- [correctness-pitfalls](../categories/correctness-pitfalls.md) — the defect classes tests are meant to catch belong there, not the tests themselves.
- [security-practices](../categories/security-practices.md) — organization-level process such as threat modeling, penetration testing, and disclosure belongs there rather than automated suites.
- [cicd-pipeline-security](../categories/cicd-pipeline-security.md) — pipeline execution, runner, and artifact integrity belong there rather than the test gates it runs.
- [observability](../categories/observability.md) — production detection and monitoring belong there rather than pre-merge verification.

## What a finding here looks like

- An auth middleware test that mocks the middleware itself, so a broken guard still passes.
- A security test retried or skipped to silence an intermittent failure, leaving a race condition unverified.
- A golden expectation regenerated from the code under test, so the test can never catch that code being wrong.
- A linter or SAST finding logged as a warning rather than failing the pipeline.
- A fixed access-control bug merged without a regression test that reproduces the exploit.
