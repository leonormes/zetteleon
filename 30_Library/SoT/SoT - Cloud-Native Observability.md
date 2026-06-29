---
aliases:
- K8s Observability
- Logging and Tracing
- Monitoring Strategy
created: 2026-01-08 12:05:00+00:00
last_reviewed: '2026-01-08'
modified: 2026-02-11 07:34:02+00:00
status: stable
tags:
- devops
- kubernetes
- monitoring
- observability
title: SoT - Cloud-Native Observability
type: SoT
permalink: llmeon/30-library/so-t/so-t-cloud-native-observability
---

## 1. The Necessity of Observability

In distributed systems, traditional debugging (SSHing into a server) is impossible or ineffective. Observability is the property of a system that allows its internal state to be inferred from its external outputs.

## 2. The Three Pillars

### 2.1 Logs (Events)

- Definition: Discrete events (stdout/stderr streams in containers).
- Strategy:
    - Aggregation: Logs must be shipped from ephemeral pods to a central store (Elasticsearch, Loki, Splunk).
    - Context: Raw text is insufficient. Logs should be structured (JSON) and tagged with metadata (Namespace, Pod, TraceID).
    - Audit Logs: Critical for security and compliance (Who deleted this resource?).

### 2.2 Metrics (Aggregates)

- Definition: Numeric measurements over time.
- RED Method (Services):
    - Rate (Requests per second).
    - Errors (Failed requests).
    - Duration (Latency).
- USE Method (Resources):
    - Utilisation (Time resource was busy).
    - Saturation (Queue length).
    - Errors (Device errors).

### 2.3 Tracing (Context)

- Definition: The lifecycle of a request as it propagates through multiple microservices.
- Goal: Identify latency bottlenecks and dependency failures.

## 3. Alerting Philosophy

- The Danger: "Alert Fatigue" caused by noisy, low-fidelity alerts.
- The Rule: Alert on Symptoms (High Error Rate), not just Causes (High CPU).
- High Fidelity: Use Machine Learning or correlation to group related alerts into a single incident.

## 4. Kubernetes-Native Tools

- Hubble UI / Cilium: Visualizes network flows, DNS drops, and policy verdicts in real-time.
- Kubectl:
    - `kubectl logs`: Immediate stream inspection.
    - `kubectl describe`: Event history for resources (Scheduling failures, ImagePullBackOff).

## ## 4. Kubernetes-Native Tools

### Project Logs & Updates