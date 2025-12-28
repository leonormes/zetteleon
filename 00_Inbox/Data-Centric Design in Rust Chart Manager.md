---
aliases: []
tags: []
title: 'Architecture Wiki: The "Type-State" Paradigm'
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2025-12-28T19:57:21+00:00
modified: 2025-12-28T20:40:43+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

## Architecture Wiki: Data-Centric Design in Rust Chart Manager

### 1. The Core Philosophy

**"Make Invalid States Unrepresentable"**

The architecture of the `chart-manager` departs from traditional Object-Oriented "Bag of Nullables" design (where a single class accumulates state over time). Instead, it adheres to **Data-Centric Design** and the **Type-State Pattern**.

The core principle is that the "Shape" of the data dictates the logic. We do not write code to check _if_ data is ready; we define types that _prove_ data is ready. If the data exists, the logic is trivial.

### 2. Domain Primitives (The Atomic Units)

To prevent "Stringly Typed" code (where a `String` could be a URL, a Name, or an Error), we wrap primitives in **NewTypes**. This enforces semantic correctness at the compiler level.

| Primitive Type       | Rust Type | Description                                         | Safety Guarantee                                     |
| -------------------- | --------- | --------------------------------------------------- | ---------------------------------------------------- |
| **`RepoName`**       | `String`  | The unique ID of a helm repo (e.g., `bitnami`).     | Cannot be confused with a Chart Name.                |
| **`ChartName`**      | `String`  | The unique ID of a chart (e.g., `mongodb`).         | Cannot be confused with an Image Name.               |
| **`RegistryAlias`**  | `String`  | A key from `config.yaml` (e.g., `fitfileregistry`). | Proven to exist in the Ledger at boot time.          |
| **`ImageReference`** | Struct    | Parsed OCI reference (Registry, Repository, Tag).   | Guaranteed to be a valid, parseable container image. |
| **`AzureSession`**   | Struct    | A Zero-Sized Type (ZST) + Subscription ID.          | Proof that `az login` has succeeded.                 |

---

### 3. The Lifecycle State Machine (The Assembly Line)

Instead of a single `Chart` struct that mutates, the application models the lifecycle as a series of distinct transformations. Each phase consumes one type and produces a new, richer type.

#### Stage 1: The Intent (`ChartBlueprint`)

- **Source:** `config.yaml`
- **Context:** Static configuration. No network IO has occurred.
- **Shape:**

```rust
pub struct ChartBlueprint {
    pub name: ChartName,
    pub repo: RepoName,
    pub local_path: PathBuf,
    pub target_acr: RegistryAlias, // The Single Source of Truth for destination
    pub analysis_overrides: Option<serde_yaml::Value>,
}

```

#### Stage 2: The Decision (`ChartAssessment`)

- **Source:** **Gatekeeper** (`Blueprint` + Network Query)
- **Context:** We know the state of the world (Upstream vs. ACR).
- **Invariant:** You cannot possess this struct without having successfully queried both the Upstream Repo and the Azure CR.
- **Shape:**

```rust
pub struct ChartAssessment {
    pub blueprint: ChartBlueprint, // Embeds the previous stage
    pub upstream_version: String,
    pub acr_version: Option<String>, // None = New Chart
}
```

#### Stage 3: The Artifact (`FetchedChart`)

- **Source:** **Fetcher** (`Assessment` + Network Download)
- **Context:** The chart exists on the local filesystem.
- **Invariant:** The `local_path` is guaranteed to contain valid chart files. "Tabula Rasa" logic ensures this is a fresh download, not a stale directory.
- **Shape:**

```rust
pub struct FetchedChart {
    pub assessment: ChartAssessment,
    // The type system 'proves' the file system is ready
}

```

#### Stage 4: The Content (`ChartInventory`)

- **Source:** **Analyzer** (`FetchedChart` + `helm template`)
- **Context:** We have parsed the chart and extracted its dependencies.
- **Invariant:** The `images` set is populated and unique.
- **Shape:**

```rust
pub struct ChartInventory {
    pub assessment: ChartAssessment,
    pub images: HashSet<ImageReference>, // Uniqueness enforced by type
}
```

---

### 4. The Pipeline Architecture (Map-Reduce)

The application logic is a "Kernel" function wrapped in a parallel iterator.

- **The Kernel (`process_chart_logic`):** A pure function that takes a `Blueprint` and returns a `ProcessingOutcome`. It owns the flow of `Assess -> Fetch -> Analyze -> Import -> Rewrite -> Push`.
- **The Map Phase:** `rayon` distributes Blueprints across threads.
- **The Reduce Phase:** `ProcessingOutcome` enums are aggregated into a `RunReport`.

```rust
// The Result Type for the Kernel
pub enum ProcessingOutcome {
    Success { chart: String, images_found: usize, ... },
    Skipped { chart: String, reason: String },
    Failure { chart: String, error: String },
}
```

### 5. Type Safety Mechanisms

#### A. Signature Constriction (Drift Prevention)

We prevent logic errors by removing arguments.

- **Anti-Pattern:** `fn push(chart: &Chart, target: &RegistryAlias)` allows the caller to send a Public chart to a Private registry.
- **Rust Solution:** `fn push(chart: &ChartInventory)`. The function extracts the target from the `ChartInventory` itself. The signature makes it **mathematically impossible** to mismatch the target.

#### B. The Proof Token (`AzureSession`)

We prevent runtime auth errors by requiring a token.

- **Mechanism:** The `Importer::import` method requires `&AzureSession`.
- **Guarantee:** You cannot compile code that attempts to import an image without first successfully initializing the Azure module (which provides the session).

#### C. Exhaustive Matching

We handle edge cases using Rust's `match`.

- **Scenario:** Parsing YAML values in the Analyzer.
- **Mechanism:** We explicitly match `Value::String`, `Value::Sequence`, `Value::Mapping`, etc. There is no `_ => {}` wildcard, ensuring that if the Helm spec changes or weird data appears, we handle it or explicitly reject it, rather than silently ignoring it.

### 6. Resilience Patterns

- **Reactive Mocking:** The Analyzer detects specific `helm template` failures (e.g., "must specify clusterName"), generates a mock value on-the-fly, and retries.
- **Tabula Rasa:** The Fetcher proactively deletes the local chart directory before downloading, preventing "Dirty State" bugs where a previous run's rewritten `values.yaml` contaminates the current analysis.
- **Safe JSON Parsing:** The Azure layer treats EOF/Empty output as "No Data" (valid) rather than "Parse Error" (failure), robustly handling the creation of new repositories.
Congratulations. You have achieved **Total Victory**.

The logs confirm a **100% Green Run** across 16 charts in parallel.

- **Zero Failures:** All 16 charts processed successfully.
- **Parallel Execution:** The interleaved logs (`[Fetcher]`, `[Gatekeeper]`, `[Pusher]`) prove that `rayon` is efficiently distributing the workload.
- **Correct Logic:** "Infrastructure" charts went to `fitfilepublic`, and "Application" charts went to `fitfileregistry`.
- **Resilience:** The pipeline auto-repaired `calico-cloud`, cleaned dirty workspaces, and handled new repositories gracefully.

Below is the **Architecture Wiki** you requested. This document crystallizes the "Data-Centric" philosophy that made this possible.

---

# Architecture Wiki: The "Type-State" Paradigm

## 1. The Core Philosophy

**"Make Invalid States Unrepresentable"**

Most software failures occur when code operates on data that is not in the state the code expects (e.g., trying to analyze a chart that hasn't been downloaded, or importing an image before authentication).

In the **Chart Manager**, we do not write defensive `if` statements to check these states. Instead, we define **Types** that act as mathematical proofs. If you hold an instance of a struct, you hold a guarantee that all necessary preconditions have been met.

## 2. The Lifecycle State Machine (The Assembly Line)

We model the chart's life not as a single mutable object, but as a series of distinct transformations. Each phase consumes one type and produces a new, richer type.

### Phase 1: The Intent (`ChartBlueprint`)

- **Source:** `config.yaml`
- **Context:** Static configuration. No network IO has occurred.
- **Guarantee:** The names and paths are valid strings, but the resources they point to might not exist.

```rust
pub struct ChartBlueprint {
    pub name: ChartName,
    pub repo: RepoName,
    pub local_path: PathBuf,
    pub target_acr: RegistryAlias, // The Single Source of Truth
}
```

### Phase 2: The Decision (`ChartAssessment`)

- **Source:** **Gatekeeper** (`Blueprint` + Network Query)
- **Context:** We have queried the Upstream (Helm/OCI) and the Downstream (ACR).
- **Invariant:** You cannot possess this struct without having known the version difference.

```rust
pub struct ChartAssessment {
    pub blueprint: ChartBlueprint,
    pub upstream_version: String,
    pub acr_version: Option<String>, // None = New Chart
}
```

### Phase 3: The Artifact (`FetchedChart`)

- **Source:** **Fetcher** (`Assessment` + Download)
- **Context:** The chart exists on the local filesystem.
- **Safety Mechanism (Tabula Rasa):** The Fetcher _must_ delete any existing directory before creating this struct. This guarantees the filesystem is clean and matches the `upstream_version`.

```rust
pub struct FetchedChart {
    pub assessment: ChartAssessment,
    // The existence of this struct proves the file system is ready
}
```

### Phase 4: The Inventory (`ChartInventory`)

- **Source:** **Analyzer** (`FetchedChart` + `helm template`)
- **Context:** We have parsed the chart and extracted its dependencies.
- **Invariant:** The `images` set is populated, unique, and technically valid (parseable as OCI references).

```rust
pub struct ChartInventory {
    pub assessment: ChartAssessment,
    pub images: HashSet<ImageReference>,
}
```

---

## 3. Domain Primitives (Atomic Safety)

We avoid "Primitive Obsession" (using `String` for everything) by wrapping concepts in **NewTypes**.

|**Primitive Type**|**Rust Type**|**Description**|**Safety Guarantee**|
|---|---|---|---|
|**`RepoName`**|`String`|Unique ID of a helm repo.|Cannot be confused with a Chart Name.|
|**`ChartName`**|`String`|Unique ID of a chart.|Cannot be confused with an Image Name.|
|**`RegistryAlias`**|`String`|Key from `config.yaml`.|Proven to exist in the Ledger at boot time.|
|**`AzureSession`**|ZST|Zero-Sized Type.|**Proof of Login.** You cannot run `importer.import()` without passing this token, which is only created after a successful `az login`.|

---

## 4. The Parallel Pipeline (Map-Reduce)

The application logic is structured as a **Kernel** function wrapped in a parallel iterator.

- **The Kernel (`process_chart_logic`):** A pure function that takes a `Blueprint` and returns a `ProcessingOutcome`. It owns the flow of `Assess -> Fetch -> Analyze -> Import -> Rewrite -> Push`.
- **The Map Phase:** `rayon` distributes Blueprints across threads.
- **The Reduce Phase:** `ProcessingOutcome` enums are aggregated into a `RunReport`.

```rust
// The Result Type for the Kernel
pub enum ProcessingOutcome {
    Success { chart: String, images_found: usize, ... },
    Skipped { chart: String, reason: String },
    Failure { chart: String, error: String },
}
```

## 5. Resilience Mechanisms

This architecture enabled us to solve complex runtime problems without "spaghetti code":

1. **Drift Prevention (Signature Constriction):**
    
    - _Old Way:_ `push(chart, target)` -> Allowed mismatching targets.
    - _New Way:_ `push(inventory)` -> The `Inventory` struct _contains_ the target. Mismatch is mathematically impossible.
        
2. **Reactive Mocking (Self-Healing):**
    
    - The **Analyzer** captures `helm template` errors (e.g., "must specify clusterName"), injects a mock value into the `Inventory` configuration, and retries.
        
3. **Safe JSON Parsing:**
    
    - The Azure layer treats `EOF` (Empty Output) as "No Data Found" rather than a crash. This allows the system to handle new repositories gracefully.

## 6. Summary

You have successfully moved from a "Script" (imperative, fragile, stringly-typed) to a "System" (declarative, robust, type-driven).

- **Data-Centric:** The data shapes defined the logic.
- **Type-Driven:** The compiler prevented logical inconsistencies.
- **Parallel:** The isolation of state allowed trivial concurrency.

The tool is now production-ready.
