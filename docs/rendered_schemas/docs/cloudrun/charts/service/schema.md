---
title: CloudRun Helm Chart
description: A Helm chart to template the manifest of a Cloud Run service or job.
---

# CloudRun Helm Chart

A Helm chart to template the manifest of a Cloud Run service or job.


```yaml
None:
  name: my-service
  image: ghcr.io/my-org/my-image@sha256:abc123
  autoscaling:
    minScale: 0
```

## <!-- md:setting values.name -->

<!-- md:deprecated -->
<!-- md:version 0.1.0 -->
<!-- md:type `string` -->
<!-- md:maxLength 63 -->
<!-- md:pattern `^[a-z0-9]([-a-z0-9]*[a-z0-9])?$` -->
<!-- md:default none -->
<!-- md:flag required -->

Name of the Cloud Run Service to deploy. Must be unique within the project region combination.

```yaml
name: my-service
```

## <!-- md:setting values.description -->

<!-- md:version 0.1.0 -->
<!-- md:type `string` -->
<!-- md:default none -->

A human-readable description of the CloudRun service.

```yaml
description: My service does xyz.
```

## <!-- md:setting values.image -->

<!-- md:version 0.1.0 -->
<!-- md:type `object`, `string` -->
<!-- md:default none -->
<!-- md:flag required -->

Container image to deploy. You can provide a direct reference to an image using a `string` or split up the inputs using the `object`.

=== "Direct image reference"
    ```yaml
    image: ghcr.io/my-org/my-image@sha256:abc123
    ```
=== "Split image reference"
    ```yaml
    image:
      repository: ghcr.io/my-project
      name: my-image
    ```
=== "Split image reference with tag and registry"
    ```yaml
    image:
      registry: ghcr.io
      repository: my-project
      name: my-image
      tag: 1.0.0
    ```


### <!-- md:setting values.image.name -->

<!-- md:version 0.1.0 -->
<!-- md:type `string` -->
<!-- md:default none -->

Container image name.

```yaml
image.name: my-image
```

### <!-- md:setting values.image.registry -->

<!-- md:version 0.1.0 -->
<!-- md:type `string` -->
<!-- md:default none -->

Container image registry.

```yaml
image.registry: gcr.io
```

### <!-- md:setting values.image.repository -->

<!-- md:version 0.1.0 -->
<!-- md:type `string` -->
<!-- md:default none -->

Container image repository.

=== "gcr.io/my-project"
    ```yaml
    image.repository: gcr.io/my-project
    ```
=== "my-project # if used with a registry"
    ```yaml
    image.repository: my-project # if used with a registry
    ```

### <!-- md:setting values.image.tag -->

<!-- md:version 0.1.0 -->
<!-- md:type `string` -->
<!-- md:default `latest` -->

Container image tag.

=== "latest"
    ```yaml
    image.tag: latest
    ```
=== "@sha256:abc123"
    ```yaml
    image.tag: @sha256:abc123
    ```
=== "1.0.0"
    ```yaml
    image.tag: 1.0.0
    ```

## <!-- md:setting values.command -->

<!-- md:version 0.1.0 -->
<!-- md:type `array` -->
<!-- md:default `[]` -->

Command that runs when the container starts.

```yaml
command: ['echo', 'Hello, world!']
```

## <!-- md:setting values.args -->

<!-- md:version 0.1.0 -->
<!-- md:type `array` -->
<!-- md:default `[]` -->

Arguments to pass to the command.

```yaml
args: ['--help']
```

## <!-- md:setting values.autoscaling -->

<!-- md:version 0.1.0 -->
<!-- md:type `object` -->
<!-- md:default none -->

=== "Default"
    ```yaml
    autoscaling:
      minScale: 1
      maxScale: 100
      maxConcurrentRequests: 80
    ```
=== "Scale to zero"
    ```yaml
    autoscaling:
      minScale: 0
      maxScale: 100
      maxConcurrentRequests: 80
    ```


### <!-- md:setting values.autoscaling.maxConcurrentRequests -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer` -->
<!-- md:default `80` -->

The number of concurrent requests per instance. Controls how many requests are processed before the autoscaler scales up. Setting this to 1 means 1 request per instance at a time.

### <!-- md:setting values.autoscaling.maxScale -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer` -->
<!-- md:default `100` -->

Maximum number of replicas to scale up to.

### <!-- md:setting values.autoscaling.minScale -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer` -->
<!-- md:default `1` -->

Minimum number of replicas to scale down to. 0 enables scale to zero.

## <!-- md:setting values.containerPort -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer` -->
<!-- md:default none -->

Container port to expose. In CloudRun only a single port can be exposed and defaults to 8080.

## <!-- md:setting values.env -->

<!-- md:version 0.1.0 -->
<!-- md:type `object` -->
<!-- md:default none -->

Environment variables to set in the CloudRun container.


## <!-- md:setting values.executionEnvironment -->

<!-- md:version 0.1.0 -->
<!-- md:type `string` -->
<!-- md:default none -->

The execution environment to use for the CloudRun container. Must be either 'gen2' or 'gen1'.

## <!-- md:setting values.ingress -->

<!-- md:version 0.1.0 -->
<!-- md:type `string` -->
<!-- md:default none -->

The ingress settings for the CloudRun service. Controls where the service can be accessed from.

## <!-- md:setting values.labels -->

<!-- md:version 0.1.0 -->
<!-- md:type `object` -->
<!-- md:maxLength 63 -->
<!-- md:pattern `^[a-z0-9]([-a-z0-9]*[a-z0-9])?$` -->
<!-- md:default none -->

Labels to add to the CloudRun container. Must conform to the CloudRun label schema.


## <!-- md:setting values.launchStage -->

<!-- md:version 0.1.0 -->
<!-- md:type `string` -->
<!-- md:default none -->

The launch stage of the CloudRun service. Controls feature availability and SLA.

## <!-- md:setting values.livenessProbe -->

<!-- md:version 0.1.0 -->
<!-- md:type `object` -->
<!-- md:default none -->

Configuration for liveness probe health checking.


### <!-- md:setting values.livenessProbe.failureThreshold -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer`, `null` -->
<!-- md:default none -->

Number of consecutive failures before considering the container unhealthy.

### <!-- md:setting values.livenessProbe.httpGet -->

<!-- md:version 0.1.0 -->
<!-- md:type `object` -->
<!-- md:default none -->

HTTP GET probe configuration.


#### <!-- md:setting values.livenessProbe.httpGet.path -->

<!-- md:version 0.1.0 -->
<!-- md:type `string` -->
<!-- md:default none -->

Path to probe for HTTP health check.

#### <!-- md:setting values.livenessProbe.httpGet.port -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer`, `string` -->
<!-- md:default none -->

Port to probe for HTTP health check.

### <!-- md:setting values.livenessProbe.initialDelaySeconds -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer`, `null` -->
<!-- md:default none -->

Number of seconds to wait before starting probe checks.

### <!-- md:setting values.livenessProbe.periodSeconds -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer`, `null` -->
<!-- md:default none -->

How often to perform probe checks.

## <!-- md:setting values.readinessProbe -->

<!-- md:version 0.1.0 -->
<!-- md:type `object` -->
<!-- md:default none -->

Configuration for readiness probe health checking.


### <!-- md:setting values.readinessProbe.failureThreshold -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer`, `null` -->
<!-- md:default none -->

Number of consecutive failures before considering the container not ready.

### <!-- md:setting values.readinessProbe.httpGet -->

<!-- md:version 0.1.0 -->
<!-- md:type `object` -->
<!-- md:default none -->

HTTP GET probe configuration.


#### <!-- md:setting values.readinessProbe.httpGet.path -->

<!-- md:version 0.1.0 -->
<!-- md:type `string` -->
<!-- md:default none -->

Path to probe for HTTP health check.

#### <!-- md:setting values.readinessProbe.httpGet.port -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer`, `string` -->
<!-- md:default none -->

Port to probe for HTTP health check.

### <!-- md:setting values.readinessProbe.initialDelaySeconds -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer`, `null` -->
<!-- md:default none -->

Number of seconds to wait before starting probe checks.

### <!-- md:setting values.readinessProbe.periodSeconds -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer`, `null` -->
<!-- md:default none -->

How often to perform probe checks.

## <!-- md:setting values.region -->

<!-- md:version 0.1.0 -->
<!-- md:type `string` -->
<!-- md:default none -->

The region to deploy the CloudRun service to.

## <!-- md:setting values.resources -->

<!-- md:version 0.1.0 -->
<!-- md:type `object` -->
<!-- md:default none -->

Resource requests and limits for the CloudRun container. If not provided, defaults are used.


### <!-- md:setting values.resources.cpuThrottling -->

<!-- md:version 0.1.0 -->
<!-- md:type `boolean` -->
<!-- md:default `True` -->

Whether to throttle the CPU. This has significant impact on billing.

### <!-- md:setting values.resources.limits -->

<!-- md:version 0.1.0 -->
<!-- md:type `object` -->
<!-- md:default none -->


#### <!-- md:setting values.resources.limits.cpu -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer` -->
<!-- md:default `1` -->

Maximum CPUs to allocate for the CloudRun container. Can be 1, 2, 4, 6, 8, or any fractional value from 0.01 to 1.

#### <!-- md:setting values.resources.limits.memory -->

<!-- md:version 0.1.0 -->
<!-- md:type `string` -->
<!-- md:default none -->

Maximum memory to allocate for the CloudRun container. Requires a minimum number of CPUs of 2 over 4GiB.

### <!-- md:setting values.resources.startupBoost -->

<!-- md:version 0.1.0 -->
<!-- md:type `boolean` -->
<!-- md:default `False` -->

Whether to boost the CPUs at the start of the container.

## <!-- md:setting values.serviceAccountName -->

<!-- md:version 0.1.0 -->
<!-- md:type `string`, `null` -->
<!-- md:default none -->

Service account to use to run the CloudRun container. If not provided, the default service account of the project is used.

## <!-- md:setting values.sessionAffinity -->

<!-- md:version 0.1.0 -->
<!-- md:type `boolean` -->
<!-- md:default `False` -->

Whether to enable session affinity for the CloudRun service. When enabled, requests from the same client are routed to the same container instance.

## <!-- md:setting values.startupProbe -->

<!-- md:version 0.1.0 -->
<!-- md:type `object` -->
<!-- md:default none -->

Configuration for startup probe health checking.


### <!-- md:setting values.startupProbe.failureThreshold -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer`, `null` -->
<!-- md:default none -->

Number of consecutive failures before considering the startup failed.

### <!-- md:setting values.startupProbe.httpGet -->

<!-- md:version 0.1.0 -->
<!-- md:type `object` -->
<!-- md:default none -->

HTTP GET probe configuration.


#### <!-- md:setting values.startupProbe.httpGet.path -->

<!-- md:version 0.1.0 -->
<!-- md:type `string` -->
<!-- md:default none -->

Path to probe for HTTP health check.

#### <!-- md:setting values.startupProbe.httpGet.port -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer`, `string` -->
<!-- md:default `8080` -->

Port to probe for HTTP health check.

### <!-- md:setting values.startupProbe.initialDelaySeconds -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer`, `null` -->
<!-- md:default none -->

Number of seconds to wait before starting probe checks.

### <!-- md:setting values.startupProbe.periodSeconds -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer`, `null` -->
<!-- md:default none -->

How often to perform probe checks.

## <!-- md:setting values.timeoutSeconds -->

<!-- md:version 0.1.0 -->
<!-- md:type `integer` -->
<!-- md:default `60` -->

The maximum time the container will wait before responding with a 504 error.

## <!-- md:setting values.type -->

<!-- md:version 0.1.0 -->
<!-- md:type `string` -->
<!-- md:default none -->

Type of CloudRun resource to deploy. Must be either 'service' or 'job'.

## <!-- md:setting values.volumeMounts -->

<!-- md:version 0.1.0 -->
<!-- md:type `array` -->
<!-- md:default none -->

## <!-- md:setting values.volumes -->

<!-- md:version 0.1.0 -->
<!-- md:type `array` -->
<!-- md:default none -->

## <!-- md:setting values.vpc -->

<!-- md:version 0.1.0 -->
<!-- md:type `object` -->
<!-- md:default none -->


### <!-- md:setting values.vpc.connector -->

<!-- md:version 0.1.0 -->
<!-- md:type `string`, `null` -->
<!-- md:default none -->

Name of the VPC connector to use for the CloudRun container. Uses a serverless VPC access connector. Cannot be used with network.

### <!-- md:setting values.vpc.egress -->

<!-- md:version 0.1.0 -->
<!-- md:type `string` -->
<!-- md:default none -->

Name of the VPC egress to use for the CloudRun container.

### <!-- md:setting values.vpc.network -->

<!-- md:version 0.1.0 -->
<!-- md:type `string`, `null` -->
<!-- md:default none -->

Name of the VPC network to use to create a direct VPC connection. Must be used tohether with subnetwork. Cannot be used with connector.

### <!-- md:setting values.vpc.subnetwork -->

<!-- md:version 0.1.0 -->
<!-- md:type `string`, `null` -->
<!-- md:default none -->

Name of the VPC subnetwork to use to create a direct VPC connection. Must be used together with network. Cannot be used with connector.
