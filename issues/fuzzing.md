# Fuzzing

**SHOULD** continuously fuzz externally reachable parsers, file format handlers, and API endpoints with malformed and random inputs in CI or nightly jobs.

**Why:** Hand-written tests cannot anticipate the input shapes that trigger memory corruption or parser confusion attackers hunt for; fuzzing surfaces the memory-corruption bugs attackers actively weaponize in parsers.

**Detect:** oss-fuzz targets, `atheris`/`libFuzzer`/`honggfuzz`/AFL configs, `fuzz_targets` declarations and seed/corpus directories, `cargo-fuzz`, restler or schemathesis fuzz runs in CI; zero fuzz targets on C/C++ or upload handlers.

**References:** OWASP WSTG v4.2 (fuzzing), CWE-119, NIST SP 800-218 PW.8 (fuzzing), Google OSS-Fuzz

---

**Part of:** [testing-strategy](../categories/testing-strategy.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
