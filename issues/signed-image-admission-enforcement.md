---
categories: [containers-k8s, supply-chain]
domains: [infrastructure]
---

# Admission Enforcement of Signed Images (Verify, Not Just Sign)

**MUST** enforce signature verification at admission so unsigned or wrongly-signed images are rejected before they ever schedule.

**Why:** Signing without enforcement is decoration: an attacker pushes an unsigned image and the cluster runs it happily because nothing checks.

**Detect:** ClusterPolicy `cosigned` / `verify-images` with `match` on all registries; absence of kyverno/admission-controller verify rules; `--image-verification` disabled in k3s config.

**References:** SLSA L4, Sigstore, NSA Kubernetes Hardening Guide, CIS K8s 5.4

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [supply-chain](../categories/supply-chain.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
