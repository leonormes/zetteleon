---
assignee: Unassigned
created: 2026-04-30 00:00:00+00:00
jira_key: FTFL-638
jira_url: https://fitfile.atlassian.net/browse/FTFL-638
modified: 2026-05-26 11:43:56+00:00
priority: Highest
reporter: Ollie Rushton
status: Backlog
tags:
- bug
- grafana
- jira
- kubernetes
- loki
- monitoring
- prometheus
title: FTFL-638 - Missing Grafana Monitoring
permalink: llmeon/work/jira/ftfl-638-missing-grafana-monitoring
---

## FTFL-638—Missing Grafana Monitoring in Testing Cluster

Type: Bug | Priority: Highest | Status: Backlog

Reporter: Ollie Rushton | Assignee: Unassigned

### Description

The testing cluster was migrated to the new Grafana Alloy Helm chart. Since deployment, visibility has been lost on two fronts:

1. Missing Loki logs for Grafana pods—logs can be found by container name but not by pod name
2. Missing Prometheus metrics—on the Observability → Kubernetes pages, testing cluster nodes, pods, etc. no longer appear

### Blocker

This must be resolved before upgrading any other clusters to the new Grafana monitoring Helm charts.

### Investigation Checklist

- [ ] Check Alloy config for pod label scraping (Loki pipeline stages)
- [ ] Verify `podLogs` / `discovery.kubernetes` components are configured for `pod` role, not just `container`
- [ ] Check Prometheus remote_write / scrape configs in Alloy for testing cluster namespace
- [ ] Compare working cluster Alloy config vs testing cluster config
- [ ] Check ServiceMonitor / PodMonitor selectors—may need namespace label updates post-migration

### Related

- [[FTFL-206 — Configure Calico Monitoring via Grafana Stack]]