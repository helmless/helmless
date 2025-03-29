---
title: Configuration
description: Learn how to configure a Helmless application
icon: material/table-settings
---

# Configuration

Helmless works by templating and deploying a Helm chart.
Helm charts are configured using the `values.yaml` file.

For Helmless you have two options:

1. Create a new application Helm chart and add the Helmless charts as dependencies
2. Directly provide the `values.yaml` file to Helmless and use the Github Action that will automatically pick the Helmless charts to render

## Option 1: Create a new application Helm chart

This is the recommended approach, which brings the following benefits:

- Use a dependency update mechanism like dependabot
- Use Helm compatible tools, like intellisense and linting
- Deploy multiple applications from the same chart and share values between them

To get started, create a new Helm chart and remove the default templates and values.yaml file.

```bash
helm create my-app && rm -rf my-app/templates/* && rm my-app/values.yaml
```

Add the Helmless charts as dependencies to your Helm chart.

```yaml title="my-app/Chart.yaml"
dependencies:
  - name: google-cloudrun-service
    version: 0.3.0
    repository: oci://ghcr.io/helmless
    alias: service
  - name: google-cloudrun-job
    version: 0.3.0
    repository: oci://ghcr.io/helmless
    alias: job
```

You can add multiple services and jobs to the same chart, just make sure to use different aliases.

The config above will allow you to configure the `values.yaml` like this:

<div class="annotate" markdown>
```yaml title="my-app/values.yaml"
global: (1)
  project: my-project
  region: europe-west1

env: &env (2)
  COMMON_ENV_VAR: my-value

service:
  name: my-service
  env:
    <<: *env (3)
    COMMON_ENV_VAR: override-value
    SERVICE_SPECIFIC_ENV_VAR: my-value

job:
  name: my-job
  env:
    <<: *env
    JOB_SPECIFIC_ENV_VAR: my-value (4)
```
</div>

1. These global values are shared between all services and jobs
2. You can use YAML anchors to share values between the service and job
3. The common env variables are spread out and can be overridden or extended by the service and job specific variables
4. This is a job only variable and will not be used by the service

You can template the Cloud Run manifests with the following command:

```bash
helm template my-app
```

In the Github Action you can deploy the application with the following workflow. See [Github Deployment Action](../cloudrun/ci-cd.md) for more details.

```yaml title="my-app/.github/workflows/deploy.yaml"
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

    steps:
      - name: 📥 Checkout Repository
        uses: actions/checkout@v4

      - name: 🔑 Google Auth
        id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_POOL }}

      - name: 🚀 Deploy Service
        uses: helmless/google-cloudrun-action@v1
        id: deploy
        with:
          chart: my-app/
```

## Option 2: Directly provide the `values.yaml` file

This is less complex and creates another abstraction layer for your developers, hiding the Helm charts from them.
It comes with the downside that you have no out-of-the-box dependency update mechanism and no Helm tooling support.

To use this option, you can directly provide the `values.yaml` file to Helmless and use the Github Action that will automatically pick the Helmless charts to render.

```yaml title="my-app/values.yaml"
name: my-service
env:
  MY_ENV_VAR: my-value
```

You can locally template the Cloud Run Service manifest with the following command:

```bash
helm template oci://ghcr.io/helmless/google-cloudrun-service \
  -f my-app/values.yaml \
  > my-app/service.yaml
```

In the Github Action you can deploy the application with the following workflow. See [Github Deployment Action](../cloudrun/ci-cd.md) for more details.

```yaml title="my-app/.github/workflows/deploy.yaml"
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

    steps:
      - name: 📥 Checkout Repository
        uses: actions/checkout@v4

      - name: 🔑 Google Auth
        id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_POOL }}

      - name: 🚀 Deploy Service
        uses: helmless/google-cloudrun-action@v1
        id: deploy
        with:
          type: service # or job
          values: |
            my-app/values.yaml
```

## Environment Overrides

You can override the environment variables for a specific environment by adding a `values.<environment>.yaml` file in the application directory.

```yaml title="my-app/values.dev.yaml"
env:
  MY_ENV_VAR: dev-value
```

This will override the `MY_ENV_VAR` environment variable to `dev-value` for the `dev` environment.

You can also override the global values by adding a `values.<environment>.yaml` file in the application directory.

```yaml title="my-app/values.dev.yaml"
global:
  project: dev-project
```

This will override the `project` value to `dev-project` for the `dev` environment.

Then extend your Github Action workflow to include the environment values file.

```yaml title="my-app/.github/workflows/deploy.yaml"
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

    steps:
      - name: 📥 Checkout Repository
        uses: actions/checkout@v4

      - name: 🔑 Google Auth
        id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_POOL }}

      - name: 🚀 Deploy Service
        uses: helmless/google-cloudrun-action@v1
        id: deploy
        with:
          type: service # or job
          values: |
            my-app/values.yaml
            my-app/values.dev.yaml
```

You can extract this into a reusable workflow and use matrix deployments to deploy to multiple environments.
