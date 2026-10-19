---
categories: [containers-k8s]
domains: [infrastructure]
---

# PersistentVolume Reclaim Policy and NFS root_squash Data Exposure

**MUST** set PersistentVolume `spec.persistentVolumeReclaimPolicy` deliberately (Retain for data-bearing volumes) and enable `root_squash` on NFS exports.

**Why:** A careless Delete policy destroys data on release, while NFS without root_squash lets any pod's root read and write the export.

**Detect:** PVs with `persistentVolumeReclaimPolicy: Delete` on stateful data; NFS export options missing `root_squash` in `/etc/exports` or provisioner config.

**References:** CIS K8s 5.2.3, NFS man root_squash, CWE-284, NIST SP 800-190 5.3
