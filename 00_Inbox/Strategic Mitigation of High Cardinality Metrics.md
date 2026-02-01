---
created: 2026-01-30T08:29:44+00:00
modified: 2026-02-01T15:09:20+00:00
title: Strategic Mitigation of High Cardinality Metrics
---

Since you are dealing with high cardinality, we can skip the basics and look at the specific mechanisms Prometheus and Grafana Alloy offer to mitigate resource exhaustion.

Based on the texts, here are the advanced strategies for managing high cardinality:

## 1. Identify the "Top 10"

The "Top 10" biggest metrics in a Prometheus instance often account for over 50% of total resource usage 1. Before optimizing everything, identify these specific metrics (often histograms or metrics with labels like user_id or path).

 Rule of Thumb: Ideally, keep the cardinality of a metric on a single instance below 10. A handful around 100 is acceptable, but anything higher usually belongs in a logging system rather than a metrics system 2.

## 2. Ingestion-Time Mitigation (Metric Relabeling)

If fixing the instrumentation code isn't an immediate option, you can use metric_relabel_configs to drop expensive data after the scrape but before storage 3.

 Drop Specific Histogram Buckets: Histograms are expensive because they multiply series count. You can use regex to drop less useful le (bucket) labels while preserving the _sum, _count, and the +Inf bucket (which is required for valid queries) 4, 5.

 Drop Entire Metrics: You can drop high-cardinality metrics entirely by matching against the name label with the drop action 3.

## 3. Emergency Valves

To prevent a single misbehaving target from crashing your Prometheus instance, configure sample_limit in your scrape config.

 This places a hard limit on the number of samples a single target can return. If the limit is exceeded (e.g., a developer adds a customer_id label), the scrape fails entirely, protecting the server 6.

## 4. Horizontal Sharding (Target Cardinality)

If the issue is the volume of targets rather than just label cardinality, you can horizontally shard Prometheus.

 Use the hashmod relabel action to distribute targets across multiple Prometheus servers. A master server can then aggregate specific metrics via federation or remote read 7.

 Alloy Specifics: If using Grafana Alloy in a clustered setup, be aware that disproportionately large targets (high cardinality sources) can cause uneven load distribution. In these cases, the documentation suggests scaling vertically rather than horizontally to handle the outlier targets 8.

## 5. Native Histograms (Experimental)

The texts mention "Native Histograms" as a newer feature that uses dynamic buckets to solve many of the cardinality and accuracy issues inherent in standard static buckets 9.

Would you like to see a configuration example for dropping specific histogram buckets using metric_relabel_configs?
