# Slow query log captured, reviewed, and regression-tracked

**SHOULD** enable the slow query log (or `pg_stat_statements`) at an SLO-appropriate threshold, review it on a standing cadence, and treat new entrants as regressions worth a ticket.

**Why:** Slow queries are both outage-causing and attacker-friendly: an unindexed query on an auth path is a DoS lever at volume and the first domino of a connection-pool meltdown. A log nobody reads is telemetry theater.

**Detect:** Check `log_min_duration_statement` or MySQL `slow_query_log`/`long_query_time`, and whether `pg_stat_statements` is loaded. Ask for the review artifact — dashboard, weekly triage note, CI perf gate. Enabled-but-unread logs fail too.

**Bad:**
```ini
log_min_duration_statement = -1   # logging disabled
```

**Good:**
```ini
shared_preload_libraries = 'pg_stat_statements'
log_min_duration_statement = 200  # tied to p95 SLO
# weekly triage: new top queries -> tickets
```

**References:** PostgreSQL pg_stat_statements docs, MySQL slow query log docs, Google SRE Book saturation monitoring
