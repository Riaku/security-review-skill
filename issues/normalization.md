---
categories: [database]
domains: [data]
---

# Normalization

**SHOULD** normalize transactional schemas to at least 3NF so each fact is stored once and updates cannot leave copies inconsistent.

**Why:** Duplicated attributes — a customer address copied into every order row — mean one correction requires updating N rows; miss any and reports, invoices, and shipping disagree about the same customer.

**Detect:** Repeated non-key columns across tables (same `customer_name` in orders, invoices, tickets); application code copying fields between tables on write; ad-hoc "sync" jobs patching copies.

**Bad:**
```sql
CREATE TABLE orders (id INT, customer_name TEXT, customer_addr TEXT, total NUMERIC);
-- address change = UPDATE across every order, forever
```

**Good:**
```sql
CREATE TABLE customers (id INT PRIMARY KEY, name TEXT, addr TEXT);
CREATE TABLE orders (id INT, customer_id INT REFERENCES customers(id), total NUMERIC);
```

**References:** Codd normal forms (1NF–3NF), Date *An Introduction to Database Systems*, CWE-1105
