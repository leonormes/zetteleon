# Grafana Alloy

Grafana Alloy is a vendor-neutral distribution of the OpenTelemetry (OTel) Collector. Alloy uniquely combines the very best OSS observability signals in the community.

---

## Overview

Alloy offers native [pipelines](https://app.heptabase.com/c16a6d60-49a6-4aec-9d1a-6161cbbe31a8/card/30ada2ec-3d38-46b1-a441-b6eae1bfa167) for [OTel](https://opentelemetry.io/ecosystem/distributions/), [Prometheus](https://prometheus.io/), [Pyroscope](https://grafana.com/docs/pyroscope/), [Loki](https://grafana.com/docs/loki/), and many other metrics, logs, traces, and profile tools. In addition, you can use Alloy pipelines to do different tasks, such as configure alert rules in Loki and [Mimir](https://grafana.com/docs/mimir/). Alloy is fully compatible with the OTel Collector, Prometheus Agent, and [Promtail](https://grafana.com/docs/loki/latest/send-data/promtail/). You can use Alloy as an alternative to either of these solutions or combine it into a hybrid system of multiple collectors and agents. You can deploy Alloy anywhere within your IT infrastructure and pair it with your Grafana LGTM stack, a telemetry backend from Grafana Cloud, or any other compatible backend from any other vendor. Alloy is flexible, and you can easily configure it to fit your needs in on-prem, cloud-only, or a mix of both.

> Tip
>
> Alloy uses the same components, code, and concepts that were first introduced in Grafana Agent Flow.

## What can Alloy do?

Alloy is more than just observability signals like metrics, logs, and traces. It provides many features that help you quickly find and process your data in complex environments. Some of these features include custom components, GitOps compatibility, clustering support, security, and debugging utilities. Refer to the Alloy [Introduction](https://grafana.com/docs/alloy/latest/introduction/) for more information on these and other key features.

## Explore

[Install Alloy](https://grafana.com/docs/alloy/latest/set-up/install/)

[Learn how to install and uninstall Alloy on Docker, Kubernetes, Linux, macOS, or Windows.](https://grafana.com/docs/alloy/latest/set-up/install/)

[Run Alloy](https://grafana.com/docs/alloy/latest/set-up/run/)

[Learn how to start, restart, and stop Alloy after you have installed it.](https://grafana.com/docs/alloy/latest/set-up/run/)

[Configure Alloy](https://grafana.com/docs/alloy/latest/configure/)

[Learn how to configure Alloy on Kubernetes, Linux, macOS, or Windows.](https://grafana.com/docs/alloy/latest/configure/)

[Migrate to Alloy](https://grafana.com/docs/alloy/latest/set-up/migrate/)

[Learn how to migrate to Alloy from Grafana Agent Operator, Prometheus, Promtail, Grafana Agent Static, or Grafana Agent Flow.](https://grafana.com/docs/alloy/latest/set-up/migrate/)

[Collect OpenTelemetry data](https://grafana.com/docs/alloy/latest/collect/opentelemetry-data/)

[You can configure Alloy to collect OpenTelemetry-compatible data and forward it to any OpenTelemetry-compatible endpoint. Learn how to configure OpenTelemetry data delivery, configure batching, and receive OpenTelemetry data over OTLP.](https://grafana.com/docs/alloy/latest/collect/opentelemetry-data/)

[Collect and forward Prometheus metrics](https://grafana.com/docs/alloy/latest/collect/prometheus-metrics/)

[You can configure Alloy to collect Prometheus metrics and forward them to any Prometheus-compatible database. Learn how to configure metrics delivery and collect metrics from Kubernetes Pods.](https://grafana.com/docs/alloy/latest/collect/prometheus-metrics/)

[Concepts](https://grafana.com/docs/alloy/latest/get-started/)

[Learn about components, modules, clustering, and the Alloy configuration syntax.](https://grafana.com/docs/alloy/latest/get-started/)

[Reference](https://grafana.com/docs/alloy/latest/reference/)

[Read the reference documentation about the command line tools, configuration blocks, components, and standard library.](https://grafana.com/docs/alloy/latest/reference/)



Source: <https://grafana.com/docs/alloy/latest/>