---
aliases: []
confidence: 
created: 2025-04-15T12:23:47Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:52Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Overcoming These Challenges
type:
uid: 
updated: 
version:
---

Many of these challenges *can* be overcome with the right architectural decisions and investments:

## Data Sensitivity-a

Implementing robust encryption, access controls (Azure RBAC, Network Security Groups), and potentially dedicated storage within the Shared Services Subscription could mitigate some data sensitivity concerns.

## Data Volume and Growth-a

Utilizing scalable storage solutions in Azure (like Azure Blob Storage or Azure Data Lake Storage) and efficient data transfer mechanisms could handle large volumes.

## Data Freshness-a

Implementing Change Data Capture (CDC) mechanisms or other real-time synchronization techniques could address freshness requirements, though with added complexity.

## Data Transformation and Governance-a

Investing in data integration tools and adapting governance workflows to include the Azure environment would be necessary.

## Security Perimeter-a

Implementing strong network segmentation, identity and access management, and security monitoring in the Azure Shared Services Subscription is crucial.

## Existing Infrastructure-a

A phased approach to migration could be considered to leverage existing investments while gradually adopting Azure services.

[[why not move data to the shared sub]]
