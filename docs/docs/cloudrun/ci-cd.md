---
title: CI/CD with Github Actions
description: Deploy your container to Google Cloud Run using Github Actions
icon: simple/githubactions
---

# CI/CD with Github Actions

Helmless is designed to be used in any CI/CD pipeline to deploy your container to the cloud provider of your choice. Since we use Github Actions as our CI/CD platform of choice, this guide will show you how to deploy your container to Google Cloud Run using Github Actions.

Helmless provides a [Github Action][github-action] that you can use in your workflow to deploy your container to Google Cloud Run.

!!! info "Contributing other CI/CD Platforms"
    If you want to extend Helmless to other CI/CD platforms, we kindly ask you to get in touch and contribute to the project.

## Prerequisites

Before you can start using Github Actions to deploy your container to Google Cloud Run, you need to allow your Github repository access to your GCP project.

See the [Terraform guide](./terraform.md#workload-identity-federation) for more information on how to do this.

## Github Deployment Action

You can find a full example of a Github Actions workflow in the [GitHub repository](https://github.com/helmless/google-cloudrun-charts/blob/main/.github/workflows/e2e.yaml).

Here is a simplified version of the workflow with matrix deployment for multiple services:

<div class="annotate" markdown>
```yaml title="deploy.yml"
name: 🚀 Deploy Cloud Run Service

on:
  workflow_dispatch:
  push:
    branches: [main]

jobs:
  deploy:
    name: 🚀 helmless-service
    runs-on: ubuntu-24.04
    permissions:
      contents: read
      id-token: write
    concurrency:
      group: helmless-service

    steps:
      - name: 📥 Checkout Repository
        uses: actions/checkout@v4

      - name: 🔑 Google Auth
        id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_POOL }} (1)

      - name: 🚀 Deploy Service
        uses: helmless/google-cloudrun-action@v1 (6)
        id: deploy
        with:
          files: |
            helmless/values.yaml (2)
          chart: oci://ghcr.io/helmless/google-cloudrun-service (3)
          chart_version: "latest" (4)
          dry_run: false (5)
```
</div>

1. The `GCP_WORKLOAD_IDENTITY_POOL` is the workload identity pool you created in the [Github Workload Identity Federation](#github-workload-identity-federation) section.
2. The `files` argument takes one or more `values.yaml` files. In this example we use a single `helmless/values.yaml` file that was created in the [Getting Started](./getting-started.md) guide. The files are applied in the order they are listed. So if you need to override values in a specific file, you can do so by listing the file with the higher precedence last.
3. The Helmless chart to use for the templating. Defaults to `oci://ghcr.io/helmless/google-cloudrun-service`. See [packages](https://github.com/orgs/helmless/packages) for a list of available charts.
4. The version of the Helm chart to deploy. `latest` and all valid Helm chart version ranges are supported.
5. If true the template will only be validated against the GCP Cloud Run API but not deployed.
6. The version of the [Helmless Github Action][github-action] to use. Make sure to use the latest version.


!!! info "Helmless Github Action"
    You can find more examples in the Readme of the [helmless/google-cloudrun-action][github-action] and the [e2e tests][e2e-tests].

[github-action]: https://github.com/helmless/google-cloudrun-action
[e2e-tests]: https://github.com/helmless/google-cloudrun-charts/blob/main/.github/workflows/e2e.yaml
