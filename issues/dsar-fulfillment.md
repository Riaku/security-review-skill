---
categories: [compliance-privacy]
domains: [governance]
---

# DSAR Fulfillment (GDPR access/deletion requests)

**MUST** provide a verified mechanism to retrieve and erase all personal data for a data subject within one month of request (extendable by two further months for complex requests), including a machine-readable export (JSON/CSV) of the data the subject provided and that is processed on consent or contract (GDPR Art. 20).

**Why:** Inability to fulfill DSARs violates GDPR Articles 15/17 and invites regulatory enforcement and subject complaints.

**Detect:** grep for missing DSAR endpoints or deletion jobs; check `dsar`, `right_to_erasure`, `data_export` handlers, SLA timers absent; review export coverage against the datastore inventory (the Art. 20 export must cover provided data while the Art. 15 response covers activity/logs/derived records) and confirm the self-service export is access-controlled.

**References:** GDPR Art. 15, GDPR Art. 17, GDPR Art. 20 (portability), GDPR Art. 12(3), ISO 27701 §9, DSAR platform docs
