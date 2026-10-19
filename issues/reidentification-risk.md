---
categories: [compliance-privacy]
domains: [data, governance]
---

# Anonymization vs pseudonymization and re-identification risk in shared datasets

**MUST NOT** describe a dataset as anonymous unless re-identification is infeasible with auxiliary data; pseudonymized data — reversible keys, stable IDs — remains personal data under GDPR.

**Why:** Substituting user IDs is not anonymization. Linking "anonymized" exports against public sources (voter rolls, breach dumps, location traces) routinely re-identifies people, as the Netflix Prize showed.

**Detect:** Review shared exports for stable identifiers and quasi-identifiers (birth date + ZIP + gender), and whether k-anonymity or differential privacy was applied. Check whether the agreement's claimed classification matches custody of the mapping table.

**Bad:**
```python
export = df[["user_id", "zip", "dob", "purchase"]]  # "anonymous"
# join zip+dob against voter file -> names
```

**Good:**
```python
export = anonymize(df, k=20,
    generalize={"dob": "year", "zip": "5->3"})
# or differential-privacy aggregates, not row-level release
```

**References:** GDPR Recital 26 (anonymised vs pseudonymised), NIST SP 800-188 De-Identifying Datasets, Narayanan & Shmatikov
