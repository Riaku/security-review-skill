# Volume IOPS/throughput ceilings profiled before launch

**SHOULD** benchmark the storage volume's IOPS and throughput ceilings under a realistic workload before launch, and size expected database load against them with headroom.

**Why:** Cloud volumes advertise tiers, but the database discovers the ceiling at the worst moment: launch day. A volume pinned at its IOPS limit surfaces as mysterious slow queries and rising `await`, and the application gets blamed for a provisioning mistake.

**Detect:** Ask for fio results tied to the launch checklist. Compare peak read/WAL generation against provisioned IOPS in IaC (`aws_ebs_volume.iops`, StorageClass annotations). No storage numbers, no pass.

**Bad:**
```hcl
resource "aws_ebs_volume" "pg" {
  type = "gp2"   # burst credits; steady-state surprise
}
```

**Good:**
```hcl
resource "aws_ebs_volume" "pg" {
  type = "io2"
  iops = 8000   # fio peak 5.2k + 50% headroom
}
```

**References:** AWS EBS volume types docs, fio benchmarking guide, Google SRE Book capacity planning
