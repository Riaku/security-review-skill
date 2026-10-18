# Open Directory Listing

**SHOULD NOT** enable directory indexes on web servers or object storage where file enumeration reveals backups, configs, or internal artifacts.

**Why:** `Autoindex on` / bucket list permission turns one known filename pattern into a full inventory of everything ever placed there.

**Detect:** grep server configs for `autoindex on`, `Options +Indexes`, bucket `ListBucket` grants; probe for `Index of /` responses.

**References:** OWASP WSTG-CONF-01, CWE-548, AWS S3 ACL best practices
