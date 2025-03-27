---
title: Why Helmless?
description: Learn how Helmless works and why it's different from other tools.
icon: material/cloud
---

# Why Helmless?

Fast and easy deployments are critical for velocity. However, some organizations find Kubernetes too complex and Terraform too slow.

Helmless bridges this gap and provides fast and flexible deployments without requiring Kubernetes.

## 🚀 Faster Deployment Times

By switching to Helmless, you can reduce the time it takes to deploy your containers to Google Cloud Run from hours to minutes. Terraform is not built for fast iterations and continuous delivery. That however is exactly what you need for the deployment of your containers.

Helmless bypasses Terraform and directly integrates with your app repository. It uses Helm to render the Google Cloud Run manifest and then directly deploys it using the `gcloud` CLI.

<figure markdown="span">
  ![Deployment Times](/assets/images/helmless-deployment-times.png)
  <figcaption style="font-size: 0.8em;">*Manually setting the image tag from the app repository in a Terraform monorepository; waiting for plan preview and pull request review; repeating this process up to three times, once per stage.</figcaption>
</figure>

## ⭐ Higher Deployment Frequency

Helmless allows you to deploy your containers to Google Cloud Run at any time, without waiting for the long approval and preview process of infrastructure changes done in Terraform. It can be directly integrated into your CI/CD pipeline and unlocks the full potential of continuous delivery.

<figure markdown="span">
  ![Deployment Frequency Diagram](/assets/images/deployment-frequency.png){ width="75%" }
  <figcaption>By using Helmless, <strong>1KOMMA5°</strong> significantly improved deployment times and frequency to Google Cloud Run.</figcaption>
</figure>

## :material-rocket: Getting Started

<div class="grid cards" markdown>

-   :material-book-open-page-variant:{ .lg .middle } __What is Helmless?__

    ---

    Learn what Helmless is, how it works and why it's different from other tools.

    [:octicons-arrow-right-24: Learn more](./docs/index.md)

-   :material-cog-outline:{ .lg .middle } __Helmless Architecture__

    ---

    Understand the architecture, technical details behind Helmless, and how to extended it to other platforms.

    [:octicons-arrow-right-24: Understand the Architecture](./docs/architecture.md)

-   :material-rocket-launch:{ .lg .middle } __Deploy Your First Service__

    ---

    Get hands-on experience and deploy your first service to Google Cloud Run with Helmless

    [:octicons-arrow-right-24: Get Started](./docs/cloudrun/quickstart.md)

-   :material-code-braces:{ .lg .middle } __Examples__

    ---

    Explore real-world examples and sample configurations, including a complete CI/CD pipeline.

    [:octicons-arrow-right-24: View Examples](./docs/cloudrun/examples.md)

</div>

## :material-kubernetes: Why not Kubernetes?

Wether you need Kubernetes or not is your decision to make. However, if you decided that for the current state of your organization or platform Kubernetes is not the right choice, Helmless will help you to bring a similar developer experience to Google Cloud Run. All without the overhead of Kubernetes or slowness of Terraform.

## :material-terraform: Why not Terraform?

Terraform is a great tool for managing infrastructure. However, it's not built for fast iterations and continuous delivery. That however is exactly what you need for the deployment of your containers.

Helmless bypasses Terraform and directly integrates with your app repository. It uses Helm to render the Google Cloud Run manifest and then directly deploys it using the `gcloud` CLI.

## :simple-helm: Why Helm?

Helm is a great tool for deploying applications to Kubernetes. However, it's not built for Google Cloud Run.

Helmless uses Helm to render the Google Cloud Run manifest and then directly deploys it using the `gcloud` CLI. This way you can still benefit from the developer experience of Helm, while not having to deal with the complexity of Kubernetes.
