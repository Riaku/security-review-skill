# Decision-Record Provenance

**SHOULD** keep decision artifacts (assumption logs, decision records/ADRs) alongside the outputs and code they govern: who decided what, when, on what evidence.

**Why:** Months later, nobody can distinguish a deliberate assumption from an oversight — and future reviewers re-litigate settled choices or trust stale ones without provenance.

**Detect:** judgment on presence of decision/assumption records near consequential logic and outputs (ADRs in docs/adr, assumption logs in analysis projects), with dates and authors.

**References:** ADR practice (Nygard)