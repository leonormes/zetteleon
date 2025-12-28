---
aliases: []
tags: []
title: UDE-CLI Architecture & Data Structures
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2025-12-28T09:15:03+00:00
modified: 2025-12-28T09:49:14+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

# UDE-CLI Architecture & Data Structures

## Overview

The **UDE-CLI** is a high-performance Rust application designed for **Privacy-Preserving Record Linkage**. It transforms datasets by converting direct identifiers (like generic IDs or names) into cryptographic tokens (Ciphers/Proofs) based on configured protocols. It supports both **Linear processing** (Pseudonymization) and **Linkage/Matching** (Re-identification).

The core philosophy is **Protocol Agnosticism**: The main execution flow handles data loading, schema management, and I/O, while pluggable **Strategies** implement specific cryptographic logic (e.g., HMAC-SHA256, Zero-Knowledge Proofs).

---

## 🏗 Architecture

The application is layered into **CLI**, **Execution**, and **Strategies**.

### 1. The Execution Core (`src/strategies/execute.rs`)

The `execute` module acts as the Dispatcher. It:

1. **Parses CLI Arguments**: Determines which protocol to run (`Zkp`, `BasicPseudo`, etc.).
2. **Loads Data**: Uses `Polars` to load CSV/JSON/Parquet files into `DataFrames`.
3. **Loads Schema**: deserializes `src/schema.rs`.
4. **Instantiates Strategy**: Factory pattern creates a `Box<dyn UDECreateStrategy>` or `Box<dyn UDEMatchStrategy>`.
5. **Executes**: Calls `.create_ciphers()` or `.match_ciphers()`.

### 2. The Strategy Pattern (`src/strategies/mod.rs`)

All cryptographic operations implement one of two traits:

* **`UDECreateStrategy`**:
    * **Goal**: Turn raw data into Tokens/Proofs.
    * **Flow**: `Input DataFrame` -> `Crypto Function` -> `Augmented DataFrame (with Ciphers)`.
    * **Used By**: `ude-cli create`
* **`UDEMatchStrategy`**:
    * **Goal**: Find intersection between Input Data and a provided list of "Target Ciphers".
    * **Flow**: `Input DataFrame` -> `Generate Ciphers` -> `Intersect with Target Ciphers` -> `Filtered DataFrame`.
    * **Used By**: `ude-cli match`

---

## 🧠 Key Data Structures

### 1. Schema System (`src/schema.rs`)

The application is "Schema-First". Every dataset must be accompanied by a JSON schema describing its fields.

* **`DatasetSchema`**: Wrapper around a `BTreeMap<String, SchemaNode>`.
* **`SchemaNode`**: Recursive Enum supporting nested JSON structures.
    * `Field(FieldSchema)`: A leaf node (actual data column).
    * `Node(Schema)`: A branch (nested object).
* **`FieldSchema`**:
    * `identifier_type`: Critical enum (`Direct`, `Indirect`, `NonID`, `UniqueNonId`). Determines if a field is PII.
    * `data_type`: `String`, `Integer`, `Date`, etc.
    * (Architectural Note: This struct currently exhibits the "Bag of Options" smell).

### 2. Cryptographic Protocols

#### A. Basic Pseudonymisation (`src/strategies/basic_pseudonymisation.rs`)

* **Type**: Deterministic Encryption / Tokenization.
* **Primitive**: HMAC-SHA256.
* **Process**:
    1. **Concatenation**: Select key columns (e.g., `Firstname` + `Lastname`).
    2. **Normalization**: Lowercase, remove whitespace.
    3. **Salt**: Append optional salt.
    4. **Hash**: `HMAC_SHA256(Key, Data | Salt)`.
    5. **Output**: Hex string.

#### B. Zero-Knowledge Proofs (ZKP) (`src/strategies/zkp/`)

* **Type**: Probabilistic / Elliptic Curve Cryptography.
* **Primitive**: Ristretto Group (`curve25519-dalek`).
* **Protocol**:
    * **Setup**: Generate a private UDE key. Derive generator point $G$.
    * **Commitment**: Hash data $d$ to scalar $x$. Compute $xG$.
    * **Proof Generation**: Create a non-interactive Zero-Knowledge Proof that verifies knowledge of $x$ without revealing it.
* **Data Structure (`Proof` in `proofs.rs`)**:

```rust
pub struct Proof {
  r: Scalar,            // Random component
  vg: RistrettoPoint,   // Ephemeral commitment
}
```

* (Architectural Note: Serializable via primitive `String` types in `JsonProof`, identified as a "Stringly Typed" smell).

### 3. I/O & Buffers

* **Polars DataFrame**: The data is heavily processed in-memory using Polars.
* **`UDECipherCollection`**: A container for holding the generated cryptographic columns before they are merged back into the main DataFrame.

---

## 🔄 Data Flow

### The "Create" Pipeline

1. **Input:** `dataset.csv`, `schema.json`, `ude_key`.
2. **Validation:** Check if Key Fields exist in DataFrame. Remove rows with null/empty key values.
3. **Preparation**:
    * Sort DataFrame by Key Fields (important for some optimizations).
    * `prepare_cipher_input_column`: Concatenates multiple columns into a single string `A|B|C`.
4. **Transformation**:
    * Apply Strategy (HMAC or ZKP) to every row.
    * Generate `Cipher` column.
5. **Schema Update**: Add the new Cipher Field to the Schema (marked as `NonID`).
6. **Output:** Write `output.csv` and `output_schema.json`.

### The "Match" Pipeline

1. **Input:** `dataset.csv`, `schema.json`, `ude_key`, `target_tokens.csv`.
2. **Target Loading:** Read `target_tokens.csv` into a `HashSet` or `BTree` (depending on strategy).
3. **Generation:** Generate Ciphers for the *current* dataset (same as Create pipeline).
4. **Intersection:**
    * **Hash Match**: `O(N)` lookup against the Target Set.
    * **Binary Search**: `O(N log M)` search against sorted targets.
5. **Filtering**: Keep only rows where generated cipher exists in target set.
6. **Output:** A subset of the original dataset containing only identified records.
