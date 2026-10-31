---
categories: [compliance-privacy]
domains: [backend, frontend]
---

# Privacy Notice

**MUST** publish a privacy notice, reachable from every screen that collects personal data, naming the fields collected, why they are collected, how long they are kept, and who receives them.

**Why:** A notice that is missing, unreachable, or out of date is the first artifact a regulator, an app-store reviewer, or a customer's legal team opens, and every field it fails to describe — an added phone number, a new analytics vendor — is processing with no disclosed purpose.

**Detect:** grep the router and templates for a privacy route (`/privacy`, `/privacy-policy`, `privacy-notice`) and the footer, consent-banner or signup link that reaches it; then diff the fields the models and schema collect (email, phone, address, birth date, IP, government id) and the third parties that receive them against the notice's sections — a collected field or recipient the notice never names is the finding.

**References:** GDPR Arts. 12–13, https://eur-lex.europa.eu/eli/reg/2016/679/oj, California Civ. Code §1798.100, https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.100, NIST Privacy Framework, https://www.nist.gov/privacy-framework
