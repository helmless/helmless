---
title: Migrate from Terraform to Helmless
description: Learn how to migrate from Terraform to Helmless
---

# Migrate from Terraform to Helmless

--8<-- "docs/_partials/wip.md"

This guide is a work in progress, but the basic steps are:

1. Export your current Cloud Run YAML configuration using `gcloud run services describe --format=yaml > service.yaml`
2. Map the YAML configuration to the Helmless Helm chart
3. Update your current Terraform Cloud Run module and add `lifecycle > ignore_changes` to make Helmless authoritative
4. Add the Helmless deployment to your CI/CD pipeline
