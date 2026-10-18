# cloud-network — full checklist (59 items)

Cloud networking, DNS, edge, cloud resource exposure.

> Generated artifact. Canonical source: `issues/<slug>.md`.

# TLS Certificate Expiry

**MUST** Every TLS certificate serving traffic be renewed automatically before expiry, with alerting firing at least 30 days ahead of the notAfter date.

**Why:** An expired certificate breaks every HTTPS session and trains users to click through warnings; silent renewal failures routinely surface only as a customer-visible outage.

**Detect:** Check dates with `openssl s_client -servername <host> -connect <host>:443`. Flag cert-manager Certificates stuck NotReady, and hardcoded `ssl_certificate` paths in nginx/HAProxy with no renewal hook.

**Bad:**
```yaml
# nginx.conf — hand-issued cert, nobody owns renewal
server {
    listen 443 ssl;
    ssl_certificate /etc/ssl/manual-2024.pem;
}
```

**Good:**
```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
spec:
  secretName: app-tls
  renewBefore: 720h   # 30 days
  issuerRef: { name: letsencrypt-prod }
```

**References:** CWE-298, OWASP A05:2021 Security Misconfiguration, Let's Encrypt renewal docs

# HSTS

**SHOULD** Every HTTPS response carry a `Strict-Transport-Security` header with a max-age of at least one year, plus `includeSubDomains` on apex domains.

**Why:** Without HSTS, a single HTTP request or an SSL-stripping proxy can downgrade a connection; the header pins browsers to TLS so later visits can't be intercepted in plaintext.

**Detect:** Grep server and framework configs for `Strict-Transport-Security` and verify `max-age=31536000` or higher. Watch for nginx `add_header` directives in nested locations silently overriding each other.

**Bad:**
```nginx
server {
    listen 443 ssl;
    # no HSTS header at all
    location / { proxy_pass http://app; }
}
```

**Good:**
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

**References:** RFC 6797, CWE-319, OWASP A02:2021 Cryptographic Failures, OWASP WSTG-401-14

# DNS

**MUST NOT** Any security decision rely on DNS names or reverse DNS without validation, and resolvers in use be explicitly configured rather than inherited from DHCP.

**Why:** DNS is spoofable at the resolver, cache, and host-file level; trusting `*.internal` names or PTR records for authentication lets an attacker with resolver access impersonate services.

**Detect:** Inspect `/etc/resolv.conf` and container base images for unset or DHCP-supplied nameservers. Grep code for `gethostbyaddr` or auth checks keyed on hostname strings; review CoreDNS upstream forwarders.

**Bad:**
```python
if request.remote_addr.resolve_ptr().endswith(".internal.corp"):
    grant_admin(request)   # spoofable via PTR control
```

**Good:**
```python
# authenticate by certificate identity, never by name
if client_cert.subject == expected_service_identity:
    grant_admin(request)
```

**References:** CWE-350 (Reliance on Reverse DNS), OWASP A08:2021, RFC 1034

# DNS Propagation

**SHOULD** Lower record TTLs to 300 seconds or less well before a planned cutover, and keep them low until the migration is confirmed stable.

**Why:** Stale caches holding the old IP keep sending users to a decommissioned endpoint; that endpoint may be released, re-IP'd, or claimed by someone else, producing silent traffic loss or a takeover window.

**Detect:** Look for a TTL-lowering step in the change plan ahead of the cutover date. Query `dig +noall +answer SOA <zone>` for current TTLs; flag runbooks that flip records without waiting out the old TTL.

**Bad:**
```bash
# cutover now while old records are cached for 24h
dig A old.app.example.com          # ttl = 86400
```

**Good:**
```bash
# 48h before cutover: TTL 86400 -> 300, wait it out, then flip
dig +short A app.example.com @8.8.8.8   # verify resolvers agree
```

**References:** RFC 2181, AWS Route 53 failover/TTL guidance, Google Cloud DNS caching docs

# Egress Fees

**SHOULD** Cross-AZ and internet-bound data paths be designed with egress cost in mind, and high-volume cross-zone chatter be treated as an architecture smell.

**Why:** Egress and NAT data-processing charges are a classic surprise line item; a chatty service pinned to the wrong AZ can multiply a bill without any security or capacity alarm firing.

**Detect:** Grep configs for AZ-specific endpoints (`us-east-1a`) instead of regional ones. Look for S3/SQS/DB calls over public endpoints rather than gateway endpoints. Review NAT gateway "Data Processed" metrics for top talkers.

**Bad:**
```python
# worker in us-east-1a hitting the public S3 endpoint across AZs
s3 = boto3.client("s3", endpoint_url="https://s3.amazonaws.com")
```

**Good:**
```python
# regional endpoint + S3 gateway endpoint keeps traffic on the AWS backbone
s3 = boto3.client("s3", region_name="us-east-1")
```

**References:** AWS Well-Architected Cost Optimization pillar, AWS NAT gateway pricing, GCP network egress pricing

# VPCs

**MUST** Workloads of different trust levels live in separate VPCs or equivalent network boundaries, with explicit, audited peering rather than one flat network.

**Why:** A single VPC holding production, staging, and third-party integrations means one compromised host can laterally scan everything; the blast radius equals the entire address space.

**Detect:** Map VPCs and CIDR allocations; flag one VPC mixing prod with dev/staging. Review peering for transitive-routing hacks, `0.0.0.0/0` routes into peering connections, and missing flow logs.

**Bad:**
```hcl
# one VPC for everything: prod, staging, vendor VPN
resource "aws_vpc" "everything" { cidr_block = "10.0.0.0/8" }
```

**Good:**
```hcl
resource "aws_vpc" "prod"    { cidr_block = "10.10.0.0/16" }
resource "aws_vpc" "staging" { cidr_block = "10.20.0.0/16" }
# peering only where required, flow logs on
```

**References:** AWS VPC Peering FAQ, AWS Well-Architected Security pillar, CIS AWS Foundations 1.x

# Subnets

**MUST NOT** Stateful application servers or databases sit in subnets that auto-assign public IPs; only load balancers, NAT gateways, and bastions belong in public subnets.

**Why:** A compute instance with a routable public address is directly exposed to internet-wide scanning, bypasses the load balancer's WAF and TLS termination, and becomes the easiest lateral entry point.

**Detect:** In Terraform/CloudFormation check `map_public_ip_on_launch = true` on non-edge subnets and `associate_public_ip_address` in launch templates. Verify app/DB subnets have no IGW route.

**Bad:**
```hcl
resource "aws_subnet" "app" {
  map_public_ip_on_launch = true   # every app pod internet-reachable
  route_table_id          = aws_route_table.igw.id
}
```

**Good:**
```hcl
resource "aws_subnet" "app_private" {
  map_public_ip_on_launch = false
  route_table_id = aws_route_table.nat_only.id  # no IGW route
}
```

**References:** CIS AWS Foundations 1.x, AWS VPC best practices, CWE-284

# NAT Gateways

**SHOULD** Outbound traffic from private subnets traverse a managed NAT gateway deployed one-per-AZ, and long-lived NAT instances with static EIPs be eliminated.

**Why:** A NAT instance is an ordinary VM: if compromised, the attacker inherits a trusted outbound path for exfiltration and C2, and one shared NAT turns a zonal failure into a region-wide egress outage.

**Detect:** Search IaC for `aws_instance` with `source_dest_check = false` — the DIY-NAT tell. Compare NAT gateway count against AZ count, and flag egress `0.0.0.0/0` where a filtering proxy is expected.

**Bad:**
```hcl
resource "aws_instance" "nat" {
  source_dest_check = false        # DIY NAT on a patchable VM
  associate_public_ip_address = true
}
```

**Good:**
```hcl
resource "aws_nat_gateway" "az_a" {
  allocation_id = aws_eip.nat_a.id
  subnet_id     = var.edge_subnet_a
}   # one per AZ; private route tables use their local NAT
```

**References:** AWS NAT gateway best practices, CIS AWS Foundations 2.x, AWS Well-Architected Reliability pillar

# Firewalls

**MUST** Default to deny for all inbound traffic, explicitly allowing only the ports and sources a service actually needs, with rules managed as code rather than clicked in a console.

**Why:** Rules added "temporarily" during incidents accumulate into a wide-open perimeter; a firewall whose real policy is unknown to anyone is not a control, and console-only changes leave no review trail.

**Detect:** Enumerate rulesets for `any`/`0.0.0.0/0` sources on management ports (22, 3389, 5432, 27017, 6379). Diff running state against committed config to catch console drift and ownerless rules.

**Bad:**
```
# "temporary" rule, now permanent
allow from 0.0.0.0/0 to port 22   # SSH open to the world
```

**Good:**
```
allow from 10.20.0.0/16 (ops-vpn) to port 22
deny  from any to any               # explicit default deny, logged
```

**References:** CWE-284, CIS Benchmark network rules sections, NIST SP 500-207 Zero Trust Architecture

# Security Groups

**MUST NOT** A security group admit `0.0.0.0/0` or `::/0` on administrative or data ports; prefer referencing other security groups over raw CIDR ranges.

**Why:** SGs are the de facto perimeter for every instance in a VPC, and one wide-open rule on Redis, Postgres, or SSH is internet-scanned within hours — ransomware entry points start exactly like this.

**Detect:** Grep Terraform for `cidr_blocks = ["0.0.0.0/0"]` in `ingress` blocks, especially paired with ports 22/3389/5432/3306/6379/27017. Flag blanket self-referencing groups and unused groups with unclear ownership.

**Bad:**
```hcl
ingress { from_port = 5432 to_port = 5432 protocol = "tcp"
         cidr_blocks = ["0.0.0.0/0"] }
```

**Good:**
```hcl
ingress { from_port = 5432 to_port = 5432 protocol = "tcp"
         security_groups = [aws_security_group.app.id] }  # SG-to-SG
```

**References:** CIS AWS Foundations 5.x, CWE-284, AWS VPC security group best practices

# Service Mesh

**SHOULD** Where a service mesh is deployed, enforce mutual TLS in STRICT mode between sidecars and remove plaintext permissive fallbacks before production sign-off.

**Why:** A mesh left in PERMISSIVE mode still accepts plaintext, so encryption becomes optional and identity unauthenticated — an attacker inside the cluster can impersonate any service, and the mesh's own telemetry records the impostor.

**Detect:** Check Istio `PeerAuthentication`/`DestinationRule` for `mtls.mode: STRICT` versus `PERMISSIVE`/`DISABLED`. Look for namespace-wide exemptions and `excludeOutboundPorts` annotations smuggling traffic around the mesh.

**Bad:**
```yaml
kind: PeerAuthentication
spec: { mtls: { mode: PERMISSIVE } }   # plaintext still accepted
```

**Good:**
```yaml
spec:
  mtls: { mode: STRICT }
  selector: { matchLabels: { app: payments } }
```

**References:** Istio mTLS docs, NIST SP 800-207 Zero Trust, CNCF zero-trust whitepaper

# Ingress Controllers

**MUST** Treat the ingress controller as a high-value attack surface: run it least-privileged, patch on the vendor's security cadence, and never expose admin or metrics ports publicly.

**Why:** Ingress controllers parse attacker-controlled headers and hostnames at the edge; annotation-injection CVEs in NGINX Ingress have yielded cluster-admin, so broad RBAC plus a wildcard host turns one bug into total cluster compromise.

**Detect:** Review the controller's ClusterRole for wildcards and secret-read access. Grep Ingress resources for `server-snippet`/`configuration-snippet` annotations accepted from untrusted namespaces; check for `host: "*"` catch-alls and exposed `:10254` metrics.

**Bad:**
```yaml
# any namespace can inject arbitrary nginx config via annotation
metadata:
  annotations:
    "nginx.ingress.kubernetes.io/server-snippet": "..."
```

**Good:**
```yaml
# controller args: snippets disabled, annotation allowlist enforced,
# --watch-namespace scoped, metrics cluster-internal only
```

**References:** CVE-2021-25742, OWASP A03:2021 Injection, Kubernetes ingress security docs

# Public S3 Buckets

**MUST NOT** Any bucket holding application data, backups, or user content be publicly readable or writable; Block Public Access must be on at account and bucket level.

**Why:** Misconfigured ACLs and `Principal: "*"` policies are the most common cause of large-scale data leaks — and write-enabled buckets allow malware hosting or ransom via object overwrite.

**Detect:** Grep IaC for `acl = "public-read"` and `"Principal": "*"` with `s3:GetObject`/`PutObject`. Run `aws s3api get-public-access-block` per bucket; scan with Prowler or s3scanner. Watch for policies widening `Resource` beyond the intended prefix.

**Bad:**
```json
{ "Effect": "Allow", "Principal": "*", "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::prod-backups/*" }
```

**Good:**
```hcl
resource "aws_s3_bucket_public_access_block" "backups" {
  bucket = aws_s3_bucket.backups.id
  block_public_acls = true   ignore_public_acls = true
  block_public_policy = true restrict_public_buckets = true
}
```

**References:** CWE-284, CIS AWS Foundations 2.1.5, OWASP A01:2021 Broken Access Control, AWS S3 security best practices

# Presigned URLs

**SHOULD** Presigned URLs carry the shortest expiry the user journey tolerates — minutes, not days — and MUST NOT be generated for destructive or administrative operations.

**Why:** A presigned URL is a bearer credential: anyone holding it bypasses IAM entirely, and links pasted into chats, logs, and Referer headers keep working long after the session ends.

**Detect:** Grep for `generate_presigned_url`, `sign_url`, `X-Amz-Expires` and audit the expiry values — anything above 15 minutes needs justification. Check whether logs record full signed URLs, and whether any flow presigns `DeleteObject`/`PutObject`.

**Bad:**
```python
url = s3.generate_presigned_url("get_object",
        Params={"Bucket": b, "Key": k}, ExpiresIn=60*60*24*7)  # 7 days
```

**Good:**
```python
url = s3.generate_presigned_url("get_object",
        Params={"Bucket": b, "Key": k}, ExpiresIn=300)  # 5 minutes
```

**References:** AWS S3 presigned URL best practices, CWE-539, OWASP A07:2021

# Cloud Billing Alerts

**MUST** Budget alarms exist at account and per-project level, wired to a channel someone actually reads, with thresholds low enough to catch a runaway resource before it becomes a five-figure month.

**Why:** Compromised keys, crypto-mining spin-ups, and retry-storm Lambda loops all manifest first as a billing spike; teams without alarms discover them at invoice time, weeks after the abuse started.

**Detect:** Check IaC for AWS Budgets / GCP Budget Alerts / Azure Cost Management exports — absence is the finding. Verify recipients are distribution lists, not one departing engineer, and that daily-velocity checks exist alongside monthly totals.

**Bad:**
```
# no budgets defined; first signal is the month-end invoice: $41,000
```

**Good:**
```hcl
resource "aws_budgets_budget" "acct" {
  budget_limit { amount = 2000 cost_types { include_tax = true } }
  notification_type { threshold = 500 comparison_operator = "GREATER_THAN"
    subscriber_info { subscription_type = "EMAIL" address = "ops-alerts@corp" } }
}
```

**References:** AWS Budgets docs, GCP Budget alerts, CIS AWS Foundations 4.x, OWASP A09:2021 Logging & Monitoring Failures

# Subdomain Takeover / Dangling DNS

**MUST NOT** Any DNS record remain pointing at a deprovisioned cloud resource — S3 bucket, Heroku app, CloudFront distribution — after that resource is released.

**Why:** A CNAME to a vacant target is a claim ticket: an attacker registers it under their own account and instantly serves arbitrary content, sets cookies, and harvests credentials on your trusted domain.

**Detect:** Enumerate A/CNAME records and probe targets for "not found" signatures: `NoSuchBucket`, Heroku "No such app", GitHub Pages 404. Diff DNS against live provisioned resources in CI; flag records for retired campaigns and expired vendor trials.

**Bad:**
```
marketing.example.com.  CNAME  old-campaign.s3-website-us-east-1.amazonaws.com
# bucket deleted; attacker creates it and pages on your domain
```

**Good:**
```
# CI check: every CNAME target must exist and be org-owned,
# or the record fails the pipeline and gets removed
```

**References:** OWASP WSTG-CONF-10 (Subdomain Takeover), HackerOne takeover methodology, Can-I-Takeover-it project

# mTLS / Service-to-Service Authentication

**SHOULD** Internal service-to-service calls authenticate with short-lived client certificates rather than shared API keys or network-location trust.

**Why:** "It's inside the VPC so it's fine" collapses the moment one workload is compromised: shared keys leak in env files and logs and identify no caller, while per-workload certs give cryptographic identity that expires before reuse.

**Detect:** Look for SPIFFE/SPIRE or cert-manager `Certificate` with `usages: [client auth]`. Grep for peers authenticated only by IP allowlist or a fleet-wide `INTERNAL_API_KEY`. Check cert lifetimes (hours, not years) and automated rotation. Mesh-enforced mTLS counts as satisfying this: check `mtls.mode: STRICT`, `PeerAuthentication`, `security.istio.io` annotations, Linkerd/Consul `tls: ENABLE` policy manifests.

**Bad:**
```python
# one key for every caller, checked by every callee
if request.headers["X-Internal-Key"] == env("INTERNAL_API_KEY"): ok()
```

**Good:**
```python
peer = verify_client_cert(request, ca=trust_bundle)   # SPIFFE ID per workload
if peer.spiffe_id in allowed_callers[endpoint]: ok()
```

**References:** SPIFFE/SPIRE docs, NIST SP 800-207 Zero Trust, Istio identity & certificate docs, CIS Kubernetes Benchmark 5.x

# DNSSEC

**SHOULD** Authoritative zones sign their records with DNSSEC, security-sensitive lookups use validating resolvers, and key rollover be automated and monitored.

**Why:** Unsigned DNS answers are forgeable by an on-path attacker or a compromised upstream resolver, silently redirecting users and services; DNSSEC makes forged answers cryptographically detectable.

**Detect:** Run `dig +dnssec <zone>` and check for `RRSIG` and the `AD` flag; verify the DS record exists in the parent. Watch for unmanaged KSK/ZSK rollover calendars — expired signatures break resolution as surely as an attack.

**Bad:**
```
$ dig example.com +dnssec     # no RRSIG, AD flag absent — unsigned zone
```

**Good:**
```
$ dig example.com +dnssec     # RRSIG present, AD set, DS in parent
# KSK rollover automated via registrar API with expiry alerts
```

**References:** RFC 4033/4034, RFC 6781 (key rollover), Cloudflare DNSSEC docs

# IPv6

**MUST NOT** IPv6 be enabled on an interface or load balancer without the same firewall coverage applied to IPv4; every rule set needs a `::/0` exposure review.

**Why:** IPv6 is often enabled by default or by an OS upgrade while firewall tooling manages only IPv4, leaving a fully routable, unfiltered second path into every host — and IPv4-only audits can't see it.

**Detect:** Audit security groups and host firewalls for IPv6 separately; flag `::/0` ingress on non-edge ports. Check `ip -6 addr` and SLAAC/Accept-RA settings on server subnets; verify WAF and logging actually bind the v6 listener.

**Bad:**
```bash
# IPv4 firewalled, IPv6 autoconfigured and wide open
ip6tables -L   # policy ACCEPT on everything
```

**Good:**
```bash
# same default-deny posture on both families, one policy source
ip6tables -P INPUT DROP
ip6tables -A INPUT -p tcp --dport 443 -j ACCEPT
```

**References:** CIS Benchmarks dual-stack sections, AWS IPv6 security group guidance, NIST SP 500-267r1

# CIS Benchmarks (OS/container/k8s/cloud)

**MUST** Every OS image, container base, Kubernetes cluster, and cloud account be baselined against the applicable CIS Benchmark, with deviations recorded as explicit, time-boxed exceptions rather than silent drift.

**Why:** CIS Benchmarks encode thousands of reviewed hardening decisions; skipping them means rediscovering — as a breach — the weak SSH config or unlogged audit trail that was already solved and documented.

**Detect:** Run `kube-bench`, `lynis`, or ScoutSuite and diff against a documented exception list. Check CI for a benchmark stage on built images; flag exceptions with no owner or expiry date.

**Bad:**
```
# "we hardened it last year" — no automated check, drift unknown
```

**Good:**
```yaml
# CI job on every image build + weekly cluster scan
- run: kube-bench --json | jq '[.NodeResults[].Tests[] | select(.failures>0)]'
# failures fail the build unless matched to a registered exception
```

**References:** CIS Benchmarks (cisecurity.org), CIS Kubernetes Benchmark, CIS Docker Benchmark, DISA STIGs

# TLS/ Cipher Suite Hardening (Mozilla profiles, disable legacy)

**MUST** Terminating endpoints offer only modern suites per the Mozilla Intermediate (or Modern) profile, and MUST NOT negotiate RC4, 3DES, SHA-1 MACs, export, or anonymous suites.

**Why:** Legacy ciphers carry known breaks — Sweet32 against 3DES, Lucky13 against CBC, total break of RC4 — so one enabled weak suite lets an on-path attacker force the connection down to a level they can decrypt.

**Detect:** Probe with `nmap --script ssl-enum-ciphers -p 443 host` or SSL Labs. Grep nginx `ssl_ciphers`, Java `jdk.tls.disabledAlgorithms`, and LB security policies for `RC4`, `3DES`, `MD5`, `NULL`. Verify TLS 1.2+ with AEAD preference.

**Bad:**
```nginx
ssl_ciphers "ALL:eNULL:RC4:3DES:+HIGH";   # everything and the kitchen sink
```

**Good:**
```nginx
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-ECDSA-CHACHA20-POLY1305;
ssl_protocols TLSv1.2 TLSv1.3;
```

**References:** Mozilla Server-Side TLS (Intermediate profile), RFC 8446, CWE-326 Inadequate Encryption Strength

# Cloud Provider Security Benchmarks (AWS Foundations / Azure / GCP CIS)

**SHOULD** The provider's own framework — AWS Foundational Security Best Practices, Azure Secure Score, GCP CIS recommendations — be continuously evaluated in the native tool rather than spot-checked by hand.

**Why:** Provider frameworks catch platform-specific misconfigurations generic hardening misses: live root keys, audit logging off, IAM users with `*:*`, unencrypted snapshots — each a documented incident pattern.

**Detect:** Confirm Security Hub standards / Defender for Cloud cover every account and subscription, not just the primary one. Check for findings aged past 30 days with no owner and member accounts silently excluded from the aggregator.

**Bad:**
```
# Security Hub enabled in one region of one account; 14 others unmonitored
```

**Good:**
```hcl
# org-wide aggregation: standards enabled per member account via StackSets,
# findings exported to SIEM with an SLA on high severity
```

**References:** AWS Foundational Security Best Practices standard, CIS AWS Foundations Benchmark, Microsoft Defender for Cloud, GCP Security Command Center

# Cost Optimization & Cost Alerting (unit-economics tracking, budget alarms, anomaly detection)

**SHOULD** Track unit economics — cost per request, per user, per pipeline run — alongside raw spend, and enable native anomaly detection so a cost surprise pages someone before the invoice does.

**Why:** Aggregate budgets miss slow-burn regressions like an N+1 query tripling per-request cost, and anomaly detection is often the first visible signal of credential abuse mining compute.

**Detect:** Check for Cost Anomaly Detection subscriptions and velocity-based thresholds. Flag teams tracking only monthly totals. Scan cost-explorer exports for idle resources: unattached EBS volumes, idle NAT gateways, oversized node pools.

**Bad:**
```
# one monthly total budget alarm at 100%; regressions invisible until overrun
```

**Good:**
```
# weekly cost/1k-requests trend + anomaly detection (daily, $50 threshold)
# routed to the owning team's channel, not just finance
```

**References:** AWS Cost Anomaly Detection docs, AWS Well-Architected Cost Optimization pillar, FinOps Framework (finops.org)

# HTTP Request Smuggling (CL.TE / TE.CL Desync)

**MUST** Front-end and back-end agree on one framing per request: reject requests carrying both `Content-Length` and `Transfer-Encoding`, and disable lenient chunked parsing downstream.

**Why:** When proxy and server disagree on where a request ends, an attacker smuggles a second request inside the first — hijacking someone else's credentials on the shared connection and poisoning caches with attacker-controlled responses.

**Detect:** Test the full proxy chain with the `http-request-smuggler` tool. Grep for proxies forwarding raw `Transfer-Encoding` to frameworks that also honor `Content-Length`; flag hops running different HTTP parser versions, and keepalive between desync-prone tiers.

**Bad:**
```
POST / HTTP/1.1
Content-Length: 13
Transfer-Encoding: chunked   # front-end trusts TE, back-end trusts CL

0

GET /admin HTTP/1.1         # smuggled request runs on the back-end
```

**Good:**
```nginx
# front-end rejects ambiguous framing before any parser sees it
if ($http_transfer_encoding) { return 400; }
proxy_set_header Transfer-Encoding "";   # normalize, never pass through raw
```

**References:** CWE-444, PortSwigger HTTP desync research, RFC 9112 §6.3 (reject both headers)

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

# Cloud Instance Metadata Endpoint Protection (IMDSv2)

**MUST** require session-token (IMDSv2) mode on every EC2-style instance and container host, with a hop limit of 1–2, so that simple single-request SSRF cannot read credentials.

**Why:** The original v1 metadata service answers any GET from the link-local address; an SSRF in user-facing code can then exfiltrate the instance's IAM role credentials in one request.

**Detect:** Review `aws ec2 modify-instance-metadata-options` settings, launch templates/user-data for `HttpTokens=required` and `HttpPutResponseHopLimit`, EKS nodegroup configs, and any Terraform `metadata_options` blocks left at defaults or `optional`.

**Bad:**
```hcl
metadata_options {
  http_tokens = "optional"   # v1 still reachable by plain GET SSRF
}
```

**Good:**
```hcl
metadata_options {
  http_tokens                 = "required"
  http_put_response_hop_limit = 1
}
```

**References:** AWS Security Bulletin IMPDS-2019-001, AWS Security Best Practices (SCA) SEC2-BP07, CIS AWS 5.6

# Cloud IAM Privilege Escalation Paths

**MUST** trace every newly granted cloud permission for escalation edges before merge: actions that let a principal widen its own access.

**Why:** One overlooked `PassRole` or `AttachPolicy` grant turns a low-privilege service account into an administrator-in-waiting — the most common path from foothold to full account takeover. Escalation rarely arrives as one obvious admin grant; it hides in combinations (PassRole plus a role that trusts you, or a wildcard that later resolves to a new powerful action), so the diff must be judged against what the principal already holds.

**Detect:** In IAM JSON and IaC, look for `iam:PassRole`, `iam:AttachUserPolicy`, `iam:CreateAccessKey`, `iam:UpdateLoginProfile`, GCP `setIamPolicy`, and bindings referencing wildcards; check whether managed-policy attachments or GCP folder/organization inheritance silently widen the effective set, and whether any `NotAction` or `Resource: "*"` will be inherited by future service launches. Tools: Cloudsplaining, PMapper, IAM Access Analyzer — diff the reachable-permissions graph before/after the change.

**Bad:**
```json
{"Effect": "Allow", "Action": ["iam:AttachRolePolicy", "iam:PassRole"], "Resource": "*"}
```

**Good:**
```json
{"Effect": "Allow", "Action": "iam:PassRole",
 "Resource": "arn:aws:iam::111122223333:role/deploy-app",
 "Condition": {"StringEquals": {"iam:PassedToService": "lambda.amazonaws.com"}}}
```

**References:** CWE-269, MITRE ATT&CK T1548.005, Cloudsplaining, AWS IAM Security Best Practices, GCP Policy Analyzer

# DNS Rebinding Against Internal Services

**SHOULD** validate `Host`/`Origin` headers and pin DNS resolution at connect time, so a fetch cannot be re-pointed from a public name to a private IP between lookups.

**Why:** A short-TTL record that flips from the attacker's server to `127.0.0.1` smuggles client requests past filters that only checked the name once — a classic route to admin panels and metadata services.

**Detect:** Handlers trusting `Host` for routing; SSRF allowlists validating DNS once instead of at connect; missing `Origin` checks on state-changing endpoints reachable from browsers. Test with a rebinding service like `rbndr.us`.

**Bad:**
```python
if urlparse(url).hostname.endswith(".example.com"):
    fetch(url)   # second lookup may now return 127.0.0.1
```

**Good:**
```python
ip = ipaddress.ip_address(socket.gethostbyname(host))
if not (ip.is_private or ip.is_loopback or ip.is_link_local):
    fetch(pinned_ip_url)   # connect vetted IP, keep SNI/Host pinned
```

**References:** CWE-350, OWASP SSRF Prevention Cheat Sheet, OWASP A10:2021

# Cloud Metadata Endpoint Credential Theft (IMDS / 169.254.169.254)

**MUST** treat the link-metadata range (`169.254.169.254/32`, GCE `metadata.google.internal`, Azure `169.254.169.254/metadata`) as hostile territory: block it at the network layer from any workload that processes user-supplied URLs.

**Why:** Reaching the metadata service from a compromised or SSRF-able workload hands the attacker the node's IAM credentials verbatim — no exploitation needed, just a GET — and any single missing layer in the chain (v1-tolerant instance, open egress, string-only URL filter) completes the attack.

**Detect:** In SSRF filters, confirm the blocklist covers link-local, loopback, and cloud-specific IPs and is applied after DNS resolution, not on the raw string; test filters with decimal (`2852039166`), IPv6-mapped, and DNS-rebind forms. Check Kubernetes `hostAliases`, egress NetworkPolicies denying `169.254.169.254`, iptables/ip sets on nodes, container `hostNetwork` settings that sidestep pod-level blocks, and proxy configurations that allow CONNECT to it. On instances, verify `HttpTokens=required` plus `HttpPutResponseHopLimit=1` on launch templates. Search code for hardcoded `169.254.169.254` outside legitimate credential-fetching libraries.

**Bad:**
```python
url = user_input
if "localhost" not in url:      # trivially bypassed by decimal/hex IP forms
    requests.get(url)
```

**Good:**
```
# egress deny at the pod network boundary
ipset -A blacklist 169.254.169.254
iptables -A FORWARD -m set --match-set blacklist dst -j DROP
```

**References:** CWE-200, AWS IMDSv2 bulletin, GCP metadata protection docs, OWASP SSRF Prevention Cheat Sheet, CIS AWS 5.6/5.7

# Workload Identity / IRSA Audience and Claim Validation Gaps

**MUST** validate the audience (`aud`) and issuer (`iss`) claims on every federated workload token and scope each identity to the single service it is meant to reach.

**Why:** If a token minted for service A is accepted by service B without audience checks, any workload holding the weaker token can impersonate the stronger one — cross-service confusion that bypasses IAM entirely.

**Detect:** In STS `AssumeRoleWithWebIdentity` trust policies, check `Condition.StringEquals` on `token.actions.githubusercontent.com:aud` and `:sub` (repo + ref, not just `repo:*`). For SPIFFE/IRSA reviews, look for trust policies matching only the issuer URL with no audience or subject constraints, and app code that skips `aud` verification in JWT libraries (`verify_aud=False`).

**Bad:**
```json
"Condition": {"StringEquals": {
  "token.actions.githubusercontent.com:iss": "https://token.actions.githubusercontent.com"}}
```

**Good:**
```json
"Condition": {"StringEquals": {
  "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
  "token.actions.githubusercontent.com:sub": "repo:acme/deploy:ref:refs/heads/main"}}
```

**References:** CWE-287, OWASP ASVS 3.5, AWS IRSA trust policy docs, SPIFFE/SPIFFI threat model

# Confused Deputy: Cross-Account Roles Without ExternalId or Source Conditions

**MUST** require a caller-specific `sts:ExternalId` (or equivalent source-account/source-ARN conditions) in the trust policy of every cross-account role, so third parties cannot trick the role into acting on another customer's behalf.

**Why:** Without an ExternalId, any account that learns the role's ARN can ask the STS to assume it — the "deputy" cannot tell which client actually requested the action, letting one tenant read or modify another's resources.

**Detect:** Review trust policies (`assume_role_policy` in Terraform, `AssumeRolePolicyDocument` in CloudFormation) for cross-account principals lacking a `Condition` block on `sts:ExternalId`, `aws:SourceArn`, or `aws:SourceAccount`. Check partner-integration docs and IaC modules that accept a bare `principal_arn` parameter with no external-id input.

**Bad:**
```json
"Principal": {"AWS": "arn:aws:iam::999988887777:root"}
```

**Good:**
```json
"Principal": {"AWS": "arn:aws:iam::999988887777:root"},
"Condition": {"StringEquals": {
  "sts:ExternalId": "acme-tenant-42",
  "aws:SourceArn": "arn:aws:events:us-east-1:999988887777:rule/nightly-sync"}}
```

**References:** AWS Confused Deputy Prevention Guide, CWE-915, AWS Security Best Practices SEC3-BP05

# API Gateway / Edge Endpoints Deployed Without Authorizers

**MUST** attach an authorizer (IAM, JWT, Lambda/Cognito, or mTLS) to every deployed API route, with authorization denied by default rather than per-route opt-in.

**Why:** Routes created quickly for testing routinely reach production still marked `AUTH = NONE`; scanners find them within hours, and internal endpoints often carry admin-shaped functionality with the assumption that "nobody knows the URL."

**Detect:** In OpenAPI/Swagger specs check for missing or `security: []` operations; in SAM/CloudFormation look for `AuthorizationType: NONE` on `AWS::ApiGateway::Method`; on API Gateway v2 check `AuthorizationType` absent from routes. Also review ingress annotations and edge-function configs where auth middleware is applied per-route instead of globally.

**Bad:**
```yaml
MyMethod:
  Type: AWS::ApiGateway::Method
  Properties:
    AuthorizationType: NONE
    Integration: {Type: AWS_PROXY, Uri: !GetAtt AdminFn.Arn}
```

**Good:**
```yaml
MyMethod:
  Type: AWS::ApiGateway::Method
  Properties:
    AuthorizationType: COGNITO_USER_POOLS
    AuthorizerId: !Ref UserPoolAuthorizer
```

**References:** OWASP A01:2021, OWASP ASVS 4.1, AWS API Gateway authorization docs, CWE-306

# API Gateway Mapping Template / Proxy Passthrough Injection

**MUST NOT** interpolate raw request data into VTL mapping templates or constructed upstream payloads without escaping and schema validation; treat `$input` and `$context` fields as attacker-controlled strings.

**Why:** Naive `$input.json()` splicing into JSON or header templates lets a crafted body break out of the intended structure — forging identity headers, smuggling backend directives, or corrupting the upstream request that the backend trusts because it "came from the gateway."

**Detect:** Audit `*.vm`/VTL templates for direct `$input.json('...')` or `$context.identity.*` writes into headers and bodies without `escapeJson`/`escapeJava`; look for passthrough mode `WHEN_NO_TEMPLATE` on sensitive integrations, and templates that set `X-User-Id` from the body instead of the verified authorizer context.

**Bad:**
```vtl
{ "user": $input.json('$.user'), "role": $input.json('$.role') }
```

**Good:**
```vtl
#set ($user = $input.json('$.user'))
{ "user": "$util.escapeJson($user)",
  "role": "$context.authorizer.claims.role" }
```

**References:** CWE-74, AWS API Gateway mapping template docs, OWASP Injection cheatsheet

# Serverless Execution Environment Reuse Leaking Data Across Invocations

**MUST NOT** cache per-request data — customer records, tokens, decrypted keys — in module-level or global mutable state of a serverless function, because warm containers are shared by later, possibly different, invocations.

**Why:** Lambda and friends reuse a warmed container across tenants' requests when concurrency allows; a global populated during request A can be read during request B, producing cross-customer data disclosure that only appears under load.

**Detect:** In Lambda/Cloud Function/Cloud Run code, flag module-scope dicts, lists, or connection objects that store request-derived values (`current_user = None` at top level then assigned inside the handler), memoized decryption caches keyed loosely, and background threads outliving the handler. Contrast with connection pools (acceptable) versus data caches (not).

**Bad:**
```python
cached_profile = None          # module scope, survives invocations
def handler(event, ctx):
    global cached_profile
    cached_profile = fetch_profile(event["user_id"])
    return {"sso": cached_profile["email"]}
```

**Good:**
```python
def handler(event, ctx):
    profile = fetch_profile(event["user_id"])   # request-local only
    return {"sso": profile["email"]}
```

**References:** CWE-459, AWS Lambda execution environment reuse docs, OWASP Serverless Top 10 (A02)

# NodePort / LoadBalancer Accidentally Exposing Internal Services

**SHOULD NOT** publish admin dashboards, databases, or metrics endpoints via NodePort or an internet-facing LoadBalancer; internal services stay internal unless a reviewed ingress explicitly fronts them.

**Why:** A `type: NodePort` service opens a 30000-32767 port on every node's public IP, and a defaulted `LoadBalancer` scope often lands on the open internet — exposing unauthenticated UIs that were designed for cluster-internal access only.

**Detect:** Audit manifests for `type: NodePort`, `type: LoadBalancer` without `loadBalancerSourceRanges` or `service.beta.kubernetes.io/aws-load-balancer-internal: "true"`, and Helm values overriding service type. Live check: `kubectl get svc -A | grep -E 'NodePort|LoadBalancer'`, then probe the node ports externally. Flag `/metrics`, `/actuator`, dashboard UIs surfacing this way.

**Bad:**
```yaml
spec:
  type: NodePort        # admin UI now on every node's public IP:31234
  ports: [{port: 8080, targetPort: 8080}]
```

**Good:**
```yaml
spec:
  type: ClusterIP   # expose only via authenticated Ingress with TLS
```

**References:** CWE-284, CIS Kubernetes 5.2.2, OWASP Kubernetes Top 10, AWS LB isolation docs

# Ingress Host-Header / vHost Routing Collisions and TLS Passthrough Misrouting

**MUST** define explicit host matching on every Ingress rule and a catch-all default backend that returns 404/421, so an unexpected `Host` header cannot route traffic to the wrong service.

**Why:** When rules overlap or a controller falls back to its default vhost, a request aimed at `admin.example.com` can land on an unrelated backend that processes it as if trusted — and TLS passthrough makes the mismatch invisible because the outer SNI never gets re-checked inside.

**Detect:** Look for Ingress resources with empty `host:` (matches everything), duplicate hosts across namespaces, `nginx.ingress.kubernetes.io/ssl-passthrough` on shared ports without per-SNI routing, and controllers configured with a permissive default backend. Test by sending crafted `Host:` headers to the LB IP and observing which service answers.

**Bad:**
```yaml
- http:
    paths:
      - path: /            # no host: matches ANY hostname
        backend: {serviceName: payments, servicePort: 443}
```

**Good:**
```yaml
- host: payments.example.com
  http:
    paths:
      - path: /
        pathType: Prefix
        backend: {serviceName: payments, servicePort: 443}
```

**References:** CWE-441, RFC 9110 §7.2 (Host), Kubernetes Ingress docs, OWASP A01:2021

# Service Mesh Permissive mTLS and Direct-Pod-IP Bypass

**MUST NOT** treat permissive-mode mTLS as an access-control boundary; enforce STRICT mTLS per namespace and pair it with NetworkPolicies that block plaintext direct-pod-IP access.

**Why:** Permissive mode accepts both meshed (mTLS) and raw plaintext traffic, so an attacker inside the cluster — or a compromised pod — simply bypasses the sidecar by dialing the pod IP on the plaintext port, and any authorization policy keyed on peer identity silently fails open for that path.

**Detect:** Check PeerAuthentication `mtls.mode: PERMISSIVE` (or mesh-wide default), AuthorizationPolicies that allow when principal is empty, CNI/network policies that don't restrict pod ports to sidecar traffic only, and services reachable on `podIP:port` in egress tests. Verify destination rules route through the service, not resolved pod endpoints.

**Bad:**
```yaml
mtls:
  mode: PERMISSIVE   # plaintext to podIP:8080 still accepted
```

**Good:**
```yaml
mtls:
  mode: STRICT
# plus NetworkPolicy restricting the port to the mesh sidecar
```

**References:** Istio security docs (permissive mTLS caveats), OWASP Kubernetes Top 10, CWE-300

# File descriptor and conntrack table limits sized for peak

**SHOULD** size file-descriptor limits and conntrack tables above measured peak concurrency with headroom, and alert before the ceiling is hit rather than after.

**Why:** A busy proxy hitting `ulimit -n` starts refusing connections with `EMFILE`, and a full `nf_conntrack` table silently drops new flows — both look like mysterious upstream flakiness while capacity metrics still show idle CPU.

**Detect:** Compare `ulimit -n` / `fs.file-max` and container `no-new-privileges` securityContext defaults against peak connection counts; check `net.netfilter.nf_conntrack_max` versus `nf_conntrack_count` (watch for `nf_conntrack: table full, dropping packet` in dmesg). In Kubernetes, review Pod `ulimit` inheritance, kube-proxy conntrack settings, and whether monitoring exports fd/conntrack saturation.

**Bad:**
```
# 100k concurrent proxy on default 1024 fds
$ ulimit -n
1024
```

**Good:**
```
# sized for peak + 3x headroom, alarmed at 70%
ulimit -n 65536
sysctl -w net.netfilter.nf_conntrack_max=524288
```

**References:** Netflix tuning guides, Netfilter conntrack docs, Google SRE Book (capacity monitoring), USE method

# Ephemeral port / TIME_WAIT exhaustion on busy clients

**SHOULD** pool and reuse outbound connections on high-fan-out clients so the ephemeral port range and TIME_WAIT backlog never become the bottleneck.

**Why:** Every unclosed TCP connection from a client burns a local port for 60 seconds in TIME_WAIT; a chatty service opening a fresh socket per request can exhaust the ~28k available ports and fail with `EADDRNOTAVAIL` — a self-inflicted outage triggered by success, not attack.

**Detect:** Watch `ss -s` / `netstat -an | grep TIME_WAIT | wc -l` against `net.ipv4.ip_local_port_range`; grep code for HTTP clients constructed per request (`requests.get(...)` without a session, `new HttpClient()` inside loops) instead of shared pooled clients. Check keep-alive settings, pool max-size, and whether the platform's port range is unusually narrow.

**Bad:**
```python
for url in urls:
    requests.get(url)          # fresh socket + TIME_WAIT each time
```

**Good:**
```python
s = requests.Session()         # one pooled, keep-alive client
adapter = HTTPAdapter(pool_maxsize=100)
s.mount("https://", adapter)
for url in urls:
    s.get(url)
```

**References:** RFC 9293 (TIME-WAIT), Cloudflare "Why your server runs out of ports", nginx/HAProxy connection pooling docs

# Path MTU blackholes diagnosed on tunnel/VPN paths

**SHOULD** verify path MTU handling on every tunnel, VPN, or encapsulated route: clamp MSS at tunnel ingress and never blanket-drop ICMP "fragmentation needed" messages.

**Why:** When ICMP Type 3 Code 4 is blocked, packets larger than the tunnel's reduced MTU vanish silently — TLS handshakes and small requests succeed while larger payloads hang forever, a failure pattern users describe as "some sites work, others just spin."

**Detect:** Probe with `ping -M do -s 1472` (and descending sizes) across the tunnel; check tunnel interface MTU vs underlay, iptables rules dropping ICMP unreachables, MSS clamping presence (`--clamp-mss-to-pmtu` or LB/Cloud NAT settings), and VPN configs (WireGuard `MTU=1420`, IPsec overhead). Look for TCP windows stalling at handshake in packet captures.

**Bad:**
```
iptables -A FORWARD -p icmp --icmp-type fragmentation-needed -j DROP
# oversized packets now disappear with no error back to the sender
```

**Good:**
```
iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN \
         -j TCPMSS --clamp-mss-to-pmtu
```

**References:** RFC 8899 (PMTUD), RFC 1191, AWS VPN MTU docs, Black Hole Router / PMTU blackhole literature

# Load balancer health-check flapping detected and damped

**SHOULD** configure hysteresis on health checks — separate healthy/unhealthy thresholds, realistic timeouts, and jittered intervals — and alert on state-transition rate, not just current state.

**Why:** A single slow response ejects a healthy backend; when the ejected node's traffic overloads its siblings, they fail too, and the whole pool oscillates in a cascade. Flapping also thrashes DNS/LB control planes and hides the true failure during postmortems.

**Detect:** Review health-check configs (ALB target groups, nginx `max_fails`/`fail_timeout`, HAProxy `fall`/`rise`, Consul health checks) for threshold=1 on removal and timeouts tuned to p50 instead of p99. Query LB metrics for backend health-state transitions per minute; check whether monitoring fires on flapping patterns rather than only fully-down states.

**Bad:**
```
health_check: {interval: 2s, timeout: 1s, unhealthy_threshold: 1}
# one GC pause ejects a perfectly healthy node
```

**Good:**
```
health_check: {interval: 10s, timeout: 5s,
               unhealthy_threshold: 3, healthy_threshold: 2}
```

**References:** AWS ELB health check best practices, HAProxy tuning docs, Google SRE Book (overloading & health checks)

# PQC readiness of TLS/VPN termination (hybrid KEM deployment)

**SHOULD** inventory every TLS and VPN termination point today and plan hybrid post-quantum key agreement (X25519 + ML-KEM) for long-lived, harvest-now-decrypt-later traffic before the client ecosystem forces a rushed rollout.

**Why:** Adversaries can record encrypted sessions now and decrypt them years later once quantum computers mature; data with a multi-decade confidentiality lifetime — VPN tunnels, backups, personal data — needs the quantum transition clocked deliberately, not in a panic.

**Detect:** Enumerate termination points (nginx/Apache, Envoy, cloud LBs, WireGuard/IPsec concentrators) and their TLS library versions; check for `ML-KEM`/`X25519MLKEM768` support (OpenSSL 3.5+, BoringSSL, AWS KMS/PQN), client-population coverage, and whether the inventory records each endpoint's data-sensitivity lifetime. Review VPN cipher suites for absence of any KEM upgrade path.

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

# Unauthenticated data stores exposed (Redis, Elasticsearch, MongoDB, Memcached)

**MUST NOT** expose any datastore port (Redis, Elasticsearch, MongoDB, Memcached, etcd) to a network where untrusted clients can reach it without authentication and network-level restriction.

**Why:** These engines shipped with auth off by default, and scanned-and-looted instances appear daily: Redis dumps of sessions, Elasticsearch clusters of leaked PII. An unauthenticated store on a reachable network is a breach with a countdown timer.

**Detect:** Scan inventories for default ports (6379, 9200, 27017, 11211) bound to `0.0.0.0`; check Redis `requirepass`/ACLs, MongoDB auth, Elasticsearch `xpack.security.enabled`, and security groups opening them beyond the app tier.

**Bad:**
```yaml
kind: Service
spec:
  type: LoadBalancer        # redis straight to the internet
  ports: [{ port: 6379 }]
```

**Good:**
```yaml
spec:
  type: ClusterIP   # plus requirepass and a NetworkPolicy
---
# NetworkPolicy: apps namespace -> redis:6379 only
```

**References:** CWE-306 Missing Authentication for Critical Function, OWASP A02, Redis security docs, Shodan exposed-database research

# Data Exfiltration Monitoring

**SHOULD** baseline per-host and per-account egress volume and alert on anomalous outbound transfers, especially off-hours and to untrusted destinations.

**Why:** Stolen data must leave the network eventually; without egress baselines, a multi-gigabyte dump to an unknown endpoint looks like ordinary traffic.

**Detect:** grep flow-log analytics for `bytes_out` thresholds, new-destination first-seen alerts, and DB export / S3 egress alarms; verify egress paths are actually observable.

**References:** MITRE ATT&CK T1048 Exfiltration Over Alternative Protocol, T1567, CWE-200, NIST SP 800-53 AC-4

# Attack Surface Management (continuous exposure discovery)

**MUST** continuously discover and inventory every internet-facing asset (domains, subdomains, IPs, cloud endpoints) rather than relying on a static list.

**Why:** Forgotten shadow IT and stale exposed services are the most common initial-access entry points attackers find before defenders do.

**Detect:** Certstream/subdomain enumeration output, `external-exposure.csv`, cloud security hub findings, diff of DNS zone records vs. approved inventory.

**References:** OWASP WSTG-INFO-02, CWE-1059, NIST SP 800-119, AWS Security Hub, Cloudflare for Teams

# Attack Surface Reduction (deliberate exposure minimization)

**SHOULD NOT** expose administrative interfaces, dashboards, or debug endpoints directly to the public internet without an access broker such as VPN or zero-trust gateway.

**Why:** Every unnecessary open port is a tested entry point; exposed admin panels are routinely brute-forced or exploited via known CVEs.

**Detect:** `admin`, `console`, `/debug`, `:8080`, `:9200`, `kibana`, `phpmyadmin` in public ingress or SecurityGroup rules; Terraform `ingress = 0.0.0.0/0`.

**References:** OWASP ASVS V1.3, CWE-489, NIST SP 800-53 AC-3, CIS Benchmark 5.1

# Dangerous IAM Policies (admin/*, *:*, PassRole chains flagged by policy linting)

**MUST NOT** grant wildcard actions/resources (`*:*`, `admin/*`) or unscoped PassRole; linters must fail CI on them.

**Why:** Over-broad grants turn one leaked credential into full account takeover; IaC makes the blast radius reproducible across every environment the module touches, and PassRole hides escalation inside "read-only" roles.

**Detect:** Grep IAM JSON for `"Action": "*"`, `"Resource": "*"`, bare `iam:PassRole`, `AdministratorAccess`. Lint Terraform `aws_iam_policy`/`google_service_account_iam_*`, CloudFormation `AWS::IAM::Policy`, and Pulumi policy docs for wildcards and modules that accept `policy_json` verbatim; run Cloudsplaining or `tfsec`/`checkov` IAM rules in CI and flag any policy the analyzer reports as admin-equivalent.

**References:** AWS IAM best practices, CWE-269, NIST SP 800-53 AC-6, Cloudsplaining, GCP Policy Intelligence, CIS AWS 5.28–5.36

# Cloud Privilege-Escalation Paths (cross-role/cross-account escalation graph reviewed)

**SHOULD** periodically compute the role-to-role and cross-account escalation graph, pruning every path from low privilege to admin.

**Why:** Individually reasonable grants compose into escalation ladders (create-role, assume-role, modify-trust) no single-policy review catches.

**Detect:** run pmapper `analyze`, cloudsplaining cross-account reports; grep trust policies for `"AWS": "*"`.

**References:** AWS IAM Access Analyzer, NIST SP 800-53 AC-3/AC-6, CWE-269, Cloudsplaining, Azure AD escalation analysis

# CSPM Continuous Cloud Posture Scanning (misconfig drift detected continuously)

**MUST** scan cloud configuration continuously for misconfigurations instead of relying on point-in-time audits.

**Why:** Public buckets, open security groups, and disabled logging appear between audits; attackers scan for them constantly.

**Detect:** grep for `prowler`, `scoutsuite`, `cloudsploit`, `checkov --framework cloud`, scheduled posture-scan jobs with alert routing.

**References:** NIST CS2 (SP 800-223), CIS Cloud Benchmarks, NIST SP 800-53 CM-6, CWE-16

# Lateral Movement Detection (post-compromise horizontal motion in cloud/host)

**SHOULD** alert on post-compromise horizontal motion: unusual SSH/RDP hops, mass SMB enumeration, anomalous cross-account role assumption.

**Why:** Without motion alerts, dwell time stretches to months while one foothold becomes total compromise of crown jewels.

**Detect:** grep detection rules for `T1021`, `remote_services`, `admin_shares`, `pass-the-hash`, unusual-login Sigma/YARA-L rules.

**References:** MITRE ATT&CK TA0008/T1021, NIST SP 800-61, Sigma rules, GuardDuty UnauthorizedAccess

# Infrastructure Drift Detection (live state vs IaC diffed and alerted)

**MUST** continuously diff live infrastructure against IaC definitions and alert on unauthorized manual changes.

**Why:** Console-clicked changes bypass review and become invisible holes — an undocumented open security group never gets fixed.

**Detect:** grep `terraform plan -detailed-exitcode` cron jobs, Driftctl, AWS Config drift rules, `kubectl diff -f`.

**References:** NIST SP 800-53 CM-3/CM-6, CIS Control 2, Terraform drift docs

# Attack-Path Analysis (reachable chains from exposure to crown jewels)

**SHOULD** continuously map reachable attack paths from internet exposure and low-privilege identities to critical assets, cutting shortest chains first.

**Why:** Findings look minor in isolation; it's the composed chain — public bucket to role trust to database — that actually breaches you.

**Detect:** grep `cartography`, `bloodhound`, `attack_path` reports, reachability graph exports.

**References:** MITRE ATT&CK, NIST SP 800-30, BloodHound docs

# Egress Control (outbound traffic allow-listed; exfil paths narrowed)

**SHOULD** restrict outbound traffic to an explicit allow-list so compromised hosts cannot freely phone home or exfiltrate.

**Why:** Default-open egress is the exfiltration highway: malware, reverse shells, and data staging all reach arbitrary endpoints.

**Detect:** grep `NetworkPolicy` egress rules, `egress gateway`, proxy allow-lists, `default-deny` outbound rules.

**References:** NIST SP 800-207 Zero Trust, CIS Control 12, MITRE ATT&CK TA0011

# Open Directory Listing

**SHOULD NOT** enable directory indexes on web servers or object storage where file enumeration reveals backups, configs, or internal artifacts.

**Why:** `Autoindex on` / bucket list permission turns one known filename pattern into a full inventory of everything ever placed there.

**Detect:** grep server configs for `autoindex on`, `Options +Indexes`, bucket `ListBucket` grants; probe for `Index of /` responses.

**References:** OWASP WSTG-CONF-01, CWE-548, AWS S3 ACL best practices

# Exposed Data-Service Ports

**MUST NOT** expose database, cache, search, and daemon ports (Redis 6379, Elasticsearch 9200, MongoDB 27017, Memcached 11211, Docker API 2375, Postgres 5432) beyond the trusted network without authentication and TLS.

**Why:** Internet-scanned services (Shodan/Censys) find unauthenticated Redis/Elasticsearch weekly — no creds needed to read or wipe the dataset.

**Detect:** scan own external IP range for 6379/9200/27017/11211/2375; grep security groups/firewall rules and Service type=LoadBalancer for data ports; check `bind`/`requirepass`/`xpack.security` settings.

**References:** MITRE ATT&CK T1190, CIS Docker 2.x, Shodan exposed-database reports

# Zero Trust Architecture

**SHOULD** verify every request explicitly regardless of network location — no implicit trust for internal networks, device posture checked, per-request authorization, least-privilege service identity.

**Why:** Perimeter-based trust collapses the moment one host is compromised; zero trust contains blast radius by treating every call as coming from an attacker until proven otherwise.

**Detect:** look for mTLS everywhere / service mesh, identity-aware proxies (BeyondCorp-style), absence of "trusted internal network" CIDR allow-lists as sole authz, continuous session validation rather than once-at-connect.

**References:** NIST SP 800-207 Zero Trust Architecture, CISA Zero Trust Maturity Model

# CAA Record Policy

**SHOULD** publish CAA records restricting which CAs may issue certificates for the domain, with issuewild and iodef contact configured.

**Why:** Without CAA, any trusted CA can issue for your domain — a compromised or careless CA anywhere is a MITM cert waiting to happen; CAA narrows that to chosen issuers.

**Detect:** `dig CAA <domain>` and check issuewild coverage (missing issuewild = wildcards blocked for all CAs — verify intent); confirm CAA covers all public cert domains including delegated subdomains.

**References:** RFC 8659 CAA, CA/B Forum baseline requirements, letsencrypt CAA documentation

# Certificate-Issuance Monitoring

**SHOULD** alert on any certificate issued for your domains (CT-log monitoring via Certstream/CRT.sh) to detect unauthorized issuance fast.

**Why:** Rogue/mistaken certs for your domain appear in Certificate Transparency logs publicly — if you're not watching, you learn about the fake cert from an outage or a breach report.

**Detect:** check for CT-monitoring service/cron (Censys monitor, Certstream consumer, crt.sh search alerts) covering all brand domains and wildcard patterns; verify alert routing to a responder.

**References:** Certificate Transparency project (certificate-transparency.org), Censys/Certstream monitoring, Google CT policy

# Agent Egress Allowlist & Proxy Control

**MUST** route coding-agent egress (model calls, MCP-over-HTTP, web fetch) through an explicit proxy/allowlist — and repo-supplied env must never control where agent traffic goes.

**Why:** DeepSeek's harness refuses to start rather than let a cloned repo set proxy vars; OpenAI uses allowlist-first domain rules where deny always wins — repo-controlled egress is an exfiltration path.

**Detect:** agent runs without managed proxy; wildcard `*` in agent network allow rules; MCP servers reaching arbitrary hosts; repo .env containing proxy settings honored by agent tooling.

**References:** DeepSeek harness proxy-refusal pattern, OpenAI Codex domain rules, GitHub agent internet firewall, Cursor fixed-destination egress

