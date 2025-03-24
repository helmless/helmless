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
