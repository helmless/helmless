---
title: 5min Quick Start
description: Deploy your first service to Google Cloud Run with Helmless in 5 minutes
---

# Quickstart: Deploy to Google Cloud Run

This tutorial will get you up and running with Helmless by deploying a simple "Hello World" container to Google Cloud Run.

!!! note "Time to complete"
    This tutorial will take approximately 5 minutes to complete.

## Prerequisites

You'll need:

- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) installed
- [Helm CLI](https://helm.sh/docs/intro/install/) installed
- A Google Cloud account with billing enabled

## Step 1: Set Up Your Environment

1. Login to Google Cloud:
   ```bash
   gcloud auth login
   ```

2. Set your project and region:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   gcloud config set run/region europe-west1  # or your preferred region
   ```

## Step 2: Create Your Service Configuration

1. Create a new directory for your service:
   ```bash
   mkdir -p my-first-service/helmless && cd my-first-service
   ```

2. Create a `helmless/values.yaml` file:
   ```bash
   cat <<EOF > helmless/values.yaml
   # yaml-language-server: \$schema=https://raw.githubusercontent.com/helmless/helmless/main/charts/cloudrun/service/values.schema.json
   name: hello-helmless
   region: $(gcloud config get run/region)
   project: $(gcloud config get project)
   image: 'us-docker.pkg.dev/cloudrun/container/hello'
   env:
      COLOR: 'blue'
   EOF
   ```

This is your service configuration. It defines everything about your service that would normally be defined via the GCP Console or Terraform.

!!! note "Helmless Chart Schema"
    You can find the full schema for the Google Cloud Run Service Helmless chart [here](/docs/cloudrun/schema).

## Step 3: Generate the Cloud Run Configuration

Run this command to template your service:

```bash
helm template oci://ghcr.io/helmless/google-cloudrun-service \
  -f helmless/values.yaml \
  > helmless/service.yaml
```

This will generate a `service.yaml` manifest in the GCP native format and will be used to deploy your service using the CLI.

## Step 4: Deploy Your Service

Deploy to Cloud Run:

```bash
gcloud run services replace helmless/service.yaml
```

That's it! Your service is now deployed to Google Cloud Run.

## Step 5: Test Your Service

1. Start the Cloud Run proxy:
   ```bash
   gcloud run services proxy hello-helmless
   ```

2. Open [http://localhost:8080](http://localhost:8080) in your browser

You should see a blue-themed "Hello World" page! 🎉

## Try Something New

Change the color of your service:

1. Update `COLOR` in `helmless/values.yaml`:
   ```yaml
   env:
     COLOR: 'green'  # change from 'blue' to 'green'
   ```

2. Re-run the template and deploy commands:
   ```bash
   helm template oci://ghcr.io/helmless/google-cloudrun-service \
     -f helmless/values.yaml \
     > helmless/service.yaml

   gcloud run services replace helmless/service.yaml
   ```

3. Refresh your browser to see the new color!

## Clean Up

When you're done, delete the service:

```bash
gcloud run services delete hello-helmless
```

## What's Next?

- [Deploy from GitHub Actions](../cloudrun/ci-cd.md)
- [Explore the full configuration options](../cloudrun/schema.md)
- [See more examples](./examples.md)
- [Learn more about Helmless](../helmless/what-is-helmless.md)
