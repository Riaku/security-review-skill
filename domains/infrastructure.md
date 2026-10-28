# infrastructure

How it is built and where it runs: containers, cloud, CI/CD.

## Detection signals

- Dockerfile / docker-compose / Containerfile
- Kubernetes manifests, Helm charts, kustomize, operators
- Terraform/OpenTofu/Pulumi/CloudFormation/Bicep
- .github/workflows, .gitlab-ci.yml, Jenkinsfile, argo/flux configs

## Stack quick-map

- Dockerfile present → containers-k8s, supply-chain
- K8s manifests/Helm → containers-k8s, cloud-network, sre-incidents
- IaC present → deployment-release, cloud-network
- CI config present → cicd-pipeline-security, supply-chain
- K8s manifests, Helm or host provisioning present → hardening-benchmarks
- Any deployable → observability
- Secrets referenced in manifests or IaC → secrets-crypto
