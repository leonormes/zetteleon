---
title: 'Data points per minute in Grafana Cloud: What you need to know about DPM'
source: https://grafana.com/blog/data-points-per-minute-in-grafana-cloud-what-you-need-to-know-about-dpm/
captured: 2026-08-24T10:25:52+01:00 2026-08-24T10:25:52+01:00
status: processing
tags:
- input
type: head
permalink: llmeon/00-inbox/head-data-points-per-minute-in-grafana-cloud-what-you-need-to-know-about-dpm
---

## Data points per minute in Grafana Cloud: What you need to know about DPM

If you’re working with metrics in Grafana Cloud, chances are you’ve come across DPM (data points per minute). It shows up in usage dashboards, invoice breakdowns, and occasionally pops up in Slack when your ingestion numbers start looking suspicious.

DPM can also be seen in the Grafana Cloud [billing and usage dashboard](https://grafana.com/docs/grafana-cloud/cost-management-and-billing/understand-your-invoice/?pg=data-points-per-minute-in-grafana-cloud-what-you-need-to-know-about-dpm&plcmt=in-text#billing-and-usage-dashboard), which is available by default in every Grafana Cloud account. It helps you understand how much data you’re sending—and whether it’s more than you need.

But what is DPM really measuring? Why does it matter? And what should you do if it’s higher than you expected?

This post is your all-in-one guide to understanding DPM: how it works, why we care about it, how to spot issues, and how to keep things clean and efficient.

## What Is DPM? (And why does it exist?)

DPM is a measure of how frequently each unique time series sends data to Grafana Cloud. If you’re scraping a metric every 60 seconds, that series has a DPM of 1. Scrape it every 10 seconds? Now you’re at 6 DPM.

Grafana Cloud uses DPM as a core part of its billing and usage model—and not arbitrarily. It’s a proxy for ingestion volume and system load. More DPM means more compute, more storage, and more bandwidth.

![DPM panels in Grafana Cloud](https://grafana.com/mw/_next/image/?url=https%3A%2F%2Fa-us.storyblok.com%2Ff%2F1022730%2Fbf45e4d774%2Fmetrics-active-series.png%2Fm%2Ffilters%3Aformat(webp)%3Aquality(100)%2F&w=3840&q=75)

And here’s the baseline: 1 DPM per active time series is what’s included in Grafana Cloud plans. That’s not just a quota—it’s the expected norm. For most metrics, 1 DPM is the sweet spot. It gives you the granularity you need for dashboards and alerting, without wasting resources or overloading your pipeline.

## Why high DPM usually isn’t worth it

You might assume that scraping more frequently equals more accuracy, which equals better monitoring. But in reality, it’s usually just…more.

- **Dashboards don’t benefit:** Most panels aggregate to 1 data point per pixel.
- **Alerts won’t fire faster:** Most rules evaluate once per minute or longer.
- **Costs go up:** Anything over 1 DPM is considered overage.

If you’re sending the same data six times more often, but not actually using that resolution, you’re just adding noise (and possibly higher bills).

## When higher DPM does make sense

That said, there are cases where more frequent data is genuinely useful. For example:

- **SLO burn rate alerts** with short time windows (e.g., 1-minute error windows)
- **Real-time incident debugging** where second-by-second changes matter
- **Low latency systems** like trading engines, game servers, or high frequency telemetry

In those scenarios, higher DPM might be intentional and worthwhile. Just be sure it’s driven by actual need, not default scrape configs.

## How to investigate and reduce high DPM

If your usage dashboards show DPM creeping up, or your bill looks higher than expected, here’s a checklist to get things under control.

### 1\. Scrape intervals

Look at your Prometheus or [Grafana Alloy config](https://grafana.com/docs/grafana-cloud/cost-management-and-billing/reduce-costs/metrics-costs/adjust-data-points-per-minute/?pg=data-points-per-minute-in-grafana-cloud-what-you-need-to-know-about-dpm&plcmt=in-text). Are you scraping everything every 15 seconds? Try bumping lower priority targets to 30 or 60 seconds.

### 2\. Identify DPM per series with Explore

To see DPM per series for a specific metric, try this PromQL query in Explore:

```
sort_desc(count_over_time({__name__="your_metric_name"}[1m]))
```

This shows how frequently each series is sending data. If you’re not sure where to start, begin with metrics that have high cardinality and work your way down.

### 3\. Check for discarded writes

Samples that get discarded still count toward your total DPM, even though they don’t show up in your active series count. You can find these in the billing and usage dashboard, under the panel titled “Discarded Metric Samples.”

### 4\. Aggregation by label set

If multiple instances emit identical label sets—even if each producer sends reasonable data—Grafana will merge them. This can lead to a DPM spike.

To address this, either:

- Add a per-producer label (like `instance`) to separate them
- Or aggregate earlier (e.g., in the agent or via recording rules)

### 5\. Check recording rule frequency

Sometimes high DPM isn’t coming from scraped metrics at all—it’s being generated by recording rules. To find out if that’s the case:

- In Grafana Cloud, go to **Alerting** > **Alert Rules**, edit a rule group, and check its evaluation interval.
- You may also have recording rules defined in any upstream Prometheus instances. Validate those by checking the `interval` setting within the `rule_group` configuration.

### 6\. Cardinality dashboard

The [cardinality management dashboard](https://grafana.com/docs/grafana-cloud/cost-management-and-billing/analyze-costs/metrics-costs/prometheus-metrics-costs/cardinality-management/?pg=data-points-per-minute-in-grafana-cloud-what-you-need-to-know-about-dpm&plcmt=in-text) helps you spot when a single metric expands into thousands of unique label combinations. While high cardinality and high DPM aren’t directly connected, they often correlate in practice. That makes this dashboard a useful place to look when you’re investigating unexpected DPM spikes.

### 7\. Adaptive Metrics

Grafana Cloud’s [Adaptive Metrics](https://grafana.com/docs/grafana-cloud/cost-management-and-billing/adaptive-telemetry/adaptive-metrics/?pg=data-points-per-minute-in-grafana-cloud-what-you-need-to-know-about-dpm&plcmt=in-text) feature is typically used to automatically suggest aggregations or drop unused series based on real usage patterns.

But it can also be used manually, as you can define custom Adaptive Metrics rules to drop specific metrics. This is especially useful when the source of the high DPM isn’t easily traceable or when you want more control over what gets retained.

### 8\. OpenTelemetry Collector / Grafana Alloy interval processors

If you’re using an OpenTelemetry collector (contrib or Grafana Alloy), you can control DPM directly at the pipeline level using an interval processor.

This component reduces the frequency of metric emission by aggregating metrics and periodically forwarding the latest values to the next component in the pipeline:

- In OpenTelemetry Collector, see the [intervalprocessor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/intervalprocessor)
- In Alloy, check out the [otelcol.processor.interval](https://grafana.com/docs/alloy/latest/reference/components/otelcol/otelcol.processor.interval/?pg=data-points-per-minute-in-grafana-cloud-what-you-need-to-know-about-dpm&plcmt=in-text) component

## Analyze metrics with dpm-finder

If you want a more direct, data-driven look at what’s actually being ingested—especially across a large set of metrics—a CLI tool can make that a lot easier.

This is where [dpm-finder](https://github.com/grafana-ps/dpm-finder), a lightweight Python tool, comes into play. It connects directly to the Prometheus HTTP API to check how often each metric is being scraped, so you can get a clear picture of DPM across your dataset.

Setting it up is pretty simple: Add the right environment variables, run the script, and dpm-finder gives you a list of metrics with their calculated DPM.

If you’re using Grafana Cloud, you can find all the connection details you’ll need in your stack settings at [grafana.com](https://grafana.com/?pg=data-points-per-minute-in-grafana-cloud-what-you-need-to-know-about-dpm&plcmt=in-text). Go to your stack, click **Details** under Prometheus, and copy:

- The Prometheus remote write URL
- Your tenant ID (used as the username)
- Then, generate an API key with read access
![Query endpoint menu](https://grafana.com/mw/_next/image/?url=https%3A%2F%2Fa-us.storyblok.com%2Ff%2F1022730%2Fd5b2137033%2Fquery-endpoint.png%2Fm%2Ffilters%3Aformat(webp)%3Aquality(100)%2F&w=3840&q=75)

Save them as the following environmental variables:

```
export PROMETHEUS_ENDPOINT="https://prometheus-XXX.grafana.net/api/prom"
export PROMETHEUS_USERNAME="1234567"
export PROMETHEUS_API_KEY="glc_XXX=="
```

Install the required Python packages:

```
pip install -r requirements.txt
```

Once everything’s set, run the script to get DPM results per active-series:

![Output code](https://grafana.com/mw/_next/image/?url=https%3A%2F%2Fa-us.storyblok.com%2Ff%2F1022730%2F821ccf9a4e%2Fdpm-finder-py.png%2Fm%2Ffilters%3Aformat(webp)%3Aquality(100)%2F&w=3840&q=75)

## Final thoughts

DPM isn’t just a billing metric—it’s a lens into how your observability pipeline behaves.

If you’re seeing unexpectedly high usage, start with scrape intervals and instrumentation. Use the dashboards. Use the tooling. Know when high DPM is worth it, and when it’s not.

*[Grafana Cloud](https://grafana.com/products/cloud/?pg=blog&plcmt=body-txt)* *is the easiest way to get started with metrics, logs, traces, dashboards, and more. We have a generous forever-free tier and plans for every use case.**[Sign up for free now](https://grafana.com/auth/sign-up/create-user/?pg=blog&plcmt=body-txt)**!*