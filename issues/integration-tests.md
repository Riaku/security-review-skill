# Integration Tests

**SHOULD** exercise real component boundaries — database, queues, external APIs — so auth and data-flow bugs hidden by isolation surface before production.

**Why:** Mocked boundaries hide authorization bypasses and serialization errors that only appear when real services interact.

**Detect:** docker-compose.test.yml, testcontainers usage, `pytest -m integration` markers; absence of any test touching a live DB or HTTP stub.

**References:** OWASP ASVS V4.1.4, CWE-1057, NIST SP 800-218 PW.8

---

**Part of:** [testing-strategy](../categories/testing-strategy.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
