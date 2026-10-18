# GDPR

**MUST** process personal data of EU residents only under a documented lawful basis, with data minimization enforced at collection.

**Why:** Unlawful processing exposes organizations to fines up to 4% of global annual turnover under GDPR Article 83.

**Detect:** grep for personal data fields collected without consent flags; check privacy policy config, `lawful_basis`, `consent_required` keys absent from data models.

**References:** GDPR Art. 5-6, GDPR Art. 83, ISO 27701
