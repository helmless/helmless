---
title: Getting Started
description: Learn how to deploy a simple Hello World image to Google Cloud Run using Helmless.
---

# Getting Started

In this guide you will learn how to deploy a simple Hello World image to Google Cloud Run using Helmless. Read [what is Helmless](../what-is-helmless.md) first if you want to understand how it works. See the [architecture](../architecture.md) for more information on how to adopt it to other cloud providers.

Deploying from a CI/CD pipeline is covered in a [later guide](./ci-cd.md).

## Prerequisites

- A Google Cloud account
- The [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
- The [Helm CLI](https://helm.sh/docs/intro/install/)

Make sure you have a Google Cloud project ready. If you don't have one yet, create a new one using the [Google Cloud Console](https://console.cloud.google.com/projectcreate).

## Deploying Your First Helmless Service

<div class="annotate" markdown>
First login to Google Cloud and set the project and region you want to deploy the service to. (1)

```sh
gcloud auth login
gcloud config set project <your-project-id>
gcloud config set run/region <your-region> # e.g. europe-west1
```

After that create a `helmless/values.yaml` file, with the following content: (2)

```bash
cat <<EOF > helmless/values.yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/helmless/helmless/main/charts/cloudrun/service/values.schema.json
name: helmless-service
region: europe-west1
image: 'us-docker.pkg.dev/cloudrun/container/hello'
env:
  COLOR: 'blue'
EOF
```

!!! info "Full Chart Specification"
    You can find the full chart specification and all supported configuration options in the [chart schema](./schema.md).

Then run `helm template` to template the Helm chart into a Cloud Run service manifest. (3)

```bash
helm template oci://ghcr.io/helmless/google-cloudrun-service \
  -f helmless/values.yaml \
  > helmless/google-cloudrun-service.manifest.yaml
```

Now you only need to deploy the templated Cloud Run service manifest to Google Cloud Run using the Google Cloud CLI.

```bash
gcloud run services replace helmless/google-cloudrun-service.manifest.yaml
```

!!! success "Tada! 🥳"
    You can now see your Cloud Run service in action when starting the Cloud Run proxy and navigating to [`http://localhost:8080`](http://localhost:8080). (4)
    ```bash
    gcloud run services proxy helmless-service
    ```
</div>

1.   Setting the project and region is only required when deploying locally. When deploying from a CI/CD pipeline the project and region are automatically extracted from the rendered manifest.
2.   Helmless uses the Helm pattern of a `values.yaml` file to configure the service. You can store this anywhere in your repository, but for this example we will use the `helmless` directory.
3.   `helm template` is the [command to template a Helm chart](https://helm.sh/docs/helm/helm_template/) and in Helmless used to create create a cloud provider specific service manifest.
4.   By default Cloud Run services are not publicly accessible, so you need to start the [Cloud Run proxy](https://cloud.google.com/run/docs/authenticating/developers) to access the service locally.


### Cleaning up

You can delete the service using the `gcloud run services delete` command.

```sh
gcloud run services delete helmless-service
```

## Next Steps

From here you can head back to the [overview](../what-is-helmless.md) to learn more about Helmless for Google Cloud Run or jump to the next guide to learn how to [deploy from a CI/CD pipeline](./ci-cd.md) using Github Actions.


--8<-- "docs/_partials/getting-started_grid.md"

[chart]: https://github.com/helmless/google-cloudrun-chart
