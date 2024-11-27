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

## Setting up the Configuration

Helmless uses the Helm pattern of a `values.yaml` file to configure the service. You can store this anywhere in your repository, but for this example we will use the `config` directory.

Create a `config/values.yaml` file, with the following content:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/helmless/cloudrun/main/values.schema.json
name: tutorial-service
image: 'us-docker.pkg.dev/cloudrun/container/hello'
env:
  COLOR: 'blue'
```

- `yaml-language-server` is used to provide syntax highlighting and validation for the `values.yaml` file
- `name` is the name of the service and must be unique per project
- `image` is the URL to the Docker image you want to deploy
- `env` is an optional set of environment variables to pass to the service

!!! info "Full Chart Specification"
    You can find the full chart specification and all supported configuration options [on GitHub][chart].

## Deploying the Service

To deploy the service you need to template the Helm chart into a Cloud Run service and then use the Google Cloud CLI to deploy it.

### Templating the Helm Chart

Use `helm template` command and our custom [Helmless Cloud Run chart][chart] to template your `values.yaml` into a **Cloud Run YAML**[^1] specification.

```sh
helm template oci://ghcr.io/helmless/cloudrun -f config/values.yaml --output-dir out/
```

- `helm template` is the [command to template a Helm chart](https://helm.sh/docs/helm/helm_template/)
- `oci://ghcr.io/helmless/cloudrun` is the URL to our [Helmless Cloud Run chart][chart] in GitHub Container Registry
- `-f config/values.yaml` uses the `values.yaml` file in the `config` directory as the configuration for the service
- `--output-dir out/` writes the templated Cloud Run YAML specification to the `out` directory

You should now have a `out/cloudrun/templates/cloudrun.yaml` file that looks like this:

??? example "View the complete YAML output"
    ```yaml
    ---
    # Source: cloudrun/templates/cloudrun.yaml
    apiVersion: serving.knative.dev/v1
    kind: Service
    metadata:
        name: tutorial-service
        labels:
        annotations:
          run.googleapis.com/launch-stage: GA
          run.googleapis.com/ingress: all
          run.googleapis.com/region: europe-west1
      spec:
        template:
          metadata:
            annotations:
              run.googleapis.com/execution-environment: gen2
              run.googleapis.com/cpu-throttling: "true"
              autoscaling.knative.dev/maxScale: "100"
          spec:
            containerConcurrency: 80
            timeoutSeconds: 300
            containers:
              - image: us-docker.pkg.dev/cloudrun/container/hello
                env:
                  - name: "COLOR"
                    value: "blue"
                resources:
                  limits:
                    cpu: "1"
                    memory: "512Mi"
                ports:
                  - containerPort: 8080
                livenessProbe:
                  failureThreshold: null
                  httpGet:
                    path: /
                    port: 8080
                  initialDelaySeconds: null
                  periodSeconds: null
                readinessProbe:
                  failureThreshold: null
                  httpGet:
                    path: /
                    port: 8080
                  initialDelaySeconds: null
                  periodSeconds: null
                startupProbe:
                  failureThreshold: null
                  httpGet:
                    path: /
                    port: 8080
                  initialDelaySeconds: null
                  periodSeconds: null
    ```

### Deploying the Service

Use the Google Cloud CLI to deploy the templated Cloud Run YAML specification to Google Cloud Run.

First login to Google Cloud and set the project and region[^2] you want to deploy the service to.

```sh
gcloud auth login
gcloud config set project <your-project-id>
gcloud config set run/region <your-region> # e.g. europe-west1
```

Then deploy the service using the `gcloud run services replace` command.

```sh
gcloud run services replace out/cloudrun/templates/cloudrun.yaml
```

You should see an output like the following:

```text
Applying new configuration to Cloud Run service [tutorial-service] in project [...] region [...]
✓ Deploying new service... Done.
  ✓ Creating Revision...
  ✓ Routing traffic...
Done.
New configuration has been applied to service [tutorial-service].
URL: https://tutorial-service-836227714099.europe-west1.run.app
```

But when you navigate to the URL you'll see a `Error: Forbidden` page. This is because the service is not publicly accessible by default.

To access your service locally without exposing it to the public internet, you can use [Cloud Run proxy](https://cloud.google.com/run/docs/authenticating/developers).

```sh
gcloud run services proxy tutorial-service
```

!!! success "Tada! 🥳"
    You can now see your Cloud Run service in action when navigating to [`http://localhost:8080`](http://localhost:8080).

### Cleaning up

You can delete the service using the `gcloud run services delete` command.

```sh
gcloud run services delete tutorial-service
```

## Next Steps

From here you can head back to the [overview](../what-is-helmless.md) to learn more about Helmless for Google Cloud Run or jump to the next guide to learn how to [deploy from a CI/CD pipeline](./ci-cd.md) using Github Actions.


--8<-- "docs/_partials/getting-started_grid.md"


[^1]: The [Cloud Run YAML specification](https://cloud.google.com/run/docs/reference/yaml/v1) is just a standard [Knative](https://knative.dev/) Service specification under the hood.
[^2]: The region must be a valid Google Cloud Run region. You can choose a region using the [region picker](https://cloud.withgoogle.com/region-picker/).

[chart]: https://github.com/helmless/google-cloudrun-chart
