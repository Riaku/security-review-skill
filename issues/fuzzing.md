# Fuzzing

**SHOULD** continuously fuzz externally reachable parsers, file format handlers, and API endpoints with malformed and random inputs in CI or nightly jobs.

**Why:** Hand-written tests cannot anticipate the input shapes that trigger memory corruption or parser confusion attackers hunt for.

**Detect:** oss-fuzz targets, `atheris`/`libFuzzer`/`honggfuzz` configs, restler or schemathesis fuzz runs in CI; zero fuzz targets on C/C++ or upload handlers.

**References:** OWASP WSTG v4.2 (fuzzing), CWE-119, NIST SP 800-218 PW.8 (fuzzing), Google OSS-Fuzz
