---
created: 2026-06-16T14:00:00+00:00
modified: 2026-07-04T10:49:23+00:00
permalink: llmeon/raw/2026-06-16-ftfl-657-bastion-direct-aks
source: jira
source_url: https://fitfile.atlassian.net/browse/FTFL-657
tags: [aks, bastion, infrastructure, jira, raw]
title: 2026-06-16-ftfl-657-bastion-direct-aks
---

## FTFL-657—Investigate Bastion Direct to Private AKS Cluster

Jira Key: FTFL-657

Issue Type: Spike

Status: Selected for Development

Priority: Low

Assignee: Leon Ormes (leon.ormes@fitfile.com)

Reporter: Robin Mofakham (robin.mofakham@fitfile.com)

Labels: Infrastructure

Created: 2026-05-14

Updated: 2026-06-10

### Description

> Timebox: 1 day only

As part of [FTFL-579](https://fitfile.atlassian.net/browse/FTFL-579).

We should investigate the possibility of using Bastion Direct to Private AKS cluster to avoid Jumpbox password/SSH connectivity (and costs), as well as improving the overall architecture.

This can be tested on the Sandbox cluster.
