# Software Licenses

**MUST** track third-party dependency licenses and enforce policy against incompatible or copyleft terms in proprietary distributions.

**Why:** Unlicensed or GPL-contaminated code in shipped products creates legal liability, forced open-sourcing, and distribution injunctions.

**Detect:** grep dependency manifests for `GPL`, `AGPL`, `UNLICENSED`; check license scanner config, `allowed_licenses`, `license_policy` files absent.

**References:** SPDX License List, GPL v2/v3, AGPL v3, OWASP Dependency-Check
