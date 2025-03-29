---
title: 5min Quick Start
description: Deploy your first service to Google Cloud Run with Helmless in 5 minutes
icon: material/timer-outline
---

# Quickstart: Deploy to Google Cloud Run

   version: 1.0.0
   repository: oci://ghcr.io/helmless
   alias: service
- name: google-cloudrun-job
   version: 1.0.0
   repository: oci://ghcr.io/helmless
   alias: job


## Prerequisites

You'll need:

- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) installed
- [Helm CLI](https://helm.sh/docs/intro/install/) installed
- A Google Cloud account with billing enabled and the `roles/run.admin` role

## Your First Helmless Application

### Step 1: Set Up Your Environment

1. Login to Google Cloud:
   ```bash
   gcloud auth login
   ```

2. Set your project and region:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   gcloud config set run/region europe-west1  # or your preferred region
   ```

### Step 2: Create Your Application Chart

Create a new directory for your service and initialize a Helm chart:

```bash
helm create helmless && cd helmless
rm -rf helmless/templates/* && rm -f helmless/values.yaml
echo "output" >> .gitignore
```


### Step 3: Add the Helmless Charts

You now need to add the Helmless charts as dependencies to your application chart.

<div class="annotate" markdown>
1. Add the Helmless chart to your service:
   ```bash
   cat <<EOF >> Chart.yaml

   dependencies:
     - name: google-cloudrun-service (1)
       version: 1.0.0
       repository: oci://ghcr.io/helmless
       alias: service (2)
   EOF
   ```
2. Run `helm dependency update` to update the dependencies:
   ```bash
   helm dependency update
   ```
</div>

1. This adds the Helmless [Google Cloud Run Service chart](../schemas/index.md) as a dependency to your application chart.
2. This aliases the Helmless chart as `service` so we can refer to it in the `values.yaml` file.

### Step 4: Configure Your Service

Now you can configure your service using the `values.yaml` file.

<div class="annotate" markdown>
```bash
cat <<EOF > values.yaml
global:
  region: "$(gcloud config get run/region)"
  project: "$(gcloud config get project)"
service:
  name: hello-helmless (1)
  image:
    name: "cloudrun/container/hello"
    repository: "us-docker.pkg.dev"
    tag: "latest"
  env:
    COLOR: "blue" (2)
EOF
```
</div>

1. This is the name of your service, which must be unique within your project and region combination.
2. This is an environment variable that will be set in the container.

!!! note "Google Cloud Run Service Schema"
    You can find the full schema for the Google Cloud Run Service [here](../schemas/index.md).

### Step 5: Template the Cloud Run Service Manifest

Next, you can template the Cloud Run Service manifest using the `helm template` command.

```bash
helm template --output-dir output .
```

This will generate a `service.yaml` manifest in the `output` directory that can be used to deploy your service using the `gcloud` CLI.

### Step 6: Deploy Your Service

You can now deploy your service using the `gcloud` CLI.

```bash
gcloud run services replace output/**/service.yaml
```

That's it! Your service is now deployed to Google Cloud Run.

### Step 7: Test Your Service

1. Start the Cloud Run proxy:
   ```bash
   gcloud run services proxy hello-helmless
   ```
<!-- markdown-link-check-disable-next-line -->
2. Open [http://localhost:8080](http://localhost:8080) in your browser

You should see a blue-themed "Hello World" page! 🎉

### Step 8: Add a Second Environment

Let's simulate a development environment by adding a `values.dev.yaml` file.

1. Create a `values.dev.yaml` file:
   ```bash
   cat <<EOF > values.dev.yaml
   service:
     env:
       COLOR: "green"
   EOF
   ```

2. Re-run the template with the new values:
   ```bash
   helm template --output-dir output -f values.dev.yaml .
   ```

3. Deploy the new manifest:
   ```bash
   gcloud run services replace output/**/service.yaml
   ```

4. Refresh your browser to see the new color!

## Clean Up

When you're done, delete the service:

```bash
gcloud run services delete hello-helmless
```

## What's Next?

<div class="grid cards" markdown>

-   :simple-githubactions:{ .lg .middle } __CI/CD with Github Actions__

    ---

    Learn how to deploy your Helmless chart using Github Actions.

    [:octicons-arrow-right-24: Learn More](./ci-cd.md)

-   :material-file-document-outline:{ .lg .middle } __Cloud Run Schemas__

    ---

    See the full schema for the Google Cloud Run Service and Job.

    [:octicons-arrow-right-24: View Schema](../schemas/index.md)

-   :material-code-braces:{ .lg .middle } __Examples__

    ---

    See an example of a Helmless chart for Google Cloud Run.

    [:octicons-arrow-right-24: View Examples](./examples.md)

-   :material-information-outline:{ .lg .middle } __Architecture__

    ---

    Learn more about Helmless and how it works.

    [:octicons-arrow-right-24: Learn More](../helmless/architecture.md)

</div>
