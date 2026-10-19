---
categories: [documentation-quality]
domains: [backend]
---

# Developer-Doc Style Consistency

**SHOULD** follow a single documented style guide (e.g. Google developer documentation style) across project docs: present tense, second person ("you"), active voice, sentence-case headings, consistent terminology per glossary.

**Why:** Inconsistent style reads as unreliable; inconsistent terminology is worse — two names for one concept makes docs contradict each other and users distrust all of it.

**Detect:** spot-check docs for voice/tense/person consistency and terminology drift (same concept under different names); check for a linked style guide and linting (Vale, proselint) enforcing it.

**References:** Google developer documentation style guide, ASD-STE100 Simplified Technical English (controlled-language rules), Write the Docs style-guide guidance, Vale linter
