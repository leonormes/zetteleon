---
created: 2026-02-06T09:00:00+00:00
modified: 2026-02-06T09:22:57+00:00
status: evergreen
tags: [architecture, azure, cloud, concept/system-design, type/SoT]
title: SoT - Azure Resource Manager Architecture
type: SoT
---

## Minimum Viable Understanding (MVU)

Azure Resource Manager (ARM) functions as the "Operating System" of the Azure Cloud. It decouples the Control Plane (API, Auth, Policy) from the Data Plane (Compute, Network, Storage) using a standardized Resource Provider contract. Everything in Azure is a JSON document stored at a specific URL path (Resource ID).

## Working Knowledge

### 1. The Architecture: Kernel and Drivers

ARM acts as a Dispatcher and State Store, not the execution engine.

- The Kernel (ARM): Handles Authentication (AuthN), Authorization (AuthZ), Policy, Locking, and Tagging. It knows _nothing_ about how to create a VM or VNet.
- The Drivers (Resource Providers): Microservices that perform the actual work. They register with ARM to handle specific namespaces.
    - `Microsoft.Compute` handles VMs.
    - `Microsoft.Network` handles VNets.
    - `Oracle.Database` (3rd party) handles Oracle DBs.

### 2. The Namespace System (The Primary Key)

Every resource is identified by a globally unique URI, functioning as the primary key in the distributed database.

`root` / `scope` / `namespace` / `resource-type` / `resource-name`

Example:

`/subscriptions/{sub-id}/resourceGroups/{rg-id}/providers/Microsoft.Network/virtualNetworks/{vnet-name}`

- Partition Key: Subscription + Resource Group.
- Schema: `Microsoft.Network` (The Provider).
- Table: `virtualNetworks` (The Resource Type).

### 3. The "VNet is a Document" Concept

When you create an Azure Resource (like a VNet), you are not "plugging in a cable." You are performing a `PUT` operation of a JSON Document into the ARM Database.

- The Input: A JSON file describing the _Desired State_ (Address Space, Subnets).
- The Action: The `Microsoft.Network` provider reads this JSON and programs the underlying Software Defined Networking (SDN) switches (the "Virtual Filtering Platform") to enforce that policy.
- Implication: The network is a _policy object_, not physical infrastructure.

### 4. Reconciliation Loop (Level-Triggered)

Azure follows a Level-Triggered architecture (similar to Kubernetes).

1. Desired State: The User `PUT`s a JSON document.
2. Current State: The Provider checks reality.
3. Reconciliation: The Provider performs actions to make Reality match the Document.

This contrasts with Edge-Triggered systems (Classic AWS/RPC) which fire a "Create" command once and forget.

## Current Understanding

### Comparison: Azure Vs AWS Primitives

| Feature | Azure (ARM) | AWS (Classic/EC2) |
|:--- |:--- |:--- |
| Paradigm | Resource-Centric (Nouns) | Action-Centric (Verbs) |
| Identity | Hierarchical Path (Tree) | Flat ARN (Graph) |
| Coupling | Strong (Strict Containment) | Loose (Tags & References) |
| Operation | `PUT` (Idempotent by default) | `RunInstances` (RPC) |

_Note: AWS is converging towards this model with the "Cloud Control API", but the legacy distinction remains relevant._

### The "Dangling Dependency" Problem

Because Azure enforces strict hierarchy (Resource Groups), it enables Cascading Deletes. Deleting a Resource Group deletes all contained resources.

AWS's flat graph model requires "Garbage Collection" (manually finding and deleting unattached dependencies like ENIs or Volumes), though CloudFormation/Terraform mitigates this.
