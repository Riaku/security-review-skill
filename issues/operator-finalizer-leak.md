# Operator Finalizer Leaks Blocking Resource Deletion

**MUST** ensure operators remove their finalizers on owned resources even when reconciliation errors, so deletion never hangs indefinitely.

**Why:** A leaked finalizer leaves resources stuck in Terminating, blocking namespace deletion and cascading cleanup failures across the cluster.

**Detect:** Resources with `metadata.finalizers` referencing an operator whose controller is down; namespace stuck `Terminating` with lingering finalizers.

**References:** K8s docs finalizers, etcd garbage collection, CWE-404, operator-sdk finalizer patterns
