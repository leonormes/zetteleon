# An Intro to PromQL: Basic Concepts & Examples

PromQL, short for Prometheus Querying Language, is the main way to query metrics within Prometheus. You can display an expression’s return either as a graph or export it using the [HTTP API](https://prometheus.io/docs/prometheus/latest/querying/api/). PromQL uses three data types: scalars, range vectors, and instant vectors. It also uses strings, but only as literals. This intro will provide basic PromQL examples and concepts to understand as you get used to Prometheus queries. To familiarize yourself with Prometheus-formatted metrics, see our recent blog [here](https://logz.io/learn/prometheus-metrics-guide/).

Many people arrive on this blog towards the beginning of their Prometheus journey. If you’re looking for an easy way to get started with Prometheus, check out Logz.io’s [Prometheus-as-a-service](https://logz.io/platform/infrastructure-monitoring/), which provides a simple, scalable, and low maintenance way to begin monitoring cloud infrastructure and popular cloud-native technologies with Prometheus.

Learn about the way Logz.io unifies and enhances the leading open source observability technologies [here](https://logz.io/solutions/simplify-open-source-observability/).

But alas, this blog is about PromQL, so let’s get started.

## PromQL: The Down-Low

Because it’s a DSL (domain-specific language) built upon Go, you’ll find PromQL has a lot in common with the language. But it’s also a nested functional language (NFLs), where data appears as nested expressions within larger expressions. The outermost, or overall, expression defines the final value, while nested expressions represent values for arguments and operands.

### PromQL Nested Expressions

We’ll cover PromQL nesting throughout the article. As you see more PromQL examples in different sections, these will appear from time to time, so while this seems like a more advanced concept, it’s good to explain it from the outset. And, on top of that, it’s probably a good idea to contrast it with less concise queries in other DSLs.

Unlike SQL or some domain-specific query languages, nested languages are not imperative/declarative languages as you’ll find in other places. PromQL and other nesting languages will insert expressions or queries within other queries.

Each subquery produces a value that serves as a variable for the larger expressions. Just like with the rules of operations, the outer, encompassing parenthetical expression returns the final answer (and thus the value you want).

```
sum(rate(http_requests_total{job="prometheus"}[5d]
```

```

```

You can also grab similar metrics by type, grouping them together in a PromQL query to display them together. It makes things far easier to view, without switching between the two. Similarly, PromQL lets you group multiple labels together, then sorting according to those groupings.

## Prometheus Metric and Data Types

If you want a more thorough intro to installation and configuration, check out our recent Prometheus tutorial for system and Docker metrics.

To be clear, there are two kinds of “types” in Prometheus. There are the metric types of metrics and the data types of PromQL expressions.

Prometheus has four *metric types*: 

1. Counters

2. Gauges

3. Histograms 

4. Summaries 

Counters give the absolute value of something, such as `prometheus_http_requests_total` or `prometheus_sd_consul_rpc_duration_seconds_count`. While counters only count upward, gauges will count upward and downward. Gauges might provide an average or range of values. Histograms cover `_count`, `_sum`, and `_bucket`.

In turn, summaries are similar to histograms but mainly cover service level indicators azs they offer a gauge of histograms, specifically of limited selections (quantiles) of a range of values.

PromQL subsequently has four *data types*:

1. Floats (mostly scalars) 

2. Range vectors

3. Instant vectors

4. Time (though it’s often not counted in this category)

#### **Floats**

PromQL has two kinds of literals: strings and floats. Specify string literals with backticks, single quotes, or double quotes. Just like Golang — the language Prometheus is written in — escaping uses a backslash (either single or double quotes). Any backslash within single or double quotes won’t function as an escape character.

Scalars or float literals can be integers or floats, using regex.

Take the following PQL example:

```
prometheus_http_requests_total{code=~"2.*", job="prometheus"}
```

![PromQL examples, showing labels for jobs and codes in regex, in the Prometheus UI](https://dytvr9ot2sszz.cloudfront.net/wp-content/uploads/2021/02/image1-1-1024x758.png)

PromQL examples, showing labels for jobs and codes in regex, in the Prometheus UI

For instance, you can return all values in the 200s or 400s:

```
prometheus_http_requests_total{code=~"2.*|4.*"}
```

![Prometheus returns multiple values for a single query, thanks to the PromQL built-in "OR" operator "|"](https://dytvr9ot2sszz.cloudfront.net/wp-content/uploads/2021/02/Screen-Shot-2021-02-16-at-15.36.43-1024x633.png)

Prometheus returns multiple values for a single query, thanks to the PromQL built-in “OR” operator “|”

#### **Instant Vectors**

Instant vectors can be queries simply by identifying the metric name. You can filter these values by referring to labels within curly brackets. Labels also include vector matching to either ignore or pay attention to a certain keyword, both in 1:1 matches and many:one matches.

Instant queries for table views contain the PromQL expression and a timestamp. Using an expression like some\[6h\] shows metrics from the last six hours for the series of some metrics. It can’t be used inversely. As in, you can’t mark \[-6h\] to view a point afterwards.

This is the basic syntax of those queries with some basic PromQL examples:

```
some_key {some_label="THATLABEL",another_label="THISLABEL"} [#value]
```

For a clearer example:

```
http_total_requests{job=”prometheus”, method=”post”, code=”404”} [5m]
```

Here are some other operators to know:

\#Labels *that don’t match* to the string

```
access_log{job!=”apache2”}
```

\#Labels with *exact match* to the string

```
http_total_requests{job=”prometheus”,method!=”GET”}
```

\#For labels *that don’t regex match* the string

```
http_total_requests{job=!~".prom*"}
```

\#Labels with exact regex match to the string

```
http_total_requests{job=~".prom*",environment=~”}
```

#### **Range Vectors** 

Range vectors select from a range within the instant that instant vectors select. Likewise, you’ll get to see a similar basic syntax:

```
<<metric name>>{<<label>>=”<<value>>”}[duration]
```

A duration to cover the length of that range goes at the end of the vector. For example, this gives metrics for the previous two minutes:

```
node_scrape_collector_duration_seconds{job=”node”}[2m]
```

You can go with other time durations also with the following symbols: ms, s, m, h, d, w, and y. They can be concatenated together but must be ordered by longest to shortest (years, weeks, days, seconds, etc.).

Critically, using the offset method will return results relative to a certain point in time.

For instance, ask for counters up until two days ago in this PromQL example:

```
http_requests_total offset 2d
```

They should follow the selector and can also be used on range vectors.

```
rate(http_requests_total[1h] offset 2d)
```

And if you are getting into range vectors, you need to acquaint yourself with subqueries.

## PromQL Feature Flags

Starting with v2.25,0, PromQL now includes a number of feature flags that you can activate. They’re also called Disabled Features, as you have to, as said before, activate them with a command.

That command follows this syntax:

```
--enable-feature=<name-of-the-feature>
```

Here’s the rundown of the new additions:

#### **The @ Modifier**

This lets you be extremely specific with the metrics you’re querying. 

It’s inactive by default, so activate it with the following command:

```
--enable-feature=promql-at-modifier
```

Add @ <timestamp> in front of the metric you’re querying to get what you want:

```
--enable-feature=promql-at-modifier @ 1623656380000)
```

#### **Negative Offset**

```
--enable-feature=promql-negative-offset
```

This lets you shift from a past metric value to a more recent one (essentially, instead of a back comparison, you shift closer to the present or future).

#### **Remote Write Receiver**

```
--enable-feature=remote-write-receiver
```

This lets you be extremely specific with the metrics you’re querying. 

#### **Exemplar Storage**

```
--enable-feature=promql-exemplar-storage
```

This lets you be extremely specific with the metrics you’re querying. 

#### **Expand Environment Variables in External Labels**

```
--enable-feature=expand-external-labels
```

This lets you be extremely specific with the metrics you’re querying. 

## PromQL Subqueries

Prometheus supports a large number of [functions](https://prometheus.io/docs/prometheus/latest/querying/functions/), aggregation operators, and binary [operators](https://prometheus.io/docs/prometheus/latest/querying/operators/). Other features include hashed comments by line (like many other languages) and subqueries for instantaneous queries when triggered.  

Subqueries, a themselves a feature of PromQL’s nested expression capabilities, allow for some sophisticated querying. Think of it as a range query within a query.

Here, you can check the 4-minute rate of http requests, but also over the course of two hours, at a timestamp resolution of 30 seconds.

```
rate(http_requests_total[4m])[2h:30s]
```

## PromQL Operators

Arithmetic binary operators

*Arithmetic Operators*

- \+ (add)

- – (subtract)

- \* (multiply)

- / (divide)

- % (percentage)

- ^ (exponents)

Comparison Binary Operators

*The following binary comparison operators exist in Prometheus:*

- == (equal to)

- != (does not equal)

- \> (greater than)

- < (less than)

- \>= (greater than or equal to)

- <= (less than or equal to)

Aggregation Operators

- `sum` 

- avg

- `min` 

- `max`

- `group` 

- `count` 

- `count_values` 

- `topk` (k = the number of elements; this selects the largest values among those elements)

- `bottomk` (like topk but for lowest values)

- `quantile` (calculate a quantile over dimensions)

- `stddev` (standard deviation over dimensions)

- `stdvar` (standard variance over dimensions)

## PromQL Functions

Most things available in query syntax will be there in a function option, too, plus some other options.

Time and date functions, unlike with basic query syntax, might include months:

```
day_of_month() - Returns a specific date, ranging from 1 through 31.
days_in_month() - Returning the total number of days in a month: 28, 29, 30, or 31.
month() - Returns the number of the month, ranging from 1 through 12.
```

Also found are `absolute value abs()`; predicting the values of a time series based on a vector with `predict_linear()`; and options for aggregations over time (avg_over_time, max_over_time, stddev_over_time, etc.). Here’s a full list of PromQL functions (with the type of metric selectors they display):

```
 
abs(instant-vector)
absent(instant-vector)
absent_over_time(range-vector)
ceil(instant-vector)
changes(range-vector)
clamp_max(instant-vector, scalar)
clamp_min(instant-vector, scalar)
day_of_month(some vector(time()) instant-vector)
day_of_week(some vector(time()) instant-vector)
days_in_month(some vector(time()) instant-vector)
delta(range-vector) #for use with gauge metrics
deriv(range-vector) #for use with gauge metrics
exp(instant-vector)
floor(instant-vector)
histogram_quantile(scalar, instant-vector)
holt_winters(range-vector, scalar, scalar)
hour(some vector(time()) instant-vector)
idelta(range-vector)
increase(range-vector)
irate(range-vector)
label_join()
label_replace()
ln(instant-vector)
log2(instant-vector)
log10(instant-vector)
minute(some vector(time()) instant-vector)
month(some vector(time()) instant-vector)
predict_linear() #for use with gauge 
rate(range-vector)
resets(range-vector) #for use with counter metrics
round((instant-vector, to_nearest=## scalar)
scalar(instant-vector)
sort(instant-vector)
sort_desc()
sqrt(instant-vector)
time()
timestamp(instant-vector)
vector()
year(some vector(time()) instant-vector)
avg_over_time(range-vector)
min_over_time(range-vector)
max_over_time(range-vector)
sum_over_time(range-vector)
count_over_time(range-vector)
quantile_over_time(scalar, range-vector) #φ-quantile (0 ≤ φ ≤ 1) of an interval’s values
stddev_over_time(range-vector) #standard deviation
stdvar_over_time(range-vector) #standard variance

```

## Prometheus and Logz.io

PromQL is a robust, extremely efficient language to survey Prometheus instances. By nesting queries within each other, a lot of information can be filtered quickly and cleanly. It makes querying more concise, especially compared to other DSLs tied to other metrics tools.

As mentioned earlier, if you’re interested in using Prometheus, but also want a unified view of your metrics, logs, and traces, check out [Logz.io ](https://logz.io/platform/)– which unites and enhances log, metric, and trace analysis using the leading open source observability technologies.



Source: <https://logz.io/blog/promql-examples-introduction/#prometheustypes>