---
aliases: ["Data Structures in Infrastructure", "Data-Centric View", "Infrastructure as Data"]
confidence: "5/5"
created: 2025-12-25T12:10:00Z
epistemic: "index"
last_reviewed: "2025-12-25"
modified: 2025-12-27T20:40:58+00:00
purpose: "A Map of Content (MOC) connecting infrastructure components through the lens of their underlying data structures and synchronization models."
review_interval: "6 months"
see_also: ["[[SoT - HashiCorp Vault Architecture]]", "[[SoT - Kubernetes Networking & DNS]]", "[[SoT - State Synchronization Models]]"]
source_of_truth: []
status: "stable"
tags: ["data_structures", "infrastructure", "mental_models", "moc"]
title: MOC - Data-Centric Infrastructure
type: "MOC"
uid: 
updated: 
---

## 1. The Core Thesis

Infrastructure tools are best understood not by their "Marketing Features" (Secrets, Deployments, GitOps) but by their **First-Principles Data Structures** (Tries, Merkle Trees, Event Logs).

> "Show me your flowcharts and conceal your tables, and I shall continue to be mystified. Show me your tables, and I won't usually need your flowcharts; they'll be obvious."—*Fred Brooks*

## 2. Synchronization Models

How systems agree on "Truth."

- **[[SoT - State Synchronization Models]]** - The fundamental divergence:
    - **Merkle Trees (Integrity):** Used by [[SoT - HashiCorp Vault Architecture|Vault]] and [[SoT - Git Architecture|Git]]. "Is it *exactly* the same?"
    - **Reconciliation Loops (Intent):** Used by [[SoT - Kubernetes Architecture|Kubernetes]] and **ArgoCD**. "Is it *functionally* compliant?"

## 3. Data Structures by Tool

| Tool | Core Data Structure | Addressing Model |
|:--- |:--- |:--- |
| **[[SoT - HashiCorp Vault Architecture|HashiCorp Vault]]** | **Versioned Prefix Trie** | Path-based (`secret/data/app`) |
| **Kubernetes (etcd)** | **B+Tree / Event Log** | Namespace-based (`ns/name`) |
| **Git** | **Merkle DAG** | Content-based (SHA-1 Hash) |
| **DNS** | **Distributed Tree** | Hierarchical (`.com` -> `.google`) |
| **Secure Transport** | **Encapsulated Tunnel** | Private IP (`10.0.x.x`) vs Public IP |

## 4. Architectural Patterns

- **[[SoT - Container Security & Hardening]]** - Defense-in-depth for containerized workloads.
- **[[SoT - Namespacing in Computing]]** - How distinct systems isolate data (OS, K8s, Languages).
- **[[SoT - Data-Centric Infrastructure (Terraform)]]** - Treating infrastructure as a configuration graph.
- **[[SoT - FITFILE Secret Management Architecture]]** - Practical application of the Vault-to-K8s bridge (VSO).

## 5. Bridges & Transformers

Tools that translate between data models:

- **Vault Secrets Operator:** Transforms *Path-Addressed JSON* (Vault) -> *Namespace-Addressed Maps* (K8s).
- **Ingress Controller:** Transforms *Host Headers* (HTTP) -> *Service Selectors* (K8s Labels).
