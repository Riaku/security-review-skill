# documentation-quality — full checklist (8 items)

Docs and comments quality: BCP 14 keywords, style, sync with code, runnable READMEs.

> Generated artifact. Canonical source: `issues/<slug>.md`.

# BCP 14 Keyword Usage (RFC 2119 + RFC 8174)

**MUST** use requirement keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) in ALL CAPS with their RFC 2119/8174 meanings in specs, API docs, and policy documents, and define them on first use per RFC 8174 §3.

**Why:** Mixed-case or casual "should/must" makes requirements ambiguous — readers can't tell a hard requirement from advice, and compliance reviews can't cite them.

**Detect:** grep docs for lowercase must/should/may in requirement contexts; check specs include the RFC 2119/8174 keyword-definition boilerplate; flag "must" used as emphasis rather than obligation.

**References:** RFC 2119, RFC 8174 §3, IETF BCP 14

# Developer-Doc Style Consistency

**SHOULD** follow a single documented style guide (e.g. Google developer documentation style) across project docs: present tense, second person ("you"), active voice, sentence-case headings, consistent terminology per glossary.

**Why:** Inconsistent style reads as unreliable; inconsistent terminology is worse — two names for one concept makes docs contradict each other and users distrust all of it.

**Detect:** spot-check docs for voice/tense/person consistency and terminology drift (same concept under different names); check for a linked style guide and linting (Vale, proselint) enforcing it.

**References:** Google developer documentation style guide, Write the Docs style-guide guidance, Vale linter

# Comments Explain Why, Not What

**SHOULD** write comments that explain intent, rationale, and constraints — not restate what the code already says.

**Why:** What-comments duplicate the code, go stale on every edit, and crowd out the why-context that actually helps the next reader (and the security reviewer looking for the invariant).

**Detect:** flag comments that restate the adjacent line (`// increment counter` above `count++`); look for TODO/dead commented-out code left in; positive signal: comments citing constraints, bug IDs, invariants, spec sections.

**References:** Stack Overflow code-comment best practices, MIT CommKit coding-and-comment style, clean-code comment guidance

# Docs-Code Synchronization

**MUST** update documentation in the same change that alters the behavior it describes; stale docs are treated as a bug, not a backlog item.

**Why:** Docs that lag code are actively harmful — users follow documented behavior that no longer exists, and security-relevant drift (auth steps, config keys) becomes a silent trap.

**Detect:** review PRs touching public behavior for corresponding doc updates; flag documented commands/config/APIs that no longer match code (run documented examples in CI where possible); check docs last-modified vs code churn on covered surfaces.

**References:** docs-as-code practice, Google style guide (keep docs current), CI doc-example testing (doctest/mddoc patterns)

# Single-Source Documentation

**SHOULD** document each fact once with links pointing at the canonical location, rather than repeating it across files.

**Why:** Every duplicate is a future contradiction — copies drift out of sync and readers can't tell which one is current; the fix cost multiplies with each copy made.

**Detect:** grep docs for the same instructions/config/versions appearing in multiple files; flag copy-pasted blocks; check cross-references use links/includes instead of duplication.

**References:** Write the Docs DRY documentation guidance, docs-as-code single-source practice

# Inclusive & Accessible Documentation

**SHOULD** use inclusive, jargon-free language in docs (Google style: avoid master/slave, blacklist/whitelist, gendered defaults) and meet doc accessibility basics (heading hierarchy, alt text, readable tables).

**Why:** Terminology carries exclusion history and confuses global audiences; inaccessible docs lock out users with disabilities — both are quality and compliance failures, not style nits.

**Detect:** grep docs for flagged terms (master/slave, blacklist/whitelist, guys, he/she defaults); check heading hierarchy and alt-text presence on images; lint with inclusive-language checkers (e.g. Vale rules).

**References:** Google style guide (inclusive language), IETF inclusive-naming RFC 5424 historic guidance, Write the Docs accessibility guidance

# Runnable README

**MUST** provide a README that takes a newcomer from zero to running the project: prerequisites, install, run, test commands — each verified to actually work.

**Why:** The README is the first attack surface for wasted time and a common failure point in onboarding and incident response; untested commands rot within weeks and erode trust in all documentation.

**Detect:** run README commands verbatim in a clean environment (CI doc-testing where possible); flag missing install/run/test sections, version-pinned prerequisites that no longer exist, or "TODO" placeholders.

**References:** Google style guide (readme content), docs-as-code tested-README practice, twelve-factor dev-environment onboarding

# Architecture Doc & ADR Coverage

**SHOULD** maintain a current architecture overview (components, data flow, trust boundaries) plus ADRs for settled design decisions, kept in the repo.

**Why:** Without a current overview, every reviewer and new engineer rebuilds the mental model from code — and without ADRs, settled decisions get re-litigated endlessly or silently violated by people who never knew they were settled.

**Detect:** check for architecture doc with a diagram covering current components (compare against actual services/dirs); check docs/adr/ (or equivalent) exists with dated, numbered records; flag overview last-updated far behind structural changes.

**References:** C4 model, ADR practice (Nygard), adaptive-architecture guidance

