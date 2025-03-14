# helmless.io

[![📜 Docs](https://github.com/helmless/helmless/actions/workflows/deploy-docs.yaml/badge.svg)](https://helmless.io)
[![CloudRun Chart GitHub Release](https://img.shields.io/github/v/release/helmless/helmless?include_prereleases&label=google-cloudrun-service&color=blue)](https://github.com/helmless/google-cloudrun-chart/)
![GitHub Org's stars](https://img.shields.io/github/stars/helmless)

> Deploy serverless containers to cloud platforms with Helm's simplicity, bypassing the overhead of Kubernetes and Terraform.

## 🚀 What is Helmless?

Helmless gives you the power of GitOps workflows for serverless deployments without the complexity of Kubernetes or the overhead of Terraform. Think of it as "Helm for serverless" - familiar tools, simpler deployments.

### Key Features

- 🎯 **Kubernetes-like DX** - Familiar Helm-based workflows
- ⚡ **Lightning Fast** - Direct serverless deployments without K8s overhead
- 🌐 **Cloud Agnostic** - Works across major cloud providers
- 🤝 **Open Source** - Community-driven and built to evolve

## 🏃‍♂️ Quick Start

Visit [helmless.io](https://helmless.io) for comprehensive documentation, or jump right in:

1. [What is Helmless?](https://helmless.io/docs/getting-started)
2. [Architecture Overview](https://helmless.io/docs/helmless/architecture/)
3. [Deploy to Google Cloud Run](https://helmless.io/docs/cloudrun/)

## 🏗️ Project Components

Helmless is organized into focused repositories:

- **[helmless](https://github.com/helmless/helmless)** - Charts Monorepo and Documentation
- **[template-action](https://github.com/helmless/template-action)** - GitHub Action for templating Helmless charts into cloud provider specific manifests
- **[google-cloudrun-deploy-action](https://github.com/helmless/google-cloudrun-deploy-action)** - Deployment action for Google Cloud Run
- **[google-cloudrun-service-terraform-module](https://github.com/helmless/google-cloudrun-service-terraform-module)** - Supporting Terraform module for Google Cloud Run
- **[google-workload-identity-federation-terraform-module](https://github.com/helmless/google-workload-identity-federation-terraform-module)** - Supporting Terraform module for Google Workload Identity setting up GitHub Actions to deploy to Google Cloud Run

## 🤝 Contributing

You want to contribute to Helmless? Great ❤️!
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

### 📜 Documentation

The documentation site is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

To setup the development environment, install [Python](https://www.python.org/) using asdf and the following dependencies:

```sh
pip install -r docs/requirements.txt
```

To run the documentation site locally, run:

```sh
mkdocs serve
```

All primary documentation is located in the `docs/docs/` folder and written in [Markdown](https://www.markdownguide.org/) with some additional files for the website.

The Chart schemas are written in [JSON Schema](https://json-schema.org/) and are located in the `charts/` folder and rendered using a [custom mkdocs plugin](docs/_hooks/schema_renderer.py).

### ⚙️ Helm Charts

All charts are written schema and test first and use [helm-unittest](https://github.com/helm-unittest/helm-unittest) to test the charts. To setup the testing environment, install the helm-unittest plugin:

```sh
helm plugin install https://github.com/helm-unittest/helm-unittest.git
```

To run the tests for a chart, navigate to the chart directory and run:

```sh
helm unittest .
```

To update the snapshot tests, run:

```sh
helm unittest . -u
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

⭐ If you find Helmless useful, please consider giving it a star! It helps the project grow and improve.
