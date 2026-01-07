---
aliases: ["ZK Architecture", "Proof of SQL", "Plonky3", "Zero Knowledge Proofs"]
confidence: "High"
created: 2026-01-06
epistemic: "Architecture"
last_reviewed: 
modified: 
purpose: "To define the architectural standards for high-performance Zero Knowledge systems, specifically for large-scale data linkage (15M+ rows)."
review_interval: "1 year"
see_also: 
  - "[[SoT - Rust Type Mechanics]]"
  - "[[SoT - Data-Centric Software Engineering]]"
source_of_truth: []
status: "Active"
tags: ["cryptography", "zkp", "rust", "SoftwareEngineering/Architecture", "data"]
title: SoT - Zero Knowledge Architecture
type: "SoT"
uid: 
updated: 
---

# SoT - Zero Knowledge Architecture

> **The Constraint:** Traditional ZKP systems scale poorly ($O(n \times m)$) for massive data linkage (e.g., 15M records).
> **The Solution:** Move from **Arithmetic Circuits** (checking every row) to **Lookup Arguments** and **Native Data Commitments** (checking set membership).

## 1. The "Proof of SQL" Pattern

For relational data (joins, filters), generic ZKVMs are too slow. We must use specialized provers that bypass Merkle Trees.

### A. Native Data Commitments
Instead of verifying data via Merkle paths (logarithmic cost per row), we generate a single **Cryptographic Digest** (Commitment) of the entire column.
*   **Mechanism:** The Prover commits to Column A. The Verifier holds only the Digest.
*   **Query:** `SELECT * FROM A JOIN B ON A.id = B.id`.
*   **Proof:** The Prover generates a ZKP attesting that the result matches the Digest.
*   **Performance:** Sub-second queries on 1M+ rows (using GPU acceleration).

### B. Blitzar (GPU Backend)
*   **Framework:** Rust-based acceleration for cryptographic primitives (MSM, NTT).
*   **Hardware:** Requires NVIDIA GPUs for massive parallelization of the field arithmetic.

## 2. Plonky3: The Modular Toolkit

Plonky3 is the standard for building custom, high-performance ZK circuits in **Stable Rust**.

### A. Small-Field Optimization
*   **Legacy:** 256-bit fields (BN254) require BigInt arithmetic (slow).
*   **Modern:** **31-bit fields** (BabyBear, Mersenne31) fit into native CPU/GPU registers (AVX-512, NEON).
*   **Impact:** 10x-100x speedup in proof generation.

### B. The Lookup Argument (LogUp)
To solve the "Non-Match" bottleneck:
1.  **Don't Compare:** Do not write `if A[i] == B[j]` inside the circuit.
2.  **Do Lookup:** Use a **Cross-Table Lookup**.
    *   *Constraint:* "Every value in Column X exists in Table Y."
    *   *Math:* $\sum \frac{1}{X - t} = \sum \frac{1}{X - q}$ (Logarithmic Derivative).
3.  **Result:** Complexity drops from $O(n^2)$ to $O(n)$.

### C. Recursive Proving (IVC)
To handle 15M rows without OOM (Out of Memory):
*   **Batching:** Process 500k rows at a time.
*   **Folding:** The output of Batch $N$ verifies Batch $N-1$.
*   **Finality:** One constant-sized proof represents the entire dataset.

## 3. Privacy-Preserving Record Linkage (PPRL)

When ZK is overkill, use **Zero-Relationship Encoding** for $O(n)$ matching.

### A. The "Is_Match" Witness Strategy
1.  **Local Search:** The CLI (Prover) finds matches using a standard Hash Map (fast).
2.  **Witness Generation:** The CLI writes `1` to an `is_match` column for found records.
3.  **ZK Proof:** The circuit proves: *"For every row marked `1`, the ID exists in the Commitment."
*   *Benefit:* The heavy cryptography is only run on the matches, not the non-matches.

### B. Deterministic Hashing
*   **Technique:** HMAC with a one-time nonce.
*   **Usage:** If `ID_A == ID_B` reveals the ID anyway, hashing is secure enough for the *matching* phase. ZK is reserved for proving *properties* of the match (e.g., "Age > 18" without revealing Age).

## 4. Jolt (Lookup-Centric VM)
*   **Concept:** A zkVM that maps every CPU instruction to a Lookup Table.
*   **Use Case:** Proving execution of standard Rust code (compiled to RISC-V) without writing custom circuits.
*   **Trade-off:** Currently requires Rust Nightly; less mature than Plonky3.

## 5. Recommended Stack (2026)
*   **Language:** Rust (Stable).
*   **Toolkit:** **Plonky3** (for circuits) or **Proof of SQL** (for relational queries).
*   **Field:** **BabyBear** (31-bit).
*   **Hash:** **Poseidon2** (for circuit efficiency).
*   **Hardware:** GPU (CUDA/Metal) for Prover; CPU for Verifier.
