---
aliases: [K8s MOC, Kubernetes Map]
confidence: 5/5
created: 2025-12-16T14:15:00Z
epistemic: index
last_reviewed: 2025-12-16
modified: 2025-12-19T10:12:38Z
purpose: The central Map of Content for Kubernetes architecture, configuration, and operations within the ProdOS library.
review_interval: 
see_also: []
source_of_truth: []
status: stable
tags: [devops, infrastructure, kubernetes, moc]
title: MOC - Kubernetes Architecture
type: map
uid: 2025-12-16-MOC-K8S
updated: 
---

## 1. Core Architecture (The Mental Model)

- **[[SoT - Kubernetes Cluster State Architecture]]** - **Start Here.** The foundational mental model: K8s as a relational database, not a file tree. Covers Selectors, Namespaces, and the API.

- **[[SoT - Kubernetes Networking & DNS]]** - The flat network model, Service Discovery, and Cross-Cloud resolution.

- **[[SoT - Kubernetes Secrets Management]]** - Technical implementation of `v1/Secret`, encryption at rest, and consumption models.

## 2. Platform Implementation (FITFILE Context)

- **[[SoT - FITFILE Platform Deployment]]** - How we apply these concepts to our specific platform.

- **[[SoT - FITFILE Secret Management Architecture]]** - The VSO implementation standard.

- **[[SoT - FITFILE CI/CD Pipelines]]** - The delivery mechanism.

## 3. Configuration & Management

- **[[SoT - Software Configuration Management Patterns]]** - Broad IaC principles.

- **[[Kubernetes Secrets in Helm Chart Deployment]]** - Specifics of Helm/Secret interaction.

- **[[Vault to Kubernetes Secrets Management Guide]]** - Operational guide for Vault integration.

## 4. Security & Access

- **[[SoT - FITFILE Secret Management Architecture]]** (VSO)

- **[[Network Policies]]** - Firewalling the Namespace boundaries.
