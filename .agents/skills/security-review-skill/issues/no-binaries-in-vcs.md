---
categories: [supply-chain]
domains: [governance]
---

# No Binaries In Version Control

**MUST NOT** commit generated executables or opaque binary artifacts to version control.

**Why:** Binaries cannot be reviewed in a diff, so they hide planted code while adding noise that discourages review of the change.

**Detect:** command `git ls-files | xargs file | grep -Ei 'ELF|Mach-O|PE32|executable'`, and check ignore rules for build output.

**References:** OpenSSF OSPS Baseline: no generated or unreviewable binaries in VCS, https://www.bestpractices.dev/en/criteria
