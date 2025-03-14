# Helmless Chart for Google Cloud Run Job

This Helm chart helps you create Google Cloud Run Job manifests that can be deployed using the Google Cloud CLI.

## Features

- Basic job configuration (name, project, region)
- Container image configuration (supports direct and split references)
- Task parallelism and count configuration
- Environment variables and secrets management
- Timeout and retry configuration

## Installation

```bash
helm repo add helmless https://charts.helmless.dev
helm repo update
```

## Usage

Create a values.yaml file:

```yaml
name: my-job
project: my-project
image: ghcr.io/my-org/my-image:latest

# Optional configurations
taskCount: 5
parallelism: 3
timeoutSeconds: 300

env:
  MY_ENV_VAR: my-value

secrets:
  API_KEY: my-secret
  DB_PASSWORD:
    secret: db-password
    version: '2'
```

Then install the chart:

```bash
helm install my-job helmless/cloudrun-job -f values.yaml
```

## Configuration

| Parameter        | Description                      | Default       |
| ---------------- | -------------------------------- | ------------- |
| `name`           | Name of the Cloud Run Job        | Required      |
| `project`        | Google Cloud project ID          | Required      |
| `region`         | Google Cloud region              | `us-central1` |
| `image`          | Container image reference        | Required      |
| `taskCount`      | Number of tasks to execute       | `1`           |
| `parallelism`    | Maximum number of parallel tasks | `1`           |
| `timeoutSeconds` | Task timeout in seconds          | `600`         |
| `maxRetries`     | Maximum number of retries        | `3`           |
| `env`            | Environment variables            | `{}`          |
| `secrets`        | Secret Manager secrets           | `{}`          |

For more detailed configuration options, please refer to the [values.schema.json](values.schema.json) file.
