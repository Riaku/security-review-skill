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

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [containers-k8s](../categories/containers-k8s.md) · [hardening-benchmarks](../categories/hardening-benchmarks.md) · [infrastructure](../domains/infrastructure.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)
