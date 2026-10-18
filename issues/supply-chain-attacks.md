# Supply Chain Attacks

**MUST** pin all external build inputs (base images, actions, tools) to immutable digests rather than mutable tags.

**Why:** Attackers compromise upstream tags or CI actions to inject malicious code into otherwise trusted builds, as in SolarWinds and event-stream.

**Detect:** `uses: owner/action@v1` without `@sha256:`; `FROM image:latest`; unpinned `curl | bash` in Dockerfiles or CI scripts.

**References:** NIST SP 800-161, CWE-829, SLSA L2
