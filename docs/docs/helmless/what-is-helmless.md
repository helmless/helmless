---
title: What is Helmless?
description: Learn the core concepts and understand how Helmless simplifies serverless deployments.
---

# What is Helmless?

Helmless is a workflow and collection of resources that allows you to deploy serverless containers to Google Cloud Run, and potentially other platforms (1), with Helm, bypassing the complexity of Kubernetes and Terraform.
{ .annotate }

1.   :material-information-slab-circle: See the [extending to other platforms](./architecture.md) page for more information.

It takes a container specification in the form of a Helm chart and a values file, and uses the templating feature of Helm to generate a Cloud Run manifest. This manifest is then deployed using the `gcloud` CLI.

--8<-- "docs/_partials/architectur-diagram.md"

Helmless gives you a powerful serverless deployment workflow that is very simple to use, yet flexible and extensible. It can be easily integrated into your existing CI/CD pipeline and is fully compatible with Helm charts and all tooling surrounding it.

## Getting Started

<div class="grid cards" markdown>

-   :material-book-open-page-variant:{ .lg .middle } __Why Helmless?__

    ---

    Not convinced yet? Learn why you should use Helmless and why it's different from other tools.

    [:octicons-arrow-right-24: Learn the WHY](/docs/helmless/)

-   :material-cog-outline:{ .lg .middle } __Helmless Architecture__

    ---

    Understand the architecture, technical details behind Helmless, and how to extended it to other platforms.

    [:octicons-arrow-right-24: Understand the Architecture](/docs/helmless/architecture)

-   :material-rocket-launch:{ .lg .middle } __Deploy Your First Service__

    ---

    Get hands-on experience and deploy your first service to Google Cloud Run with Helmless

    [:octicons-arrow-right-24: Get Started](/docs/getting-started/quickstart)

-   :material-code-braces:{ .lg .middle } __Examples__

    ---

    Explore real-world examples and sample configurations, including a complete CI/CD pipeline.

    [:octicons-arrow-right-24: View Examples](/docs/getting-started/examples)

</div>



## Repositories

Helmless is open source and welcomes contributions! The project consists of several focused repositories:

- [helmless](https://github.com/helmless/helmless): _The home of [helmless.io](https://helmless.io)_
- [helmless/charts/cloudrun/service](https://github.com/helmless/helmless/tree/main/charts/cloudrun/service): _Helmless chart for a Google Cloud Run Service_
- [google-cloudrun-deploy-action](https://github.com/helmless/google-cloudrun-deploy-action): _Deployment action_
- [google-cloudrun-service-terraform-module](https://github.com/helmless/google-cloudrun-service-terraform-module): _Supporting infrastructure module_
- [google-workload-identity-federation-terraform-module](https://github.com/helmless/google-workload-identity-federation-terraform-module): _Identity and security module_
- [template-action](https://github.com/helmless/template-action): _GitHub Action for templating_
