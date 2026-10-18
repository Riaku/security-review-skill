# Error Handling

**MUST** catch errors at the boundary that can recover, and propagate everything else with context instead of letting it vanish.

**Why:** Swallowed or generic error paths hide failures, leak stack traces to users, and let corrupted state persist silently.

**Detect:** `except:`, `except Exception: pass`, `catch {}`, `catch (e) {}`, `.catch(() => {})`, `err != nil` ignored, `|| pass`

**References:** CWE-390, CWE-209, OWASP ASVS 7.4
