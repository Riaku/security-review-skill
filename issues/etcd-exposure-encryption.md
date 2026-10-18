# etcd Exposure and Missing etcd Encryption

**MUST** restrict etcd (2379/2380) to control-plane peers and enable encryption at rest for all stored Secrets.

**Why:** etcd holds every secret in plaintext by default; a reachable or unencrypted datastore dumps the cluster's entire credential set.

**Detect:** etcd client port reachable off-node; kube-apiserver missing `--encryption-provider-config`; no EncryptionConfiguration resource.

**References:** CIS K8s 2.0, 3.2.1, CWE-311, NIST SP 800-190 5.2, K8s encryption-at-rest docs
