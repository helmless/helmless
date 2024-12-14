---
title: Introduction to Helmless
description: Learn how Helmless simplifies serverless container deployments using familiar tools
---

# Introduction to Helmless

## What is Helmless?

Helmless is a workflow and collection of tools that lets you deploy serverless containers using Helm's familiar templating system - without the complexity of Kubernetes or Terraform. It's designed for teams who want:

- Simple container deployments using familiar Helm syntax
- Fast deployment cycles without infrastructure bottlenecks
- The flexibility to use different cloud providers
- A GitOps-friendly workflow

## How Does it Work?

At its core, Helmless:

1. Takes your container configuration as a Helm values file
2. Templates it into your cloud provider's native format
3. Deploys it using the provider's CLI

```yaml title="Your simple values.yaml"
name: my-service
image: us-docker.pkg.dev/cloudrun/container/hello:latest
env:
  API_KEY: secret
```

--8<-- "docs/_partials/architectur-diagram.md"

## Key Benefits

### 🎯 Simplified Deployments
- Use familiar Helm syntax without Kubernetes complexity
- Deploy directly to serverless platforms
- Avoid infrastructure approval bottlenecks

### 🔄 Fast Development Cycles
- Quick iterations with simple value changes
- Direct container updates without infrastructure changes
- Native CI/CD integration

### 🔌 Cloud Provider Flexibility
- Currently supports Google Cloud Run
- Extensible to other serverless platforms
- Keep your workflow when changing providers
- Easy migration to Kubernetes using familiar workflows

## Core Concepts

### Values Files
Like Helm, Helmless uses `values.yaml` files to configure your deployments. These files define everything about your service:

```yaml
name: my-service
image: us-docker.pkg.dev/cloudrun/container/hello:latest
env:
  API_KEY: secret
```

### Helmless Charts
Helmless charts template your values into cloud-provider specific formats. They handle:

- Resource configuration
- Environment variables
- Secrets and volumes mapping
- Scaling rules

### Deployment Actions
Helmless provides deployment tools that:

- Template your values
- Validate configurations
- Deploy to your cloud provider

## Getting Started

Ready to try Helmless? Choose your path:

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } __Quick Start Tutorial__

    ---

    Learn how to deploy your first Google Cloud Run Service in 5 minutes

    [:octicons-arrow-right-24: Get Started](/docs/getting-started/quickstart)

-   :material-book-open-page-variant:{ .lg .middle } __Core Concepts__

    ---

    Dive deeper into how Helmless works

    [:octicons-arrow-right-24: Dive Deeper](/docs/concepts/overview)

-   :material-code-braces:{ .lg .middle } __Examples__

    ---

    See real-world implementations of Helmless

    [:octicons-arrow-right-24: View Examples](/docs/getting-started/examples)
</div>
