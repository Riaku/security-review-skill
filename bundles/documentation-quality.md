# documentation-quality — full checklist (13 items)

Docs and comments quality: BCP 14 keywords, style, sync with code, runnable READMEs.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/documentation-quality.md](../categories/documentation-quality.md) · Index: [SKILL.md](../SKILL.md)

# Agent Instruction-File Review Surface

**MUST** code-review and CODEOWN every agent instruction file (CLAUDE.md, AGENTS.md, .cursor/rules/*.mdc, copilot-instructions.md, .gemini/styleguide.md, QWEN.md) and keep it concise — bloated instruction files are silently ignored, making unenforced policy invisible.

**Why:** These files steer all generated code in the repo; a one-line frontmatter change (e.g. `alwaysApply: true`) is a prompt-injection-from-inside-the-repo vector, and rot makes claims diverge from CI reality.

**Detect:** PRs touching instruction files without review; instruction files >500 lines or full of task-specific one-offs; divergence between instruction-file claims and actual CI config.

**References:** GitHub custom-instructions guidance (≤2 pages), Cursor rules docs (<500 lines, check into git), Anthropic "bloated CLAUDE.md gets ignored"

# Architecture Doc & ADR Coverage

**SHOULD** maintain a current architecture overview (components, data flow, trust boundaries) plus ADRs for settled design decisions, kept in the repo.

**Why:** Without a current overview, every reviewer and new engineer rebuilds the mental model from code — and without ADRs, settled decisions get re-litigated endlessly or silently violated by people who never knew they were settled.

**Detect:** check for architecture doc with a diagram covering current components (compare against actual services/dirs); check docs/adr/ (or equivalent) exists with dated, numbered records; flag overview last-updated far behind structural changes.

**References:** C4 model, ADR practice (Nygard)

# BCP 14 Keyword Usage (RFC 2119 + RFC 8174)

**MUST** use requirement keywords (MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, OPTIONAL) in ALL CAPS where a requirement is intended, since only all-caps usage carries the BCP 14 meaning (RFC 8174 §2), and **SHOULD** include near the beginning of a spec, API doc, or policy document the RFC 8174 boilerplate wording "are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals".

**Why:** Mixed-case or casual "should/must" makes requirements ambiguous — readers can't tell a hard requirement from advice, and compliance reviews can't cite them.

**Detect:** grep docs for lowercase must/should/may in requirement contexts; check specs include the RFC 2119/8174 keyword-definition boilerplate; flag "must" used as emphasis rather than obligation.

**References:** RFC 2119, RFC 8174 §2, IETF BCP 14

# Capability Envelope Documentation

**MUST** document each model-backed feature's knowledge limits, tested validity range, and intended human oversight, and surface them where decisions are made.

**Why:** Undocumented capability boundaries invite over-trust, and over-trust is the exploit: users act on output outside the range where it was ever validated.

**Detect:** read the feature's model card or docs for stated limits, tested scope, and oversight expectations, then check whether the UI repeats them.

**References:** NIST AI 600-1 MAP 2.2, https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf

# Comments Explain Why, Not What

**SHOULD** write comments that explain intent, rationale, and constraints — not restate what the code already says.

**Why:** What-comments duplicate the code, go stale on every edit, and crowd out the why-context that actually helps the next reader (and the security reviewer looking for the invariant).

**Detect:** flag comments that restate the adjacent line (`// increment counter` above `count++`); look for TODO/dead commented-out code left in; positive signal: comments citing constraints, bug IDs, invariants, spec sections.

**References:** Code Complete (McConnell) on comments, MIT CommKit coding-and-comment style, Clean Code comment guidance

# Developer-Doc Style Consistency

**SHOULD** follow a single documented style guide (e.g. Google developer documentation style) across project docs: present tense, second person ("you"), active voice, sentence-case headings, consistent terminology per glossary.

**Why:** Inconsistent style reads as unreliable; inconsistent terminology is worse — two names for one concept makes docs contradict each other and users distrust all of it.

**Detect:** spot-check docs for voice/tense/person consistency and terminology drift (same concept under different names); check for a linked style guide and linting (Vale, proselint) enforcing it.

**References:** Google developer documentation style guide, ASD-STE100 Simplified Technical English (controlled-language rules), Write the Docs style-guide guidance, Vale linter

# Docs-Code Synchronization

**MUST** update documentation in the same change that alters the behavior it describes; stale docs are treated as a bug, not a backlog item.

**Why:** Docs that lag code are actively harmful — users follow documented behavior that no longer exists, and security-relevant drift (auth steps, config keys) becomes a silent trap.

**Detect:** review PRs touching public behavior for corresponding doc updates; flag documented commands/config/APIs that no longer match code (run documented examples in CI where possible); check docs last-modified vs code churn on covered surfaces.

**References:** docs-as-code practice, Google style guide (keep docs current), CI doc-example testing (doctest/mddoc patterns)

# Inclusive & Accessible Documentation

**SHOULD** use inclusive, jargon-free language in docs (Google style: avoid master/slave, blacklist/whitelist, gendered defaults) and meet doc accessibility basics (heading hierarchy, alt text, readable tables).

**Why:** Terminology carries exclusion history and confuses global audiences; inaccessible docs lock out users with disabilities — both are quality and compliance failures, not style nits. Controlled-language standards (ASD-STE100) exist precisely because plain, one-word-one-meaning prose is comprehensible to non-native readers worldwide.

**Detect:** grep docs for flagged terms (master/slave, blacklist/whitelist, guys, he/she defaults); check heading hierarchy and alt-text presence on images; lint with inclusive-language checkers (e.g. Vale rules); for procedural docs, check STE-controlled vocabulary adherence.

**References:** Google style guide (inclusive language), ASD-STE100 Simplified Technical English, Write the Docs accessibility guidance

# Mechanism Assumptions and Non-Goals

**MUST** state, in the mechanism's own documentation, the assumptions it depends on and the attacks it does not stop.

**Why:** A mechanism trusted outside its assumptions is worse than none, because it displaces the control that would have covered the gap. Non-goals are what prevent that substitution.

**Detect:** Security module README or docstrings lacking a non-goals or 'does not protect against' section.

**References:** RFC 3552, https://www.rfc-editor.org/rfc/rfc3552.txt

# Runnable README

**MUST** provide a README that takes a newcomer from zero to running the project: prerequisites, install, run, test commands — each verified to actually work.

**Why:** The README is the first attack surface for wasted time and a common failure point in onboarding and incident response; untested commands rot within weeks and erode trust in all documentation.

**Detect:** run README commands verbatim in a clean environment (CI doc-testing where possible); flag missing install/run/test sections, version-pinned prerequisites that no longer exist, or "TODO" placeholders.

**References:** Google style guide (readme content), docs-as-code tested-README practice, twelve-factor dev-environment onboarding

# Secure API Examples

**MUST** ship a complete, secure, copy-ready example for every security-sensitive API, and review that example as production code.

**Why:** Developers copy the example rather than the prose; when it is missing or unsafe they improvise the crypto, and the vulnerability ships with the library's blessing.

**Detect:** judgment — for each auth, crypto, and signing API in the docs, confirm an end-to-end example with key generation, error handling, and no placeholder secrets.

**References:** CryptoExamples controlled experiment, https://arxiv.org/abs/1807.01095

# Simplified Technical English for Procedures

**SHOULD** write operational/procedural documentation in controlled language per ASD-STE100: short sentences (max ~25 words), one meaning per word, active voice, one instruction per step, no idioms.

**Why:** Procedures followed under stress by non-native speakers must be unambiguous — STE exists because aerospace maintenance deaths traced to prose ambiguity; the same failure mode applies to runbooks and security procedures.

**Detect:** for runbooks/install steps: check sentence length, one-action-per-step structure, controlled vocabulary consistency (no synonym rotation: "log in/sign in/login" for the same action); flag idiomatic or marketing prose in procedural sections.

**References:** ASD-STE100 Simplified Technical English (asd-ste100.org), aerospace/defense doc standards, runbook readability practice

# Single-Source Documentation

**SHOULD** document each fact once with links pointing at the canonical location, rather than repeating it across files.

**Why:** Every duplicate is a future contradiction — copies drift out of sync and readers can't tell which one is current; the fix cost multiplies with each copy made.

**Detect:** grep docs for the same instructions/config/versions appearing in multiple files; flag copy-pasted blocks; check cross-references use links/includes instead of duplication.

**References:** Write the Docs DRY documentation guidance, docs-as-code single-source practice

