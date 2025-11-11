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
source: "https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/optimize-resource-usage/container-requests-limits-cpu/#cpu-requests"
source_of_truth: []
status: 
tags: []
title: Strategies for assigning CPU requests and limits to containers  Grafana Cloud documentation
type: 
uid: 
updated: 
---

![ObservabilityCON 2025](https://grafana.com/media/events/obscon/2025/grafana-obscon2025-promo-logo-black.svg)

📢 Registration + agenda now live Explore the latest Grafana Cloud and AI solutions, learn tips & tricks from demos and hands-on workshops, and get actionable advice to advance your observability strategy. Register now and get 50% off - limited tickets available (while they last!).

Strategies for assigning CPU requests and limits to containers

## Strategies for Assigning CPU Requests and Limits to Containers

You can place CPU usage [requests and limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) on every container. As a best practice:

- Always set CPU usage requests on containers.
- Only in some cases, set CPU limits on containers.

Use Kubernetes Monitoring to discover:

- Whether your CPU usage requests are appropriate or need adjusting
- When a CPU limit is temporarily needed

When neither CPU requests nor limits are set, Pods use as much resource as the kernel makes available to them, which can become chaotic on contended Nodes. If you are using a Kubernetes autoscaler in the Cluster, additional Nodes may be provisioned to help counter the effect of runaway Pod resource consumption, but this can also mean increased infrastructure cost.

A Pod with no CPU request is assigned a BestEffort quality of service, and can grow with no limits. When the Node attempts to regain some CPU to keep remaining Pods operational, kubelet evicts any BestEffort Pods first.

## CPU Requests

When you set a CPU request for a container, the container has that amount of CPU reserved from a Node’s total capacity, which is then guaranteed by the Scheduler. Just like a set of reserved hotel rooms that are not all occupied, the requested CPU usage is available even if the container doesn’t use it all.

![Graph of container CPU use compared to allocation](https://grafana.com/media/docs/grafana-cloud/k8s/containerCPU-use-allocation.png?w=320)

Graph of container CPU use compared to allocation

This usage request is like a “soft” threshold, meaning a container might use more than the amount of CPU reserved. The CPU needed for a Pod is the sum of the CPU needed by the containers within it.

### Analyze Historical CPU Usage

Here’s an example you can follow which highlights the major steps for identifying and handling an issue with the CPU request setting.

1. Determine the time range.
	Use the time range selector to look at the history of a Pod’s CPU usage. At the Pod detail page, select a time frame. In this example, the time range is selected for the past two days.
	![Time range selector showing calendar options and various set ranges in a list](https://grafana.com/media/docs/grafana-cloud/k8s/screenshot-time-picker-2-day.png?w=320)
	Selecting two-day time period
2. Examine the behavior pattern.
	In the Pod optimization panel, look at the pattern of behavior for CPU usage. In this example, there have been several CPU bursts above the CPU request of 5 cores within a two-day period.
	![Graph of Pod CPU usage bursting above the line for CPU limits for two-day period](https://grafana.com/media/docs/grafana-cloud/k8s/screenshot-pod-2-day-cpu-bursts.png?w=320)
	Pod with CPU bursts in two-day time period
3. Set the time range farther back for more data.
	Investigate more history by changing the time range to the past 30 days, which shows more CPU bursts far beyond the CPU request’s current setting. Here, it looks as though this behavior has been happening for some time.
	![Graph of Pod CPU usage bursting above the line for CPU limits for 30-day period](https://grafana.com/media/docs/grafana-cloud/k8s/screenshot-pod-30-day-more-cpu-req-need.png?w=320)
	Pod with CPU bursts in 30-day time period
4. Go to a view of the container.
	The Pod detail page contains a list of all containers within the Pod. To determine which container might be the issue for this Pod, click on a container in the list to view more detail.
	![List of Pods in the container](https://grafana.com/media/docs/grafana-cloud/k8s/container-list.png?w=320)
	List of containers in Pod on Pod detail page
	At the Container detail page, you can see the data is conclusive. The CPU request is undersized for the container, and an additional 1.7 cores is recommended.
	![Graph of container CPU usage bursting above limits requested and a gauge showing CPU limit is undersized](https://grafana.com/media/docs/grafana-cloud/k8s/screenshot-container-30-day-more-req-needed.png?w=320)
	Container detail page with gauge indicating CPU request is undersized
5. Take action based on the data.
	You can make an adjustment to this container knowing the data shows it’s needed. And you can continue to monitor it to ensure your change solved the issue.

### Allow for Some Bursting

It is important to allow and expect CPU bursting to occur over short periods, to reduce application latency during usage peaks. Just keep in mind containers with undersized CPU requests “steal” spare capacity from the Node they’re running on.

### Recognize Undersized CPU Requests

What about containers that don’t show bursting behavior? An undersized CPU request can also cause the consumed CPU to remain consistently at a level very close to or above the requests. Make sure Nodes always have some spare “flex” capacity to be distributed among its Pods. Increase the CPU requests for an undersized container so that the general ebb and flow of daily peaks and troughs of CPU usage are handled in a predictable manner.

When more than one Pod has containers with undersized CPU requests, the Scheduler has difficulty trying to correctly fit the Pods within your cluster, due to the unpredictable nature of the CPU burst distribution. As a result, it is harder to right-size your Nodes and work toward predictable infrastructure costs.

### Continue Monitoring to Refine CPU Requests

There is a delicate balance and, perhaps, an ongoing effort to maintain the ideal resource limits for containers as your service usage evolves over time. Set and reset the CPU requests and monitor the usage to find your equilibrium.

## CPU Limits

A CPU limit is a *hard* threshold. In the same way you can only reserve the total amount of rooms in a hotel, no more CPU use is available beyond the set CPU limit. If a workload needs more CPU, it can’t access any more than the limit. This causes [CPU throttling](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/optimize-resource-usage/cpu-throttling/), which leads to performance issues caused by latency.

While there are many discussions about setting CPU limits, it’s vital to understand [how they work](https://medium.com/omio-engineering/cpu-limits-and-aggressive-throttling-in-kubernetes-c5b20bd8a718) ([including the CFS quota mechanism](https://www.kernel.org/doc/Documentation/scheduler/sched-design-CFS.txt)) and whether you truly need them. The following links can provide some clarification and potential guidance:

- [Stop Using CPU Limits on Kubernetes](https://home.robusta.dev/blog/stop-using-cpu-limits)
- [CPU limits and aggressive throttling in Kubernetes](https://medium.com/omio-engineering/cpu-limits-and-aggressive-throttling-in-kubernetes-c5b20bd8a718)
- [The case for Kubernetes resource limits](https://kubernetes.io/blog/2023/11/16/the-case-for-kubernetes-resource-limits/)
- [Requests are all you need](https://www.numeratorengineering.com/requests-are-all-you-need-cpu-limits-and-throttling-in-kubernetes/)
- [The Case for Kubernetes Resource Limits: Predictability vs. Efficiency](https://kubernetes.io/blog/2023/11/16/the-case-for-kubernetes-resource-limits/)

### Set Temporary CPU Limits

You can set a CPU limit temporarily to stop an issue from going out of control, as well as give you time to troubleshoot an issue. Let’s say a bug is introduced into your code that causes [backtracking](https://www.regular-expressions.info/catastrophic.html), which begins to consume an enormous amount of CPU. You replicate the Node, but unfortunately, that doesn’t solve the problem.

When you set the time range for the last seven days on the Pod detail page, you see the CPU bursting for the last day is now far beyond the set CPU request.

![Graph of Pod CPU usage bursting far beyond the CPU limit threshold](https://grafana.com/media/docs/grafana-cloud/k8s/screenshot-runaway-pod.png?w=320)

Runaway Pod with CPU bursting out of control

Currently, there is no CPU limit on the containers in this Pod. As a temporary solution, set the CPU limit so that you can prevent CPU exhaustion and troubleshoot the issue.
