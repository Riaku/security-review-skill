# cloud-network

Cloud networking, DNS, edge, cloud resource exposure.

## What this category covers

This category covers the network and cloud-control-plane surface between the internet and a workload: what is reachable, from where, and under whose identity. Member items span DNS and certificate lifecycle, edge and ingress routing, firewalls and security groups, VPC and subnet segmentation, cloud IAM and metadata credentials, and the exposure of storage and data stores. They also cover the operational side of that surface — cost alarms, posture scanning, attack-path analysis, and the detection signals that reveal lateral movement or exfiltration. A reviewer should expect findings about who can reach a service, whether that reach was deliberate, and whether the identity behind a connection is actually verified.

- DNS records, CAA, DNSSEC, propagation TTLs, and dangling or hijackable names.
- TLS termination: certificate renewal, cipher suites, client verification, and post-quantum readiness.
- Edge routing: API gateway authorizers and mapping templates, ingress host matching, and load balancers.
- Network segmentation: VPCs, subnets, security groups, NAT, IPv6 coverage, and service-to-service mTLS.
- Cloud identity: IAM policy breadth, privilege-escalation edges, cross-account trust, and instance metadata.
- Exposure and cost: public buckets, open data-store ports, presigned URLs, egress baselines, and billing alarms.

## What it does not cover

- [containers-k8s](../categories/containers-k8s.md) — pod-level security contexts, admission policy, and in-cluster RBAC or NetworkPolicy enforcement belong there.
- [web-api-security](../categories/web-api-security.md) — request parsing, injection, and endpoint authorization inside the application belong there; this category stops at the edge.
- [secrets-crypto](../categories/secrets-crypto.md) — key storage, rotation, and cryptographic primitive selection belong there, even when the keys protect TLS or cloud credentials.

## What a finding here looks like

- A security group or firewall rule admits `0.0.0.0/0` on an administrative or data port, and no other layer blocks it.
- A DNS record still points at a deprovisioned bucket, app, or distribution, leaving the name claimable by someone else.
- An API route or ingress path reaches a backend with no authorizer, or with a per-route opt-in that one route missed.
- A workload that fetches user-supplied URLs can reach the metadata endpoint and return the node's role credentials.
- IPv6 is enabled on an interface while the firewall ruleset covers only IPv4, leaving a second unfiltered path in.
