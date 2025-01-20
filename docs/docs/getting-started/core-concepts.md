---
title: Core Concepts
---

As Helmless is built on top of Helm, it shares the same core concepts, but with some differences and new features specific to serverless deployments.

## Helmless Charts
Helmless charts template your values into cloud-provider specific formats. They handle:

- Resource configuration
- Environment variables
- Secrets and volumes mapping
- Scaling rules

## Values Files
Like Helm, Helmless uses `values.yaml` files to configure your deployments. These files define everything about your service:

```yaml
name: my-service
image: us-docker.pkg.dev/cloudrun/container/hello:latest
env:
  API_KEY: secret
```

## Deployment Actions
Helmless provides deployment tools that:

- Template your values
- Validate configurations
- Deploy to your cloud provider
