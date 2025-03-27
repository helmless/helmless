---
title: Terraform
description: Use Terraform to link your application container to the underlying infrastructure.
icon: material/terraform
---

# Terraform

Helmless provides a Terraform shell for your application container, which you can then use in your Terraform code to link the application container to the underlying infrastructure. It does this by using the `lifecycle > ignore_changes` block of the Terraform resource, ignoring all fields that are managed by Helmless.

You can either use the Helmless modules directly or create your own shell.

## Helmless Cloud Run Service Terraform Module

The Helmless Cloud Run Service Terraform Module is a Terraform module that is used to create a shell for your application container. It is located in the [helmless/google-cloudrun-service-terraform-module](https://github.com/helmless/google-cloudrun-service-terraform-module) repository.

```hcl
--8<-- "https://raw.githubusercontent.com/helmless/google-cloudrun-service-terraform-module/refs/heads/main/example/main.tf"
```

The workload identity federation is used to securely connect Github Actions to GCP and give it the necessary permissions to deploy the application container. See below or in the [CI/CD](./ci-cd.md) documentation for more details.

### Creating your own shell

If you don't want to use the Helmless Cloud Run Service Terraform Module, you can create your own shell by using the `lifecycle > ignore_changes` block of the Terraform resource.

```hcl
resource "google_cloud_run_v2_service" "cloud_run_service" {
  ...
  # This will make the app pipeline with Helmless the authoritive source of truth for the service.
  lifecycle {
    ignore_changes = [
      binary_authorization,
      client,
      client_version,
      description,
      ingress,
      labels,
      launch_stage,
      template,
      traffic,
    ]
  }
}
```

A module for the job is in progress, for now you can use the same approach and make the module yourself. Contributions are welcome!

```hcl
resource "google_cloud_run_v2_job" "cloud_run_job" {
  ...
  lifecycle {
    ignore_changes = [
      binary_authorization,
      client,
      client_version,
      labels,
      launch_stage,
      location,
      template,
    ]
  }
}
```

## Workload Identity Federation

To allow your Github organization to access your GCP organization, you need to setup [Github Workload Identity Federation](https://cloud.google.com/blog/products/identity-security/enabling-keyless-authentication-from-github-actions) once somewhere in a project of your organization.

To make this as easy as possible, we created a small [Terraform module](https://github.com/helmless/google-workload-identity-federation-terraform-module) that can be used to setup the necessary resources in your GCP project.

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

### Creating Cloud Run Services with IAM

After setting up the workload identity federation, you can create the individual Cloud Run services and grant your Github repositories the necessary permissions to deploy to them.

!!! info "principalSet"
    The `principalSet` is similar to a `serviceAccount` but is tightly coupled to a workload identity pool. It is the safest way to grant permissions to a repository.
    You can use this for more than just Cloud Run, it can be used for [almost any resource](https://cloud.google.com/iam/docs/federated-identity-supported-services) in GCP.
    The [helmless/google-workload-identity-federation-terraform-module//repository](https://github.com/helmless/google-workload-identity-federation-terraform-module/tree/main/repository) sub module takes care of creating the somewhat complicated format of the `principalSet` for you.

<div class="annotate" markdown>
```hcl title="cloudrun.tf"
--8<-- "https://raw.githubusercontent.com/helmless/gcp-infrastructure/refs/heads/main/stacks/e2e-tests/cloudrun.tf"
```
</div>

1. Use your own `github_organization` and `repositories` to create the correct `principalSet` for your repositories.
2. This name must match the `name` in the [values.yaml](./values.md) of your Helmless deployment.
3. The deployment account is a list of repository principals that will be granted the `roles/run.admin` role on the Cloud Run service in order to deploy it. In a real scenario this will just be one repository.
4. By default the module will create a new service account just for the Cloud Run service. This is best practice as it allows you to scope the permissions to the individual service account. You must set the `serviceAccountName` in your [values.yaml](./values.md) to use this.

### Project wide permissions

You can also grant your repositories project wide permissions to create and deploy Cloud Run services. This is more permissive and should only be used in a development environment or for dynamic creation of feature branch deployments for example. By default Helmless will create the Cloud Run service if it doesn't exist yet.

<div class="annotate" markdown>
```hcl title="cloud_deploy.tf"
--8<-- "https://raw.githubusercontent.com/helmless/gcp-infrastructure/refs/heads/main/stacks/github-federation/project_iam.tf"
```
</div>

1. Use your own `github_organization` and `repositories` to create the correct `principalSet` for your repositories.
2. This grants every repository listed above the `roles/run.admin` role in the whole GCP project.
3. This is the default Cloud Run service account used if no specific service account is specified in the [values.yaml](./values.md).
4. The `roles/iam.serviceAccountUser` is required by Cloud Run to deploy the service.

!!! success "Success"
    You have now setup the necessary resources to allow your Github repository to access your GCP project and to deploy your container to Google Cloud Run.
