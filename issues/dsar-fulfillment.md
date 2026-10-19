---
categories: [compliance-privacy]
domains: [governance]
---

# DSAR Fulfillment (GDPR access/deletion requests)

**MUST** provide a verified mechanism to retrieve and erase all personal data for a data subject within one month of request (extendable by two further months for complex requests).

**Why:** Inability to fulfill DSARs violates GDPR Articles 15/17 and invites regulatory enforcement and subject complaints.

**Detect:** grep for missing DSAR endpoints or deletion jobs; check `dsar`, `right_to_erasure`, `data_export` handlers, SLA timers absent.

**References:** GDPR Art. 15, GDPR Art. 17, GDPR Art. 12(3), ISO 27701 §9
