---
aliases: []
confidence: 
created: 2025-11-10T00:00:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-11T08:39:48Z
purpose: 
review_interval: 
see_also: []
source: "https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/configuration/helm-chart-config/helm-chart/migrate-helm-chart/"
source_of_truth: []
status: 
tags: []
title: Migrate to another Helm chart version  Grafana Cloud documentation
type: 
uid: 
updated: 
---

![ObservabilityCON 2025](https://grafana.com/media/events/obscon/2025/grafana-obscon2025-promo-logo-black.svg)

📢 Registration + agenda now live Explore the latest Grafana Cloud and AI solutions, learn tips & tricks from demos and hands-on workshops, and get actionable advice to advance your observability strategy. Register now and get 50% off - limited tickets available (while they last!).

Migrate to another Helm chart version

## Migrate to Another Helm Chart Version

Use the following information to migrate from one Helm chart version to another.

## Migrate from Version 1.0 to 3.x

To migrate from version 1.0 to 3.x:

1. Follow the steps for migrating from [version 1.x to 2.0](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/configuration/helm-chart-config/helm-chart/migrate-helm-chart/#migrate-from-version-1x-to-20).
2. Follow steps to migrate from [version 2.0 to 3.x](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/configuration/helm-chart-config/helm-chart/migrate-helm-chart/#migrate-from-version-20-to-3x). Consider any [changes to the values.yaml file](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/configuration/helm-chart-config/helm-chart/migrate-helm-chart/#potential-values-file-updates) that might benefit you when migrating to 3.x.

## Migrate from Version 2.0 to 3.x

The 3.0 release of the Kubernetes Monitoring Helm chart no longer uses the [Alloy Helm chart](https://github.com/grafana/alloy/tree/main/operations/helm/charts/alloy) as a subchart dependency. Instead, the chart uses the new [Alloy Operator](https://github.com/grafana/alloy-operator) to deploy Alloy instances. This allows for a more flexible and powerful deployment of Alloy, as well as the ability of your chosen features to appropriately configure those Alloy instances.

### Potential Values File Updates

There are no required changes to your values.yaml file. However, if you are using any of these options, you may want to update your values file:

- Private image registries: The addition of the Alloy Operator brings another image that may need to be referenced from a new location.
- Tail Sampling: If you were pairing this chart with the Grafana Sampling chart to perform tail sampling, this functionality has been embedded into the Kubernetes Monitoring Helm chart. Send your trace destinations to their ultimate destination. You can use the [tail sampling option](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/docs/examples/tail-sampling) of the trace destination.
- Service Graph Metrics: Similar to tail sampling, in version 3.1, the service graph metrics functionality has been embedded into the Kubernetes Monitoring Helm chart.

## Migrate from Version 1.x to 2.0

The version 2.0 release of the Kubernetes Monitoring Helm chart includes major changes from the 1.x version. Many of the features have been reorganized around features rather than data types (such as metrics, logs, and so on). In version 1, many features were enabled by default, such as Cluster metrics, Pod logs, Cluster events, and so on.

In version 2, all features are turned off by default. This means your values file better reflects your desired feature set.

To migrate to version 2, use the following sections to map destinations, collectors, Cluster events, Cluster metrics, annotation autodiscovery, Application Observability, Beyla, Pod logs, Prometheus Operator, and integrations. A migration tool is available at [https://grafana.github.io/k8s-monitoring-helm-migrator/](https://grafana.github.io/k8s-monitoring-helm-migrator/).

### Destinations Mapping

The definition of where data is delivered has changed from `externalServices`, an object of four types, to `destinations`, an array of any number of types. Before the `externalServices` object had four types of destinations:

- `prometheus`: Where all metrics are delivered. This could refer to a true Prometheus server or an OTLP destination that handles metrics.
- `loki`: Where all logs are delivered. This could refer to a true Loki server or an OTLP destination that handles logs.
- `tempo`: Where all traces are delivered. This could refer to a true Tempo server or an OTLP destination that handles traces.
- `pyroscope`: Where all profiles are delivered.

In version 1, the service essentially referred to the destination for the data type. In version 2, the destination refers to the protocol used to deliver the data type. Refer to [Destinations](https://github.com/grafana/k8s-monitoring-helm/blob/main/charts/k8s-monitoring/docs/destinations/README.md) for more information.

The following table shows an example of how to map from v1 `externalServices` to v2 `destinations`:

| Service | v1.x setting | v2.0 setting |
| --- | --- | --- |
| Prometheus | `externalServices.prometheus` | `destinations: [{type: "prometheus"}]` |
| Prometheus (OTLP) | `externalServices.prometheus` | `destinations: [{type: "otlp", metrics: {enabled: true}}]` |
| Loki | `externalServices.loki` | `destinations: [{type: "loki"}]` |
| Loki (OTLP) | `externalServices.loki` | `destinations: [{type: "loki", logs: {enabled: true}}]` |
| Tempo | `externalServices.tempo` | `destinations: [{type: "otlp"}]` |
| Pyroscope | `externalServices.pyroscope` | `destinations: [{type: "pyroscope"}]` |

Complete the following to map destinations:

1. Create a destination for each external service you are using.
2. Provide a `name` and a `type` for the destination.
3. Provide the URL for the destination.

	> Note
	> 
	> This is a full data writing/pushing URL, not only the hostname.

4. Map the other settings from the original service to the new destination as shown in the following table:
	| Original service | New destination |
	| --- | --- |
	| `authMode` | `auth.type` |
	| Auth definitions (e.g. `basicAuth`) | `auth` |
	| `externalLabels` | `extraLabels` |
	| `writeRelabelRules` | `metricProcessingRules` |

### Collector Mapping

Alloy collectors (or instances) have been further split from the original to allow for more flexibility in the configuration and predictability in their resource requirements. Each feature allows for setting the collector, but the defaults have been chosen carefully. You should only need to change these if you have specific requirements.

| Responsibility | v1.x Alloy | v2.0 Alloy | Notes |
| --- | --- | --- | --- |
| Metrics | `alloy` | `alloy-metrics` |  |
| Logs | `alloy-logs` | `alloy-logs` |  |
| Cluster events | `alloy-events` | `alloy-singleton` | Also applies to anything that must be deployed only to a single instance. |
| Application receivers | `alloy` | `alloy-receiver` |  |
| Profiles | `alloy-profiles` | `alloy-profiles` |  |

Complete the following to map collectors:

1. Rename `alloy` to `alloy-metrics`.
2. Rename `alloy-events` to `alloy-singleton`.
3. Move any open receiver ports to the `alloy-receiver` instance.

### Cluster Events Mapping

Gathering of Cluster events has been moved into its own feature called [`clusterEvents`](https://github.com/grafana/k8s-monitoring-helm/blob/main/charts/k8s-monitoring/docs/examples/features/cluster-events/default/README.md).

| Feature | v1.x setting | v2.0 setting |
| --- | --- | --- |
| Cluster Events | `logs.cluster_events` | `clusterEvents` |

If using Cluster events `logs.cluster_events.enabled`:

1. Enable `clusterEvents` and `alloy-singleton` in your values file:
	YAML

	```yaml
	clusterEvents:
	  enabled: true
	alloy-singleton:
	  enabled: true
	```

2. Move `logs.cluster_events` to `clusterEvents`.
3. Rename `extraStageBlocks` to `extraProcessingStages`.

### Cluster Metrics Mapping

Cluster metrics refers to any metric data source that scrapes metrics about the cluster itself. This includes the following data sources:

- Cluster metrics (Kubelet, API Server, and so on)
- Node metrics (Node Exporter and Windows Exporter)
- kube-state-metrics
- Energy metrics via Kepler
- Cost metrics via OpenCost

These have all been combined into a single feature called [`clusterMetrics`](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/docs/examples/features/cluster-metrics).

| Feature | v1.x setting | v2.0 setting | Notes |
| --- | --- | --- | --- |
| Kubelet metrics | `metrics.kubelet` | `clusterMetrics.kubelet` |  |
| cAdvisor metrics | `metrics.cadvisor` | `clusterMetrics.cadvisor` |  |
| kube-state-metrics metrics | `metrics.cadvisor` | `clusterMetrics.kube-state-metrics` |  |
| kube-state-metrics deployment | `kube-state-metrics` | `clusterMetrics.kube-state-metrics` | The decision to deploy is controlled by `clusterMetrics.kube-state-metrics.deploy`. |
| Node Exporter metrics | `metrics.node-exporter` | `clusterMetrics.node-exporter` |  |
| Node Exporter deployment | `prometheus-node-exporter` | `clusterMetrics.node-exporter` | The decision to deploy is controlled by `clusterMetrics.node-exporter.deploy`. |
| Windows Exporter metrics | `metrics.windows-exporter` | `clusterMetrics.windows-exporter` |  |
| Windows Exporter deployment | `prometheus-windows-exporter` | `clusterMetrics.windows-exporter` | The decision to deploy is controlled by `clusterMetrics.windows-exporter.deploy`. |
| Energy metrics (Kepler) | `metrics.kepler` | `clusterMetrics.kepler` |  |
| Kepler deployment | `kepler` | `clusterMetrics.kepler` |  |
| Cost metrics (OpenCost) | `metrics.opencost` | `clusterMetrics.opencost` |  |
| OpenCost deployment | `opencost` | `clusterMetrics.opencost` |  |

If using Cluster metrics `metrics.enabled`:

1. Enable `clusterMetrics` and `alloy-metrics` in your values file:
	YAML

	```yaml
	clusterMetrics:
	  enabled: true
	alloy-metrics:
	  enabled: true
	```

2. Move each of the sections in the previous table to `clusterMetrics`.
3. Rename any `extraRelabelingRules` to `extraDiscoveryRules`.
4. Rename any `extraMetricRelabelingRules` to `extraMetricProcessingRules`.

### Annotation Autodiscovery Mapping

Discovery of Pods and Services by annotation has been moved into its own feature called `annotationAutodiscovery`.

| Feature | v1.x setting | v2.0 setting |
| --- | --- | --- |
| Annotation autodiscovery | `metrics.autoDiscover` | `annotationAutodiscovery` |

If using annotation autodiscovery `metrics.autoDiscover.enabled`:

1. Enable `annotationAutodiscovery` and `alloy-metrics` in your values file:
	YAML

	```yaml
	annotationAutodiscovery:
	  enabled: true
	alloy-metrics:
	  enabled: true
	```

2. Move the contents of `metrics.autoDiscover` to `annotationAutodiscovery`.
3. Rename any `extraRelabelingRules` to `extraDiscoveryRules`.
4. Rename any `extraMetricRelabelingRules` to `extraMetricProcessingRules`.

### Application Observability Mapping

[Application Observability](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/docs/examples/features/application-observability) is the new name for the feature that encompasses receiving data via various receivers (such as OTLP, Zipkin, and so on) within the metrics, logs, and traces sections. This has been moved into its own feature.

| Feature | v1.x setting | v2.0 setting |
| --- | --- | --- |
| Collector ports | `alloy.alloy.extraPorts` | `alloy-receiver.alloy.extraPorts` |
| Receiver definitions | `receivers` | `applicationObservability.receivers` |
| Processors | `receivers.processors` | `applicationObservability.processors` |
| Metric Filters | `metrics.receiver.filters` | `applicationObservability.metrics.filters` |
| Metric Transforms | `metrics.receiver.transforms` | `applicationObservability.metrics.transforms` |
| Log Filters | `logs.receiver.filters` | `applicationObservability.logs.filters` |
| Log Transforms | `logs.receiver.transforms` | `applicationObservability.logs.transforms` |
| Trace Filters | `traces.receiver.filters` | `applicationObservability.traces.filters` |
| Trace Transforms | `traces.receiver.transforms` | `applicationObservability.traces.transforms` |

If using application observability `traces.enabled` and `receivers.*.enabled`:

1. Enable `applicationObservability` and `alloy-receiver` in your values file:
	YAML

	```yaml
	applicationObservability:
	  enabled: true
	alloy-receiver:
	  enabled: true
	```

2. Move any extra ports opened for applications from `alloy.alloy.extraPorts` to `alloy-receiver.alloy.extraPorts`
3. Enable the receivers you want to use in `applicationObservability.receivers`, for example:
	YAML

	```yaml
	applicationObservability:
	  receivers:
	    grpc:
	      enabled: true
	```

4. Move receiver processors from `receivers.processors` to `applicationObservability.processors`.
5. Move metric filters from `metrics.receiver.filters` to `applicationObservability.metrics.filters`.
6. Move metric transforms from `metrics.receiver.transforms` to `applicationObservability.metrics.transforms`.
7. Move log filters from `logs.receiver.filters` to `applicationObservability.logs.filters`.
8. Move log transforms from `logs.receiver.transforms` to `applicationObservability.logs.transforms`.
9. Move trace filters from `traces.receiver.filters` to `applicationObservability.traces.filters`.
10. Move trace transforms from `traces.receiver.transforms` to `applicationObservability.traces.transforms`.

### Grafana Beyla Mapping

Deployment and handling of the zero-code instrumentation feature using Grafana Beyla has been moved into its own feature called [`autoInstrumentation`](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/docs/examples/features/auto-instrumentation).

| Feature | v1.x setting | v2.0 setting |
| --- | --- | --- |
| Auto-instrumentation metrics | `metrics.beyla` | `autoInstrumentation.beyla` |
| Beyla deployment | `beyla` | `autoInstrumentation.beyla` |

If using Beyla `beyla.enabled`:

1. Enable `autoInstrumentation` and `alloy-metrics` in your values file:
	YAML

	```yaml
	autoInstrumentation:
	  enabled: true
	alloy-metrics:
	  enabled: true
	```

2. Combine `beyla` and `metrics.beyla` and copy to `autoInstrumentation.beyla`

### Pod Logs Mapping

Gathering of Pods logs has been moved into its own feature called `podLogs`.

| Feature | v1.x setting | v2.0 setting |
| --- | --- | --- |
| Pod logs | `logs.pod_logs` | `podLogs` |

If using Pod logs `logs.pod_logs.enabled`:

1. Enable `podLogs` and `alloy-logs` in your values file:
	YAML

	```yaml
	podLogs:
	  enabled: true
	alloy-logs:
	  enabled: true
	```

2. Move `logs.pod_logs` to `podLogs`.
3. Rename:
	- `extraRelabelingRules` to `extraDiscoveryRules`
	- `extraStageBlocks` to `extraLogProcessingStages`

### Prometheus Operator Objects Mapping

Handling for Prometheus Operator objects, such as `ServiceMonitors`, `PodMonitors`, and `Probes` has been moved to the [`prometheusOperatorObjects` feature](https://github.com/grafana/k8s-monitoring-helm/blob/main/charts/k8s-monitoring/docs/examples/features/prometheus-operator-objects/default/README.md). This feature also includes the option to deploy the Prometheus Operator CRDs.

| Feature | v1.x setting | v2.0 setting |
| --- | --- | --- |
| PodMonitor settings | `metrics.podMonitors` | `prometheusOperatorObjects.podMonitors` |
| Probe settings | `metrics.probes` | `prometheusOperatorObjects.probes` |
| ServiceMonitor settings | `metrics.serviceMonitors` | `prometheusOperatorObjects.serviceMonitors` |
| CRDs deployment | `prometheus-operator-crds.enabled` | `crds.deploy` |

If using Prometheus Operator objects, `metrics.podMonitors.enabled`, `metrics.probes.enabled`,`metrics.serviceMonitors.enabled`, `prometheus-operator-crds.enabled`:

1. Enable `prometheusOperatorObjects` and `alloy-metrics` in your values file:
	YAML

	```yaml
	prometheusOperatorObjects:
	  enabled: true
	alloy-metrics:
	  enabled: true
	```

2. Move the following:
	- `metrics.podMonitors` to `prometheusOperatorObjects.podMonitors`
	- `metrics.probes` to `prometheusOperatorObjects.probes`
	- `metrics.serviceMonitors` to `prometheusOperatorObjects.serviceMonitors`

### Integrations Mapping

[Integrations](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/docs/examples/features/integrations) is a new feature in version 2.0 that allow you to enable and configure additional data sources. This includes the Alloy metrics that were previously part of `v1`. Some service integrations that previously needed to be defined in the `extraConfig` and `logs.extraConfig` sections can now be used in the integration feature.

Replace your `extraConfig` to the new `integrations` feature if you are using either of these settings:

- The `metrics.alloy` setting for getting Alloy metrics
- The `extraConfig` to add config to get data from any of the new built-in integrations

The following are built-in integrations:

| Built-in integration | v1.x setting | v2.0 setting |
| --- | --- | --- |
| Alloy | `metrics.alloy` | `integrations.alloy` |
| cert-manager | `extraConfig` | `integrations.cert-manager` |
| etcd | `extraConfig` | `integrations.etcd` |
| MySQL | `extraConfig` and `logs.extraConfig` | `integrations.mysql` |

If using the Alloy integration `metrics.alloy.enabled`, or if using `extraConfig` for cert-manager, etcd, or MySQL:

1. Create instances of the integration that you want, and enable `alloy-metrics` in your values file:
	YAML

	```yaml
	integrations:
	  alloy:
	    instances:
	      - name: 'alloy'
	alloy-metrics:
	  enabled: true
	```

2. Move `metrics.alloy` to `integrations.alloy.instances[]`.

For service integrations that are not available in the built-in integrations feature, you can continue to use them in the `extraConfig` sections. Refer to the [Extra Configs](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/configuration/helm-chart-config/helm-chart/migrate-helm-chart/#extra-configs-mapping) section for guidance.

### Extra Configs Mapping

The variables for adding arbitrary configuration to the Alloy instances have been moved inside the respective Alloy instance. If you are using `extraConfig` to add configuration for scraping metrics from an integration built-in with the [integrations](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/charts/feature-integrations) feature (such as cert-manager, etcd, or MySQL), you can move that configuration to the new `integrations` feature.

For other uses of `extraConfig`, refer to the following table:

| extraConfig | v1.x setting | v2.0 setting |
| --- | --- | --- |
| Alloy for Metrics | `extraConfig` | `alloy-metrics.extraConfig` |
| Alloy for Apps | `extraConfig` | `alloy-receiver.extraConfig` |
| Alloy for Events | `logs.cluster_events.extraConfig` | `alloy-singleton.extraConfig` |
| Alloy for Logs | `logs.extraConfig` | `alloy-logs.extraConfig` |
| Alloy for Profiles | `profiles.extraConfig` | `alloy-profiles.extraConfig` |

1. Move the following:
	- `extraConfig` related to metrics to `alloy-metrics.extraConfig`
	- `extraConfig` related to application receivers to `alloy-receivers.extraConfig`
	- `logs.cluster_events.extraConfig` to `alloy-singleton.extraConfig`
	- `logs.extraConfig` to `alloy-logs.extraConfig`
	- `profiles.extraConfig` to `alloy-profiles.extraConfig`
2. Rename destinations for telemetry data to the appropriate destination component. Refer to [Destination names](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/configuration/helm-chart-config/helm-chart/migrate-helm-chart/#destination-names).

#### Destination Names

The `<destination_name>` in the component reference is the name of the destination, set to lowercase and with any non-alphanumeric characters replaced with an underscore. For example, if your destination is named `Grafana Cloud Metrics`, then the destination name would be `grafana_cloud_metrics`.

| Data type | v1.x setting | v2.0 setting |
| --- | --- | --- |
| Metrics | `prometheus.relabel.metrics_service.receiver` | `prometheus.remote_write.<destination_name>.receiver` |
| Logs | `loki.process.logs_service.receiver` | `loki.write.<destination_name>.receiver` |
| Traces | `otelcol.exporter.otlp.traces_service.input` | `otelcol.exporter.otlp.<destination_name>.input` |
| Profiles | `pyroscope.write.profiles_service.receiver` | `pyroscope.write.<destination_name>.receiver` |

### Dropped Features

The following features have been removed from the 2.0 release:

- Pre-install hooks: The pre-install and pre-upgrade hooks that performed config validation have been removed. The Alloy Pods now validate the configuration at runtime and log any issues, and do so without these Pods. This greatly decreases startup time.
- `helm test` functionality: The `helm test` functionality that ran a config analysis and attempted to query the databases for expected metrics and logs has been removed. This functionality was either not fully developed or not useful in production environments. The query testing was mainly for CI/CD testing in development. This has been replaced by more effective and comprehensive methods.
