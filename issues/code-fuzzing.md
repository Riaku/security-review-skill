# Code Fuzzing for Attack Surfaces (AFL/libFuzzer on parsers and untrusted-input paths)

**SHOULD** continuously fuzz parsers, decoders, and other untrusted-input handlers with AFL/libFuzzer or OSS-Fuzz-style harnesses.

**Why:** Hand-written tests miss edge cases; fuzzing finds the memory corruption and crash bugs attackers actively weaponize in parsers.

**Detect:** grep for `libFuzzer`, `afl-fuzz`, `oss-fuzz`, `fuzz_targets`, `FUZZ_TARGET`, `cargo-fuzz`, `atheris`, corpus/seed directories in repos and CI.

**References:** OWASP Fuzzing chapter, CWE-119/CWE-20, NIST SP 800-218 PW.8, OSS-Fuzz docs
