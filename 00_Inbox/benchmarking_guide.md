---
aliases: []
tags: []
title: Rust Benchmarking Guide
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2026-01-02T15:27:55+00:00
modified: 2026-01-02T19:50:39+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

# Rust Benchmarking Guide

This guide explains how to use Rust's built-in benchmarking tool (`cargo bench`), interpret its output, and track performance changes over time.

## 1. Running Benchmarks

`cargo bench` uses the nightly `test` crate feature (enabled via `#![feature(test)]`) to compile and execute benchmarks.

### Basic Command

Run all benchmarks in the project:

```sh
cargo bench
```

### Running Specific Benchmarks

You can filter which benchmarks to run by passing a name filter. For example, to run only HMAC-related benchmarks:

```sh
cargo bench -- bench_hmac_
```

*This executes any benchmark function containing the string `bench_hmac_`.*

---

## 2. Understanding the Output

When you run a benchmark, the output looks like this:

```sh
test tests::bench_hmac_1000_rows ... bench:     12,345 ns/iter (+/- 456)
```

### Key Metrics

| Metric | Value Example | Meaning |
|:--- |:--- |:--- |
| **Median Time** | `12,345 ns/iter` | The **median** time it took to run one iteration of your code, measuring in nanoseconds. **Lower is better.** |
| **Variance** | `(+/- 456)` | The specific variance (difference between min/max runs). **Lower is better.** |

### Interpreting Variance

- **Low Variance**: Your test is stable and results are reliable.
- **High Variance**: Your results are noisy. This can be caused by:
  - Other apps using CPU/RAM (Browser, IDE, etc.).
  - OS background tasks.
  - CPU thermal throttling or Turbo Boost.
  - Cold start effects (caches not warmed up).

---

## 3. Tracking Performance Changes

Rust's built-in bencher does not automatically save history. Use one of the following workflows to track improvements or regressions (+/-).

### Method A: The Snapshot Workflow (Simple)

This manual method involves saving the output to a file and diffing it.

1. **Establish Baseline**: Before making changes, run the benchmark and save the output.

```sh
cargo bench > baseline.txt
```

1. **Apply Changes**: Refactor your code or apply optimizations.
2. **Compare**: Run the benchmark again and compare the new output to the baseline.

```sh
cargo bench > new_result.txt
diff -u baseline.txt new_result.txt
```

### Method B: Using `cargo-benchcmp` (Recommended)

`cargo-benchcmp` is a small utility specifically designed to compare the output of two `cargo bench` runs.

1. **Install the tool**:

```sh
cargo install cargo-benchcmp
```

1. **Generate Files**: Save your `baseline.txt` and `new.txt` as described in Method A.
2. **Run Comparison**:

```sh
cargo benchcmp baseline.txt new.txt
```

**Example Output:**

```text
name            baseline ns/iter  new ns/iter  diff ns/iter   diff % 
bench_hmac_1k   12,345            10,000       -2,345         -18.99%
```

*This clearly shows a ~19% performance improvement.*

---

## 4. Advanced: Criterion.rs

For long-term projects requiring rigorous statistical analysis/plots, consider migrating from `#![feature(test)]` to [Criterion.rs](https://bheisler.github.io/criterion.rs/book/).

- **Pros**: Stable Rust support, graphical reports (HTML), statistical caching, automatic regression detection.
- **Cons**: Slower compile/run times, slightly more complex API.
