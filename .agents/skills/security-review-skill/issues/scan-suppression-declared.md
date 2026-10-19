---
categories: [security-practices]
domains: [backend]
---

# Declared Scan Suppressions

**MUST** record every scanner suppression as a scoped, justified, expiring declaration naming the rule and the non-exploitability argument.

**Why:** Inline ignores and blanket exclude files accumulate silently until the gate passes for reasons nobody can reconstruct.

**Detect:** grep for `# nosec`, `// nolint`, `.trivyignore`, `--exclude`, and scanner `ignore` entries; require an adjacent justification and expiry.

**References:** OpenSSF OSPS Baseline: suppressed findings must be declared, https://www.bestpractices.dev/en/criteria
