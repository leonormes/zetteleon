# Prometheus Labels: Understanding and Best Practices

![rw-book-cover](https://www.cncf.io/wp-content/uploads/2025/07/Blog-Default-6.jpg)

## Metadata
- Author: [[Neel Shah]]
- Full Title: Prometheus Labels: Understanding and Best Practices
- Category: #articles
- Summary: Prometheus labels add important context to metrics, helping to filter and group data effectively. They improve observability by distinguishing metrics and supporting detailed queries with PromQL. To get the best results, use labels carefully and manage them well to avoid performance issues.
- URL: https://share.google/LKKWNJNbNutMnK8RK

## Full Document
*Member post originally published on the* [***Middleware***](https://middleware.io/)*blog by* [*Keval Bhogayata*](https://middleware.io/blog/authors/keval/), covering all the best practices for [prometheus labels](https://middleware.io/blog/prometheus-labels/).

In observability, Prometheus is a well-known tool amongst SREs and engineers alike. What makes Prometheus so effective is the labels Prometheus implements, which provide context to its metrics and facilitate operations such as filtering and aggregations.

By the end of this post, you’ll understand what Prometheus labels are, why they matter and how you can use them. We’ll also learn some Prometheus labels best practices that you can use to make the most out of Prometheus labels and supercharge your observability.

#### **Anatomy of a Prometheus Metric**

Each Prometheus metric is composed of the following components:

* Metric Name: Description of what metric is being measured
* Prometheus Metric Labels: Key-value pairs that add context to the metric
* Value: The measurement value itself
* Timestamp: Point in time that indicates the exact moment the metric was recorded

Let’s understand the anatomy of a typical Prometheus metric using a Prometheus labels example. Consider the following Prometheus time series:

In the above time series, http\_requests\_total is the metric name. It’s self-explanatory in it’s purpose, as it measures the number of HTTP requests made over a specific period. Then, we have the Prometheus metric labels with their key-value pairs:

Finally, we have the timestamp with value `1024`. As you can see, the labels give a more well-rounded meaning to the metric.

#### **Why Labels Matter in Prometheus**

Consider the Prometheus time series in the previous section. What if we removed all the labels from it? This is what it would look like:

We can see this metric and understand what it means, but there’s still so much to unravel. What kind of requests is this metric measuring? How is this metric correlated to your service or backend in general? Does it tell me all the successful requests, redirects or failures?

Prometheus labels offer immense value by providing more granular context for the metric. They enrich your metrics with contextual metadata, improving visibility across services and environments.

They also help differentiate between two metrics with the same name.

The above label, as seen previously, measures `HTTP POST` requests made to the `/login` endpoint that respond with a status code of `200`.

On the other hand, the above label measures `HTTP GET` requests made to the `/auth-token` endpoint that respond with a status code of `400`.

If you were to remove labels from both the metrics, you’d be unable to tell them apart.

Moreover, Prometheus labels are used for PromQL aggregations like grouping and filtering. We’ll see them in action later.

Prometheus employs its query language, called PromQL, which you can use to generate queries on top of your metrics. You can also use PromQL extensively for visually understanding your observability patterns through custom dashboards.

Here are some of the common examples of where PromQL leverages Prometheus labels for its queries. We’ll explore these in detail and understand how they can be useful in the coming sections:

The above query calculates how many HTTP requests have a status code 500 in the last 5 minutes. Using PromQL, we filter the metric to focus only on failed requests, to quickly spot error spikes without being distracted by successful requests.

The above query measures how many POST requests were sent to the endpoint “`/api/login`” in one second over the last 5 minutes. We’ve combined the two label filters (method and endpoint) to precisely target a critical authentication pathway in our application.

The above grouping query helps us understand the total request rate for each method separately to assess how traffic is spread across different APIs. The query first calculates the per-second rate of all HTTP requests over 5 minutes, then groups and sums these rates by the HTTP method `(GET, POST, PUT, etc.)`.

Let’s explore some of the common use cases for Prometheus labels with examples

A modern observability system has tons of valuable metrics defined. How do you filter these metrics and only observe metrics that are relevant to the situation at hand? For instance, you might want to see the response times metrics for a specific region that is experiencing high traffic. Or you might want to see metrics for only the staging environment to test your feature releases.

Using the labels Prometheus provides, you can easily filter metrics by various properties or attributes such as method, environment, region, team, etc.

Let’s say you want to monitor response times for staging environments only. If you set a label environment with the value “staging”, you can then filter all the response times for your staging environment using this label.

Similarly, you can also filter your metrics by a label called region. This can help you isolate metrics from a specific region.

You can also combine the two:

##### **2. Aggregating by Status Codes**

Combining various metrics can give you a great sense of your system’s overall health. You can aggregate metrics such as errors or successes for this purpose.

This can be extremely helpful in monitoring HTTP request success rates and, in turn, understanding any issues with specific endpoints. Consider the following aggregation:

The above will first group all the HTTP request rates in the last 5 minutes by the value of the labels Prometheus provides, specifically status and endpoint. It will then sum the HTTP request rate for these 5 groups and give the sum as a result.

Using the above aggregation, you can see if there was an anomaly in the last 5 HTTP request rates.

Let’s consider a real-life example where an aggregation can be immensely helpful. You can use aggregations to identify which endpoints are failing in your system:

Breaking down the above aggregation:

* `rate(http_requests_total[5m])` calculates the per-second rate of requests over a 5-minute window
* `sum by (endpoint, status_code)` aggregates these rates by endpoint and status code
* The > 0 filter shows only endpoints actively experiencing errors

The above query could tell you that a specific endpoint is returning 5XX errors, which can propel you to focus your debugging efforts on that specific service, rather than going through all the services.

Further, you could extend this to create error alerts by comparing error rates to total requests:

```
sum by (endpoint) (rate(http_requests_total{status_code=~"5.."}[5m])) / sum by (endpoint) (rate(http_requests_total[5m])) > 0.01
```

When an endpoint exceeds an error rate of 1%, you can get an alert and take the necessary action.

We know that Prometheus labels help add additional context to your metrics. A common use case is adding multiple dimensions such as host, service, version of their software, etc.

For instance, let’s say you want to pinpoint CPU spikes to a specific software version. The CPU usage across different application versions and hosts can be given by the following metric:

Using the Prometheus labels for multiple dimensions, such as host, service and version, you can now understand CPU usage across a specific dimension.

Let’s say you’ve rolled out a new version, `v2.0.1` of your authentication microservice. Now you’re seeing an increased latency in your application. You can use Prometheus labels to perform multi-dimensional monitoring and hence compare how your new version of the endpoint consumes resources for the previous version:

The above query will give you how much more your new version is using CPU resources than the previous version, which can prompt you to fix the new release or roll it back if needed.

Another useful scenario for multi-dimensional monitoring is combining these dimensions to track metrics across your entire infrastructure. Consider the following query:

The above query gives you a broad overview of memory usage metrics from datacenter clusters down to individual containers for targeted troubleshooting.

##### **4. Monitoring Infrastructure and Application Health**

Prometheus labels help you distinguish your resource usage across various infrastructure components, which can help you assess your application’s health.

For example, if you want to prevent database outages, you can monitor disk usage on your database nodes:

Moreover, you can also detect and address any memory leaks in specific microservices running in container environments like Kubernetes.

Imagine getting hold of your engineers at 2 AM to debug performance issues of your database. With Prometheus labels, your metrics can help you easily determine the root cause of such performance issues:

```
node_disk_io_time_seconds_total{host="db-server-1", device="sda"} / node_disk_io_time_weighted_seconds_total{host="db-server-1", device="sda"}
```

The above query gives you disk utilization, and another related query shown below tells you the remaining space in your file system:

```
(node_filesystem_size_bytes{mountpoint="/var/lib/postgresql/data"} - node_filesystem_free_bytes{mountpoint="/var/lib/postgresql/data"}) / node_filesystem_size_bytes{mountpoint="/var/lib/postgresql/data"} * 100
```

Maybe a recent data import that you ran didn’t clean up any temporary files, which is causing your database to slow down due to low disk space and high memory usage, thanks to a result of the above queries.

With these labelled metrics, you identify that a recent data import job didn’t clean up temporary files, causing the database to slow down as disk space approached capacity.

##### **5. Business Metrics and Custom Dimensions**

Perhaps the most underrated use case of Prometheus labels is tracking business metrics such as signups, purchases or transactions, drop-offs,etc. This metadata is helpful for your business and analytics teams to improve your product.

The following metrics use the source and campaign Prometheus labels to measure the effectiveness of your marketing campaigns by checking the number of signups that occurred via that campaign.

Here’s another example that helps you analyse trends in the transaction and performance across different payment methods and currencies to give you insights on how to improve the checkout process of your product.

When you’re using Prometheus labels in your observability environment, it’s important to follow some standard Prometheus labels best practices to ensure these labels don’t end up being counter-productive.

The keys to your labels should always be self-explanatory and descriptive. Avoid using random strings or keywords to name your label keys. Instead, use words that depict the meaning of the label, like method, status etc.

Avoid labels that have high cardinality or unique values, as they can lead to performance issues. For example, labels such as `user_id="12345"`, request\_id=”abc-123″ have high cardinality. Instead, use labels with low cardinality, ex `status="200"`. Avoid labels like UUIDs or IP addresses.

For simplicity and intuitiveness, keep your label values short and finite. A label such as `region="us-west"` represents a short and finite value. Whereas, a label like `query="SELECT * FROM large_table"` represents unbounded values.

Define your label schema upfront as part of your observability strategy. This will help you structure your labels effectively. If you don’t plan a schema, you might end up creating too many labels or adding unnecessary complexity to your observability system.

##### **Debugging and Managing Labels in Practice**

Creating Prometheus labels is barely scratching the surface of a foolproof observability system. You also need to learn how to debug these labels and translate them into engineering insights and manage them effectively throughout your monitoring cycle.

The most effective way to verify if your Prometheus labels are correct and troubleshoot any issues related to them is directly using the /metrics endpoint. This is the most reliable way to get information on your labels when you’re debugging them. You can even use visualisation tools like Grafana and Prometheus to understand your label usage pattern and, in turn, identify any issues more intuitively. Since Prometheus integrates well with external monitoring tools like Middleware, you can use any monitoring tool of your choice to visualise Prometheus labels more effectively.

You should also perform routine housekeeping and remove any unused metrics or labels that are cluttering your observability platform. Managing labels periodically and updating them as your system evolves is crucial to make the most of your Prometheus labels.

We’ve discussed where Prometheus labels are helpful and how you can utilise them for monitoring, but a real-world system involves rapidly changing complexities and constraints. Following certain strategies can help you demystify label design for practical systems.

For instance, a consistent labelling strategy is essential in a microservices architecture. Due to the presence of multiple services interacting with one another, consistent labelling can ensure easy queries across those services and maintain uniformity in your observability.

In cloud native environments, labels can be used to capture relationships within service meshes. It can provide clarity on how services are interacting with one another and map out their dependencies.

Prometheus Labels are a powerful feature that provides meaningful context to your metrics. Using Prometheus labels for the right use case with the right set of practices and tools can help you enhance its effect on the observability of your system.

 [![KubeCon + CloudNativeCon India 2025](https://www.cncf.io/wp-content/uploads/2024/11/CNCF-Desktop.jpg)](https://events.linuxfoundation.org/kubecon-cloudnativecon-india-2025/)
