# Full-Text Search

**MUST NOT** implement user-facing search with `LIKE '%term%'` on large tables; use the database's full-text engine or a dedicated search service.

**Why:** Leading-wildcard LIKE cannot use a B-tree index, so every keystroke triggers a full scan — a cheap amplification attack for anyone with a search box. It also mishandles stemming, ranking, and language.

**Detect:** `LIKE '%' || ? || '%'` patterns in query code; search endpoints without rate limiting; missing tsvector/GIN index (Postgres) or external index (Meilisearch, Elasticsearch).

**Bad:**
```sql
SELECT * FROM articles WHERE body LIKE '%' || :q || '%';  -- full scan per keystroke
```

**Good:**
```sql
CREATE INDEX articles_fts ON articles USING gin(to_tsvector('english', body));
SELECT * FROM articles WHERE to_tsvector('english', body) @@ plainto_tsquery(:q);
```

**References:** PostgreSQL Full Text Search + GIN indexes, OWASP ASVS V3.1, CWE-400

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
