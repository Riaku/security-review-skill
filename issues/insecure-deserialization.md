# Insecure Deserialization

**MUST NOT** Deserialize untrusted data with pickle, ObjectInputStream, unserialize, or BinaryFormatter; use schema-validated JSON.

**Why:** Native deserializers instantiate arbitrary classes, yielding remote code execution.

**Detect:** `pickle.loads`, `ObjectInputStream`, `unserialize(`, `yaml.load` without SafeLoader on request data.

**References:** OWASP A08:2021, CWE-502, OWASP Deserialization Cheat Sheet

---

**Part of:** [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
