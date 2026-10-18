# Hermetic Builds (no undeclared network/env deps during build)

**SHOULD NOT** let builds reach the open network or read undeclared environment variables; all inputs must be declared and cached.

**Why:** Non-hermetic builds silently pull mutated or malicious dependencies mid-build, making artifacts unreproducible and quietly tamperable.

**Detect:** grep CI for `network:` modes, `--network=none`, `bazel --noenable_bzlmod`, unguarded `curl`/`pip install` outside lockfiles, ambient `export` in build scripts.

**References:** SLSA build isolation, NIST SP 800-218 PW.4, Reproducible Builds project, CWE-494
