---
aliases: ["Gemini Swarm", "Multi-Agent Refactoring"]
created: 2026-01-11T17:21:01+00:00
modified: 2026-01-12T11:40:04+00:00
status: "research"
tags: ["agents", "architecture", "gemini-cli", "obsidian", "python"]
title: Project - Multi-Agent Obsidian Refactoring Architecture
type: "project"
---

# Project - Multi-Agent Obsidian Refactoring Architecture

## 1. Problem Statement

**Context Rot:** Feeding large volumes of notes into a single LLM context window dilutes signal, increases hallucinations, and hits token limits. To effectively refactor a large Obsidian vault, we cannot use a "context stuffing" approach.

## 2. Core Architecture: Semantic Map-Reduce

The solution is to partition the problem space _before_ the LLM sees it, using a pipeline of specialised agents orchestrated by a stateless controller.

### Design Philosophy (The "Fleet Commander" Model)

Derived from _Boris Cherny_ and _Agentic Trends 2026_:

- **Fleet over Chat:** We treat the LLM not as a conversational partner but as a fleet of autonomous workers.
- **Heterogeneous Intelligence:** Use "Small Language Models" (SLMs) for high-volume Map tasks (Atomization) and "High Intelligence Models" (e.g., Gemini 1.5 Pro) for Reduce tasks (Synthesis).
- **Self-Correcting Protocols:** Agents must have the capacity to update their own system instructions (`GEMINI.md`) when they encounter recurring failures.

### The Pipeline

1. **Ingestion (The Atomizer):** Pre-process raw notes to split compound ideas (e.g., Daily Notes) into "Atomic Units". _Optimization: Use SLM._
2. **Dispatch (The Semantic Indexer):** Vectorise atomic units and cluster them semantically (e.g., "Docker Cluster", "Psychology Cluster") using local embeddings (`all-MiniLM-L6-v2`).
3. **Map Phase (The Specialists):** Low-level agents process specific clusters.
    - _Redundancy Scout:_ Finds duplicates.
    - _Ontologist:_ Extracts entities and naming conventions.
    - _Critic:_ (From LLM Council) Reviews the output of other agents for hallucinations before passing to Reduce.
4. **Reduce Phase (The Architect):** A high-level agent synthesises the "Map" outputs into a global refactoring plan.
5. **DSPy Integration (Future State):** Move from "Prompt Engineering" to "System Programming" by defining **Signatures** (Typed Inputs/Outputs) and using **Optimizers** to automatically refine agent instructions based on success metrics.

## 3. Implementation Strategy (Python + Gemini CLI)

### Phase A: The Atomizer (Pre-processing)

_Objective:_ Clean data before clustering.

- **Logic:** Iterate vault -> Identify compound notes (>500 words or Daily Notes) -> Pipe to Gemini.
- **Prompt:** "Split this text into standalone atomic concepts. Preserve meaning."
- **Output:** Temporary Atomic JSONs.

### Phase B: The Semantic Indexer

_Objective:_ Group related concepts to ensure efficient context usage.

- **Stack:** Python `sentence-transformers`, `scikit-learn` (DBSCAN/K-Means).
- **Action:** Embed Atomic Units -> Cluster -> Output `manifest.json` (`Cluster_ID: [Note_A, Note_B]`).

### Phase C: The Agent Pipeline (Map-Reduce)

_Objective:_ Stateless orchestration via Gemini CLI.

- **Controller:** Python script loops through clusters.
- **Map Agent (Scout):** `cat cluster_files | gemini -s sys_scout.txt > report.json`
- **Reduce Agent (Architect):** `cat reports/*.json | gemini -s sys_architect.txt > master_plan.md`

## 4. Next Actions

- [x] **Develop Atomizer Prompt:** Create the system instruction for breaking down daily notes.
- [x] **Prototype Dispatcher:** Build a simple Python script to generate embeddings for a sample folder.
- [x] **Define JSON Schemas:** Strict output definitions for the Map agents to ensure the Reduce agent can parse them.

## 5. References

- **Concept:** "Open Auggie" (Atomic Extraction + Graph Analysis).
