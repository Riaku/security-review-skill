---
categories: [correctness-pitfalls, security-practices]
domains: [backend]
---

# Trusted-Side Validation

**MUST** validate every value that crosses an internal trust boundary in the consuming component — plugin, sandbox, worker, or a service the team does not own — never only in the producer, which the trust model already assumes an attacker can control.

**SHOULD** install that check at the first trusted function that interprets the value rather than at the deeper site where it finally detonates, so one check covers every later use and still lands in code the team can change.

**Why:** A producer-side check is a promise from the component you are defending against: if the plugin, sandbox or upstream service is compromised, its validation runs under the attacker's control and approves whatever it is handed. The value is not made trustworthy by having been validated somewhere — only by being validated where the privileges are at stake.

**Detect:** validation living inside plugin/extension/worker code, in the library that produces the value, or in a shared validator the untrusted side invokes; trusted handlers consuming a plugin return value, a registered callback, or a shared-memory field with no local check; guards added at the crash line, especially inside a dependency with no source, instead of at the first consumer in first-party code.

**References:** CWE-501, CWE-807, CWE-345
