---
title: Frequently Asked Questions
description: Explore the most common questions about Helmless.
icon: material/frequently-asked-questions
---

# FAQ

## Why use Helm?

Helm is a great tool for managing containerized applications, and its templating feature offers a great developer experience. It allows you to define your application container specification in a very simple YAML file and gives the platform teams an easy way to add abstractions and customizations on top of it, making container-based deployments a breeze.

However by default Helm is built for Kubernetes, which brings a lot of overhead and complexity for container-based deployments, where often times you don't need the full power of Kubernetes. And small teams and organizations often don't have the resources to maintain a production-grade Kubernetes cluster.

Helmless aims to give you the developer experience of Helm, without the overhead of Kubernetes. It does this by only using Helm's templating feature, linting and schema validation and not the full Helm CLI.

## :material-kubernetes: Why **no** Kubernetes?

Every team and organization is different, and so are their infrastructure and application requirements. Kubernetes is a great tool for managing containerized applications, but it's not the only tool for the job. And often times you don't need the full power of Kubernetes. But in the end, it's up to you to decide what's best for your team and organization.

Helmless just offers a different path to deploy your application containers, without the need to have a Kubernetes cluster or use Terraform.

## :material-terraform: Why **no** Terraform?

Terraform is a great tool for managing infrastructure as code, but especially for frequent deployments it can quickly become a bottleneck. Infrastructure changes should be carefully managed and gated, and not be a part of the fast feedback loop that developers expect for deploying their own code as an application container.

With the increasing size of the stack, the plan and apply times of Terraform can quickly become a bottleneck.

But we also recognize that you still need to somehow link the application container to the underlying infrastructure. This is why we created the [helmless/google-cloudrun-service-terraform-module](https://github.com/helmless/google-cloudrun-service-terraform-module) that creates a [Terraform shell for your application container](./docs/cloudrun/terraform.md), which you can then use in your Terraform code to link the application container to the underlying infrastructure.
