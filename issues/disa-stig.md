# DISA STIG Hardening

**SHOULD** apply DISA STIG checklists to systems handling regulated or government-adjacent data, documenting every deviation with a documented mitigation.

**Why:** STIG gaps show auditors unmitigated known vulnerabilities; unreviewed deviations become compliance findings and exploitable defaults left in place.

**Detect:** Look for STIG checklist files, `stig`/`STIG` annotations in Ansible or Puppet roles, and `openscap-scanner` profiles referencing `disa_stig`.

**References:** DISA STIG, NIST SP 800-70, CIS Controls v8 IG2, SCAP/OSCAL

---

**Part of:** [hardening-benchmarks](../categories/hardening-benchmarks.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)
