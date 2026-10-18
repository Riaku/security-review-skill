# Decompression Bombs & XML Entity Expansion

**MUST** Cap compressed size, decompressed output, and entity expansion depth before and during parsing of untrusted input.

**Why:** A kilobyte zip-bomb or "billion laughs" XML expands to gigabytes, exhausting memory in seconds.

**Detect:** `zipfile.extractall`, `zlib.decompress` without size caps; XML parsers without entity-expansion limits.

**References:** CWE-409, CWE-776, CWE-789
