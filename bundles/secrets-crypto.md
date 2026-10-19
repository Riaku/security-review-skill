# secrets-crypto — full checklist (66 items)

Secrets handling and cryptographic primitives.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/secrets-crypto.md](../categories/secrets-crypto.md) · Index: [SKILL.md](../SKILL.md)

# Agent Context-Exclusion Files

**SHOULD** maintain agent exclusion files (.cursorignore, .aiexclude, equivalent) covering secrets, credentials, and sensitive modules so they never enter agent context or indexes.

**Why:** Anything the agent can read, it can echo into code, logs, or a PR; exclusion files are the gitignore of the AI-context layer and their absence means sensitive paths are agent-reachable by default.

**Detect:** repo root lacks .cursorignore/.aiexclude while secrets/sensitive dirs are agent-reachable; index covers branches/patterns beyond the stable set; exclusion list missing recently-added sensitive paths.

**References:** Cursor .cursorignore, Gemini .aiexclude, GitHub content-exclusion controls

# Build Artifact Secret Scanning

**MUST** scan every built package and image layer for credentials before publishing it, not only the source tree.

**Why:** A credential baked into a package or image layer ships to every consumer and is invisible to working-tree scans.

**Detect:** `trufflehog filesystem` or `gitleaks dir` against the built artifact and each extracted image layer before publish.

**References:** Threagile accidental-secret-leak risk, https://github.com/Threagile/threagile/blob/master/pkg/risks/scripts/accidental-secret-leak.yaml, Docker image secret leakage study (arXiv 2307.03958), https://arxiv.org/abs/2307.03958

# bcrypt & Argon2

**SHOULD** use Argon2id (preferred) or bcrypt with cost ≥12 for password hashing; MD5, SHA-1, and bare SHA-256 are unacceptable for credentials.

**Why:** Fast general-purpose hashes let GPUs test billions of guesses per second, cracking weak passwords in hours after a database breach.

**Detect:** `hashlib.md5`, `sha1(` on password fields, `bcrypt.gensalt(rounds=` below 12, absence of `argon2` in dependencies.

**References:** OWASP Password Storage Cheat Sheet, CWE-916, NIST SP 800-63B §5.1.1.2

# Class-Identifying Secret Prefixes

**MUST** give every token the system issues a fixed, non-configurable prefix that identifies its class, and register that prefix with every secret scanner.

**Why:** Without a prefix a leaked token is indistinguishable from noise, so it survives in scanners, logs, and commit history undetected and unrevocable by pattern.

**Detect:** grep token issuance code for a constant prefix beside the signing call, and for that prefix in the secret-scanning rule set.

**References:** GitLab Secure Coding Guidelines, https://docs.gitlab.com/development/secure_coding_guidelines/

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

**References:** CWE-295, CWE-299, OWASP ASVS V9.2.1, OWASP WSTG-CRYP-01

# Constant Time After Compilation

**MUST** verify constant-time behavior on the compiled artifact, not only the source, because optimization passes can reintroduce timing leaks.

**Why:** A correct constant-time routine can be transformed into a branch on secret data, and only the generated code shows what the CPU executes.

**Detect:** command run a `dudect` or `ctgrind` timing harness against the built binary with the pinned compiler version and flags.

**References:** Compiler-introduced timing leaks, https://arxiv.org/abs/2507.06112, CWE-208 (Observable Timing Discrepancy)

# Credentials Never in URLs

**MUST NOT** place credentials, API keys, reset tokens, or session identifiers in URL paths, query strings, or fragments.

**Why:** URLs are copied into access logs, browser history, Referer headers, proxy caches and shell history, so a URL-borne secret spreads to systems you never authorized.

**Detect:** grep for `?token=`, `?api_key=`, `?access_token=`, `?password=`, and route definitions that take a secret in a path segment

**References:** OWASP Authentication Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html, CWE-598 Use of GET Request Method With Sensitive Query Strings

# Crypto Algorithm Lifecycle States

**MUST** classify every algorithm in use as acceptable, deprecated, legacy-verify-only or disallowed, with per-state rules and dated deadlines.

**Why:** Without explicit states, deprecated primitives keep generating new signatures because nothing distinguishes 'can still verify old data' from 'may be used today'.

**Detect:** Inspect the crypto inventory: each algorithm and key has a state, and code enforces it (legacy keys verify only, never sign).

**References:** NIST SP 800-131A Rev. 2, https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-131Ar2.pdf, BSI TR-02102-2, https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR02102/BSI-TR-02102-2.pdf

# Crypto Finding Scope Triage

**SHOULD** assign severity to cryptographic findings by what the code protects, treating non-security uses as out of scope.

**Why:** A hash used for cache keys is not a weak password hash. Grading both the same floods the queue and hides the finding that protects a credential.

**Detect:** For each crypto finding, name the asset it protects (confidentiality, integrity, neither) before assigning severity.

**References:** arXiv:2209.11103, https://arxiv.org/abs/2209.11103

# Cryptographic Inventory

**MUST** maintain a discovered inventory of every key, certificate, and algorithm, recording where each may be used and what it may protect.

**Why:** You cannot rotate, migrate, or audit cryptography you do not know exists, and an unscoped key quietly accumulates uses it was never designed for.

**Detect:** diff the KMS and keystore listings against service configs; `openssl x509 -noout -text` over deployed certificates to capture algorithms and expiry.

**References:** OWASP ASVS v5.0 V11.1.2, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md

# Crypto Known-Answer Tests

**MUST** validate cryptographic code against published known-answer and edge-case test vectors, not only round-trip self-tests.

**Why:** A round trip passes for an implementation that is consistently wrong. Published vectors catch wrong curves, truncation and malformed-input handling.

**Detect:** Run the Wycheproof suite for every primitive in use; a custom wrapper needs its own harness over the same vectors.

**References:** Project Wycheproof, https://github.com/google/wycheproof, Tink, https://github.com/tink-crypto/tink

# Data In Use Protection

**MUST** minimize sensitive data held in process memory and encrypt or wipe it as soon as processing completes.

**Why:** Rest and transit get checked and memory does not, so plaintext secrets sit in heap dumps, crash reports, and swap long after the request ends.

**Detect:** grep for long-lived plaintext secret buffers and for zeroization calls (`memset_s`, `explicit_bzero`, `zeroize`, `SecureString`) around their use.

**References:** OWASP ASVS v5.0 V11.7.2, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md, CWE-316

# Device Provisioning Identity

**SHOULD** provision each device with a unique, hardware-bound identity (per-device cert/keys, TPM/secure element) — never shared fleet credentials.

**Why:** One leaked shared device key or cert compromises every unit in the field; unique identities enable individual revocation and per-device attribution.

**Detect:** grep firmware/config for shared API keys, shared client certs, hardcoded device secrets; check for per-device cert enrollment flow (ACME/EST/custom) and a revocation path.

**References:** OWASP IoT Top 10 I1 (Weak, Guessable, or Hardcoded Passwords), FIDO/TPM device attestation, NIST IoT device identity guidance

# Dockerfile Secret Leakage via COPY, Build Args, and Cache Layers

**MUST NOT** bake secrets into images via `COPY` of credential files or plain `ARG`/`ENV` values; use BuildKit `--mount=type=secret` instead.

**Why:** Copied files and build args persist in the final image: copied file contents remain in the saved layers of any pushed image, and ARG/ENV values stay visible in `docker history` and image metadata.

**Detect:** Grep Dockerfiles for `COPY .npmrc`, `COPY *credentials*`, `ARG API_KEY`, `ENV SECRET`, or `RUN ... $ARG` patterns; inspect `docker history` for leaked values.

**References:** OWASP Docker Top 10 D06 (Protect Secrets), CWE-540, NIST SP 800-218 (SSDF), BuildKit secret mounting docs, Trivy secret scanning / Checkov Dockerfile checks

# Embedding inversion and sensitive data in vector stores

**SHOULD NOT** embed raw sensitive documents in vector stores without assessment; embeddings can leak near-verbatim source text under inversion attacks.

**Why:** Published inversion techniques reconstruct personal and confidential content from vectors alone, defeating assumed one-way hashing.

**Detect:** vector DB ingest of unmasked PII fields; no access control on pgvector/Qdrant/Milvus collections; embeddings exported freely.

**References:** OWASP LLM02:2025, OWASP LLM08:2025, CWE-311

# Encrypt Operational Channels

**MUST** encrypt management, monitoring, database, and partner connections to the same standard as user-facing traffic.

**Why:** Operational links carry credentials and full records over the same hostile network, and are the ones built before anyone wrote a TLS policy.

**Detect:** grep connection strings and agent config for `sslmode=disable`, `tls=false`, `insecure: true`; nmap --script ssl-enum-ciphers on 5432, 9090, 22.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x21-V12-Secure-Communication.md, NIST SP 800-52 Rev 2

# Encrypt Then MAC

**MUST** use authenticated encryption, or encrypt-then-MAC ordering when composing primitives, and never verify after decrypting.

**Why:** Decrypt-before-verify is what powers padding-oracle classes; the ordering, not the primitive choice, is the control.

**Detect:** grep for ciphertext decryption followed by a MAC or tag check (`decrypt(` then `hmac.compare`), and for `AES/CBC/PKCS5Padding` with a separate MAC.

**References:** OWASP ASVS v5.0 V11.3.5, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md, CWE-353

# Encryption at Rest

**MUST** enable encryption at rest for databases, object storage, backups, and node disks holding sensitive data, with keys managed in a KMS rather than locally.

**Why:** Stolen drives, leaked snapshots, and misconfigured bucket exports expose everything unencrypted, bypassing every access control.

**Detect:** RDS/S3 `encrypted = false`, `storageClass` without SSE-KMS, Longhorn/Vault unencrypted PVCs, backup files with plaintext contents.

**References:** OWASP ASVS V6.1.1, CWE-311, NIST SP 800-53 SC-28

# .env in .gitignore

**MUST** list `.env`, `.env.*` (except committed `.env.example` templates) in `.gitignore` so local configuration never enters version control.

**Why:** A single committed `.env` exposes database URLs, API keys, and session secrets to everyone with repo read access, including forks.

**Detect:** `git check-ignore -v .env`; missing `.env` entry in `.gitignore`; `git ls-files | grep '\.env$'`.

**References:** OWASP Top 10 A05:2021, CWE-538, CWE-312

# Ephemeral Key Agreement

**MUST** use ephemeral per-connection key agreement so later compromise of a long-term key cannot decrypt recorded traffic.

**Why:** Static key exchange makes every recorded session decryptable the day the private key leaks. Forward secrecy bounds that loss to sessions in flight.

**Detect:** Static ECDH, `TLS_RSA_*` suites, or a shared symmetric key reused across sessions.

**References:** BSI TR-02102-2, https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR02102/BSI-TR-02102-2.pdf

# etcd Exposure and Missing etcd Encryption

**MUST** restrict etcd (2379/2380) to control-plane peers and enable encryption at rest for all stored Secrets.

**Why:** etcd holds every secret in plaintext by default; a reachable or unencrypted datastore dumps the cluster's entire credential set.

**Detect:** etcd client port reachable off-node; kube-apiserver missing `--encryption-provider-config`; no EncryptionConfiguration resource.

**References:** CIS K8s 2.0, 3.2.1, CWE-311, NIST SP 800-190 5.2, K8s encryption-at-rest docs

# Explicit Cipher Transformation

**MUST** name the full cipher transformation, including algorithm, mode, and padding, at every call site, and reject provider defaults.

**Why:** Provider defaults have historically resolved to ECB or PKCS#1 v1.5, so the same call is safe or broken depending on the runtime and its version.

**Detect:** grep for transformation strings without a mode (Cipher.getInstance("AES")), for /ECB/, and for manual CBC built on a bare block cipher

**References:** Android Secure Coding Guide, https://www.jssec.org/dl/android_securecoding_en_20250827.pdf

# FIPS 140-3 Validated Crypto

**MUST** perform cryptographic operations for regulated data using FIPS 140-3 validated modules rather than unaudited library implementations.

**Why:** Hand-rolled or non-validated crypto looks fine until a subtle implementation flaw breaks confidentiality with no compliance defense.

**Detect:** grep for "fips", "FIPS_MODE", openssl fips provider config; direct MD5/SHA1 usage, custom crypto, non-validated TLS libraries in regulated paths.

**References:** FIPS 140-3, CMVP validated module list, NIST SP 800-175B

# FIPS 186 / Digital Signature Standards

**SHOULD** generate and verify digital signatures using approved algorithms (ECDSA, RSA per FIPS 186-5) with approved curves and key lengths only.

**Why:** Deprecated curves and short keys make signatures forgeable, undermining code signing, tokens, and non-repudiation guarantees.

**Detect:** grep for signature algorithm config: "RSA-1024", "DSA", "secp112", disabled curves; verify "P-256", "P-384", "RSA-2048+" in signing code.

**References:** FIPS 186-5, NIST SP 800-89

# Git-History Secret Remediation

**MUST** remediate a committed secret by rewriting history (filter-repo/BFG), rotating the credential, and notifying collaborators to re-clone — deleting the file in a new commit is NOT remediation.

**Why:** The secret remains fully recoverable from history after deletion; the rotation must cover the entire exposure window since the key was public from first push, not last commit.

**Detect:** on any discovered secret: verify history was rewritten (not just deleted-at-HEAD), credential rotated with expiry-before-exposure-window logic, forks/clones notified; judgment on incident record completeness.

**References:** GitHub secret removal guidance, git-filter-repo/BFG docs, credential-exposure incident practice

# Harvest-now-decrypt-later exposure of long-lived confidential data

**MUST** protect data whose confidentiality must outlast ~15 years (health records, identities, keys) with post-quantum or hybrid key agreement, since today's ciphertext can be stored and decrypted later and re-keying does not re-protect ciphertext already archived under the old key.

**Why:** Adversaries archive encrypted traffic and backups now, waiting for quantum or key-compromise advances to unlock them retroactively.

**Detect:** Long-retention archives encrypted only with RSA-2048/ECC, TLS sessions without hybrid KEM, backups with no key-rotation schedule.

**References:** NIST IR 8547, NSA CNSA 2.0 timeline, CISA post-quantum cryptography guidance

# Hash Output Sizing

**MUST** use the full digest wherever collision resistance is relied on, and document the property that justifies any truncation.

**Why:** The two properties cost differently, so sizing by habit either trusts a short digest where collisions matter or pays for resistance nobody needs.

**Detect:** grep for `sha1`, `md5`, and truncated digests (`digest()[:16]`, `substr($hash, 0, 16)`) in integrity or identifier code.

**References:** OWASP ASVS v5.0 V11.4.3, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md, NIST SP 800-107

# Hashing vs Encryption

**MUST NOT** store passwords with reversible encryption; use one-way password hashing, and reserve encryption only for data that legitimately needs recovery.

**Why:** Encrypted password stores can be decrypted when the key leaks, exposing every credential at once in plaintext form.

**Detect:** `AES`, `encrypt(` near `password` fields, `Fernet`, `cryptography.fernet` applied to user credentials, ORM column named `encrypted_password`.

**References:** OWASP Password Storage Cheat Sheet, CWE-257, NIST SP 800-63B §5.1.1.2

# Plaintext Secrets in Helm values Files and Rendered Manifests

**MUST NOT** commit plaintext secrets in `values.yaml` or render them into manifests; reference ExternalSecret/SealedSecret objects or inject at deploy time instead.

**Why:** Values files and `helm get values` output are readable by anyone with repo or release access, leaking credentials through charts and CI artifacts.

**Detect:** `password:`, `apiKey:`, `token:` literals in `values*.yaml`, `helm get values` output containing credentials, missing `existingSecret` references.

**References:** OWASP ASVS V6.4.1, CWE-312, Helm security best practices, Bitnami `existingSecret` pattern

# Insufficient Randomness for Tokens and IDs

**MUST** generate session tokens, password resets, API keys, and invite codes from a cryptographically secure RNG (`secrets`, `crypto.randomBytes`, `SecureRandom`), never `random`/`Math.random`/sequential IDs.

**Why:** Predictable randomness lets attackers guess reset links and session tokens, taking over accounts without ever touching the password.

**Detect:** `Math.random()`, Python `random.` for tokens, `uuid1`/sequential IDs in auth flows, `rand()` in token generation code.

**References:** OWASP ASVS V3.2.2, CWE-330, NIST SP 800-90A

# Integration Credential Sprawl

**SHOULD** centralize third-party SaaS credentials in a secrets manager with owner, scope, and expiry metadata — no credentials in shared docs, wikis, or personal accounts.

**Why:** SaaS credential sprawl (one per engineer, pasted in runbooks, never rotated) makes offboarding impossible to audit and breach blast radius unknowable.

**Detect:** inventory integration creds: count vs documented owners; grep wikis/runbooks/env files for SaaS API keys; check rotation history per integration; flag creds tied to individual employees.

**References:** NIST SP 800-53 IA-5, OWASP Secrets Management Cheat Sheet, vendor SSO/API-token best practices

# KDF Input Handling

**MUST NOT** pre-hash, truncate, or case-fold a password in a way that shrinks its verifier space before the key-derivation function.

**Why:** A fast unsalted pre-hash recreates pass-the-hash, and naive truncation silently shortens every password past the limit.

**Detect:** grep `password[:N]`, `substr(password`, `md5(password)`, `sha1(password)` inside the hashing helper, and client-side hashing before the request is sent.

**References:** OWASP Password Storage Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

# Key Holder Limits

**MUST** distribute each private key to a single holder and each shared secret to no more than two parties, listing every holder in the key policy.

**Why:** Each extra holder is a full copy of the key with no accounting, and for signing keys it also destroys any claim that one party produced the signature.

**Detect:** read the KMS key policy or secret distribution list and count principals per key.

**References:** OWASP ASVS v5.0 V11.1.1, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md, NIST SP 800-57 Part 1

# Key Lifecycle Recovery

**MUST** define backup, recovery, rotation, and destruction for every long-lived key, protecting the recovery path as strongly as the key.

**Why:** A weak recovery path is a backdoor, and no recovery path turns one lost key into permanent data loss.

**Detect:** key-store inspection (`aws kms get-key-rotation-status`, key policy, deletion window) — rotation enabled, escrow documented, and destruction requiring the same approvers as creation.

**References:** OWASP Key Management Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html

# Key Separation

**MUST** use distinct keys per purpose, environment, and tenant, keeping each key out of the store that holds its ciphertext.

**Why:** Reusing one key couples unrelated security domains, so a single leak spans all of them; co-located keys reduce encryption to obfuscation.

**Detect:** grep for one key identifier or alias used by both signing and encryption, the same key in staging and production configs, and key material in the same bucket, table, or repo as the ciphertext.

**References:** OWASP Key Management Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html

# Key Use Logging

**MUST** log every use of a key-management key with caller identity, operation, and target resource.

**Why:** Key use without an audit trail hides both misuse and the blast radius of a stolen credential. The log is the only record separating a legitimate decrypt from an exfiltration.

**Detect:** grep key-management client wrappers for audit emission on encrypt, decrypt, and sign calls; flag direct key-service calls that bypass the wrapper.

**References:** OWASP Proactive Controls C9, https://github.com/OWASP/www-project-proactive-controls, NIST SP 800-57 key management

# Credentials Out Of Model Context

**MUST** keep credentials out of model context entirely: the model selects a connector identifier and a trusted boundary injects the secret.

**Why:** A secret pasted into a prompt enters a data pipeline that persists it in history, logs, memory, and generated code, and prompt injection turns that disclosure into action.

**Detect:** grep prompts, system messages, and tool schemas for interpolated `api_key`, `token`, `Bearer `, `password`; confirm tool handlers resolve credentials from a vault server-side.

**References:** Vault-mediated credential execution for agents, https://arxiv.org/abs/2609.33371

# Negotiation Downgrade Protection

**MUST** reject a negotiation that omits a stronger mechanism both parties support instead of silently accepting the weaker option.

**Why:** A downgrade attack strips the strong option from the offer so the weaker path is chosen legitimately. If omission is accepted, the attacker never has to break the cryptography at all.

**Detect:** judgment: the negotiation code path and its test vectors — what the implementation does when the strong mechanism is removed from the peer's offer.

**References:** CWE-757 Selection of Less-Secure Algorithm During Negotiation

# No Custom Crypto

**MUST NOT** compose raw cryptographic primitives into a construction where a maintained high-level library provides it (AEAD, sealed box, password hashing, token format).

**Why:** Design errors in crypto are invisible to the designer and fatal in production; maintained libraries already bundle the correct modes and side-channel handling.

**Detect:** grep for hand-built constructions: encrypt-then-MAC assembled by hand, raw `AES`/`Cipher` calls with a separately computed MAC, non-standard token formats, base64 or hex treated as protection.

**References:** OWASP Cryptographic Storage Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html

# Non-Exportable Signing Keys

**MUST** keep code-signing, SSH, and package-publish credentials on hardware tokens so private key material cannot be exported and each use requires physical presence.

**Why:** A key file on disk, even passphrase-protected, is copyable by malware and one cracked passphrase away from full impersonation.

**Detect:** ssh-add -l lists only hardware-backed keys; any file-based signing key is a finding

**References:** Fystack Developer Security Handbook, https://github.com/fystack/developer-security-handbook

# Password Salting

**MUST** use a unique, cryptographically random salt per password hash, generated by the hashing library rather than a shared or static value.

**Why:** Identical or missing salts let attackers crack many accounts at once with rainbow tables and expose reused passwords across users.

**Detect:** Hardcoded `salt =` constants, `md5(password + SALT)`, bcrypt/argon2 calls without per-user salt handling, same hash for duplicate passwords in DB dumps.

**References:** OWASP Password Storage Cheat Sheet, CWE-759, NIST SP 800-63B §5.1.1.2

# Per-Instance Credentials

**MUST NOT** ship one static credential that every customer instance shares; issue per-instance or per-tenant credentials that can be revoked alone.

**Why:** A single credential extracted from one deployment then authenticates every other deployment, and revoking it breaks them all.

**Detect:** grep packaged config and installer defaults for one shared API key, service token, or database password repeated across environments and tenants.

**References:** OWASP Secrets Management Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

# Per-Message Signing

**MUST** sign individual messages in multi-hop high-value transactions so integrity survives every intermediary, not just each transport leg.

**Why:** Transport encryption ends at each hop, so a compromised or curious intermediary can alter a payment instruction that every leg delivered intact.

**Detect:** read the payment or approval flow and check whether the instruction carries a signature the final party verifies, or only hop-by-hop TLS.

**References:** OWASP ASVS v5.0 V4, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x13-V4-API-and-Web-Service.md, NIST SP 800-53 SC-8

# Pipeline-Orchestrator Credential Sprawl

**MUST** centralize credentials used by data orchestrators (Airflow connections, dbt profiles, Spark configs) in a secrets backend — not in DAG files, connections tables in plaintext, or CI env dumps.

**Why:** Orchestrators hold keys to every warehouse, bucket, and DB in the estate; their configs are broadly readable by data teams, making them the flattest credential attack surface in the company.

**Detect:** grep DAGs/profiles for inline passwords, check Airflow Connections backend (secrets env/backend vs metadata DB plaintext), review dbt `profiles.yml` handling, inspect Spark `--conf` for hardcoded AWS keys.

**References:** Airflow secrets-backend docs, dbt secure credentials guidance, OWASP Data Security

# Post-quantum cryptography migration plan and crypto-agility

**SHOULD** maintain a documented PQC migration plan and crypto-agile design (algorithm negotiation, centralized crypto config) so ciphers can be swapped without rewrites.

**Why:** Systems hard-coded to RSA/ECC today cannot absorb the eventual quantum break of current public-key crypto without costly emergency rework.

**Detect:** Hardcoded `RSA-2048`/`ECDH P-256` with no config indirection, absence of `ML-KEM`/`X25519` hybrid plans, TLS library pinned without upgrade path.

**References:** NIST FIPS 203/204/205, NIST IR 8547 PQC migration, NSA CNSA 2.0

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
ssl_conf_command Groups X25519MLKEM768:X25519:secp384r1;  # hybrid, OpenSSL 3.5+
```

**References:** NIST FIPS 203 (ML-KEM), NIST PQC migration white papers, Cloudflare PQC deployment reports, IETF TLS hybrid KEM RFCs

# Resumption Key Rotation

**MUST** rotate session-ticket and resumption keys on a short schedule and destroy retired keys, so a stolen key exposes only sessions since the last rotation.

**Why:** A long-lived ticket key silently voids forward secrecy: one key compromise decrypts every session it ever wrapped.

**Detect:** grep for ticket key material and rotation (`SessionTicketKey`, `ticket_keys`, `ssl_session_timeout`, `session_ticket` rotation job) and for a retention window on retired keys.

**References:** RFC 9325 §3.4, https://www.rfc-editor.org/rfc/rfc9325.html, NIST SP 800-57 Part 1

# RNG Output Validation

**MUST** confirm the random source stays secure under heavy demand and does not fall back to a non-cryptographic generator.

**Why:** Generators degrade under forking and pool exhaustion, and some produce keys that are factorable — the failure is in the output, not the call.

**Detect:** grep for fallback branches to `random`, `rand()`, or a `/dev/urandom` exhaustion handler, then load test the entropy path under concurrency.

**References:** OWASP ASVS v5.0 V11.5.2, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md, NIST SP 800-90A/B

# Scoped Internal CA Trust

**MUST** trust only the specific internal authority or certificate each peer actually uses, rather than a broad system trust store.

**Why:** Trusting every public CA for an internal hop lets any certificate holder impersonate the service, which is the whole point of a private deployment.

**Detect:** grep client config for `NODE_EXTRA_CA_CERTS` pointing at the system bundle, `ssl_ca_certs` with a shared bundle, or `InsecureSkipVerify`.

**References:** OWASP ASVS v5.0 V12, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x21-V12-Secure-Communication.md, CWE-295

# Secret Erasure on Failure

**MUST** keep secrets in dedicated buffers and wipe them on every exit path, including error and exception paths.

**Why:** Secrets left in memory survive in core dumps, swap and crash reports. Error paths are the ones nobody writes the cleanup for.

**Detect:** Key material held in ordinary strings or heap objects; missing `explicit_bzero`/`zeroize`/`memset_s` on the failure branch of a verification routine.

**References:** ANSSI secure C programming rules, https://messervices.cyber.gouv.fr/guides/regles-de-programmation-pour-le-developpement-securise-de-logiciels-en-langage-c

# Secret Memory Lifetime

**SHOULD** minimize how long secrets and decrypted key material live in process memory, wiping buffers as soon as they are no longer needed.

**Why:** A single memory-disclosure bug or core dump walks the heap and finds whatever the process forgot to wipe. Long-lived plaintext secrets turn a read primitive into credential theft.

**Detect:** grep for `mlock`, `explicit_bzero`, `memset_s`, `Zeroize`, or equivalent wipe calls on buffers holding keys; flag key material copied into long-lived objects, caches, or log statements.

**References:** Heartbleed, https://heartbleed.com/, CWE-316 Cleartext Storage of Sensitive Information in Memory

# Secret Scanning

**MUST** run automated secret scanning (gitleaks, trufflehog, GitHub push protection) on every commit and full-history scans before publishing any repository.

**Why:** Developers routinely commit live credentials under deadline pressure; without scanning, leaks ship silently to public or shared remotes — and a secret once committed stays in git history forever, so rotation is the only true fix and is often missed.

**Detect:** `.gitleaks.toml`, `.pre-commit-config.yaml` with gitleaks/trufflehog hooks that reject at commit/push time, absent GitHub `secret_scanning`/push-protection settings in org config.

**References:** OWASP ASVS V2.10.4, CWE-540, CWE-319, NIST SP 800-218 (SSDF), GitHub push protection docs

# Secret Validity Checking (verify leaked keys are live)

**SHOULD** validate whether a reported leaked credential is still active before closing the finding, and confirm revocation actually took effect at the provider.

**Why:** Treating every leak report as stale lets live keys keep working; conversely, assuming revocation worked without verification leaves access open.

**Detect:** No post-rotation validation step, `git leak` findings closed without provider-side revoke check, missing `aws sts get-caller-identity` / GitHub `/rate_limit` verification.

**References:** OWASP ASVS V2.10.4, GitHub secret scanning docs, AWS IAM key revocation runbooks

# Secrets in CI Logs

**MUST NOT** echo, print, or interpolate secrets into CI output; mask values via CI secret masking and avoid commands that dump environment variables.

**Why:** Build logs are widely readable — teammates, forked PRs, and third-party integrations can harvest tokens from a single verbose step.

**Detect:** `echo $SECRET`, `set -x` in steps handling credentials, `env`/`printenv` in pipelines, `export` of tokens without `::add-mask::`.

**References:** OWASP ASVS V7.1.1, CWE-532, CWE-214

# Secrets in Instance Launch Payloads

**MUST NOT** place credentials, tokens, or private keys in instance launch payloads — EC2 user-data, cloud-init scripts/templates, Azure `customData`, GCP startup-script metadata; grant scoped instance roles or fetch secrets from a secrets manager at boot instead.

**Why:** Launch payloads are readable through the same instance-metadata service attackers already target via SSRF (`curl http://169.254.169.254/latest/user-data`), are copied into AMIs and launch-template history, and persist in Terraform state and console screenshots — a credential placed there leaks through every one of those surfaces at once, long after the instance is gone.

**Detect:** grep user-data/cloud-init blocks for `AWS_SECRET_ACCESS_KEY`, `password=`, `token`, `-----BEGIN`, connection strings with credentials; Terraform `aws_instance.userdata` / `google_compute_instance.metadata.startup-script` containing literals rather than role names or secret-manager references; scanned AMI user-data for inherited secrets.

**References:** cloud-init sensitive-data guidance, AWS best practices for embedded credentials, aquasecurity/trivy-checks user-data secret rules

# Hardcoded API keys and secrets in mobile app binaries

**MUST NOT** embed API keys, tokens, or symmetric secrets in app source, assets, or compiled binaries; ship them via short-lived server-issued credentials instead.

**Why:** Anyone can decompile the shipped IPA/APK and extract embedded secrets, since client code is fully inspectable.

**Detect:** run `strings`/mobSF scan on the binary; grep repo for `apiKey =`, `secret`, `BEGIN PRIVATE KEY`, hardcoded `AIza`/`sk-` prefixes in source and Info.plist/assets.

**References:** OWASP MASVS-STORAGE-2, CWE-798, CWE-321, MAS Testing Guide Reverse Engineering

# Secrets Management

**MUST** source all secrets from a dedicated store (Vault, 1Password Connect, SOPS, cloud secret manager) rather than embedding them in images, repos, or plain ConfigMaps.

**Why:** Secrets baked into artifacts leak through registries, backups, and logs where they cannot be revoked cleanly.

**Detect:** `Secret` manifests with plaintext `data:`, `stringData:` without ESO/ExternalSecret, `secretKeyRef` absence alongside hardcoded tokens.

**References:** OWASP ASVS V2.10, CWE-259, NIST SP 800-57

# Secrets Not in Arguments

**MUST NOT** pass secrets as command-line arguments, where process listings, shell history, and crash reports expose them.

**Why:** Arguments are visible in `ps`, `/proc`, shell history, and crash dumps, and child processes inherit them. A secret on a command line is disclosed to every local user before the command finishes.

**Detect:** grep for `--password`, `--token`, `-p$`, `mysql -p...`, `curl -u user:pass`, and secret values interpolated into `subprocess`/`exec` argument lists.

**References:** OWASP Secrets Management Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html, CWE-214 Invocation of Process Using Visible Sensitive Information

# Secrets Rotation Automation (scheduled/triggered rotation without downtime)

**MUST** rotate secrets automatically on schedule and immediately on suspected exposure, without manual steps or downtime.

**Why:** A leaked static secret stays valid forever; automation shrinks the attacker's usable window to the rotation interval.

**Detect:** Grep `rotation_period_days`, Secrets Manager rotation lambdas, Vault `ttl`/`lease`, ExternalSecret `refreshInterval`; IAM policies lacking `MaxAge`/rotation alarms (90 days typical); providers without rotation hooks in CI.

**References:** NIST SP 800-57, NIST SP 800-53 IA-5, CIS Control 6, OWASP ASVS V2.10.4

# Security Bits Floor

**MUST** evaluate key strength in bits of security rather than nominal key length, and reject configurations below a documented floor.

**Why:** Nominal-size review passes combinations that are far below the intended strength: a short elliptic curve and a long RSA key are not comparable by length.

**Detect:** grep key configuration for `key_size`, RSA moduli under 3072 bits, and short curves; testssl.sh grade for negotiated strength.

**References:** OWASP ASVS v5.0 V11.2.3, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md, NIST SP 800-57 Part 1

# SSH Agent Forwarding Disabled

**MUST NOT** leave SSH agent forwarding enabled on bastion or jump hosts.

**Why:** Forwarding hands any compromised intermediate host the developer's identity, without that host ever touching the key.

**Detect:** grep for ForwardAgent yes, AllowAgentForwarding yes, and ssh -A in scripts and config

**References:** Fystack Developer Security Handbook, https://github.com/fystack/developer-security-handbook

# Stream Message Authentication

**MUST** authenticate and integrity-check each message on a continuous media or telemetry stream, not only the session handshake that opened it.

**Why:** Without per-message authentication an attacker on the path injects content silently, turning eavesdropping into media or command insertion.

**Detect:** grep media/signalling config for SRTP protection disabled or optional (`srtp-policy: optional`, `use_srtp` unset, DTLS-SRTP off) and for RTP sources accepted without an auth tag check.

**References:** OWASP ASVS v5.0 V17.2.3, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x26-V17-WebRTC.md, RFC 3711 (SRTP)

# Infrastructure-as-code state kept out of repositories and encrypted at rest

**MUST NOT** commit infrastructure-as-code state to a repository or keep it on an unencrypted disk; use a remote backend with encryption at rest and state locking, and mark secret-bearing variables and outputs `sensitive` so plan output, CI logs, and pull requests cannot echo them. Terraform's `terraform.tfstate` and `terraform output` are the common case; any IaC tool's state artifact is the same class of secret-bearing file.

**Why:** State files and plan artifacts record every resource attribute in plaintext — secrets, resource IDs, network topology — so a leaked backend, backup, or CI log hands over all managed credentials at once.

**Detect:** grep tracked files for `terraform.tfstate`, `*.tfstate.backup`; check the backend block for `backend "s3"` with `encrypt = true` and DynamoDB locking; scan variables and outputs for missing `sensitive = true` and CI steps that print `terraform output`/`terraform plan` unmasked.

**References:** CIS Terraform 1.2/1.3, OWASP Secrets Management, CWE-312, HashiCorp backend security docs

# Unique Nonces

**MUST** generate a fresh nonce or IV for every encryption under a key, and treat AEAD nonce reuse as a release blocker.

**Why:** Nonce reuse under counter-mode AEAD leaks the authentication key, so one repeated nonce breaks every message under that key.

**Detect:** grep fixed or reused IV/nonce material: `iv = b'\x00'`, `nonce = 0`, a module-level `IV` constant, `Random.new(1)` seeds, and counters reset per process.

**References:** OWASP Cryptographic Storage Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html

# UUIDs Are Not Secrets

**MUST NOT** use time-ordered or MAC-derived identifiers (UUIDv1, UUIDv7, ULID) as unguessable tokens or secret material.

**Why:** Time-ordered identifiers disclose their creation instant and host, and their structure shrinks the search space a capability token must make infeasible.

**Detect:** grep token, reset, and API-key generation for `uuid1`, `uuid7`, `ulid`, and `uuid4()` where the value is used as a capability.

**References:** OWASP ASVS v5.0 V11.5.1, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md, CWE-330

# Weak Crypto Primitives in Application Code

**MUST NOT** use DES, RC4, MD5, SHA-1, ECB mode, or hand-rolled ciphers in application code; standardize on AES-GCM or ChaCha20-Poly1305 via maintained libraries.

**Why:** Broken primitives are publicly broken — collisions, key recovery, and pattern leakage turn "encrypted" data into readable data.

**Detect:** `DES`, `RC4`, `ECB`, `md5(`, `sha1(` in security paths, `Cipher.getInstance("DES")`, custom XOR/"encryption" functions.

**References:** OWASP Cryptographic Storage Cheat Sheet, CWE-327, NIST SP 800-131A

