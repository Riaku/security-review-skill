# Mocking

**SHOULD NOT** mock the component under test's own security logic (auth middleware, validators); mock only external dependencies at their network boundary.

**Why:** Mocking the guard you are supposed to be testing produces green suites that verify nothing about real enforcement.

**Detect:** mocks/stubs of auth functions in the same module's tests, `unittest.mock.patch` targeting local validators rather than outbound clients.

**References:** OWASP ASVS V4.1, CWE-453 (Insecure Default Variable), NIST SP 800-218 PW.7
