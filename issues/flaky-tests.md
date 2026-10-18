# Flaky Tests

**MUST NOT** retry or auto-skip security tests to silence intermittent failures; a flaky auth test is an unverified control, not a nuisance.

**Why:** Retried tests mask real race conditions in session handling and permission checks that attackers can exploit deterministically.

**Detect:** `retry=True`, `@flaky`, `pytest-rerunfailures` on security-tagged tests; CI configs with `continue-on-error` around auth suites.

**References:** OWASP ASVS V4.1.2, CWE-364 (Signal Fault), NIST SP 800-218 PW.7a
