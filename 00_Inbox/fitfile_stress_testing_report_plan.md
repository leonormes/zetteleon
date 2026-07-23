---
title: fitfile_stress_testing_report_plan
type: note
permalink: llmeon/00-inbox/fitfile-stress-testing-report-plan
---

# FITFILE Stress Testing Report

## Infrastructure

- Diagram of the multi node setup (5 FITFILE environments, 5 AKS clusters, 5 OMOP PostgreSQL databases)
- Details of the specs of each K8s (K8s version, NodePools, VM_Sizes)
- Database configuration differences between Sandbox Testing 1 deployment and the others (the first had database provisioned on a bigger box and pgconfig optimised for read)
- The 2 different regions (ST1 in UK_South, ST2,3,4,5 in UK_West)
- all k8s in private networks
- using public networks for data transfers between nodes

## Test Design

### Test data

- synthea_27m
- reasons why does not matter for US data
- Summary statistics of tables and record counts
- (For later, maybe a reference to the achilles reports)
- Patient expected overlap information
- Missing tables not present in synthetic data
- How we replicated it for 5 nodes

### Cohorts & Extract volumes

- List each of the cohort sizes and data extract volume (measurements, observations, visit_occurrences, etc...) sizes
- Reference the JSON cohort definitions

### Privacy treatment

- Currently out of scope

### Metrics

- Grafana as observability solution.
- Total Query Time
- Time of each subquery in each data provider
- Cost of total query
- Cost breakdown per data provider per query
- Database CPU, Memory and storage
- Workflows NodePool CPU, Memory and storage

## Results

- Table of the Test names, workflow IDs, all metrics

## Fixes

- OMOP Reindexer was not memory optimised. Modify to use vectorized column transforms, optimsed person_id remapping, increasing chunk sizes for processing, results in ~x20 faster process.
- Finalize task OOMKilled,
- Reduced the running size of the cluster pods after assessing cpu/memory constraints.
- Re-architected the NodePools (system, fitfile, omopdb, workflows)

## Observations

- Database config (read optimised) has big impact of query times for data extract
- Nginx Ingress needs to be configured for burst traffic, may need replicas if expecting to run more parrallel data extracts
- New dashboards for monitoring workflows end to end across the network
- New dashboards for cost analysis of queries