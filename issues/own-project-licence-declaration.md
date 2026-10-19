---
categories: [compliance-privacy, supply-chain]
domains: [governance]
---

# Declare a Project Licence

**MUST** declare a licence at the repository root and put the matching SPDX identifier in source file headers, so consumers and scanners can determine their obligations without asking.

**Why:** Code with no licence is all-rights-reserved: nobody may legally copy, modify or ship it, and partial or drifted headers make the answer differ per file.

**Detect:** grep for a root `LICENSE`/`COPYING` file and for `SPDX-License-Identifier` headers in source files; flag repositories with source code and no licence file, or headers naming a licence that contradicts it (`reuse lint`, `licensee detect`, `scancode-toolkit`).

**References:** SPDX License List, https://spdx.org/licenses/, REUSE Specification, https://reuse.software/spec/, choosealicense.com, https://choosealicense.com/
