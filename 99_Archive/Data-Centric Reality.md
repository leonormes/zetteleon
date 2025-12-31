---
aliases: []
tags: []
title: Data-Centric Reality
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
modified: 2025-12-31T12:21:31+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
created: 2025-12-31T09:45:32+00:00
---

### The Philosophy: Data-Centric Reality

The quote from Linus Torvalds—*"Bad programmers worry about the code. Good programmers worry about data structures and their relationships"*—encapsulates the **Data-Centric** worldview.

In this mental model, code is merely a transient mechanism to manipulate state. State (data) is the only persistent reality. When you prioritise code (algorithms, control flow, classes), you are prioritising the *symptom* of the problem rather than the *root*. Complex control flow is usually a symptom of poor data modelling. If the data structures effectively mirror the physical constraints of the reality you are modelling, the code required to manipulate them becomes trivial.

---

### The Torvalds Loop: A Structural Mental Model

Based on your note, the "Torvalds Loop" formalises this philosophy into a four-phase architectural protocol. This reverses the typical industry approach of "Logic First".

#### Phase 1: Shape (Physical Reality)

**Focus:** Memory layout and logical exclusion.
**Constraint:** How does the data look in memory? Is it cache-efficient?
**Goal:** Define `structs` and `enums` such that invalid states cannot physically exist in memory.

#### Phase 2: Access (Mechanics)

**Focus:** Ownership and movement.
**Constraint:** Who owns this data? Is it a Value (copied) or a Resource (moved/borrowed)?
**Goal:** Establish clear boundaries using affine types (Move Semantics) to prevent "use-after-invalid" errors.

#### Phase 3: Invariants (Integrity)

**Focus:** The "Parse, Don't Validate" Pattern.
**Constraint:** Never allow raw data to exist deep in the system.
**Goal:** Parse data *at the edge* into strict Types. For example, do not pass a `String` as an email; parse it once into an `Email` type. The existence of the `Email` instance is proof of its validity, removing the need for defensive coding elsewhere.

#### Phase 4: Logic (Transformation)

**Focus:** Pure transformation.
**Constraint:** Logic is the *last* step.
**Goal:** Write linear, simple algorithms that transform Valid State A to Valid State B. Logic becomes a pipeline, not a spiderweb of conditionals.

---

### The Consensus of Great Programmers

Linus is not alone in this view. The industry's "Greats" share a consensus that **Data Dominates Code**.

| Architect | Mental Model | The Core Tenet |
| --- | --- | --- |
| **Linus Torvalds** | **Data-Centric** | "Bad programmers worry about code. Good programmers worry about data structures." |
| **Fred Brooks** | **Table-Driven** | "Show me your tables, and I won't usually need your flowcharts; they'll be obvious." |
| **Rob Pike** | **Structural** | "Data dominates. If you've chosen the right data structures... the algorithms will almost always be self-evident." |
| **Mike Acton** | **Data-Oriented** | "The purpose of all programs is to transform data from one form to another." (Hardware sympathy). |

**The "Buggy Mess" Explanation:**
The "buggy mess" you observe in the industry stems from **Code-First** thinking (Object-Oriented bloat). Developers create complex webs of "Manager" objects and mutable state, then try to patch the leaks with defensive logic (Acton's "Logic First" anti-pattern). The Torvalds/Acton approach eliminates entire classes of bugs by making them impossible to represent in the data structure.

---

### Applied Mental Model: The Transformation Pipeline

*(Applying the Acton/Torvalds model to your Azure ACR context)*

To transcend mediocre techniques, you must stop viewing your Azure ACR process as a "system of objects" and start viewing it as a **Data Transformation Pipeline**.

#### 1. Conceptualising the Process (Acton’s Model)

Do not build a "ChartManager" that "updates charts". Instead, model the flow of data as a linear pipeline of struct transformations.

* **Stage 1 (Ingest):** `PublicRegistry`  `RawChartBlob`
* **Stage 2 (Parse):** `RawChartBlob`  `HelmChart` (Verified Struct)
* **Stage 3 (Discovery):** `HelmChart`  `Vec<ImageReference>`
* **Stage 4 (Transform):** `Vec<ImageReference>`  `Vec<ImportOp>`  `Vec<ACRImageRef>`
* **Stage 5 (Apply):** `(HelmChart, Vec<ACRImageRef>)`  `PrivateChartBlob`

In this model, the "Logic" is just the glue between these data states. You focus on defining the `structs` for each stage.

#### 2. Modelling Remote Queries

In a standard "mediocre" Object-Oriented model, you might iterate through charts and check versions one by one (N+1 problem).

In the **Data-Oriented (Acton)** model, you treat "Remote State" as just another input buffer:

1. **Gather:** Collect all `ChartName` and `CurrentVersion` data from your local state into a contiguous array.
2. **Batch Transform:** Send this array to a "Version Check" processor (batch query).
3. **Result:** Receive a contiguous array of `UpstreamVersion`.
4. **Join:** A simple data join (Diff) between the two arrays generates a `Vec<UpdateOp>`.

**Why this is better:**

* **Latency Hiding:** You do one network round-trip instead of thousands.
* **Simplicity:** The logic is a flat loop over two arrays, not a recursive crawl through objects.
* **Debuggability:** You can dump the "Input Array" and "Output Array" to a log file to reproduce any bug instantly.

### Next Step

Would you like me to draft the Rust `struct` definitions (The "Shape" phase) for the `HelmChart` transformation pipeline to demonstrate how to make the invalid states unrepresentable?

This response applies the **Data-Centric Philosophy** to your Azure ACR mirroring pipeline.

Following the Torvalds and Acton doctrine, we will not model "Chart Objects" that have methods. We will model **Data States** that flow through a pipeline. The goal is to design these structures so that it is impossible to confuse a public image with a private one, or to attempt to patch a chart before its images are imported.

Here is the "Shape" phase of your pipeline, defined in Rust to enforce strict memory layout and type safety.

### 1. The Core Data Types (The Atomic Reality)

First, we define the "atoms" of our universe. Note the strict separation between a `PublicImageRef` and an `ACRImageRef`. This utilizes the type system to enforce the **"Parse, Don't Validate"** pattern—you cannot accidentally use a public image string in a function that requires an ACR-hosted image.

Rust

```rust
// A strict wrapper around a string that has been validated as a semantic version.
// It is impossible to hold an invalid version string in this type.
struct SemVer(String);

// Represents a unique, content-addressable identifier. 
// Used to ensure we are talking about the exact same bytes, regardless of tags.
struct Digest(String); // e.g., "sha256:..."

// STAGE 1: The Input (Dangerous/External)
// This represents an image found in the wild (DockerHub, Quay, etc.).
// It is "Tainted" data.
struct PublicImageRef {
    original_registry: String, // "docker.io"
    repository: String,        // "bitnami/nginx"
    tag: String,               // "1.21"
    digest: Option<Digest>,    // Optional, as public charts might lack it
}

// STAGE 2: The Target (Safe/Internal)
// This represents an image that strictly exists inside YOUR Azure ACR.
// You cannot construct this type unless the image has been verified to exist in ACR.
struct ACRImageRef {
    acr_domain: String,        // "mycompany.azurecr.io"
    repository: String,        // "mirror/bitnami/nginx"
    digest: Digest,            // strictly required for immutability
}

// The Location Trace
// Tracks exactly where in the Helm Chart this image was found.
// This allows for O(1) patching later, avoiding a second scan.
enum LocationContext {
    ValuesKey(String),         // e.g., "image.repository"
    TemplateString(String),    // e.g., "deployment.yaml" (Hardcoded strings)
}
```

---

### 2. The Pipeline Buffers (Structure of Arrays)

In Mike Acton’s **Transformation Mental Model**, we process data in homogeneous batches to maximize throughput and cache coherency. We do not process one chart at a time; we process arrays of data stages.

#### Buffer A: Ingestion & Discovery

This struct holds the state of the "World" after we have downloaded and scanned the charts.

```rust
struct DiscoveryBatch {
    // Parallel arrays (Structure of Arrays layout) for cache efficiency
    
    // 1. The raw charts waiting to be patched
    chart_ids: Vec<Uuid>,
    raw_tarballs: Vec<Vec<u8>>, 
    
    // 2. The images discovered across ALL charts. 
    // We flatten the hierarchy. If 50 charts use Nginx, we see 50 entries here.
    // This allows us to de-duplicate imports easily.
    discovered_images: Vec<PublicImageRef>,
    
    // 3. Linkage back to the chart
    // index[i] corresponds to discovered_images[i]
    image_owner_chart_id: Vec<Uuid>, 
    image_location: Vec<LocationContext>,
}
```

#### Buffer B: The Import Plan (The Transformation)

Before we execute any network calls (importing), we transform `DiscoveryBatch` into an `ImportPlan`. This allows us to reason about the _entire_ operation before side effects occur.

```rust
struct ImportPlan {
    // distinct_images ensures we only call `az acr import` ONCE per unique image,
    // even if 100 charts request it.
    distinct_sources: Vec<PublicImageRef>,
    
    // The pre-calculated target destination for each source.
    planned_destinations: Vec<ACRImageRef>,
}
```

---

### 3. Making Invalid States Unrepresentable

The "Buggy Mess" usually happens when a chart is updated _before_ the image is successfully imported, or when a script blindly replaces strings. We solve this with a **State Transition Type**.

```rust
// This struct is the ONLY input accepted by the "Patch Chart" function.
// It physically couples the Chart with the PROOF that the image is in ACR.
struct VerifiedMigration {
    chart_id: Uuid,
    
    // A map that links the original public ref to the new private ref.
    // The existence of 'ACRImageRef' implies the import succeeded (if we follow strict constructors).
    replacements: HashMap<PublicImageRef, ACRImageRef>,
}

// The Final Transformation Function signature
fn patch_chart(
    tarball: Vec<u8>, 
    migration: VerifiedMigration
) -> Result<Vec<u8>, Error>;
```

In this model, you literally cannot write code that patches a chart with a failed image import, because the `VerifiedMigration` struct cannot be constructed without valid `ACRImageRef`s.

---

### 4. Modeling Remote Queries (The Batch Version Check)

You asked how to handle checking upstream versions. In a naive OOP approach, you would iterate:

for chart in charts { chart.check_upstream() }. // SLOW (N+1 Latency)

In the **Transformation Model**, we treat the "Upstream State" as a read-only buffer we fetch in one go.

```rust
// 1. The Query Buffer
// We compile ALL charts we want to check into this contiguous array.
struct VersionQueryBatch {
    chart_names: Vec<String>,      // ["nginx", "redis",...]
    current_versions: Vec<SemVer>, // ["1.19.0", "6.0.1",...]
    repo_urls: Vec<String>,        // ["https://charts.bitnami.com/bitnami",...]
}

// 2. The Transformation (Network IO happens here in parallel/batch)
// fn fetch_upstream_state(batch: VersionQueryBatch) -> UpstreamStateBatch

// 3. The Result Buffer
struct UpstreamStateBatch {
    // Parallel array to the input batch
    latest_versions: Vec<SemVer>,
}

// 4. The Diff Calculation (Pure CPU transformation)
// We treat the "Decision to Update" as a data transformation, not logic.
struct UpdateOp {
    chart_index: usize,
    upgrade_type: UpgradeType, // Major, Minor, Patch, None
}

fn compute_diffs(
    query: &VersionQueryBatch, 
    result: &UpstreamStateBatch
) -> Vec<UpdateOp> {
    // iterate arrays, compare integers, emit ops.
    // Zero allocations, cache-friendly, instantly testable.
}
```

### Summary of the Shift

1. **From:** "I have a Chart Object, let me call `import_images()` on it."
2. **To:** "I have a `DiscoveryBatch` of raw data. I will transform it into an `ImportPlan`. I will execute the plan to get `ACRImageRef`s. I will zip the `ACRImageRef`s with the `RawChartBlob` to produce the final `PrivateChartBlob`."

This separation of **Data Definition**, **Plan Generation**, and **Plan Execution** is the "transcendental technique" that prevents the system from becoming a tangled, buggy mess.
