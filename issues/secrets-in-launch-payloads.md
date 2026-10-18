# Secrets in Instance Launch Payloads

**MUST NOT** place credentials, tokens, or private keys in instance launch payloads — EC2 user-data, cloud-init scripts/templates, Azure `customData`, GCP startup-script metadata; grant scoped instance roles or fetch secrets from a secrets manager at boot instead.

**Why:** Launch payloads are readable through the same instance-metadata service attackers already target via SSRF (`curl http://169.254.169.254/latest/user-data`), are copied into AMIs and launch-template history, and persist in Terraform state and console screenshots — a credential placed there leaks through every one of those surfaces at once, long after the instance is gone.

**Detect:** grep user-data/cloud-init blocks for `AWS_SECRET_ACCESS_KEY`, `password=`, `token`, `-----BEGIN`, connection strings with credentials; Terraform `aws_instance.userdata` / `google_compute_instance.metadata.startup-script` containing literals rather than role names or secret-manager references; scanned AMI user-data for inherited secrets.

**References:** CIS AWS 5.4 (no secrets in user data), cloud-init sensitive-data guidance, AWS best practices for embedded credentials, aquasecurity/trivy-checks user-data secret rules
