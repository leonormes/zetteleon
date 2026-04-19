---
aliases: [Data Structures in Infrastructure, Data-Centric View, Infrastructure as Data]
created: 2025-12-25T12:10:00Z
last_reviewed: 2025-12-25
modified: 2026-04-19T18:30:29+00:00
status: stable
tags: [data_structures, infrastructure, mental_models, type/moc]
title: MOC - Data-Centric Infrastructure
type: map
updated:
---

## 1. The Core Thesis

Infrastructure tools are best understood not by their "Marketing Features" (Secrets, Deployments, GitOps) but by their First-Principles Data Structures (Tries, Merkle Trees, Event Logs).

> "Show me your flowcharts and conceal your tables, and I shall continue to be mystified. Show me your tables, and I won't usually need your flowcharts; they'll be obvious."—_Fred Brooks_

## 2. Synchronization Models

How systems agree on "Truth."

- [[SoT - State Synchronization Models]] - The fundamental divergence:
    - Merkle Trees (Integrity): Used by [[SoT - HashiCorp Vault Architecture|Vault]] and [[SoT - Git|Git]]. "Is it _exactly_ the same?"
    - Reconciliation Loops (Intent): Used by [[SoT - Kubernetes Cluster State Architecture|Kubernetes]] and ArgoCD. "Is it _functionally_ compliant?"

## 3. Data Structures by Tool

| Tool                                                        | Core Data Structure       | Addressing Model                     |
|:---------------------------------------------------------- |:------------------------ |:----------------------------------- |
| [[SoT - HashiCorp Vault Architecture]]                  | Versioned Prefix Trie | Path-based (`secret/data/app`)       |
| [[SoT - Kubernetes Cluster State Architecture]]         | B+Tree / Event Log    | Namespace-based (`ns/name`)          |
| [[SoT - Git]] | Merkle DAG            | Content-based (SHA-1 Hash)           |
| [[SoT - The Data Architecture of DNS]]                  | Distributed Tree      | Hierarchical (`.com` -> `.google`)   |
| [[SoT - Secure Cross-Cloud Data Transport]]             | Encapsulated Tunnel   | Private IP (`10.0.x.x`) vs Public IP |

## 4. Architectural Patterns

- [[SoT - Container Security & Hardening]] - Defense-in-depth for containerized workloads.
- [[SoT - Namespacing in Computing]] - How distinct systems isolate data (OS, K8s, Languages).
- [[SoT - FITFILE Secret Management Architecture]] - Practical application of the Vault-to-K8s bridge (VSO).

## 5. Bridges & Transformers

Tools that translate between data models:

- Vault Secrets Operator: Transforms _Path-Addressed JSON_ (Vault) -> _Namespace-Addressed Maps_ (K8s).
- Ingress Controller: Transforms _Host Headers_ (HTTP) -> _Service Selectors_ (K8s Labels).
