---
aliases: [PARA for ProdOS, ProdOS Structure, The 4-File System]
confidence: 5/5
created: 2025-12-12T12:00:00Z
epistemic:
last_reviewed: 2025-12-12
modified: 2025-12-12T23:41:23Z
purpose: To define the canonical folder structure and storage protocols for ProdOS v5.0, ensuring optimal context retrieval and LLM efficiency.
related-soTs: ["[[SoT - PRODOS - Knowledge Synthesis (Thinking)]]", "[[SoT - PRODOS (System Architecture)]]"]
review_interval: 6 months
see_also: []
source_of_truth: true
status: stable
tags: [para, pkm, prodos, structure]
title: SoT - PRODOS - Structure & Storage
type: SoT
uid:
updated:
uuid: 3cf373a9-fe2f-49ac-8575-8a4c7a4725f8
---

- [x] update the structure ticket^2025-12-12T19-24-33 [completion:: 2025-12-12]
    - [📱 View in Todoist app](todoist://task?id=6fVWW77qfRvPX6Qv) (Created: 📝 2025-12-12T19:24)

## 1. Definitive Statement

> [!definition] The 6-Component Architecture
> ProdOS v5.0 utilizes a flattened, **6-component** root structure designed for **Cognitive Throughput** and strict separation of concerns.
>
> The structure mirrors the Cognitive Loop: **Stream (Inbox/Journals) -> Dashboard (Bases) -> Processing (Thinking) -> Storage (Library) -> Output (Actions).**

---

## 2. The Core Structure (v5.0)

To maximize LLM context window efficiency and human retrieval speed, the vault is organized into these primary domains:

| Directory | Component | Role | Cognitive Phase |
| :--- | :--- | :--- | :--- |
| **`00_Inbox/`** | **The Stream** | Frictionless Capture | **Capture** |
| **`01_journals/`** | **The Log** | Daily Notes & Time Logs | **Capture / Reflect** |
| **`02_bases/`** | **The HUD** | System Dashboards (`.base` files) | **Orient** |
| **`10_Actions/`** | **The Engine** | Project Management | **Engage (Doing)** |
| **`20_Thinking/`** | **The Workbench** | Active Workspace (`HEAD` notes) | **Refine (Thinking)** |
| **`30_Library/`** | **The Canon** | Long-term Knowledge (`SoT` notes) | **Synthesize (Knowing)** |

### A. The Stream (`00_Inbox` & `01_journals`)
- **`00_Inbox/`**: A temporary holding ground for raw inputs. **Zero Retention Rule**: Must be emptied every 24-48 hours.
- **`01_journals/`**: Contains Daily Notes (`YYYY-MM-DD`). This is the chronological log of your life, capturing fleeting thoughts, logs, and rapid-fire bullets.

### B. The HUD (`02_bases`)
- **Purpose:** High-level system visibility.
- **Contents:** `.base` files (e.g., `HEAD.base`, `SoT.base`) which serve as **Dataview Dashboards** to query the state of the vault without manual curation.

### C. The Engine (`10_Actions`)
- **Sub-folder:** `11_Projects`
- **Purpose:** Project management views and "State Snapshots" (`Project - Title.md`).
- **Rule:** Projects link to `HEAD` notes for thinking and `SoT` notes for resources. They do not store knowledge themselves.

### D. The Workbench (`20_Thinking`)
- **Sub-folder:** `21_Workbench`
- **Purpose:** The home of **HEAD Notes**. This is the active "RAM" of the system.
- **Rule:** **No Folders.** A flat list of active thinking threads.
- **Naming:** `YYYY-MM-DD-HHmm-HEAD - Topic`.
- **Lifecycle:** Ephemeral. Created to solve a problem, then archived or merged.

### E. The Canon (`30_Library`)
- **Purpose:** The home of durable knowledge.
- **Current State (Hybrid):**
    - **`SoT/`**: The pure v5.0 folder for **Source of Truth** notes.
    - **`31_Resources/`**: General resources and references.
    - **Legacy Folders:** `100_zettelkasten`, `200_projects`, `300_tickets`, `400_indexes` are currently co-located here during the migration phase.
- **Rule:** **High Trust.** Only verified, synthesized knowledge enters the `SoT` folder.

### F. The Archive (`99_Archive`)
- **Purpose:** To hide "Dead" content from Search / Context Window.
- **Trigger:** Processed HEAD notes and completed Projects move here.

---

## 3. Storage Protocols

### The "No-Filing" Rule

We do not "file" notes in ProdOS; we **Tag and Link**.

- **Folders** are for *System Architecture* (Permissions/Types).
- **Links** are for *Knowledge Architecture* (Context).

---

## 4. Migration Status

The system is in a **Hybrid State**.

- **v5.0 Active:** Roots `00`, `01`, `02`, `10`, `20` are fully v5.0 compliant.
- **v5.0 Transition:** `30_Library` contains both the new `SoT` architecture and the legacy Zettelkasten folders (`100_...`).
- **Goal:** Gradually refactor `100_zettelkasten` notes into `SoT` notes (using the LLM Synthesis workflow) and move the remainder to `99_Archive`.
