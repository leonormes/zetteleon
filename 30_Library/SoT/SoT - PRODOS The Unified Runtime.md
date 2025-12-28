---
aliases: ["High-Throughput Runtime", "ProdOS Manual", "The Unified Runtime"]
confidence: "5/5"
created: 2025-12-20T00:00:00Z
epistemic: "operational"
last_reviewed: "2025-12-24"
modified: 2025-12-28T18:49:16+00:00
purpose: "To provide a single High-Throughput Runtime Manual that supersedes separate architectural SoTs, bridging the gap between knowing and doing for an Interest-Based Nervous System."
review_interval: "3 months"
see_also: ["[[SoT - PRODOS - Action Management (GTD)]]", "[[SoT - PRODOS - Knowledge Synthesis (Thinking)]]", "[[SoT - PRODOS (System Architecture)]]"]
source_of_truth: []
status: "stable"
tags: ["adhd", "architecture", "prodos", "productivity", "system_design"]
title: SoT - PRODOS The Unified Runtime
type: "SoT"
uid: 
updated: 
---

> [!abstract] Core Philosophy
> The system is not a Museum for storage; it is a Factory for throughput. Its only purpose is to bridge the gap between "knowing" and "doing" for an Interest-Based Nervous System.

---

## 1. The Hardware Constraints (The Why)

We operate on a "Deficit Model" of executive function. The system is designed to handle three specific hardware failures:

1. **RAM Failure:** Working memory is volatile. We cannot hold a plan and execute it simultaneously.
2. **Initiation Paralysis:** We cannot force importance; we can only trigger Interest, Novelty, Challenge, Urgency, or Passion (INCUP).
3. **Context Decay:** Re-loading a mental model is metabolically expensive. If "re-entry" takes >60 seconds, the project is abandoned.

---

## 2. The Core Logic: The Tri-State Router

To prevent decision fatigue, **all inputs** (Inbox, Email, Slack, Thoughts) are immediately routed into one of three metabolic states. There is no "Maybe" pile.

|**State**|**Definition**|**Destination**|**Protocol**|
|---|---|---|---|
|**1. KINETIC**|**Action.** I know the next physical step.|**Todoist**|Use **Context Bridge** to link back to context.|
|**2. STATIC**|**Reference.** I learned a fact or found a resource.|**30_Library**|Merge into existing SoT. Archive source note immediately.|
|**3. DYNAMIC**|**Thinking.** I am confused, stuck, or designing.|**20_Thinking**|Initialize **A-C-T Loop** in a HEAD Note.|

---

## 3. The Compute Engine: The A-C-T Loop

When routed to **Dynamic** (Thinking), do not "journal." Execute the **A-C-T Framework** to force convergence.

### Phase A: ACTION (Define the Output)

- **The Constraint:** You are not allowed to think without a target.
- **The Prompt:** "What is the single, physical **Minimum Viable Action (MVA)** this thinking session must produce?".
- **Tool:** Use Gemini Flash/Claude to define the MVA if you are stuck.

### Phase C: CONTAINER (The Workbench)

- **The Object:** Create a **HEAD Note** (Dev Branch).
- **The Rule:** Use the **120-Second Commitment**. If the task triggers the "Wall of Awful," commit to working for only 2 minutes.
- **Ignition Protocol:** If bored, refactor the task using **INCUP**:
    - *Mystery:* "Can I break this?"
    - *Spite:* "Prove this documentation is wrong."
    - *Sprint:* "Can I finish in 5 mins?".

### Phase T: THOUGHT (Merge & Delete)

- **The Synthesis:** Once the MVA is identified or the concept understood, **Squash and Merge**.
- **Egress:**
    
    1. Push Task to Todoist (Kinetic).
    2. Update SoT Note (Static).
    3. **Archive/Delete the HEAD Note.** Do not keep the logs.

---

## 4. State Management: The 60-Second Re-entry

Context is volatile. We never "start work"; we "resume state."

- **The Project Anchor:** Every active project must have a `## Current State` block in its dashboard. It must capture:
    - **Now:** What was just done.
    - **Next:** The exact next step.
    - **Why:** The current design intent.
- **The Test:** If you cannot read the Anchor and resume work in **< 60 seconds**, the system has failed. Refactor the note immediately.
- **NotebookLM Bridge:** For complex topics, upload HEAD notes to NotebookLM to create an "Audio Mirror" (Podcast). Listen to it to passively restore context.

---

## 5. Execution & Maintenance (The "Hardware" Care)

### The Dopamenu (Fueling)

When executive function dips, do not doom-scroll. Select from the **Dopamenu**:

- **Appetizers (<5m):** Cold water, 20 jumping jacks, loud music.
- **Mains (Deep):** Coding spike, workout, "Just Start" protocol.
- **Toxic:** Social media, news (Cheap Dopamine).

### Environmental Design

- **Visual Triage:** Use the 3-Box System (Exit, Buffer, Retain) to manage physical entropy.
- **Active vs. Passive Zones:** Keep "Hot" items visible; hide "Cold" items to reduce visual noise.

### Identity & Values

- **Process Primacy:** Ignore the goal; obsess over the system. "I am the type of person who opens my IDE at 9:00".
- **Eudaimonia:** Reframe "Boredom" as "Safety." The quiet hum of a working system is the goal, not the adrenaline of a crisis.

---

## 6. Next Actions (Kinetic Egress)

1. **Archive** all 30+ separate "SoT" files into a folder named `99_Archive/Legacy_Architecture`.
2. **Pin** this single note as your new "System Manual."
3. **Execute** a "Squash and Merge" session on your current `20_Thinking` folder using the Logic Linter.
