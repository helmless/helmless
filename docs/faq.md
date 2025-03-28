---
title: Frequently Asked Questions
description: Explore the most common questions about Helmless.
icon: material/frequently-asked-questions
---

# FAQ

Here are some of the most common questions about Helmless.

!!! question "Not finding what you're looking for?"

    If you don't find what you're looking for, please [join the Discord server](/discord) and ask away!

??? faq "What is Helmless?"

    Helmless is a tool that allows you to deploy your application containers to Google Cloud Run using a simple YAML file.

    It's designed to be a simple and easy to use tool for deploying application containers to Google Cloud Run, without the need to have a Kubernetes cluster or use Terraform.

    [:octicons-arrow-right-24: Learn more](./why-helmless.md)

??? faq "Why not use Terraform?"

    Terraform is a great tool for managing infrastructure as code, but especially for frequent deployments it can quickly become a bottleneck. Infrastructure changes should be carefully managed and gated, and not be a part of the fast feedback loop that developers expect for deploying their own code as an application container.

    That's why we created Helmless.

    [:octicons-arrow-right-24: Learn more](./why-helmless.md#why-not-use-terraform)

??? faq "Why not use Kubernetes?"

    Kubernetes comes with lots of complexity and a high opportunity cost, especially for small teams. In addition, Google Cloud Run for example is a lot cheaper than running your own Kubernetes cluster.

    That doesn't mean that you should never use Kubernetes, but it there are (lots of) cases where it's not the best solution.

    Helmless provides an alternative to Kubernetes for bringing a similar developer experience to Google Cloud Run.

    [:octicons-arrow-right-24: Learn more](./why-helmless.md#why-not-use-kubernetes)

??? faq "Is Helmless available for other cloud providers, like AWS or Azure?"

    Helmless currently only supports Google Cloud Run, but any contributions are welcome!

    Join the [Discord server](/discord) to help us build Helmless for other cloud providers.

    [:octicons-arrow-right-24: Learn more](./contributing.md)

??? faq "How can I reference a Helmless Cloud Run Service in my Terraform code?"

    We provide a [Terraform module](https://github.com/helmless/google-cloudrun-service-terraform-module) that acts as a shell for the Helmless Cloud Run Service. This way you get the best of both worlds:

    - Simple and fast deployments directly from the CI/CD pipeline of your application
    - Terraform to manage the underlying infrastructure and permissions

    [:octicons-arrow-right-24: Learn more](./docs/cloudrun/terraform.md)

??? faq "How does Helmless authenticate with Google Cloud?"

    Helmless runs in your own CI/CD pipeline, so the authentication is completely up to you.

    However to make things easier, we provide a guide and Terraform modules to use [Workload Identity Federation with Github Actions](./docs/cloudrun/ci-cd.md) for authenticatation with Google Cloud.

    [:octicons-arrow-right-24: Learn more](./docs/cloudrun/terraform.md#workload-identity-federation)

??? faq "How can I deploy a Helmless Cloud Run Service to multiple regions?"

    Helmless currently only supports deploying to a single region, but this is on our list of features to add.

    Contributions are welcome!

    [:octicons-arrow-right-24: Learn more](./contributing.md)

??? faq "Can I use sidecars with Helmless?"

    Helmless currently does not support sidecars. But this is on our list of features to add.

    Contributions are welcome!

    [:octicons-arrow-right-24: Go to Issue #4](https://github.com/helmless/google-cloudrun-charts/issues/4)

??? faq "Does it support traffic splitting on new revisions?"

    Helmless currently does not support traffic splitting on new revisions.

    Contributions are welcome!

    [:octicons-arrow-right-24: Learn more](./contributing.md)

??? faq "Does it support all the features of Cloud Run?"

    Yes it does.

    With the exception of sidecars and traffic splitting on new revisions, Helmless supports all Cloud Run features.

    Contributions are welcome!

    [:octicons-arrow-right-24: Learn more](./contributing.md)

??? faq "How can I migrate from regular Terraform to Helmless?"

    Right now the migration is not fully automated, but we are working on creating a Helmless CLI to help with the migration.

    There is documentation on how to [migrate from Terraform to Helmless](./docs/cloudrun/migrate.md) in the Helmless Cloud Run Service documentation.

    [:octicons-arrow-right-24: Learn more](./docs/cloudrun/migrate.md)

??? faq "How hard is it to extend the chart / add features?"

    Both charts (Job and Service) are built on top of the [Google Cloud Run `common`](https://github.com/helmless/google-cloudrun-charts/tree/main/charts/cloudrun/common) library chart. This allows you to overwrite some of the helper functions to customize the chart to your needs.

    The other option would be to contribute or fork the individual charts and extend them to your needs.

    [:octicons-arrow-right-24: Learn more](./contributing.md)

??? faq "Can I template the chart locally first to see changes?"

    Yes you can!

    You can use the `helm template` command to template the chart locally first to see changes.

    [:octicons-arrow-right-24: Learn more](./docs/helmless/configuration.md)

??? faq "Can I deploy multiple services from the same pipeline?"

    Yes you can!

    See the [configuration guide](./docs/helmless/configuration.md) and [examples](./docs/cloudrun/examples.md) for more information.

    [:octicons-arrow-right-24: Learn more](./docs/helmless/configuration.md)

??? faq "Is there a way to plan changes like with Terraform?"

    Yes there is. You can use `dry_run` flag in the Github Action or the `--dry-run` flag in the `gcloud` CLI.

    A diff command is coming to the Helmless CLI to make it easier to review the changes.

    [:octicons-arrow-right-24: Learn more](./docs/cloudrun/ci-cd.md)

??? faq "Can I specify per environment settings for dev, prd,... ?"

    Yes you can provide multiple `values.yaml` files to the `helm template` command to specify per environment settings for dev, prd,...

    See the [configuration guide](./docs/helmless/configuration.md) for more information.

    [:octicons-arrow-right-24: Learn more](./docs/helmless/configuration.md)

??? faq "When not to use Helmless?"

    It comes down to your specific use-case, requirements and setup.

    Take a look at the [Adoption Guide](./docs/helmless/adopting.md) for more information.

    [:octicons-arrow-right-24: Learn more](./docs/helmless/adopting.md)
