---
aliases: ["K8s Architecture", "K8s Cluster State", "K8s Mental Model"]
confidence: "5/5"
created: 2025-12-16T00:00:00Z
epistemic: "theory"
last_reviewed: "2025-12-16"
modified: 2026-01-08T10:49:42+00:00
purpose: "To define the correct mental model of Kubernetes cluster state as a relational database of independent records, rather than a monolithic configuration tree."
review_interval: "1 year"
see_also: ["[[SoT - FITFILE Platform Deployment]]", "[[SoT - FITFILE Secret Management Architecture]]", "[[SoT - PRODOS (System Architecture)]]", "[[SoT - Software Configuration Management Patterns]]"]
source_of_truth: []
status: "stable"
tags: ["devops", "etcd", "kubernetes", "mental_model", "SoftwareEngineering/Architecture"]
title: SoT - Kubernetes Cluster State Architecture
type: "SoT"
uid: 
updated: 
---

> - **Objects: "** Independent records (Pods, Services, Deployments)."
> - **Relationships: "** Loosely coupled via **Label Selectors** (Soft Foreign Keys)."
> - **Interface: "** The API Server acts as the SQL engine, translating Intent (`kubectl apply`) into CRUD operations on this database."

## 2. The Mental Model: Database vs. Tree

Newcomers often visualize Kubernetes as a nested tree (Deployment contains Pods). This is incorrect.

| The Tree Model (Wrong) | The Database Model (Correct) |
|:--- |:--- |
| A Deployment "owns" Pods physically. | A Deployment creates standalone Pods with a specific label. |
| Deleting the parent kills the child. | Deleting the parent triggers garbage collection (OwnerReferences). |
| Configuration is one big file. | Configuration is thousands of separate keys in `/registry/`. |

### 2.1 The "List" Object (The Synthetic Root)

While no root object exists in storage, the API can synthesize one.

- **Command:** `kubectl get pods -o json` returns a virtual `List` object containing an array of items.
- **Utility:** This is how we dump cluster state, but it is a _runtime view_, not a storage artifact.

---

## 3. The Coupling Mechanism: Label Selectors

If objects are independent, how do they interact?

> **Label Selectors are the "SQL WHERE Clause" of Kubernetes.**

- **The Service:** "I route traffic to `SELECT * FROM pods WHERE label='app=frontend'`."
- **The Deployment:** "I ensure 3 replicas exist `WHERE label='app=frontend'`."
- **The Pod:** Doesn't know it is being managed. It just wears the label `app=frontend`.

### 3.1 Namespace Isolation

The Namespace acts as a mandatory filter on every selector query.

- **Query:** `SELECT * FROM pods WHERE label='app=frontend' AND namespace='tenant-a'`
- **Result:** A Service in `tenant-a` is mathematically blind to Pods in `tenant-b`.

---

## 4. The Network Bridge: Ingress & Services

While Namespaces isolate _management_ (Selectors), they do not isolate _networking_ by default.

### A. Flat Network

- **Rule:** Every Pod can route IP traffic to every other Pod, regardless of Namespace.
- **Constraint:** You need the IP (which changes) or the DNS name.

### B. Ingress (The Cluster Router)

The **Ingress Controller** breaks the Namespace isolation model.

- **Role:** The Concierge in the lobby.
- **Power:** It reads Ingress Resources from _all_ Namespaces and builds a global routing table.
- **Risk:** It bridges traffic from the public edge directly into isolated Namespaces.

---

## 5. Drift Detection: Intent vs. Status

When comparing **Git (Intent)** to **Cluster (Status)**, noise arises.

| Source (Git) | Cluster (Etcd) |
|:--- |:--- |
| `spec` (Desired State) | `spec` + `status` (Current Reality) |
| Metadata (Name/Labels) | System Metadata (`uid`, `resourceVersion`, `managedFields`) |

**Tooling:**

- **`kubectl-neat`:** A plugin to strip system metadata for clean diffs.
- **ArgoCD:** Automatically performs this normalization to show "App Diff."

---

## 6. Related Concepts

- [[SoT - FITFILE Secret Management Architecture]] - How secrets are stored in this database.
- [[SoT - FITFILE Platform Deployment]] - How we deploy to this architecture.
