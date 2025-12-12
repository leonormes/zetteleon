---
aliases: [ProdOS Structure, PARA for ProdOS, The 4-File System]
confidence: 5/5
created: 2025-12-12T12:00:00Z
epistemic:
last_reviewed:
modified: 2025-12-12T12:00:00Z
purpose: To define the canonical folder structure and storage protocols for ProdOS v5.0, ensuring optimal context retrieval and LLM efficiency.
related-soTs: ["[[SoT - PRODOS (System Architecture)]]", "[[SoT - PRODOS - Knowledge Synthesis (Thinking)]]"]
review_interval: 6 months
see_also: []
source_of_truth: true
status: stable
tags: ["structure", "para", "pkm", "prodos"]
title: SoT - PRODOS - Structure & Storage
type: SoT
uid:
updated:
---

## 1. Definitive Statement

> [!definition] The 4-File Architecture
> ProdOS v5.0 replaces deep folder hierarchies with a flattened, **4-component** structure designed for **Cognitive Throughput** rather than Storage. 
> 
> The structure mirrors the Cognitive Loop: **Input (Inbox) -> Processing (Thinking) -> Storage (Library) -> Output (Actions).**

---

## 2. The Core Structure (v5.0)

To maximize LLM context window efficiency (reducing token cost by 75-90%) and human retrieval speed, the vault is organized into these primary domains:

| Directory | Component | Role | Cognitive Phase |
| :--- | :--- | :--- | :--- |
| **`00_Inbox/`** | **The Stream** | Frictionless Capture | **Capture** |
| **`20_Thinking/`** | **The Workbench** | Active Workspace (`HEAD` notes) | **Refine (Thinking)** |
| **`30_Library/`** | **The Canon** | Long-term Knowledge (`SoT` notes) | **Synthesize (Knowing)** |
| **`10_Actions/`** | **The Dashboard** | Project Management & Views | **Engage (Doing)** |

### A. `00_Inbox` (The Catch-All)
- **Purpose:** A temporary holding ground for raw inputs.
- **Rule:** **Zero Retention.** This folder must be emptied every 24-48 hours.
- **Contents:** Daily Notes, raw fleeting notes, quick captures from mobile.

### B. `20_Thinking` / `21_Workbench` (The RAM)
- **Purpose:** The home of **HEAD Notes**. This is "Work in Progress."
- **Rule:** **No Folders.** A flat list of active thinking threads.
- **Naming Convention:** `YYYY-MM-DD-HHmm-HEAD - Topic` (Timestamped to prevent collisions).
- **Lifecycle:** Files here are ephemeral. They are either archived or merged into SoTs.

### C. `30_Library` / `31_Resources` (The Hard Drive)
- **Purpose:** The home of **SoT (Source of Truth)** notes.
- **Rule:** **High Trust.** Only verified, synthesized knowledge enters here.
- **Organization:** Can use broad categories (PARA Areas) if necessary, but relies primarily on **MOCs (Maps of Content)** for navigation.

### D. `10_Actions` / `11_Projects` (The Control Center)
- **Purpose:** Project Dashboards and aggregated views.
- **Rule:** **Links, not Content.** These notes primarily point to HEAD notes (current state) and SoT notes (reference).
- **Contents:** Project Notes (e.g., `Project - ProdOS Migration.md`) containing the "State Snapshot."

---

## 3. Storage Protocols

### The "No-Filing" Rule
We do not "file" notes in ProdOS; we **Tag and Link**.
- **Folders** are for *System Architecture* (Permissions/Types).
- **Links** are for *Knowledge Architecture* (Context).

### The Archive Strategy (`99_Archive`)
- **Purpose:** To hide "Dead" content from the Search / Context Window.
- **Trigger:** When a HEAD note is processed (Action extracted, Insight merged), it is moved to `99_Archive`.
- **Retrieval:** We rarely look here. It is for audit trails only.

---

## 4. Current Migration Status
*Note: The system is currently migrating from the legacy `000_inbox` / `003_workbench` / `100_zettelkasten` structure to this v5.0 standard.*

- `003_workbench` -> Maps to `20_Thinking`
- `SoT` / `100_zettelkasten` -> Maps to `30_Library`
- `200_projects` -> Maps to `10_Actions`
