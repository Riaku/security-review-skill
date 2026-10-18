# Code Fuzzing for Attack Surfaces (AFL/libFuzzer on parsers and untrusted-input paths)

**SHOULD** continuously fuzz parsers, decoders, and untrusted-input handlers with AFL/libFuzzer-style harnesses.

**Why:** Hand-written tests miss edge cases; fuzzing surfaces the memory-corruption bugs attackers actively weaponize in parsers.

**Detect:** grep for `libFuzzer`, `afl-fuzz`, `oss-fuzz`, `fuzz_targets`, `cargo-fuzz`, `atheris`, seed/corpus directories in CI.

**References:** OWASP fuzzing guidance, CWE-119/CWE-20, NIST SP 800-218 PW.8, OSS-Fuzz docs
