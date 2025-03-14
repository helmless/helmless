# Google Cloud Run Common Chart

This chart contains common templates and functions for Google Cloud Run charts.

## Usage

Add it as a dependency to your chart:

```yaml
dependencies:
  - name: google-cloudrun-common
    version: "0.1.0"
    repository: "oci://ghcr.io/helmless/"
```

## Helpers

The following helpers are available:

- `helmless.cloudrun.image` - Returns the fully qualified image name.
- `helmless.cloudrun.region` - Returns the region from the values or uses the default: `us-central1`.
- `helmless.cloudrun.labels` - Returns a set of common labels adding chart metadata to the resources.
- `helmless.cloudrun.crossProjectSecrets` - Generates cross-project secrets annotation value
- `helmless.cloudrun.networkInterfaces` - Builds network interfaces configuration for Cloud Run
- `helmless.cloudrun.cloudsql` - Constructs CloudSQL connection string in format project:region:instance
- `helmless.cloudrun.env` - Sets environment variables for Cloud Run including secrets
- `helmless.cloudrun.volume` - Renders volume configuration based on type

The following validation functions are available:

- `helmless.cloudrun.validateCPU` - Validates CPU settings and returns error message if invalid
- `helmless.cloudrun.validateVolumes` - Validates volume names


## Testing

To test the chart, you can use the `helm-unittest` tool. Because library charts do not contain templates, a test chart is created under `tests/chart`.

```bash
helm dependency update tests/chart
helm unittest tests/chart
```

Add new tests to the `tests/chart/tests` directory and a rendering call to the helper inside a `tests/chart/templates/*.yaml` file. For example:

```yaml
image: {{- include "helmless.cloudrun.image" . }}
```

The dependency to the common chart in the test chart must be updated before running the tests.

```bash
helm dependency update tests/chart
```
