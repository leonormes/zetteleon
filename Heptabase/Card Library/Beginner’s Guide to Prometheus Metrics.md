# Beginner’s Guide to Prometheus Metrics

Over the past decade, Prometheus has become the most prominent open source monitoring tool in the world, allowing users to quickly and easily collect metrics on their systems and help identify issues in their cloud infrastructure and applications.

Prometheus was originally developed by SoundCloud when the company felt their metrics and monitoring solutions weren’t meeting their needs. Prometheus was then released to open source and later accepted by the Cloud Native Computing Foundation as their second incubated project after [Kubernetes](https://logz.io/blog/unified-observability-kubernetes-360/). 

The Prometheus open source software collects and stores [metrics as time series data](https://logz.io/blog/phantom-metrics-monitoring-dashboard-lying/)—or, info stored with timestamp data so users can gain a better understanding of the metrics at a certain point in time. Prometheus doesn’t require any upfront cost, won’t produce any vendor lock-in, and is great for organizations wanting to quickly start their cloud monitoring journey.

Prometheus is especially appealing to cloud-native organizations, due to its native integration with Kubernetes and other cloud-native technologies.

However, [infrastructure monitoring with Prometheus](https://logz.io/platform/infrastructure-monitoring/) can become time-consuming as [data volumes grow](https://logz.io/blog/expensive-metrics-monitoring-data/). This oftentimes requires elaborate architectures to horizontally scale across multiple Prometheus servers – due to Prometheus’ single node architecture. Plus, Prometheus can only collect and store metrics, which leave log and traces siloed in different systems — prolonging incident investigations that require engineers to quickly correlate across different data types.

What makes Prometheus metrics so important to your systems as you determine your path forward for full-stack observability? We’ll dive deep in this guide on what’s so critical about Prometheus metrics and how you can get the most out of them.

## **What Are Prometheus Metrics?**

In the simplest terms possible, metrics are a measure of something—quite literally anything. Prometheus metrics are quantifiable data points most commonly used to monitor cloud infrastructure, and they’ll signal when and where problems have taken or are taking place. 

[Infrastructure monitoring](https://logz.io/platform/infrastructure-monitoring/) metrics provide organizations insight into what’s happening in a given environment. Metrics collected by Prometheus are critical for staying alerted when something goes wrong in your system. They can be visualized on dashboards or continuously monitored by Prometheus’s AlertManager to trigger notifications whenever the data crosses a predefined threshold. 

Put simply, metrics are important to monitor the health of your system without waiting for end users to flood your support system.

In order for the Prometheus infrastructure monitoring system to work, it needs to have targets from which it collects metrics. These targets can be an endpoint that can be monitored, or they can be something else. Either way, Prometheus scrapes and stores these metrics from targets, which can then be cross-referenced with logs or traces to determine the root cause of any issues that might come up.



There are [numerous system components](https://prometheus.io/docs/introduction/overview/) that allow Prometheus to collect metrics (many of them being optional). They include:

- **The server** scrapes and stores time series data

- **Client libraries** that are used to instrument applications so Prometheus can monitor them

- **A push gateway** that supports short-lived data import jobs

- **Exporters** that send data to services such as HAProxy, StatsD, Graphite, etc.

- **AlertManager** for handling alerts

Prometheus contains the following main features for the collection of metrics:

- A **multi-dimensional** data model, where time series data is defined by metric name and key/value dimensions

- A **flexible query language** ([PromQL](https://logz.io/blog/promql-examples-introduction/))

- **Autonomous single server nodes** with no dependency on distributed storage;

- Data Collection via a **pull model** over HTTP

- Time series data **pushed** to other data destinations and stores via an intermediary gateway

- Targets discovered via **service discovery** or **static configuration**

- Multiple support modes for **graphs** and **dashboards,** although the most commonly-used tool for prometheus metrics visualization is Grafana.

- Federation-supported both hierarchically and horizontally

Additionally, the Prometheus client supports multiple third-party implementations for service discovery, alerting, visualization, and export—thus enabling the admin to use the best-suited technologies for each.

![](https://dytvr9ot2sszz.cloudfront.net/wp-content/uploads/2023/02/1200x520_Prometheus-Metrics-Types-1024x444.png)

[Metrics](https://logz.io/blog/phantom-metrics-monitoring-dashboard-lying/) are retrieved by Prometheus through a simple HTTP request. For this reason, there can be thousands—potentially many, many thousands—of Prometheus metric types that can be collected by a user or organization running the software. 

However, these [Prometheus metrics](https://logz.io/blog/infrastructure-monitoring-metrics-explore/) types generally fall into four core types: counter, gauge, histogram and summary. The first two metric types are fairly straightforward and fall into the normal way anything of their name would be measured, while the last two are a bit more advanced. Let’s take a look at each of these metric types.

**Counter**: Counters are used for the cumulative counting of events, as its name would indicate: think of it like a hand counter people use to keep tabs on the size of a crowd in a given location.

The value of a counter can only increase or be reset to zero when it is restarted—it will never decrease on its own. A counter metric in Prometheus can be used, for example, to show the number of errors or tasks completed depending on the use case.

**Gauge**: Gauges typically represent the latest value of measurement. It’s no different than the gauge on an automobile dashboard showing how much gasoline remains in the tank, or a thermometer showing what the temperature is like inside or outside. Unlike a counter, a gauge can go up or down depending on what’s happening with the endpoint that’s being measured.

For metrics being collected by the Prometheus client, this can include areas such as a number of concurrent requests or how much of a CPU is being utilized over a period of time.

**Histogram**: More advanced and complex than counters or gauges, a histogram takes a sample of observations and counts them in buckets that can be a configuration by the user. As an example, a user may want to understand memory usage percent segmented by pods across a Kubernetes cluster in given points in time. The best way to do that is through a histogram.

A histogram will provide a sum of all observed values in one place, including cumulative counters for observation buckets, the total sum of all observed values, and the count of events that have been observed.

Additionally, Prometheus is working on experimental support for [native histograms in recent versions as of 2023](https://logz.io/blog/prometheus-roadmap-latest-updates/). These require only one time series, include a dynamic number of buckets, and allow a much higher resolution at a fraction of the cost.

Note: histograms are more consuming in storage and in throughput, as every sample is not just a single number but rather a few samples (one per bucket).

**Summary**: Like a histogram, a summary samples observations in one place. It also offers a total count of observations, as well as a sum of all observed values. However, it can additionally calculate configurable quantiles over a desired period of time and expose them directly.

Summaries mainly cover service level indicators, as they offer a gauge of histograms, specifically of limited selections (quantiles) of a range of values. Summaries calculate streaming quantiles on the client side and expose them directly, which is the chief difference between summaries and histograms (the latter of which expose bucketed observation counts—quantile calculation happens there on the server side).

## Prometheus Metrics Format and Use Cases

![](https://dytvr9ot2sszz.cloudfront.net/wp-content/uploads/2023/02/1200x520_Prometheus-Metrics-Format-and-Use-Cases-1-1024x444.jpg)

The best use cases for Prometheus include scenarios where any purely numeric time series data needs to be recorded. If your system suffers an outage, Prometheus can be a place you can go to quickly begin your investigation of the issue. Any Prometheus server you have running doesn’t depend on remote services or network storage.

Prometheus metrics can be gleaned from different types of monitoring formats, from machine-centric to dynamic, service-oriented architectures. You’ll be able to get your metrics even if other parts of your infrastructure aren’t working.

Some of the best use cases for Prometheus metrics include:

**CPU utilization**: This can be a counter metric that tells you how much time a CPU has been running in a specific mode. This can include several modes including iowait, idle, user and system. Such a metric as this is part of a group of different use cases around Prometheus metrics from a service that runs constantly.

**Memory usage**: This metric can be used to calculate the total percentage of memory being used by a machine at a specific time. This is similar to the CPU utilization use case, where the metrics are being collected from a service that’s constantly running.

**Disk space**: In order to understand your disk usage, you can run similar methods to memory and CPU usage to see how much free disk space you have. This is also part of a group of popular Prometheus metrics use cases where operating systems are monitored. 

## The Challenges of Collecting Prometheus Metrics

When it comes to monitoring containerized microservices and the infrastructure that runs them—such as Kubernetes—Prometheus is a simple and powerful option. Yet, you should be aware of some challenges presented by Prometheus and its [methods of collecting metrics](https://logz.io/blog/aws-lambda-metrics-monitoring-guide/).

Most critically, [Prometheus doesn’t scale well](https://logz.io/blog/devops/prometheus-architecture-at-scale/). It runs on a single machine and periodically connects to an endpoint on each of the containers, servers and VMs it is monitoring to scrape metrics data from them. A single Prometheus server can see its scraping capabilities quickly overloaded by any large organization that runs multiple instances of each of hundreds of microservices.

This is by design. The Prometheus client is so easy to implement because of its single-node architecture — simplicity and scalability was a tradeoff for its designers, and they chose simplicity. 

We mentioned before about how Prometheus metrics are stored in a time-series database. This database is stored on a local disk. When cloud-native applications grow, [these metrics can very easily fill the disk of a Prometheus server](https://logz.io/blog/observability-expensive-cardinality-problem/) based on your configuration.

Once Prometheus machines fill up with data, a common way to scale Prometheus metrics beyond the machine storage capacity is by building a federated architecture. You can implement horizontally scalable solutions like M3DB, Thanos, or Cortex to collect metrics from your Prometheus servers at larger scales. [Learn more about building a scalable Prometheus architecture](https://logz.io/blog/devops/prometheus-architecture-at-scale/).

Organizations that don’t find a way to scale Prometheus are left with choices that are far from ideal. You may be required to reduce the granularity of the metrics that are being collected, or data may need to be downsampled. Neither of these are good choices because they make the metrics you’re collecting less useful. Ensure you’re able to collect and store all of the monitoring data you need as your application grows; scalable cloud applications need monitoring that scales with them along the way.

***[Sign up for a free trial of Logz.io to see how Prometheus-as-a-Service can transform your infrastructure monitoring today.](https://logz.io/freetrial/)***

## Conclusion

Prometheus metrics are a powerful way to monitor applications. It’s easy to get started and helps you diagnose problems quickly. There are numerous practical applications and business use cases where using Prometheus to monitor infrastructure is critical. 

It’s important to understand the scaling issues that often come up with Prometheus and understand how they can be addressed. You can get the most out of your Prometheus metrics by accessing them through [a fully-managed cloud service](https://logz.io/blog/prometheus-as-a-service-launch/). 

You can utilize what makes Prometheus great while also benefiting from features such as scalable and zero maintenance data storage, enhanced visualization capabilities, customized dashboards, and data correlation with logs and traces to [unify observability in one place](https://logz.io/platform/).

[Speak to a Logz.io solutions expert today so you can get the most out of your Prometheus metrics.](https://logz.io/request-demo/)



Source: <https://logz.io/learn/prometheus-metrics-guide/>