---
categories: [compliance-privacy]
domains: [backend, data]
---

# Personal-Data Inventory

**MUST** maintain an inventory mapping each personal-data field to every store and third party that holds or receives it, updated when a new store, export, or integration is added.

**Why:** An erasure request, a breach notification, and a subject-access response all depend on knowing every copy of the data; without the map the first two silently miss the analytics export, the search index, and the vendor that receives support tickets.

**Detect:** grep schema, migrations, and integration clients for personal-data columns (`email`, `phone`, `address`, `dob`, `ip_address`, national ids) and for outbound processors; compare each against the inventory artifact (`DATA_MAP.md`, a ROPA export, `data_inventory.yaml`) — a column, store, or recipient with no entry is the finding.

**References:** GDPR Art. 30, https://eur-lex.europa.eu/eli/reg/2016/679/oj, NIST SP 800-122, https://csrc.nist.gov/pubs/sp/800/122/final, NIST Privacy Framework, https://www.nist.gov/privacy-framework
