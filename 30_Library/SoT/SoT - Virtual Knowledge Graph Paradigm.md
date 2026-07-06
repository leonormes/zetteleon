---
aliases: [OBDA, Ontop, Semantic Data Access]
created: 2026-01-07T20:52:57+00:00
last_reviewed: null
modified: 2026-07-04T10:50:47+00:00
permalink: llmeon/30-library/so-t/so-t-virtual-knowledge-graph-paradigm
status: Active
tags: [architecture, data-centric, knowledge-graph, ontop, semantic-web]
title: SoT - Virtual Knowledge Graph Paradigm
type: SoT
updated: null
---

## SoT - Virtual Knowledge Graph Paradigm

> The Core Abstraction: The Virtual Knowledge Graph (VKG) is an architectural pattern that decouples the Semantic Layer (Ontology) from the Physical Layer (Database). It allows users to query complex data using high-level concepts (SPARQL) while executing optimized, performant logic on the underlying storage (SQL), without the need for expensive ETL/Materialization.

### 1. The Architecture: Ontology-Based Data Access (OBDA)

The VKG paradigm (specifically the Ontop implementation) relies on a tripartite architecture:

1. The Ontology (The Vocabulary): A conceptual model (OWL 2 QL) that defines the domain (e.g., "Patient," "Observation"). It hides the complexity of the schema.
2. The Mappings (The Bridge): Declarative rules (R2RML) that link Ontology terms to Database structures.
    - _Logic:_ `Source: SELECT id FROM users` -> `Target::User/{id} a:Person`.
3. The Data Source (The Reality): The existing relational database (RDBMS) where the data lives.

### 2. The Mechanics: From SPARQL to SQL

The "Magic" of VKG is the real-time translation of semantic intent into relational execution.

#### 2.1 T-Mappings (Saturated Mappings)

- Concept: Pre-compiling the hierarchy.
- Mechanism: If `LungCancer` is a subclass of `Neoplasm`, the system automatically generates mappings for `Neoplasm` from the `LungCancer` logic during startup ("off-line").
- Benefit: Reasoning happens _once_ at compile time, not at query time.

#### 2.2 The Intermediate Query (IQ)

- Concept: The "Algebra" of translation.
- Problem: SPARQL and SQL have different logic (3-valued logic, typing, joining).
- Solution: An internal algebraic representation that unifies both worlds, allowing optimization before the final SQL generation.

#### 2.3 Semantic Query Optimization (SQO)

- Concept: Using the schema to delete work.
- Mechanism: Ontop uses Primary/Foreign Keys to detect redundant self-joins and unnecessary `DISTINCT` operations.
- Result: The generated SQL is often more efficient than a human-written query because it mathematically guarantees redundancy elimination.

### 3. The Diplomatic Analogy

- The User (Philosopher): Speaks in abstract concepts ("Give me all Treatments").
- The Database (Librarian): Speaks in rigid storage addresses ("Row 4, Table B").
- The System (Diplomat):
    - Uses a Dictionary (Ontology) to understand the Philosopher.
    - Uses a Phrasebook (Mapping) to translate concepts to addresses.
    - Uses a Notepad (IQ) to rearrange the request so the Librarian can execute it efficiently without confusion.

### 4. Domain Integration

- Domain III (Data-Centric Systems): VKG is the ultimate expression of Data-Centricity. It leaves data in its source of truth and imposes a logical view (Type System) on top of it, rather than moving the data to fit the code.
- Impedance Mismatch: It solves the object-relational mismatch not by ORM (code), but by Mapping (declarative logic).
