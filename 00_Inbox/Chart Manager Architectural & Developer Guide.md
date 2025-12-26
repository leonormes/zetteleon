---
aliases: []
tags: []
title: "Chart Manager: Architectural & Developer Guide"
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2025-12-26T18:50:02+00:00
modified: 2025-12-26T18:51:14+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

# Chart Manager: Architectural & Developer Guide

## 1. System Abstract: The Mental Model

**"Stateless Batch Processor over a Monolithic Ledger"**

At its core, `chart-manager` is a deterministic state transformation engine. It does not maintain a persistent database or a dynamic dependency graph. Instead, the entire domain state is defined in a single static configuration (`config.yaml`), which is loaded into memory as a flat, unified list of `Chart` objects.

The system's lifecycle is a linear pipeline: **Load Configuration -> Normalize State -> Execute Transformations -> Side Effects (ACR/Helm)**.

This architecture was chosen for **predictability** over flexibility. By treating the configuration as a "Ledger of Record," the system avoids the complexity of synchronization logic. If the process dies, it is safe to restart because no intermediate state is persisted outside the artifacts themselves.

## 2. Core Data Architecture

The system's behavior is dictated by two primary data structures defined in `internal/config`.

### 2.1 The Container: `Config`

The `Config` struct is the root aggregate for the entire application state. It suffers from historical schema fragmentation, maintaining separate "buckets" for different deployment types, which requires normalization at runtime.

```go
type Config struct {
    Charts                 []Chart              // Unified format
    LegacyCharts           []Chart              // Deprecated format
    TerraformManagedCharts []Chart              // Terraform-specific charts
    ArgoCDManagedCharts    []Chart              // ArgoCD-specific charts
    // ... global settings (Azure, TFC)
}
```

*Architectural Note:* The separation of charts into different slices based on their *consumer* (Terraform vs. ArgoCD) rather than their *source* leaks deployment concerns into the storage layer. This requires the `GetAllCharts()` method to act as a hidden distinct "View" layer that unifies these disparate slices into a usable sequence.

### 2.2 The Atom: `Chart`

The `Chart` struct is the fundamental unit of work. It is a "fat" object that tightly couples **Identity** (what it is), **Storage** (where it lives), and **Deployment** (how it runs).

```go
type Chart struct {
    ChartName      string
    RepoURL        string
    ACRName        string
    DeploymentType string             // "terraform" or "argocd" (Stringly typed control flow)
    // ...
}
```

## 3. Structural Efficiency & Trade-offs

### Scalability: O(N) Linear Processing

* **Efficiency:** High. The system processes charts sequentially or in simple parallel batches.
* **Memory Footprint:** Low. The entire state (even with hundreds of charts) fits easily into memory.
* **Bottleneck:** The bottleneck is transactional network I/O (Helm pulls, ACR pushes), not internal logic.

### Critical Constraints

1. **Missing Graph Topology:** The system views the world as a bag of isolated items. It cannot naturally express dependencies (e.g., "Chart A must be imported before Chart B").
2. **String-Typed Control Flow:** Critical logic branches on string values (e.g., `DeploymentType`). This creates a risk where typos in configuration become runtime errors rather than load-time validation failures.
3. **Copy-By-Value Normalization:** The normalization steps often create copies of the chart data, which puts unnecessary pressure on the Garbage Collector as the dataset grows, though this is currently negligible for typical config sizes.

## 4. Component Architecture

The `internal` package organizes the logic into functional domains:

| Package | Responsibility |
|:--- |:--- |
| **`config`** | Defines the "Ledger". Responsible for parsing YAML and normalizing the chart lists. |
| **`helm`** | Wraps the Helm CLI. Handles the "dirty work" of pulling, identifying versions, and local caching. |
| **`chartmod`** | The "Mutator". Responsible for parsing `values.yaml` (likely using AST traversal) and injecting ACR image references. This is the core "write" operation of the tool. |
| **`acr`** | Facade for Azure Container Registry interactions. |
| **`imageops`** | Handles container image discovery and scanning logic. |
| **`validator`** | Post-processing verification to ensure the modified chart is valid. |

## 5. Data Flow Lifecycle

1. **Ingestion:** `LoadConfigWithFileSystem` reads the YAML ledger.
2. **Normalization:** `GetAllCharts()` merges the disparate chart lists (`Legacy`, `Terraform`, `ArgoCD`) into a single, iterable slice.
3. **Analysis (Read-Only):**
   * Iterate through the slice.
   * For each chart, `helm` pulls the artifact.
   * `imageops` scans templates to build a list of required images.

4. **Execution (Read-Write):**
   * **Pull:** Fetch dependencies.
   * **Modify:** `chartmod` alters the local `values.yaml` to point to private ACR images.
   * **Push:** Publish the modified chart to the private registry.
   * **Verify:** Run validation logic.

## 6. Developer Guide

### Prerequisites

* Go 1.19+
* Helm 3.x
* Azure CLI (`az login` required)

### Building

```bash
go build -o bin/chart-manager main.go
```

### Key Entry Points

* **`main.go`**: Command-line entry (Cobra w/ flags).
* **`internal/config/config.go`**: Data structures. Start here to understand the domain.
* **`internal/chartmod/`**: Look here if you need to change how values are injected.

### Common Tasks

**Adding a new Deployment Type:**

1. Modify `internal/config/types.go` to add a new logic branch or struct.
2. Update `GetAllCharts()` in `internal/config/config.go` to include the new type in the normalization process.

**Debugging Logic:**
The system is stateless. Debugging usually involves dumping the `Config` object immediately after load to see if the "Ledger" matches reality. Use `davecgh/go-spew` or `printf` debugging in `GetAllCharts` to verify normalization.
