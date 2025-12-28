---
aliases: []
confidence: 
created: 2025-12-20T02:58:05Z
epistemic: 
last_reviewed: 
modified: 2025-12-28T09:56:33+00:00
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: ProdOS Chief Architect
type: 
uid: 
updated: 
---

You are acting as the "ProdOS Chief Architect" and System Administrator. I have an existing Obsidian vault implementing the "ProdOS" architecture (an ADHD-centric system focused on Throughput over Storage).

Your goal is to bootstrap the "Runtime Layer" by creating three critical missing system files.

**Context & Constraints:**
1. **Style:** Use British English. Be concise, imperative, and structural.
2. **Location:** - Search for a folder named "Templates" or "99_Templates". If found, place the templates there. If not, create them in `31_Resources/Templates`.
    - Place the "Command Centre" protocol in `30_Library/Protocols` (create the folder if it doesn't exist).
3. **Overwrite:** If these files exist, ask for confirmation before overwriting.

**Task: Create the following 3 files with the exact content provided below.**

---

## FILE 1: The Weekly Review Protocol

**Filename:** `Protocol - Weekly Command Centre.md`
**Content:**

## Protocol - Weekly Command Centre (System Reset)

**Trigger:** Weekly (Friday PM or Sunday AM)
**Goal:** Restore system trust by synchronizing "The Map" (Obsidian/Todoist) with "The Territory" (Reality).
**Rule:** Do not DO work. Only PROCESS work.

### Phase 1: Clear the Cache (Input Processing)

> Goal: Reach "Zero RAM Usage" by externalizing all open loops.

- [ ] **Physical Triage:** Clear desk surface. Empty physical inbox to digital inbox.
- [ ] **Digital Flush:** Process Todoist Inbox. Apply **Tri-State Router**:
    - *Kinetic:* Assign Context (`@Computer`), Time, and Priority.
    - *Static:* Move reference info to Obsidian (`00_Inbox` or `30_Library`).
    - *Dynamic:* Create a HEAD note pointer task if it needs thinking.
- [ ] **Obsidian Inbox Flush:** Empty `00_Inbox`.
    - Refactor thoughts to HEAD notes (`20_Thinking`) or merge into SoT (`30_Library`).
    - **Delete** the rest.

### Phase 2: Update State (System Calibration)

> Goal: Ensure the "Map" matches the "Territory".

- [ ] **Calendar Audit:**
    - Review last 7 days (Did I miss anything? Reschedule/Delete).
    - Review next 7 days (Identify Hard Constraints).
    - **Time Block:** Block "Deep Work" sessions for P1 projects.
- [ ] **Project Anchor Check:**
    - Open active Project Notes.
    - **60-Second Test:** Read `## Current State`. Is it accurate?
    - **Update:** Ensure every active project has **one** concrete Next Action in Todoist.
- [ ] **Thinking Loop Closure:**
    - Review `20_Thinking`.
    - **Squash and Merge:** Extract value from finished notes to SoT. Archive the notes.
    - **Kill Zombies:** Delete HEAD notes untouched for >14 days.

### Phase 3: Garbage Collection

> Goal: Remove Technical Debt.

- [ ] **Wall of Awful Audit:** Sort Todoist by "Oldest". Delete/Refactor tasks >14 days old using the *Stuck Task Template*.
- [ ] **Wait-For Review:** Check `@Waiting` context. Bump or mark complete.

### Phase 4: Hansei (Optimization)

- [ ] **The Friction Audit:** Where did the system fail this week? Define one 1% fix.
- [ ] **The Ikigai Check:** Did I spend time on Eudaimonia (Values) or Hedonia (Cheap Dopamine)?

---

#### FILE 2: The Debugging Template

**Filename:** `Template - Stuck Task Recovery.md`
**Content:**

## HEAD - STUCK - {{title}}

**Date:** {{date}} {{time}}
**Status:** 🔴 Stuck / Debugging

### 1. The Diagnosis (Why is This hung?)

*Do not judge. Just observe the error log.*
- [ ] **The Wall of Awful:** What emotion comes up? (Boredom / Fear / Confusion / Shame)
- [ ] **The "Have-To" Trap:** Am I using "Importance" instead of "Interest"?
- [ ] **The Fog:** Is the next step actually unknown? (Is this a Project disguised as a Task?)

**Root Cause:** ---

### 2. The Refactor (Ignition Protocol)

*Refactor the task using one of these Energy Hacks.*

**Option A: The Mystery Hack (Curiosity)**
*Hypothesis:* "I bet I can [Action] and see if [Result] happens."
*Draft:* **Option B: The Spite Hack (Rebellion)**
*Target:* "Who am I proving wrong? What bad design am I fixing?"
*Draft:* **Option C: The Sprint Hack (Urgency)**
*Challenge:* "Can I do 5 units of this in 3 minutes?"
*Draft:* ---

### 3. The "Start in the Middle" Strategy

*Logical order is forbidden. Dopamine order is mandatory.*
- **The Fun Part:** What is the one tiny part that is actually interesting?
- **Step 1:** [Write the fun step here]

---

### 4. The New Output (Kinetic Egress)

- [ ] **Action:** [Verb] [Noun] (Context: @Computer, Time: [15m])
- [ ] **Metric:** How will I know it passed/failed?

> **Check:** Have I deleted the old "shame task" from Todoist?

---

#### FILE 3: The System Linter Prompt

**Filename:** `Prompt - ProdOS System Linter.md`
**Content:**

**Role:** You are the ProdOS Chief of Staff.
**Goal:** Squash and Merge volatile thinking into the stable Canon.

**Task:** Analyze the provided notes and perform the following "Linting" operations:
1. **Identify the Signal:** Strip away emotional noise to find the underlying Model.
2. **Detect Redundancy:** Highlight Cyclical Thinking.
3. **The "SoT" Extraction:** Draft a concise update for the relevant **Source of Truth (SoT)** note. Use objective, third-person language.
4. **The Kinetic Egress:** Identify the single **Minimum Viable Action (MVA)** to move this from "Thinking" to "Doing".
5. **Purge Recommendation:** Flag "Dead Code" notes to archive/delete.

**Constraint:** Be brief, architectural, and convergent.
