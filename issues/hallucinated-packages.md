---
categories: [ai-llm, supply-chain]
domains: [governance, infrastructure]
---

# Hallucinated Packages

**SHOULD** verify that every package name in generated or AI-assisted code actually exists and matches intent before installing.

**Why:** Attackers pre-register plausible-sounding package names that AI models invent, so blindly installing them pulls malware into the project.

**Detect:** Install logs for names absent from the registry; review AI-generated import lines against PyPI/npm search; grep manifests for near-miss spellings of popular libs.

**References:** CWE-427, Snyk "slopsquatting" research, OWASP LLM03
