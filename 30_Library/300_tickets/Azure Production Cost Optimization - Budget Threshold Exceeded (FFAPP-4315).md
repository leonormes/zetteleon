---
aliases: []
title: "`jira-sync-line-summary`Azure Production Cost Optimization - Budget Threshold Exceeded"
type: ""
confidence: ""
epistemic: ""
purpose: ""
modified: 2026-01-01T17:43:53+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
key: FFAPP-4315
summary: Azure Production Cost Optimization - Budget Threshold Exceeded
status: In Progress
assignee:
tags:
project: FFAPP
issuetype: Task
priority: High
reporter:
created: 2026-01-01T17:41:46+00:00
updated: 2025-12-29T16:15:52.258+0000
url:
---

# `jira-sync-line-summary`Azure Production Cost Optimization - Budget Threshold Exceeded

**Key:** `jira-sync-line-key`FFAPP-4315
**Type:** `jira-sync-line-issuetype`Task
**Status:** `jira-sync-line-status`In Progress
**Priority:** `jira-sync-line-priority`High
**Assignee:** `jira-sync-line-assignee`
**Reporter:** `jira-sync-line-reporter`
**Link:** [Open in Jira]({url})

## Description

`jira-sync-section-description`

# Problem Statement

Our Azure production environment costs are forecasted to exceed their budget threshold value. The biggest cost drivers identified are:

1. **Virtual machine usage**
1. **Azure backups**

# Cost Optimization Opportunities

## Virtual Machine Optimization

** **Resource Right-sizing*: Adjust CPU and memory resource limits for applications running inside each node
** **Application Cleanup*:
* Remove Primary care node in production (currently unused - note: removing will stop syncing STG data, but we can request full EMIS dump when project resumes)
* Optimize The Hyve application to run only when synthetic data updates are needed (currently runs constantly)
** **Schedule-based Scaling*:
* Turn off Kubernetes clusters outside operational hours
* Testing and staging clusters don't need to run weekends/nights
* Question: What is the operational window for Barts?
** **Dynamic Scaling*: Scale Workflows Node Pools down to minimum 0 nodes (accepting slower query startup times as VMs will deploy on-demand)

## Backup Optimization

* Reduce backup frequency and retention periods
* Investigate backing up only Persistent Volumes (PVs) instead of whole clusters
* Review what is actually backed up vs what needs to be backed up

# Next Steps

1. **Immediate Actions**:

* Quantify potential monthly savings for each optimization opportunity
* Gather current spend vs budget threshold data
* Validate that VMs and backups are still the primary cost drivers

1. **Planning & Coordination**:

* Raise with Weronika to add to roadmap
* Discuss in Wednesday meeting
* Prioritize alongside current commitments

1. **Implementation**:

* Create detailed sub-tasks for each optimization area
* Implement changes in phases with proper testing
* Monitor cost impact and adjust as needed

# Stakeholders

** **Infrastructure Team*: Implementation
** **Weronika*: Roadmap planning
** **Wednesday Meeting*: Prioritization discussion

~~--~~

*Original analysis provided by Ollie*

*Created from Azure budget alert notification*

## Comments
