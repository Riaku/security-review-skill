# Reproducible Builds

**SHOULD** produce bit-for-bit reproducible artifacts by eliminating timestamps, random paths, and nondeterministic ordering from builds.

**Why:** Non-reproducible output makes it impossible to verify that a deployed binary matches its reviewed source, hiding tampered releases.

**Detect:** `SOURCE_DATE_EPOCH` unset; build scripts embedding `date`/`hostname`; `-trimpath` absent in Go builds; unreproducible flag in `reproducible-builds.org` checks.

**References:** CWE-937, reproducible-builds.org, SLSA L3
