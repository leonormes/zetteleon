---
aliases: []
created: 2026-01-03T10:07:49+00:00
last_reviewed: ''
modified: 2026-07-13T08:52:42+00:00
permalink: llmeon/30-library/so-t/reference-file-structure
status: ''
tags: []
title: Reference - File Structure
type: ''
---

## Reference - File Structure & Naming Conventions

### 1. The Core Structure

To maximize LLM context window efficiency and human retrieval speed, the vault is organized into these primary domains:

| Directory | Component | Role | Cognitive Phase |
|:--- |:--- |:--- |:--- |
| `00_Inbox/` | The Stream | Frictionless Capture | Capture |
| `01_journals/` | The Log | Daily Notes & Time Logs | Capture / Reflect |
| `02_bases/` | The HUD | System Dashboards (`.base` files) | Orient |
| `10_Actions/` | The Engine | Project Management | Engage (Doing) |
| `20_Thinking/` | The Workbench | Active Workspace (`HEAD` notes) | Refine (Thinking) |
| `30_Library/` | The Canon | Long-term Knowledge (`SoT` notes) | Synthesize (Knowing) |

#### A. The Stream (`00_Inbox` & `01_journals`)

- `00_Inbox/`: A temporary holding ground for raw inputs. Zero Retention Rule: Must be emptied every 24-48 hours.
- `01_journals/`: Contains Daily Notes (`YYYY-MM-DD`). This is the chronological log of your life, capturing fleeting thoughts, logs, and rapid-fire bullets.

#### B. The HUD (`02_bases`)

- Contents: `.base` files (e.g., `HEAD.base`, `SoT.base`) which serve as Dataview Dashboards to query the state of the vault without manual curation.

#### C. The Engine (`10_Actions`)

- Sub-folder: `11_Projects`
- Purpose: Project management views and "State Snapshots" (`Project - Title.md`).
- Rule: Projects link to `HEAD` notes for thinking and `SoT` notes for resources. They do not store knowledge themselves.

#### D. The Workbench (`20_Thinking`)

- Sub-folder: `21_Workbench`
- Purpose: The home of HEAD Notes. This is the active "RAM" of the system.
- Rule: No Folders. A flat list of active thinking threads.
- Naming: `YYYY-MM-DD-HHmm-HEAD - Topic`.
- Lifecycle: Ephemeral. Created to solve a problem, then archived or merged.

#### E. The Canon (`30_Library`)

- Purpose: The home of durable knowledge.
- Rule: High Trust. Only verified, synthesized knowledge enters the `SoT` folder.

#### F. The Archive (`99_Archive`)

- Purpose: To hide "Dead" content from Search / Context Window.
- Trigger: Processed HEAD notes and completed Projects move here.

---

### 2. Storage Protocols

#### The "No-Filing" Rule

We do not "file" notes in ProdOS; we Tag and Link.

- Folders are for _System Architecture_ (Permissions/Types).
- Links are for _Knowledge Architecture_ (Context).
