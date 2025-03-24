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

```yaml title="values.yaml"
global:
  common: &common
    name: helmless-service
    project: helmless
    region: europe-west1
service:
  <<: *common
  env:
    COLOR: 'blue'
  secrets:
    MY_SECRET: 'secret-key-in-gcp'
job:
  <<: *common
  name: helmless-job
  env:
    COLOR: 'red'
```

## Why **no** Kubernetes?

Helm, and for this project its templating feature, offers a great developer experience for managing containerized applications. However by default Helm is built for Kubernetes, which brings a lot of overhead and complexity for container-based deployments, where often times you don't need the full power of Kubernetes. And small teams and organizations often don't have the resources to maintain a production-grade Kubernetes cluster.

Helmless aims to give you the developer experience of Helm, without the overhead of Kubernetes.

## Why **no** Terraform?

Terraform is a great tool for managing infrastructure as code, but especially for frequent deployments it quickly becomes a bottleneck. Infrastructure changes should be carefully managed and gated, and not be a part of the fast feedback loop that developers expect for deploying their own code as an application container.

This is where Helmless comes in. It decouples the container deployment from the infrastructure deployment, and allows you to use the great developer experience of Helm for application deployments, while leaving the infrastructure management to other tools, like Terraform. By defining the container specification directly inside your application repository and by using the standard CI/CD pipeline, you can frequently deploy your application without waiting for the long approval process of infrastructure changes done in Terraform.
