---
categories: [security-practices, supply-chain]
domains: [governance]
---

# Secure Development Attestation

**SHOULD** retain signed, per-release evidence that the documented secure-development practices were followed, in a form a customer can verify.

**Why:** Procurement increasingly asks for attestation rather than a questionnaire, and evidence invented after the fact is worthless. Unsigned claims of practice cannot be distinguished from aspiration.

**Detect:** judgment: the release artifacts — a signed attestation or provenance bundle per version, mapped to the practices it claims and retrievable by version.

**References:** CISA Secure Software Development Attestation Form, https://www.cisa.gov/resources-tools/resources/secure-software-development-attestation-form, NIST SP 800-218 (SSDF)
