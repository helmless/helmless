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

1. [What is Helmless?](https://helmless.io/docs/what-is-helmless/)
2. [Architecture Overview](https://helmless.io/docs/architecture/)
3. [Deploy to Google Cloud Run](https://helmless.io/docs/cloudrun/)

## 🏗️ Project Components

Helmless is organized into focused repositories:

- **[helmless](https://github.com/helmless/helmless)** - Charts Monorepo and Documentation
- **[template-action](https://github.com/helmless/template-action)** - GitHub Action for templating Helmless charts into cloud provider specific manifests
- **[google-cloudrun-deploy-action](https://github.com/helmless/google-cloudrun-deploy-action)** - Deployment action for Google Cloud Run
- **[google-cloudrun-tf-module](https://github.com/helmless/google-cloudrun-tf-module)** - Supporting Terraform module for Google Cloud Run
- **[google-workload-identity-tf-module](https://github.com/helmless/google-workload-identity-tf-module)** - Supporting Terraform module for Google Workload Identity setting up GitHub Actions to deploy to Google Cloud Run

## 🤝 Contributing

We welcome contributions! The documentation site is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/). To contribute:

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

⭐ If you find Helmless useful, please consider giving it a star! It helps the project grow and improve.
