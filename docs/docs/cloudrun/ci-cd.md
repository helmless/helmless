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

### Workload Identity Federation

To allow your Github repository to access your GCP project, you need to setup [Github Workload Identity Federation](https://cloud.google.com/blog/products/identity-security/enabling-keyless-authentication-from-github-actions). To make this as easy as possible, we created a small [Terraform module](https://github.com/helmless/google-workload-identity-federation-terraform-module) that can be used to setup the necessary resources in your GCP project.

Deploy it however you deploy your :simple-terraform: infrastructure and make sure to update the `github_organization` variable to match your Github organization.

```hcl title="workload-identity.tf"
--8<-- "https://raw.githubusercontent.com/helmless/google-workload-identity-federation-terraform-module/refs/heads/main/example/main.tf"
```

Applying this module you will get:
<div class="annotate" markdown>
- a workload identity pool (1)
- a workload identity provider for your Github repository (2)
    - that only allows repositories in your Github organization to authenticate with the workload identity pool
</div>

1. A workload identity pool is a container for your workload identities. It uses the [`google_iam_workload_identity_pool` Terraform resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/iam_workload_identity_pool).
2. A workload identity provider is a reference to the Github OIDC identity provider. It uses the [`google_iam_workload_identity_pool_provider` Terraform resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/iam_workload_identity_pool_provider) and is scoped to only allow tokens issued by Github and from repositories in your specified organization.


### Github Repository Permissions

After setting up the workload identity federation, you need to grant the Github repository the necessary permissions to access your GCP project. You do this by giving the `principalSet` scoped to the repository the `roles/iam.workloadIdentityUser` role on the GCP projects default service account that is used by Cloud Run. And it will need `roles/run.admin` permissions on the Cloud Run project where you want to deploy your container.
<div class="annotate" markdown>
!!! warning "Important"

    These permissions are quick start permissions to get you up and running quickly. In production you should scope those permissions to the individual resources you want to deploy and give each Cloud Run service its own service account. (1)
</div>
1.   See the [advanced deployment guide](./advanced.md) for more information.

<div class="annotate" markdown>
```hcl title="iam.tf"
locals {
    repositories = ["your-repository"]
    # This prefixes all repositories with the correct `principalSet` and attribute mapping.
    repository_principals = { for repository in local.repositories : repository => "${module.github_federation.repository_principal_set_id_prefix}/${repository}" }
}

data "google_project" "project" {}

resource "google_project_iam_member" "project" { (1)
  for_each = local.repository_principals
  project  = data.google_project.project.project_id
  role     = "roles/run.admin"
  member   = each.value
}

resource "google_service_account_iam_member" "cloud_run_v2" { (2)
  for_each = local.repository_principals

  service_account_id = "projects/${data.google_project.project.project_id}/serviceAccounts/${data.google_project.project.number}-compute@developer.gserviceaccount.com"
  role               = "roles/iam.serviceAccountUser"
  member             = each.value
}
```
</div>

Now run the following command to get the `GCP_WORKLOAD_IDENTITY_POOL`:

```sh
gcloud iam workload-identity-pools providers list --location=global --workload-identity-pool=github
```

This should return something like this which you will need to set as a Github secret in your repository.

```
projects/YOUR_PROJECT_ID/locations/global/workloadIdentityPools/github/providers/github-oidc
```

!!! success "Success"
    You have now setup the necessary resources to allow your Github repository to access your GCP project and to deploy your container to Google Cloud Run.

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
