# infrastructure

How it is built and where it runs: containers, cloud, CI/CD.

## Detection signals

- Dockerfile / docker-compose / Containerfile
- Kubernetes manifests, Helm charts, kustomize, operators
- Terraform/OpenTofu/Pulumi/CloudFormation/Bicep
- .github/workflows, .gitlab-ci.yml, Jenkinsfile, argo/flux configs

## Stack quick-map

- Dockerfile present → [containers-k8s](../categories/containers-k8s.md), [supply-chain](../categories/supply-chain.md)
- K8s manifests/Helm → [containers-k8s](../categories/containers-k8s.md), [cloud-network](../categories/cloud-network.md), [sre-incidents](../categories/sre-incidents.md)
- IaC present → [deployment-release](../categories/deployment-release.md), [cloud-network](../categories/cloud-network.md)
- CI config present → [cicd-pipeline-security](../categories/cicd-pipeline-security.md), [supply-chain](../categories/supply-chain.md)
