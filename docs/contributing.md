---
title: Contributing
description: Learn how to contribute to the Helmless project.
icon: material/handshake
---

<figure markdown="span">
  ![Helmless Logo](/assets/images/helmless.png){ width="50%" }
  <figcaption>WOW 😍<br/>
  Amazing to see you here!<br/>
  It is people like you that make the Helmless project possible.</figcaption>
</figure>


# Contributing

--8<-- "docs/_partials/wip.md"

We welcome any contributions to the Helmless project, be it code, documentation, helping out other users or just a friendly hello in our [Discord server][Discord].

## 🏗️ Repositories

To help organize the Helmless project, we have grouped the repositories by prefixing them with the cloud provider, e.g. `google-cloudrun-*`.

### 🪴 Core Repositories

- **[helmless](https://github.com/helmless/helmless)** - The Helmless homepage and documentation
- **[template-action](https://github.com/helmless/template-action)** - Basic GitHub Action for templating Helm charts, merging values on the fly

### 🚀 Google Cloud Run Repositories

- **[google-cloudrun-action](https://github.com/helmless/google-cloudrun-action)** - Deployment action for Google Cloud Run wrapping the `gcloud` CLI and [template-action](https://github.com/helmless/template-action)
- **[google-cloudrun-charts](https://github.com/helmless/google-cloudrun-charts)** - Helm charts for Google Cloud Run Jobs and Services
- **[google-cloudrun-service-terraform-module](https://github.com/helmless/google-cloudrun-service-terraform-module)** - Supporting Terraform module for creating a Helmless Google Cloud Run Service
- **[google-workload-identity-federation-terraform-module](https://github.com/helmless/google-workload-identity-federation-terraform-module)** - Supporting Terraform module for setting up GitHub Actions to deploy to Google Cloud Run using Workload Identity Federation

### 🗃️ Miscellaneous Repositories

- **[gcp-infrastructure](https://github.com/helmless/gcp-infrastructure)** - The GCP infrastructure for the Helmless project to setup the CI/CD end-to-end testing pipelines

## 🛠️ Tooling

We use [asdf](https://asdf-vm.com/) to manage the tools and dependencies and [pre-commit](https://pre-commit.com/) to check if everything is fine before committing.

To setup the development environment, install [asdf](https://asdf-vm.com/) and the following plugins:

```sh
asdf plugin add python
asdf plugin add helm
asdf plugin add helm-docs
asdf plugin add pre-commit
```

Then install the tools and dependencies:

```sh
asdf install
```

After that install the pre-commit hooks:

```sh
pre-commit install
```

## 🤝 Contributing to the Documentation

The documentation is built with [MkDocs for Material](https://squidfunk.github.io/mkdocs-material/) and hosted on [GitHub Pages](https://pages.github.com/).

To run the documentation locally, you can use the following command:

```bash
mkdocs serve
```

For more information on how to contribute to the documentation, please refer to the [CONTRIBUTING.md](https://github.com/helmless/helmless/blob/main/CONTRIBUTING.md) file of the `helmless` repository. That is the place where the documentation is built and hosted.

[Discord]: https://discord.gg/A5cjzfyAN5
