---
title: What is Helmless?
description: Learn the core concepts and understand how Helmless simplifies serverless deployments.
---

# What is Helmless?

Helmless is a workflow and collection of resources that allows you to deploy serverless containers to Google Cloud Run, and potentially other platforms (1), with Helm, bypassing the complexity of Kubernetes and Terraform.
{ .annotate }

1.   :material-information-slab-circle: See the [extending to other platforms](./architecture.md#extending-to-other-platforms) page for more information.

It takes a container specification in the form of a Helm chart and a values file, and uses the templating feature of Helm to generate a Cloud Run configuration. This configuration is then deployed using the Cloud Run CLI.

--8<-- "docs/_partials/architectur-diagram.md"

Helmless gives you a powerful serverless deployment workflow that is very simple to use, yet flexible and extensible.

## Getting Started

--8<-- "docs/_partials/getting-started_grid.md"

## Why Helm?

Helm is a great tool for managing containerized applications, and its templating feature offers a great developer experience. It allows you to define your application container specification in a very simple YAML file and gives the platform teams an easy way to add abstraction and customization on top of it, making container-based deployments a breeze.

```yaml title=".hemless/values.yaml"
name: minimal-service
region: europe-west1
project: helmless
```

## Why **no** Kubernetes?

Helm, and for this project its templating feature, offers a great developer experience for managing containerized applications. However by default Helm is built for Kubernetes, which brings a lot of overhead and complexity for container-based deployments, where often times you don't need the full power of Kubernetes. And small teams and organizations often don't have the resources to maintain a production-grade Kubernetes cluster.

Helmless aims to give you the developer experience of Helm, without the overhead of Kubernetes.

## Why **no** Terraform?

Terraform is a great tool for managing infrastructure as code, but especially for frequent deployments it quickly becomes a bottleneck. Infrastructure changes should be carefully managed and gated, and not be a part of the fast feedback loop that developers expect for deploying their own code as an application container.

This is where Helmless comes in. It decouples the container deployment from the infrastructure deployment, and allows you to use the great developer experience of Helm for application deployments, while leaving the infrastructure management to other tools, like Terraform. By defining the container specification directly inside your application repository and by using the standard CI/CD pipeline, you can frequently deploy your application without waiting for the long approval process of infrastructure changes done in Terraform.


## Repositories

Helmless is open source and welcomes contributions! The project consists of several focused repositories:

- [helmless](https://github.com/helmless/helmless): _The home of [helmless.io](https://helmless.io)_
- [helmless/charts/cloudrun/service](https://github.com/helmless/helmless/tree/main/charts/cloudrun/service): _Helmless chart for a Google Cloud Run Service_
- [google-cloudrun-deploy-action](https://github.com/helmless/google-cloudrun-deploy-action): _Deployment action_
- [google-cloudrun-tf-module](https://github.com/helmless/google-cloudrun-tf-module): _Supporting infrastructure module_
- [google-workload-identity-tf-module](https://github.com/helmless/google-workload-identity-tf-module): _Identity and security module_
- [template-action](https://github.com/helmless/template-action): _GitHub Action for templating_
