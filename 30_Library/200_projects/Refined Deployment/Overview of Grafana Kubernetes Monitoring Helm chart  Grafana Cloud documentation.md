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
source: "https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/configuration/helm-chart-config/helm-chart/"
source_of_truth: []
status: 
tags: []
title: Overview of Grafana Kubernetes Monitoring Helm chart  Grafana Cloud documentation
type: 
uid: 
updated: 
---

![ObservabilityCON 2025](https://grafana.com/media/events/obscon/2025/grafana-obscon2025-promo-logo-black.svg)

📢 Registration + agenda now live Explore the latest Grafana Cloud and AI solutions, learn tips & tricks from demos and hands-on workshops, and get actionable advice to advance your observability strategy. Register now and get 50% off - limited tickets available (while they last!).

Overview of Grafana Kubernetes Monitoring Helm chart

## Overview of Grafana Kubernetes Monitoring Helm Chart

The [Grafana Kubernetes Monitoring Helm chart](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring) offers a complete solution for configuring infrastructure, zero-code instrumentation, and gathering telemetry. The benefits of using this chart include:

- Flexible architecture
- Compatibility with existing systems such as OpenTelemetry and Prometheus Operators
- Dynamic creation of Alloy objects based on your configuration choices
- [Scalability](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/docs/examples/scalability) for all Cluster sizes
- Built-in [testing](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/tests) and [schemas](https://github.com/grafana/k8s-monitoring-helm/blob/main/charts/k8s-monitoring/values.schema.json) to help you avoid errors

## Release Notes

Refer to [Helm chart release notes](https://github.com/grafana/k8s-monitoring-helm/releases) for all updates.

## Helm Chart Structure

The Helm chart includes the following folders:

- [charts](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/charts): Contains the chart for each feature
- [collectors](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/collectors): The values files for each collector
- [destinations](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/destinations): The values file for each destination
- [docs](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/docs): The settings for Alloy, example files for each feature and each destination
- [schema mods](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/schema-mods): Schema modules to prevent input errors
- [scripts](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/scripts)
- [templates](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/templates): Templates used by the Helm chart
- [tests](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/tests): A set of tests to validate chart functionality to ensure it works as expected

### Features

In addition to the required contents for any Helm chart, this chart has guidance for each feature. A feature is a common monitoring task that contains:

- The Alloy configuration used to discover, gather, process, and deliver the appropriate telemetry data
- Additional Kubernetes workloads to supplement Alloy’s functionality

Each feature contains multiple configuration options. You can enable or disable a feature with the enabled flag.

The following features are available:

- [Annotation autodiscovery](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/charts/feature-annotation-autodiscovery): Collects metrics from any Pod or Service that uses a specific annotation
- [Application Observability](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/charts/feature-application-observability): Opens receivers to collect telemetry data from instrumented applications, including tail sampling
- [Beyla](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/docs/examples/features/auto-instrumentation): Options for enabling zero-code instrumentation with Grafana Beyla
- [Cluster events](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/charts/feature-cluster-events): Collects Kubernetes Cluster events from the Kubernetes API server
- [Cluster metrics](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/charts/feature-cluster-metrics): Collects metrics about the Kubernetes Cluster, including the control plane
- [Node logs](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/charts/feature-node-logs): Collects logs from Kubernetes Cluster Nodes
- [Pod logs](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/charts/feature-pod-logs): Collects logs from Kubernetes Pods
- [Profiling](https://github.com/grafana/k8s-monitoring-helm/blob/main/charts/k8s-monitoring/docs/examples/features/profiling/default/README.md): Gathers profiles from the Kubernetes Cluster and delivers them to Pyroscope
- [Prometheus Operator objects](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/charts/feature-prometheus-operator-objects): Collects metrics from Prometheus Operator objects, such as PodMonitors and ServiceMonitors
- [Service integrations](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/charts/feature-integrations): Collect profiles using Pyroscope

## Packages Installed with Helm Chart

The Grafana Kubernetes Monitoring Helm chart deploys a complete monitoring solution for your Cluster and applications running within it. The chart installs systems, such as Node Exporter and Grafana Alloy Operator, along with their configuration to make these systems run. These elements are kept up to date in the Kubernetes Monitoring Helm chart with a dependency updating system to ensure that the latest versions are used.

The Helm chart installs Alloy Operator, which renders a `kind: Alloy` object dynamically that depends on the options you choose for configuration. When an Alloy object is deployed to the Cluster based on the values.yaml file, Alloy Operator:

1. Determines the workload type and creates the components needed by the Alloy object (such as file system access, permissions, or the capability to read secrets)
2. Performs a Helm install of the Alloy object and its components
![Diagram of components installed by Helm and Alloy Operator](https://grafana.com/media/docs/grafana-cloud/k8s/helm-chart-2025-oct.png?w=320)

Diagram of components installed by Helm and Alloy Operator

The Helm chart creates configuration files for the Grafana Alloy instances, and stores them in ConfigMaps.

> Note
>
> Multiple instances of Grafana Alloy support the scalability of your infrastructure. To learn more, refer to [Deployment of multiple Alloy instances](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/configuration/helm-chart-config/helm-chart/#deployment-of-multiple-alloy-instances).

All configuration related to telemetry data destinations are automatically loaded onto the Grafana Alloy instances that require them.

### Infrastructure Metrics

Alloy Operator installs an alloy-metrics StatefulSet instance which gathers metrics related to the Cluster itself and accepts metrics, logs, and traces via receivers. This instance can retrieve metrics from:

- [`kubelet`](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/), the primary Node agent which ensures containers are running and healthy
- [cAdvisor](https://github.com/google/cadvisor), which provides container CPU, memory, and disk usage
- [Node Exporter](https://github.com/prometheus/node_exporter) within a Daemonset, which gathers hardware device and kernel-related metrics from Linux Nodes of the Cluster. The exported Prometheus metrics indicate the health and state of Nodes in the Cluster.
- [Windows Exporter](https://github.com/prometheus-community/windows_exporter) within a Daemonset, which provides hardware device and kernel-related metrics from Windows Nodes. The exported Prometheus metrics indicate the health and state of Nodes in the Cluster.
- [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics) within a Deployment, which listens to the API server and generates metrics on the health of objects inside the Cluster such as Deployments, Nodes, and Pods. This service generates metrics from Kubernetes API objects, and uses `client-go` to communicate with Clusters. For Kubernetes client-go version compatibility and any other related details, refer to [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics#versioning).
- [Prometheus Operator CRDs](https://github.com/prometheus-operator/prometheus-operator), provide the custom resources for the Prometheus Operator. Use when you want to deploy PodMonitors, ServiceMonitors, or Probes.
![Alloy metrics  instance by Alloy Operator and its function](https://grafana.com/media/docs/grafana-cloud/k8s/diagram-alloy-metrics.png?w=320)

Alloy metrics instance by Alloy Operator and its function

This Alloy instance can also gather metrics from:

- [OpenCost](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/configuration/manage-configuration/#opencost-cost-calculations), to calculate Kubernetes infrastructure and container costs. OpenCost requires [Kubernetes 1.8+](https://github.com/opencost/opencost#getting-started) Clusters.
- [Kepler](https://sustainable-computing.io/) for [energy metrics](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/navigate-k8s-monitoring/#discover-energy-usage)

### Infrastructure Logs

The following collectors retrieve logs:

- An alloy-singleton Deployment instance for Cluster events, to get Kubernetes lifecycle events from the API server and transform them into logs The alloy-singleton instance is responsible for anything that must be done on a single instance, such as gathering Cluster events from the API server. This instance does not support clustering, so only one instance should be used.![Alloy singleton  instance installed by Helm chart to gather events](https://grafana.com/media/docs/grafana-cloud/k8s/diagram-alloy-singleton.png?w=320)
 Alloy singleton instance installed by Helm chart to gather events
- An alloy-logs DaemonSet instance to retrieve Pod logs and Node logs By default, it uses HostPath volume mounts to read Pod log files directly from the Nodes. It can alternatively get logs via the API server, and be deployed as a Deployment.![Alloy logs instance for gathering logs](https://grafana.com/media/docs/grafana-cloud/k8s/diagram-alloy-logs.png?w=320)
 Alloy logs instance for gathering logs

### Application Telemetry

The Alloy Operator can also create the following to gather metrics, logs, traces, and profiles from applications running in the Cluster:

- An alloy-receiver DaemonSet instance, which opens receiver ports to process data delivered directly to itself from applications instrumented with OpenTelemetry SDKs![Alloy receiver instance installed by Helm chart to receive telemetry](https://grafana.com/media/docs/grafana-cloud/k8s/diagram-alloy-receiver.png?w=320)
 Alloy receiver instance installed by Helm chart to receive telemetry
- An alloy-events DaemonSet instance to gather profiles![Alloy profiles instance installed by Helm chart and the profiles gathered](https://grafana.com/media/docs/grafana-cloud/k8s/diagram-alloy-profiles.png?w=320)
 Alloy profiles instance installed by Helm chart and the profiles gathered

### Automatic Instrumentation

With the Helm chart, you can install a Grafana Beyla DaemonSet to perform zero code instrumentation of applications and gather network metrics.

![Beyla installed by Helm chart](https://grafana.com/media/docs/grafana-cloud/k8s/diagram-beyla.png?w=320)

Beyla installed by Helm chart

## Deployment of Multiple Alloy Instances

Multiple instances of Grafana Alloy are deployed instead of one instance that includes all functions. This design is necessary for security and balancing functionality and scalabilty.

### Security

The use of distinct instances minimizes the security footprint required. For example, the alloy-logs instance may require a HostPath volume mount, but the other instances do not. Instead they can be deployed with a more restrictive and appropriate security context. Each object, whether Alloy, Node Exporter, cAdvisor, or Beyla is restricted to the permissions required for it to perform its function, leaving Grafana Alloy to act solely as a collector.

### Functionality/scalability Balance

Each instance has unique functionality and scalability requirements. For example, the default functionality of the alloy-log instance is to gather logs via HostPath volume mounts, which requires the instance to be deployed as a DaemonSet. The alloy-metrics instance is deployed as a StatefulSet, which allows it to be scaled (optionally with a HorizontalPodAutoscaler) based on load. Otherwise, it would lose its ability to scale. The alloy-singleton instance cannot be scaled beyond one replica, because that would result in duplicate data being sent.

## Images

The following is the list of images used in the 3.3.1 version of the Kubernetes Monitoring Helm chart.

### Alloy

The telemetry data collector. Deployed by the Alloy Operator.

**Image**: `docker.io/grafana/alloy:v1.10.1`

**Deploy**: `alloy-____.enabled=true`

### Alloy Operator

Deploys and manages Grafana Alloy collector instances.

**Image**: `ghcr.io/grafana/alloy-operator:1.2.1`

**Deploy**: `alloy-operator.deploy=true`

### Beyla

Performs zero-code instrumentation of applications on the Cluster, generating metrics and traces.

**Image**: `docker.io/grafana/beyla:2.5.6`

**Deploy**: `autoInstrumentation.beyla.enabled=true`

### Config Reloader

Sidecar for Alloy instances that reloads the Alloy configuration upon changes.

**Image**: `quay.io/prometheus-operator/prometheus-config-reloader:v0.81.0`

**Deploy**: `alloy-____.configReloader.enabled=true`

### Kepler

**Image**: `quay.io/sustainable_computing_io/kepler:release-0.8.0`

**Deploy**: `clusterMetrics.kepler.enabled=true`

### Kube-state-metrics

Gathers Kubernetes Cluster object metrics.

**Image**: `registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.16.0`

**Deploy**: `clusterMetrics.kube-state-metrics.deploy=true`

### Kubectl

Used for Helm hooks for properly sequencing the Alloy Operator deployment and removal.

**Image**: `ghcr.io/grafana/helm-chart-toolbox-kubectl:0.1.1`

**Deploy**: `alloy-operator.waitForReadiness.enabled=true` and `alloy-operator.waitForAlloyRemoval.enabled=true`

### Node Exporter

Gathers Kubernetes Cluster Node metrics for Linux nodes.

**Image**: `quay.io/prometheus/node-exporter:v1.9.1`

**Deploy**: `clusterMetrics.node-exporter.deploy=true`

### OpenCost

Gathers cost metrics for Kubernetes objects.

**Image**: `ghcr.io/opencost/opencost:1.116.0@sha256:e4658c3be1119f2ab57c5a57c3e19b785d525de63f4cc57111d0da3e0a6654c0`

**Deploy**: `clusterMetrics.opencost.enabled=true`

### Windows Exporter

Gathers Kubernetes Cluster Node metrics for Windows nodes.

**Image**: `ghcr.io/prometheus-community/windows-exporter:0.31.2`

**Deploy**: `clusterMetrics.windows-exporter.deploy=true`

## Container Image Security

The container images deployed by the Kubernetes Monitoring Helm chart are built and managed by the following subcharts. The Helm chart itself uses a dependency updating system to ensure that the latest version of the dependent charts are used. Subchart authors are responsible for maintaining the security of the container images they build and release.

- [Grafana Beyla](https://github.com/grafana/beyla)
- [Node Exporter](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus-node-exporter)
- [Windows Exporter](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus-windows-exporter)
- [kube-state-metrics](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-state-metrics)
- [OpenCost](https://github.com/opencost/opencost-helm-chart)
- [Kepler](https://github.com/sustainable-computing-io/kepler-helm-chart/tree/main/chart/kepler)

## Deployment

After you have made configuration choices, the `values.yaml` file is altered to reflect your selections for configuration.

> Note
>
> In the configuration GUI, you can choose to switch on or off the collection of metrics, logs, events, traces, costs, or energy metrics during the configuration process.

When you deploy the chart, the Alloy Operator dynamically creates the Alloy objects based on your choices and the Helm chart installs the appropriate components required for collecting telemetry data. Separate instances of Alloy deploy so that there are no issues with scaling.

After deployment, you can check the [**Metrics status** tab](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/configuration/manage-configuration/#metrics-management-and-control) under **Configuration**. This page provides a snapshot of the overall health of the metrics being ingested.

![Descriptions and statuses for each item chosen to be configured and whether they are online](https://grafana.com/media/docs/grafana-cloud/k8s/metrics-statusOct31.png?w=320)

Metrics status tab showing status for last hour on one Cluster

## Customization

You can also customize the chart for your specific needs and tailor it to specific Cluster environments. For example:

- Your configuration might already have an existing kube-state-metrics in your Cluster, so you don’t want the Helm chart to install another one.
- Enterprise Clusters with many workloads running can have specific requirements.

For links to examples for customization, refer to the [Customize the Kubernetes Monitoring Helm chart](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/configuration/helm-chart-config/customize-helm-chart/).

## Troubleshoot

For Kubernetes Monitoring configuration issues, refer to [Troubleshooting](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/configuration/troubleshooting/#tips-for-helm-chart-configuration). For issues more specifically related to the Helm chart, refer to [Troubleshoot the Kubernetes Monitoring Helm chart configuration](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/configuration/helm-chart-config/helm-chart/troubleshoot-helm-chart/).

## Metrics Management

To learn more about managing metrics, refer to [Metrics management and control](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/configuration/manage-configuration/#metrics-management-and-control).

## Uninstall

To uninstall the Helm chart:

1. Delete the Alloy instances:
 YAML

 ```yaml
 kubectl delete alloy --all --namespace <namespace>
 ```

2. Uninstall the Helm chart:
 YAML

 ```yaml
 helm uninstall --namespace <namespace> grafana-k8s-monitoring
 ```
