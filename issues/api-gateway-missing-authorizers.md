---
categories: [authentication, cloud-network]
domains: [backend, infrastructure]
---

# API Gateway / Edge Endpoints Deployed Without Authorizers

**MUST** attach an authorizer (IAM, JWT, Lambda/Cognito, or mTLS) to every deployed API route, with authorization denied by default rather than per-route opt-in.

**Why:** Routes created quickly for testing routinely reach production still marked `AUTH = NONE`; scanners find them within hours, and internal endpoints often carry admin-shaped functionality with the assumption that "nobody knows the URL."

**Detect:** In OpenAPI/Swagger specs check for missing or `security: []` operations; in SAM/CloudFormation look for `AuthorizationType: NONE` on `AWS::ApiGateway::Method`; on API Gateway v2 check `AuthorizationType` absent from routes. Also review ingress annotations and edge-function configs where auth middleware is applied per-route instead of globally.

**Bad:**
```yaml
MyMethod:
  Type: AWS::ApiGateway::Method
  Properties:
    AuthorizationType: NONE
    Integration: {Type: AWS_PROXY, Uri: !GetAtt AdminFn.Arn}
```

**Good:**
```yaml
MyMethod:
  Type: AWS::ApiGateway::Method
  Properties:
    AuthorizationType: COGNITO_USER_POOLS
    AuthorizerId: !Ref UserPoolAuthorizer
```

**References:** OWASP A01:2021, OWASP ASVS 4.1, AWS API Gateway authorization docs, CWE-306

---

**Part of:** [authentication](../categories/authentication.md) · [cloud-network](../categories/cloud-network.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
