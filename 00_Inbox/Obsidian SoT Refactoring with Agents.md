---
aliases: []
tags: []
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2026-01-03T00:16:25+00:00
modified: 2026-01-05T16:59:10+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
title: Obsidian SoT Refactoring with Agents
source: "https://gemini.google.com/share/7990b6b12866"
author:
  - "[[Gemini]]"
description: "Created with Gemini"
type: "input"
---

i have been building a system of sot notes. I want to be able to find my ideas and know they are the definitive versions of my thinking and knowledge. I use obsidian and the sot notes have grown in number. I have a gemini cli that can read my local obsidian vault via a obsidian mcp. I need a prompt that will instruct the llm to analyse all the sots and work out the themes and topics. Then create a plan to dedupe them and remove redundancy. But it needs to act efficiently to stay within the context window and allowed tokens. how can i use multiple agents to build up the information needed to do this with my notes and to update them and simplify them. give me a prompt to paste into gemini cli

Here is a structural framework and the specific prompt architecture to execute this refactoring operation.

### The Strategy: Map-Reduce for Cognitive Architecture

To manage context window limits while enforcing a "Single Source of Truth," you cannot simply "read all notes." You must treat this as a **database refactoring project** using a sequential, multi-agent simulation.

We will utilise a **Map-Reduce** pattern:

1. **Map (The Surveyor):** Scan metadata/filenames to build a topology of themes without reading full content.
2. **Cluster (The Architect):** Group related files into "Semantic Blocks" (e.g., *Health*, *Productivity*, *Tech*).
3. **Reduce (The Refactorer):** Process *one block at a time* to perform the "Squash and Merge."

### The Agentic Workflow

Since you are using a CLI with MCP, we will define a "Master Prompt" that instructs the LLM to instantiate ephemeral sub-agents (modes) to handle specific stages of the pipeline.

- **Agent A: The Indexer (Low Token Cost):** Calls `list_files`. Analyses titles/tags. Outputs a JSON map of clusters.
- **Agent B: The Linter (High Intelligence):** Reads files *only* within a specific cluster. Identifies overlap, deprecated logic, and conflicts.
- **Agent C: The Synthesiser (Output):** Writes the new "Golden Master" content and lists files to delete.

---

### The Prompt

Paste the following into your Gemini CLI. It is engineered to force the LLM into an "Orchestrator" role, preventing it from hallucinating content it hasn't read and respecting your token budget.

Markdown

```markdown
# Role: ProdOS Systems Architect (Refactoring Engine)

**Objective:** Analyse the Obsidian vault via MCP to identify redundancy within "SoT" (Source of Truth) notes, deduplicate concepts, and enforce the "Single Source of Truth" architecture.

**User Cognitive Profile:** Abstract-Conceptual. Prioritise structural integrity, concept density, and utility. Avoid fluff.
**Context Constraints:** Do NOT read all files immediately. You must conserve tokens.

## Phase 1: Topology Mapping (The Surveyor)
1.  **Action:** Use your MCP tool to list all files in the vault.
2.  **Filter:** Isolate files containing "SoT" in the title or tagged \`#SoT\` / \`#architecture\` / \`#system_design\`.
3.  **Analysis:** Analyse the *filenames* only. Group them into "Semantic Clusters" (e.g., "Cognitive Performance", "System Architecture", "Health", "Tech Stack").
4.  **Output 1:** Present a table of these Clusters with their constituent files.
5.  **Stop:** Ask me which Cluster to refactor first.

## Phase 2: The Deep Dive (The Linter)
*Wait for user selection of a Cluster.*
1.  **Action:** Use MCP to read *only* the files in the selected Cluster.
2.  **Analysis:** Compare the content of these notes. Look for:
    * **Redundancy:** Identical concepts described in multiple places.
    * **Version Conflicts:** "HEAD" (WIP) thinking mixed with "SoT" (Master) canon.
    * **Fragmentation:** A single concept split unnecessarily across three files.
3.  **Output 2:** A "Refactoring Plan" listing:
    * *Keep:* The primary file to act as the Master.
    * *Merge:* Content from other files to move into the Master.
    * *Delete:* Files that will become obsolete.

## Phase 3: Squash and Merge (The Synthesiser)
*Wait for user approval of the Plan.*
1.  **Action:** rewrite the content of the "Master" note to include the merged insights.
2.  **Constraint:** adhere to ProdOS principles:
    * **Definition:** Clear, axiomatic definition at the top.
    * **Utility:** Operational rules over descriptive text.
    * **Architecture:** Use tables/lists for density.
3.  **Output 3:** The full Markdown text for the updated Source of Truth and a list of files to archive/delete.

---
**INITIATE SEQUENCE:** Start by executing **Phase 1** now. List the files and generate the Semantic Clusters.
```

### How to Execute This

1. **Paste the Prompt.** Gemini will use the MCP to scan your directory. It will *not* read file contents yet (saving tokens).
2. **Review the Clusters.** Gemini will present a list like:
	- *Cluster A: Metacognition* (`SoT - Thinking`, `SoT - Mental Models`, `SoT - Hansei`)
	- *Cluster B: Health* (`SoT - Sleep`, `SoT - Vitality`)
3. **Select a Target.** You reply: *"Refactor Cluster A."*
4. **Review the Plan.** Gemini reads *only* those 3-4 files. It enters "Linter Mode" and proposes: *"Merge 'Mental Models' into 'Thinking'. Delete 'Hansei' as it is redundant."*
5. **Finalise.** You reply: *"Proceed."* Gemini generates the final code block for the new note.

### Next Step

Would you like me to refine the "Phase 3" instructions to specifically format the output using your preferred **ProdOS Header/Metadata** standard (e.g., preserving `confidence`, `review_interval`, and `aliases`)?

yes

Here is the updated, production-ready prompt.

I have refined **Phase 3** to enforce strict adherence to your metadata schema (YAML frontmatter) and structural patterns (Definition callouts, `see_also` merging).

### The Complete System Refactoring Prompt

Paste this entire block into your Gemini CLI.

Markdown

```markdown
# Role: ProdOS Systems Architect (Refactoring Engine)

**Objective:** Analyse the Obsidian vault via MCP to identify redundancy within "SoT" (Source of Truth) notes, deduplicate concepts, and enforce the "Single Source of Truth" architecture.

**User Cognitive Profile:** Abstract-Conceptual. Prioritise structural integrity, concept density, and utility. Avoid fluff.
**Context Constraints:** Do NOT read all files immediately. You must conserve tokens.

## Phase 1: Topology Mapping (The Surveyor)
1.  **Action:** Use your MCP tool to list all files in the vault.
2.  **Filter:** Isolate files containing "SoT" in the title or tagged \`#SoT\`, \`#architecture\`, or \`#system_design\`.
3.  **Analysis:** Analyse the *filenames* only. Group them into "Semantic Clusters" (e.g., "Cognitive Performance", "System Architecture", "Health", "Tech Stack").
4.  **Output 1:** Present a table of these Clusters with their constituent files.
5.  **Stop:** Ask me which Cluster to refactor first.

## Phase 2: The Deep Dive (The Linter)
*Wait for user selection of a Cluster.*
1.  **Action:** Use MCP to read *only* the files in the selected Cluster.
2.  **Analysis:** Compare the content of these notes. Look for:
    * **Redundancy:** Identical concepts described in multiple places.
    * **Version Conflicts:** "HEAD" (WIP) thinking mixed with "SoT" (Master) canon.
    * **Fragmentation:** A single concept split unnecessarily across three files.
3.  **Output 2:** A "Refactoring Plan" listing:
    * *Keep:* The primary file to act as the Master (SoT).
    * *Merge:* Specific insights/sections from other files to move into the Master.
    * *Delete:* Files that will become obsolete (e.g., deprecated "HEAD" notes).

## Phase 3: Squash and Merge (The Synthesiser)
*Wait for user approval of the Plan.*
1.  **Action:** Rewrite the content of the target "Master" SoT note to include the merged insights.
2.  **Metadata Constraint (YAML):** You MUST preserve and consolidate the YAML Frontmatter:
    * \`aliases\`: Merge all aliases from source files.
    * \`created\`: Use the earliest date found.
    * \`modified\`: Update to today's date.
    * \`status\`: Set to "stable".
    * \`type\`: Ensure it is set to "SoT".
    * \`see_also\`: Merge and deduplicate all incoming wiki-links \`[[...]]\`.
    * \`review_interval\`: Retain or set a default (e.g., "3 months").
3.  **Structural Constraint (Markdown):** Adhere to the ProdOS layout:
    * **Header 1:** \`## 1. Definitive Statement\`
    * **Callout:** Use \`> [!definition] Definition\` for the core axiom.
    * **Style:** Use tables for comparisons. Use bolding for key terms.
4.  **Output 3:**
    * The full, ready-to-copy Markdown text for the new SoT.
    * A list of files to safely delete.

---
**INITIATE SEQUENCE:** Start by executing **Phase 1** now. List the files and generate the Semantic Clusters.
```

### Next Step

Would you like me to execute a "Dry Run" of this logic using the `SoT - PRODOS (System Architecture)` content you provided to show you exactly how the Agent would parse and restructure it?

yes

Here is the **Dry Run** simulation.

This demonstrates how the Agent (running the prompt I provided) would analyse, critique, and rebuild your `SoT - PRODOS (System Architecture)` note.

---

### Phase 1 Output: Topology Mapping (The Surveyor)

*The Agent scans your file list (simulated based on your `see_also` links) and generates the clusters.*

**Agent Output:**"I have analysed the file topology. Here are the detected Semantic Clusters:"

**Agent Query:** "I recommend starting with the **System Core** cluster to establish the foundational rules before processing the downstream modules. Shall I proceed with refactoring **System Core**?"

> *(User Action: "Yes, refactor System Core.")*

---

### Phase 2 Output: The Deep Dive (The Linter)

*The Agent reads the content of the selected files. It critiques the current `SoT - PRODOS (System Architecture)` note.*

**Agent Output:**"I have analysed the **System Core** cluster.

**Critique & Issues Found:**

1. **Broken Definition:** In the Master Note, the Definition is incomplete: `Its sole purpose is to: ""`.
2. **Redundancy:** The file `Old ProdOS Product Description` (referenced in `see_also`) is likely fully superseded by this architecture note and should be deleted.
3. **Formatting Errors:** Section 1.1 uses standard text where a list or callout would be higher density. Section 2 contains a table row (`Version Control Failure`) that lacks a header or context.
4. **Formatting Inconsistency:** Quote marks in the 'Epistemic Stance' section are malformed (`The Map is Not the Territory: "`).

**Refactoring Plan:**

- **TARGET:**`SoT - PRODOS (System Architecture).md`
- **ACTION:** Fix the broken Definition axiom.
- **ACTION:** Standardise the 'Dual-Axis' and 'Note Schema' tables for readability.
- **ACTION:** Consolidate `Old ProdOS Product Description` into the history/context (if needed) or simply delete it.
- **DELETE:**`Old ProdOS Product Description` (post-merge)."

> *(User Action: "Proceed.")*

---

### Phase 3 Output: Squash and Merge (The Synthesiser)

*The Agent rewrites the note. Below is the actual Markdown output you would receive. It creates a cleaner, stricter version of your content.*

Markdown

```markdown
---
aliases: ["My Productivity System", "ProdOS", "The PRODOS Architecture"]
confidence: "5/5"
created: 2025-11-13T00:00:00Z
last_reviewed: "2025-12-30"
modified: 2025-12-30T17:15:00+00:00
purpose: "The Master Index Note and System Specification for PRODOS, defining its architecture as an ADHD-centric cognitive augmentation system."
review_interval: "3 months"
see_also: ["[[SoT - PRODOS - Action Management (GTD)]]", "[[SoT - PRODOS - Knowledge Synthesis (Thinking)]]", "[[SoT - PRODOS - Structure & Storage (PARA/PKM)]]", "[[SoT - The Extended Mind Thesis]]", "[[SoT - ADHD and Motivation]]"]
status: "stable"
tags: ["architecture", "hansei", "prodos", "system_design", "topic/health/adhd"]
title: SoT - PRODOS (System Architecture)
type: "SoT"
uid: 
---

## 1. Definitive Statement

> [!definition] Definition
> PRODOS operates as a **Thinking Utility**, not a storage archive. Its sole purpose is to **reduce the friction of cognition**.
> 
> **The Metric:** We do not measure "notes created." We measure **clarity achieved** and **actions taken**.

### 1.1 Theoretical Foundation
ProdOS is an operational implementation of the **[[SoT - The Extended Mind Thesis|Extended Mind Thesis]]**. It treats the vault as constitutive of the user's cognitive machinery, utilising **Epistemic Actions** (thinking via doing) to bypass executive function deficits.

### 1.2 Epistemic Stance: "Utility Over Truth"
* **The Map is Not the Territory:** The system is a simplified model. When the map disagrees with reality, we update the map.
* **Utility over Completeness:** If a note does not help you *think* or *act*, it is noise. We prioritise "Good Enough" over "Perfect."

---

## 2. The Core Constraint: Zero-Maintenance Baseline

Standard systems fail ADHD users due to high "Operational Overhead." PRODOS is engineered for **< 10% Maintenance Load** (\`Time Organizing / Time Executing\`).

* **The Mandate:** Decouple maintenance from execution.
* **Low Power Mode:** The system relies on capture-first workflows that function during low executive function states. Neglect must not cause system failure.

---

## 3. The Architecture: Dual-Axis Engagement Model

PRODOS functions as a cognitive control room balancing two axes:

| Engineering Axis | Cognitive Counterpart | ADHD Deficit | PRODOS Solution |
| :--- | :--- | :--- | :--- |
| **Horizontal (Azimuth)** | **Temporal (Time)** | *Time Blindness* | **Calendar/Blocking:** Visible temporal landscape. |
| **Vertical (Elevation)** | **Attentional (Focus)** | *Distraction* | **Depth Control:** Managing "Rabbit Holes" vs. "Flow". |

---

## 4. The Data Schema: Thinking vs. Storage

The system maintains a strict separation of concerns utilizing a **Git Version Control** metaphor to prevent "Version Control Failure" (treating draft notes as truth).

| Feature | HEAD Notes (Working Tree) | SoT Notes (Master Branch) |
| :--- | :--- | :--- |
| **Role** | **The Workbench.** Volatile state. | **The Canon.** Stable knowledge. |
| **Trust** | **Zero Trust.** Chaotic stream. | **High Trust.** System of Record. |
| **Protocol** | **Continuous Commit.** Log real-time. | **Squash & Merge.** Synthesise & Delete HEAD. |

### 4.1 Workflow Protocols
1.  **HEAD Notes:** Create via hotkey (\`YYYY-MM-DD-HHmm-HEAD\`). Never resume old notes; start fresh. Output to **Action** (Todoist), **Fact** (SoT), or **Pointer** (Future Task).
2.  **SoT Notes:** Updated only through formal synthesis. Must be atomic and durable.

---

## 5. Trust & Verifiability: The Acceptance Criteria

**The Output First Metric:** If using the system feels like a chore, it is failing.

1.  **The 60-Second Context Restoration Test:** Can you recall the *Minimum Viable Understanding (MVU)* and *Next Action* in < 60s?
2.  **The Reuse Score:** Did the system avoid at least 30 minutes of new research for a project?

---

## 6. Functional Specification

The logic is implemented through five integrated modules:

1.  **Ubiquitous Capture:** Zero-friction entry (Voice/Keys) into a single \`00_Inbox\`.
2.  **Logic Processor:** Filters inputs into **Actionable** (Project/Task) or **Non-Actionable** (Reference/Trash). Enforces the **2-Minute Rule**.
3.  **Visual Flow Engine:** Uses Kanban with **WIP Limits** to prevent cognitive overload.
4.  **Review Orchestrator:** Weekly Review ritual to "Get Clear, Get Current, Get Creative."
5.  **Cognitive Support:** "Now" toggle for distraction-free focus and gamified feedback loops.

---

## 7. Execution Protocols

### 7.1 The Reality Unit Test
Thinking is only complete when it generates a **Query for Reality**.
* **Input:** Hypothesis (HEAD Note).
* **Function:** The Next Test (Action).
* **Return Value:** Data/Outcome (Update SoT).

### 7.2 The Ignition Protocol
Used to convert "Work" into "Inquiry" when motivation is low:
* **Mystery Hack:** Refactor chore into a bet/hypothesis.
* **Time Trial:** Refactor infinite task into a binary sprint.
* **Spite Hack:** Refactor compliance into rebellion/argument.

---

## 8. Maintenance: The Hansei Loop

**Philosophy:** "No problem is a problem."
1.  **Identify Friction:** Analyse failure without judgment.
2.  **Adjust Process (Kaizen):** Apply the 1% rule.
3.  **Verify Alignment (Ikigai):** Check against "Reason for Being."

### 8.1 Retrieval Strategy
Search tools must exclude \`HEAD\` folders by default. Searching a topic must yield **one result**: The SoT.

---
**Files to Delete:**
- \`Old ProdOS Product Description\` (Redundant)
```

### Key Changes Made by the Agent:

1. **Fixed Definition:** Filled in "reduce the friction of cognition" based on context.
2. **Table Repair:** Fixed the broken "Version Control Failure" table in Section 2 (moved concept to Section 4).
3. **Typos:** Fixed the messy quotes in Section 1.2.
4. **Metadata:** Cleaned up the `see_also` list (removed self-references if any, though kept valid links).
5. **Structure:** Renumbered sections for better logical flow (e.g., moving "Workflow Protocols" under "Data Schema").

**Next Step:**Would you like to proceed with the CLI prompt I provided earlier to run this on your actual vault?

I got this from gemini cli

Proceed with this plan? (I will execute the merges and file deletions upon confirmation).

\> yes

Responding with gemini-3-pro-preview

✕ \[API Error: Resource exhausted. Please try again later. Please refer to https://cloud.google.com/vertex-ai/generative-ai/docs/error-code-429 for more details.\]

This error confirms you hit the **Context Window or Rate Limit (TPM)** because the CLI session was carrying the "memory" of the entire file list (Phase 1) and the analysis (Phase 2) while trying to generate the final heavy output (Phase 3).

To fix this, you must **clear the session** (restart the CLI) and execute **Phase 3 as an isolated, atomic operation**.

Here is the "Surgical Strike" prompt. It forces the LLM to do the work without the baggage of the previous conversation history.

### The Fix: "Atomic Merge" Prompt

**Step 1:** Restart your Gemini CLI (ensure a clean slate).**Step 2:** Paste this prompt. **Crucial:** Replace the bracketed placeholders `[...]` with the actual filenames you identified in the Plan.

Markdown

```markdown
# Role: ProdOS Synthesiser (Clean Context)

**Objective:** Read specific source files and rewrite the Master Note to enforce the "Single Source of Truth."

**Target Master Note:** \`SoT - PRODOS (System Architecture).md\`
**Source Notes to Merge:** \`[Insert Filename 1]\`, \`[Insert Filename 2]\`
*(Note: If no specific source notes, just leave the Target Master Note).*

**Instructions:**
1.  **READ:** Use your MCP tool to read the contents of the **Target Master Note** and the **Source Notes**.
2.  **SYNTHESISE:** Rewrite the **Target Master Note** to include any non-redundant insights from the Source Notes.
3.  **FORMAT:** Adhere to strict ProdOS Standards:
    * **YAML:** Preserve/merge \`aliases\`, \`see_also\`, and \`tags\`. Set \`status: stable\`.
    * **Definition:** Start with \`## 1. Definitive Statement\` and use a \`> [!definition]\` callout.
    * **Style:** Use high-density tables and bullet points. No conversational fluff.
4.  **OUTPUT:** Provide the full, compiled Markdown for the new **Target Master Note**.
```

### Why this works

By restarting the session, you drop the thousands of tokens consumed by the "File List" and "Analysis" steps. This allocates your entire available token budget to the actual rewriting task.

Google Account

Leon Ormes

leonormes@gmail.com
