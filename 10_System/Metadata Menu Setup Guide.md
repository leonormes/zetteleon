---
aliases: []
confidence: ""
created: 2025-12-24T22:15:15Z
epistemic: ""
last_reviewed: ""
modified: 2025-12-25T18:35:29Z
purpose: ""
review_interval: ""
see_also: []
source_of_truth: []
status: ""
tags: []
title: Metadata Menu Setup Guide
type: ""
uid: 
updated: 
---

## Metadata Menu Setup for ProdOS

Based on the documentation, I have established a **FileClass** architecture for your **Source of Truth (SoT)** notes. This allows you to manage metadata using a structured form rather than raw YAML editing.

### 1. The Configuration

I have created the definition file at: `10_System/fileClasses/SoT.md`.

#### Required Plugin Settings

To activate this, you must configure the **Metadata Menu** plugin settings:

1. **Class Files Path:** Set this to `10_System/fileClasses/`
2. **Global FileClass:** (Optional) You can set this to `SoT` if you want it applied to everything, but it is better to map it via **Tags** or **Paths**.

### 2. The SoT Template Fields

The `SoT` FileClass defines the following structured fields:

| Field | Type | Options |
|:--- |:--- |:--- |
| **status** | `Select` | 🌱 Seedling, 🥚 Incubating, 🌳 Stable, 🗃️ Archived |
| **epistemic** | `Select` | 🧩 Synthesis, 🧪 Theory, ♟️ Strategy, ⚙️ Operational, 🔬 Scientific |
| **confidence** | `Select` | 1/5 (Low) to 5/5 (Very High) |
| **review_interval** | `Cycle` | 1m, 3m, 6m, 1y |
| **last_reviewed** | `Date` | Date Picker |
| **purpose** | `Input` | Text string |
| **see_also** | `MultiFile`| Links to other notes |

### 3. How to Use

1. **Add the Class:** In any SoT note, add `fileClass: SoT` to the frontmatter.
2. **The Button:** A Metadata Menu button will appear (depending on your settings, usually near the file header).
3. **The Form:** Click the button to open a UI form where you can select values from dropdowns instead of typing them.

> [!tip] Auto-Mapping
> You can configure Metadata Menu to automatically apply the `SoT` class to any note in the `30_Library/SoT/` folder.
> Go to **Metadata Menu Settings > FileClass Settings** and add a path mapping.
