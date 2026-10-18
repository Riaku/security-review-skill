# secrets-crypto — full checklist (31 items)

Secrets handling and cryptographic primitives.

> Generated artifact — edit the issue files, not this one. Sources: [issues/](../issues/) · manifest: [secrets-crypto](../categories/secrets-crypto.md) · index: [SKILL.md](../SKILL.md)

# Agent Context-Exclusion Files

**SHOULD** maintain agent exclusion files (.cursorignore, .aiexclude, equivalent) covering secrets, credentials, and sensitive modules so they never enter agent context or indexes.

**Why:** Anything the agent can read, it can echo into code, logs, or a PR; exclusion files are the gitignore of the AI-context layer and their absence means sensitive paths are agent-reachable by default.

**Detect:** repo root lacks .cursorignore/.aiexclude while secrets/sensitive dirs are agent-reachable; index covers branches/patterns beyond the stable set; exclusion list missing recently-added sensitive paths.

**References:** Cursor .cursorignore, Gemini .aiexclude, GitHub content-exclusion controls

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# bcrypt & Argon2

**SHOULD** use Argon2id (preferred) or bcrypt with cost ≥12 for password hashing; MD5, SHA-1, and bare SHA-256 are unacceptable for credentials.

**Why:** Fast general-purpose hashes let GPUs test billions of guesses per second, cracking weak passwords in hours after a database breach.

**Detect:** `hashlib.md5`, `sha1(` on password fields, `bcrypt.gensalt(rounds=` below 12, absence of `argon2` in dependencies.

**References:** OWASP Password Storage Cheat Sheet, CWE-916, NIST SP 800-63B §5.1.1.2

---

**Part of:** [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Client-Side TLS Verification Disabled

**MUST NOT** disable server certificate or hostname verification in outbound TLS clients; every "works in dev" toggle like `verify=False` is a production man-in-the-middle hole.

**Why:** Skipping verification lets any attacker on the network path impersonate the remote service and capture credentials, tokens, or sensitive payloads that the app believes are encrypted.

**Detect:** Grep for `verify=False`, `verify: false`, `-k`/`--insecure` in curl invocations, `rejectUnauthorized: false`, `NODE_TLS_REJECT_UNAUTHORIZED=0`, custom `X509TrustManager` that returns without checking, `ssl._create_unverified_context`, `InsecureSkipVerify: true` in Go, and trust-all `HostnameVerifier` classes.

**Bad:**
```python
import requests
resp = requests.post("https://api.internal.example/token", json=payload, verify=False)
```

**Good:**
```python
import requests
resp = requests.post("https://api.internal.example/token", json=payload,
                     verify="/etc/ssl/corp-ca-bundle.pem")
```

**References:** CWE-295, CWE-299, OWASP ASVS 14.2, OWASP Testing Guide STG-CRYPTO-03

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Device Provisioning Identity

**SHOULD** provision each device with a unique, hardware-bound identity (per-device cert/keys, TPM/secure element) — never shared fleet credentials.

**Why:** One leaked shared device key or cert compromises every unit in the field; unique identities enable individual revocation and per-device attribution.

**Detect:** grep firmware/config for shared API keys, shared client certs, hardcoded device secrets; check for per-device cert enrollment flow (ACME/EST/custom) and a revocation path.

**References:** OWASP IoT Top 10 IOT DB1/credentials, FIDO/TPM device attestation, NIST IoT device identity guidance

---

**Part of:** [iot-embedded](../categories/iot-embedded.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [iot-embedded](../domains/iot-embedded.md) · [SKILL.md](../SKILL.md)

# Dockerfile Secret Leakage via COPY, Build Args, and Cache Layers

**MUST NOT** bake secrets into images via `COPY` of credential files or plain `ARG`/`ENV` values; use BuildKit `--mount=type=secret` instead.

**Why:** Copied files and build args persist in layer history and are recoverable from any pushed image with `docker history`.

**Detect:** Grep Dockerfiles for `COPY .npmrc`, `COPY *credentials*`, `ARG API_KEY`, `ENV SECRET`, or `RUN ... $ARG` patterns; inspect `docker history` for leaked values.

**References:** OWASP Docker DS02, CWE-540, NIST SP 800-218 (SSDF), BuildKit secret mounting docs, hadolint DL3025/DL3009

---

**Part of:** [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Embedding inversion and sensitive data in vector stores

**SHOULD NOT** embed raw sensitive documents in vector stores without assessment; embeddings can leak near-verbatim source text under inversion attacks.

**Why:** Published inversion techniques reconstruct personal and confidential content from vectors alone, defeating assumed one-way hashing.

**Detect:** vector DB ingest of unmasked PII fields; no access control on pgvector/Qdrant/Milvus collections; embeddings exported freely.

**References:** OWASP LLM02:2025, OWASP LLM08:2025, CWE-311

---

**Part of:** [ai-llm](../categories/ai-llm.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Encryption at Rest

**MUST** enable encryption at rest for databases, object storage, backups, and node disks holding sensitive data, with keys managed in a KMS rather than locally.

**Why:** Stolen drives, leaked snapshots, and misconfigured bucket exports expose everything unencrypted, bypassing every access control.

**Detect:** RDS/S3 `encrypted = false`, `storageClass` without SSE-KMS, Longhorn/Vault unencrypted PVCs, backup files with plaintext contents.

**References:** OWASP ASVS V0.9.2, CWE-311, NIST SP 800-53 SC-28

---

**Part of:** [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# .env in .gitignore

**MUST** list `.env`, `.env.*` (except committed `.env.example` templates) in `.gitignore` so local configuration never enters version control.

**Why:** A single committed `.env` exposes database URLs, API keys, and session secrets to everyone with repo read access, including forks.

**Detect:** `git check-ignore -v .env`; missing `.env` entry in `.gitignore`; `git ls-files | grep '\.env$'`.

**References:** OWASP Top 10 A05:2021, CWE-538, CWE-312

---

**Part of:** [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# etcd Exposure and Missing etcd Encryption

**MUST** restrict etcd (2379/2380) to control-plane peers and enable encryption at rest for all stored Secrets.

**Why:** etcd holds every secret in plaintext by default; a reachable or unencrypted datastore dumps the cluster's entire credential set.

**Detect:** etcd client port reachable off-node; kube-apiserver missing `--encryption-provider-config`; no EncryptionConfiguration resource.

**References:** CIS K8s 2.0, 3.2.1, CWE-311, NIST SP 800-190 5.2, K8s encryption-at-rest docs

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# FIPS 140-3 Validated Crypto

**MUST** perform cryptographic operations for regulated data using FIPS 140-3 validated modules rather than unaudited library implementations.

**Why:** Hand-rolled or non-validated crypto looks fine until a subtle implementation flaw breaks confidentiality with no compliance defense.

**Detect:** grep for "fips", "FIPS_MODE", openssl fips provider config; direct MD5/SHA1 usage, custom crypto, non-validated TLS libraries in regulated paths.

**References:** FIPS 140-3, CMVP validated module list, NIST SP 800-175B

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# FIPS 186 / Digital Signature Standards

**SHOULD** generate and verify digital signatures using approved algorithms (ECDSA, RSA per FIPS 186-5) with approved curves and key lengths only.

**Why:** Deprecated curves and short keys make signatures forgeable, undermining code signing, tokens, and non-repudiation guarantees.

**Detect:** grep for signature algorithm config: "RSA-1024", "DSA", "secp112", disabled curves; verify "P-256", "P-384", "RSA-2048+" in signing code.

**References:** FIPS 186-5, NIST SP 800-89

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# Git-History Secret Remediation

**MUST** remediate a committed secret by rewriting history (filter-repo/BFG), rotating the credential, and notifying collaborators to re-clone — deleting the file in a new commit is NOT remediation.

**Why:** The secret remains fully recoverable from history after deletion; the rotation must cover the entire exposure window since the key was public from first push, not last commit.

**Detect:** on any discovered secret: verify history was rewritten (not just deleted-at-HEAD), credential rotated with expiry-before-exposure-window logic, forks/clones notified; judgment on incident record completeness.

**References:** GitHub secret removal guidance, git-filter-repo/BFG docs, credential-exposure incident practice

---

**Part of:** [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Harvest-now-decrypt-later exposure of long-lived confidential data

**MUST** protect data whose confidentiality must outlast ~15 years (health records, identities, keys) with quantum-resistant or frequently re-keyed encryption, since today's ciphertext can be stored and decrypted later.

**Why:** Adversaries archive encrypted traffic and backups now, waiting for quantum or key-compromise advances to unlock them retroactively.

**Detect:** Long-retention archives encrypted only with RSA-2048/ECC, TLS sessions without hybrid KEM, backups with no key-rotation schedule.

**References:** NIST IR 8547, NSA CNSA 2.0 timeline, CISA post-quantum cryptography guidance

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Hashing vs Encryption

**MUST NOT** store passwords with reversible encryption; use one-way password hashing, and reserve encryption only for data that legitimately needs recovery.

**Why:** Encrypted password stores can be decrypted when the key leaks, exposing every credential at once in plaintext form.

**Detect:** `AES`, `encrypt(` near `password` fields, `Fernet`, `cryptography.fernet` applied to user credentials, ORM column named `encrypted_password`.

**References:** OWASP Password Storage Cheat Sheet, CWE-257, NIST SP 800-63B §5.1.1.2

---

**Part of:** [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Plaintext Secrets in Helm values Files and Rendered Manifests

**MUST NOT** commit plaintext secrets in `values.yaml` or render them into manifests; reference ExternalSecret/SealedSecret objects or inject at deploy time instead.

**Why:** Values files and `helm get values` output are readable by anyone with repo or release access, leaking credentials through charts and CI artifacts.

**Detect:** `password:`, `apiKey:`, `token:` literals in `values*.yaml`, `helm get values` output containing credentials, missing `existingSecret` references.

**References:** OWASP ASVS V2.10, CWE-312, Helm security best practices, Bitnami `existingSecret` pattern

---

**Part of:** [deployment-release](../categories/deployment-release.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Insufficient Randomness for Tokens and IDs

**MUST** generate session tokens, password resets, API keys, and invite codes from a cryptographically secure RNG (`secrets`, `crypto.randomBytes`, `SecureRandom`), never `random`/`Math.random`/sequential IDs.

**Why:** Predictable randomness lets attackers guess reset links and session tokens, taking over accounts without ever touching the password.

**Detect:** `Math.random()`, Python `random.` for tokens, `uuid1`/sequential IDs in auth flows, `rand()` in token generation code.

**References:** OWASP ASVS V3.2.2, CWE-330, NIST SP 800-90A

---

**Part of:** [authentication](../categories/authentication.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Integration Credential Sprawl

**SHOULD** centralize third-party SaaS credentials in a secrets manager with owner, scope, and expiry metadata — no credentials in shared docs, wikis, or personal accounts.

**Why:** SaaS credential sprawl (one per engineer, pasted in runbooks, never rotated) makes offboarding impossible to audit and breach blast radius unknowable.

**Detect:** inventory integration creds: count vs documented owners; grep wikis/runbooks/env files for SaaS API keys; check rotation history per integration; flag creds tied to individual employees.

**References:** NIST SP 800-53 IA-5, OWASP Secrets Management Cheat Sheet, vendor SSO/API-token best practices

---

**Part of:** [secrets-crypto](../categories/secrets-crypto.md) · [third-party-integrations](../categories/third-party-integrations.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Least Privilege

**MUST** grant every service account, role, and credential only the permissions its workload actually uses, verified against observed access rather than assumed needs.

**Why:** Over-broad credentials turn any single compromise into a cluster-wide or account-wide breach.

**Detect:** `cluster-admin`, `roleRef`, `rbac.authorization.k8s.io/v1`, `aws:iam::*:*admin*`, wildcard `"*"` in policy Action/Resource fields.

**References:** OWASP ASVS V1.4.3, CWE-269, NIST SP 800-53 AC-6

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Password Salting

**MUST** use a unique, cryptographically random salt per password hash, generated by the hashing library rather than a shared or static value.

**Why:** Identical or missing salts let attackers crack many accounts at once with rainbow tables and expose reused passwords across users.

**Detect:** Hardcoded `salt =` constants, `md5(password + SALT)`, bcrypt/argon2 calls without per-user salt handling, same hash for duplicate passwords in DB dumps.

**References:** OWASP Password Storage Cheat Sheet, CWE-759, NIST SP 800-63B §5.1.1.2

---

**Part of:** [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Pipeline-Orchestrator Credential Sprawl

**MUST** centralize credentials used by data orchestrators (Airflow connections, dbt profiles, Spark configs) in a secrets backend — not in DAG files, connections tables in plaintext, or CI env dumps.

**Why:** Orchestrators hold keys to every warehouse, bucket, and DB in the estate; their configs are broadly readable by data teams, making them the flattest credential attack surface in the company.

**Detect:** grep DAGs/profiles for inline passwords, check Airflow Connections backend (secrets env/backend vs metadata DB plaintext), review dbt `profiles.yml` handling, inspect Spark `--conf` for hardcoded AWS keys.

**References:** Airflow secrets-backend docs, dbt secure credentials guidance, OWASP Data Security

---

**Part of:** [data-pipelines](../categories/data-pipelines.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Post-quantum cryptography migration plan and crypto-agility

**SHOULD** maintain a documented PQC migration plan and crypto-agile design (algorithm negotiation, centralized crypto config) so ciphers can be swapped without rewrites.

**Why:** Systems hard-coded to RSA/ECC today cannot absorb the eventual quantum break of current public-key crypto without costly emergency rework.

**Detect:** Hardcoded `RSA-2048`/`ECDH P-256` with no config indirection, absence of `ML-KEM`/`X25519` hybrid plans, TLS library pinned without upgrade path.

**References:** NIST FIPS 203/204/205, NIST IR 8547 PQC migration, NSA CNSA 2.0

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# PQC readiness of TLS/VPN termination (hybrid KEM deployment)

**SHOULD** inventory every TLS and VPN termination point today and plan hybrid post-quantum key agreement (X25519 + ML-KEM) for long-lived, harvest-now-decrypt-later traffic before the client ecosystem forces a rushed rollout.

**Why:** Adversaries can record encrypted sessions now and decrypt them years later once quantum computers mature; data with a multi-decade confidentiality lifetime — VPN tunnels, backups, personal data — needs the quantum transition clocked deliberately, not in a panic.

**Detect:** Enumerate termination points (nginx/Apache, Envoy, cloud LBs, WireGuard/IPsec concentrators) and their TLS library versions; check for `ML-KEM`/`X25519MLKEM768` support (OpenSSL 3.5+, BoringSSL, cloud KMS PQC offerings), client-population coverage, and whether the inventory records each endpoint's data-sensitivity lifetime. Review VPN cipher suites for absence of any KEM upgrade path.

**Bad:**
```
# nginx pinned to OpenSSL 1.1.1 — no PQC group available, no upgrade plan
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384;
```

**Good:**
```
ssl_conf_param groups=X25519MLKEM768:X25519:secp384r1;  # hybrid, OpenSSL 3.5+
```

**References:** NIST FIPS 203 (ML-KEM), NIST PQC migration white papers, Cloudflare PQC deployment reports, IETF TLS hybrid KEM RFCs

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Secret Scanning

**MUST** run automated secret scanning (gitleaks, trufflehog, GitHub push protection) on every commit and full-history scans before publishing any repository.

**Why:** Developers routinely commit live credentials under deadline pressure; without scanning, leaks ship silently to public or shared remotes — and a secret once committed stays in git history forever, so rotation is the only true fix and is often missed.

**Detect:** `.gitleaks.toml`, `.pre-commit-config.yaml` with gitleaks/trufflehog hooks that reject at commit/push time, absent GitHub `secret_scanning`/push-protection settings in org config.

**References:** OWASP ASVS V2.10.2, CWE-540, CWE-319, NIST SP 800-218 (SSDF), GitHub push protection docs

---

**Part of:** [secrets-crypto](../categories/secrets-crypto.md) · [supply-chain](../categories/supply-chain.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Secret Validity Checking (verify leaked keys are live)

**SHOULD** validate whether a reported leaked credential is still active before closing the finding, and confirm revocation actually took effect at the provider.

**Why:** Treating every leak report as stale lets live keys keep working; conversely, assuming revocation worked without verification leaves access open.

**Detect:** No post-rotation validation step, `git leak` findings closed without provider-side revoke check, missing `aws sts get-caller-identity` / GitHub `/rate_limit` verification.

**References:** OWASP ASVS V2.10.4, GitHub secret scanning docs, AWS IAM key revocation runbooks

---

**Part of:** [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Secrets in CI Logs

**MUST NOT** echo, print, or interpolate secrets into CI output; mask values via CI secret masking and avoid commands that dump environment variables.

**Why:** Build logs are widely readable — teammates, forked PRs, and third-party integrations can harvest tokens from a single verbose step.

**Detect:** `echo $SECRET`, `set -x` in steps handling credentials, `env`/`printenv` in pipelines, `export` of tokens without `::add-mask::`.

**References:** OWASP ASVS V2.10.3, CWE-532, CWE-214

---

**Part of:** [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Secrets in Instance Launch Payloads

**MUST NOT** place credentials, tokens, or private keys in instance launch payloads — EC2 user-data, cloud-init scripts/templates, Azure `customData`, GCP startup-script metadata; grant scoped instance roles or fetch secrets from a secrets manager at boot instead.

**Why:** Launch payloads are readable through the same instance-metadata service attackers already target via SSRF (`curl http://169.254.169.254/latest/user-data`), are copied into AMIs and launch-template history, and persist in Terraform state and console screenshots — a credential placed there leaks through every one of those surfaces at once, long after the instance is gone.

**Detect:** grep user-data/cloud-init blocks for `AWS_SECRET_ACCESS_KEY`, `password=`, `token`, `-----BEGIN`, connection strings with credentials; Terraform `aws_instance.userdata` / `google_compute_instance.metadata.startup-script` containing literals rather than role names or secret-manager references; scanned AMI user-data for inherited secrets.

**References:** CIS AWS 5.4 (no secrets in user data), cloud-init sensitive-data guidance, AWS best practices for embedded credentials, aquasecurity/trivy-checks user-data secret rules

---

**Part of:** [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Hardcoded API keys and secrets in mobile app binaries

**MUST NOT** embed API keys, tokens, or symmetric secrets in app source, assets, or compiled binaries; ship them via short-lived server-issued credentials instead.

**Why:** Anyone can decompile the shipped IPA/APK and extract embedded secrets, since client code is fully inspectable.

**Detect:** run `strings`/mobSF scan on the binary; grep repo for `apiKey =`, `secret`, `BEGIN PRIVATE KEY`, hardcoded `AIza`/`sk-` prefixes in source and Info.plist/assets.

**References:** OWASP MASVS-STORAGE-2, CWE-798, CWE-321, MAS Testing Guide Reverse Engineering

---

**Part of:** [mobile](../categories/mobile.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [mobile](../domains/mobile.md) · [SKILL.md](../SKILL.md)

# Secrets Management

**MUST** source all secrets from a dedicated store (Vault, 1Password Connect, SOPS, cloud secret manager) rather than embedding them in images, repos, or plain ConfigMaps.

**Why:** Secrets baked into artifacts leak through registries, backups, and logs where they cannot be revoked cleanly.

**Detect:** `Secret` manifests with plaintext `data:`, `stringData:` without ESO/ExternalSecret, `secretKeyRef` absence alongside hardcoded tokens.

**References:** OWASP ASVS V2.10, CWE-259, NIST SP 800-57

---

**Part of:** [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Secrets Rotation Automation (scheduled/triggered rotation without downtime)

**MUST** rotate secrets automatically on schedule and immediately on suspected exposure, without manual steps or downtime.

**Why:** A leaked static secret stays valid forever; automation shrinks the attacker's usable window to the rotation interval.

**Detect:** Grep `rotation_period_days`, Secrets Manager rotation lambdas, Vault `ttl`/`lease`, ExternalSecret `refreshInterval`; IAM policies lacking `MaxAge`/rotation alarms (90 days typical); providers without rotation hooks in CI.

**References:** NIST SP 800-57, NIST SP 800-53 IA-5, CIS Control 6, OWASP ASVS V2.10.4

---

**Part of:** [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

# Plaintext secrets persisted in infrastructure-as-code state and outputs

**MUST** mark secret-bearing variables and outputs sensitive and store generated state and plan artifacts encrypted under access control; never expose raw state in logs, CI output or pull requests. Terraform's `sensitive = true` and `terraform output` are the common case.

**Why:** State files record every resource attribute in plaintext, so a leaked backend, backup, or plan output hands over all managed credentials at once.

**Detect:** `sensitive = false` or absent on secret attributes, `terraform.tfstate` in git, `terraform output` without `-json | jq` masking, unencrypted S3 backend.

**References:** HashiCorp sensitive data guidance, CWE-312, NIST SP 800-53 SC-28

---

**Part of:** [deployment-release](../categories/deployment-release.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Weak Crypto Primitives in Application Code

**MUST NOT** use DES, RC4, MD5, SHA-1, ECB mode, or hand-rolled ciphers in application code; standardize on AES-GCM or ChaCha20-Poly1305 via maintained libraries.

**Why:** Broken primitives are publicly broken — collisions, key recovery, and pattern leakage turn "encrypted" data into readable data.

**Detect:** `DES`, `RC4`, `ECB`, `md5(`, `sha1(` in security paths, `Cipher.getInstance("DES")`, custom XOR/"encryption" functions.

**References:** OWASP Cryptographic Storage Cheat Sheet, CWE-327, NIST SP 800-131A

---

**Part of:** [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)

