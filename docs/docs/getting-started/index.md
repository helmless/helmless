---
title: Getting Started
description: Learn how Helmless simplifies serverless container deployments using familiar tools
icon: material/rocket-launch
---

# Introduction to Helmless

## What is Helmless?

Helmless is a workflow and collection of tools that lets you deploy serverless containers using Helm's familiar templating system - without the complexity of Kubernetes or Terraform. It's designed for teams who want:

- Simple and streamlined container configuration using Helm's familiar `values.yaml`
- Fast deployment cycles without infrastructure bottlenecks
- Flexible integration into existing CI/CD pipelines
- A GitOps-friendly workflow

## How Does it Work?

At its core, Helmless:

1. Takes your container configuration as a Helm values file
2. Templates it into your cloud provider's native specification using a Helm(less) chart
3. Deploys it using the provider's CLI

```yaml title="Your simple values.yaml"
name: my-helmless-service
image: us-docker.pkg.dev/cloudrun/container/hello:latest
env:
  API_KEY: secret
```

--8<-- "docs/_partials/architectur-diagram.md"

## Getting Started

Ready to try Helmless? Choose your path:

<div class="grid cards" markdown>

-   :material-timer:{ .lg .middle } __5min Quick Start__

    ---

    Learn how to deploy your first Google Cloud Run Service in 5 minutes

    [:octicons-arrow-right-24: Get Started](./quickstart.md)

-   :material-book-open-page-variant:{ .lg .middle } __What is Helmless?__

    ---

    Learn more about Helmless and how it works

    [:octicons-arrow-right-24: Learn More](../helmless/what-is-helmless.md)

-   :material-code-braces:{ .lg .middle } __Examples__

    ---

    See real-world implementations of Helmless

    [:octicons-arrow-right-24: View Examples](./examples.md)

-   :material-book-open-page-variant:{ .lg .middle } __Core Concepts__

    ---

    Dive deeper into how Helmless works

    [:octicons-arrow-right-24: Dive Deeper](./core-concepts.md)

</div>
