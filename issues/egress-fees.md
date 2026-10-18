# Egress Fees

**SHOULD** Cross-AZ and internet-bound data paths be designed with egress cost in mind, and high-volume cross-zone chatter be treated as an architecture smell.

**Why:** Egress and NAT data-processing charges are a classic surprise line item; a chatty service pinned to the wrong AZ can multiply a bill without any security or capacity alarm firing.

**Detect:** Grep configs for AZ-specific endpoints (`us-east-1a`) instead of regional ones. Look for S3/SQS/DB calls over public endpoints rather than gateway endpoints. Review NAT gateway "Data Processed" metrics for top talkers.

**Bad:**
```python
# worker in us-east-1a hitting the public S3 endpoint across AZs
s3 = boto3.client("s3", endpoint_url="https://s3.amazonaws.com")
```

**Good:**
```python
# regional endpoint + S3 gateway endpoint keeps traffic on the AWS backbone
s3 = boto3.client("s3", region_name="us-east-1")
```

**References:** AWS Well-Architected Cost Optimization pillar, AWS NAT gateway pricing, GCP network egress pricing
