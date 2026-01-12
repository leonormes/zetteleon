---
title: "‎Gemini – direct access to Google AI"
source: "https://gemini.google.com/share/b8830d096992"
captured: "2026-01-12T09:15:30+00:00 2026-01-12T09:15:30+00:00"
status: "phase-1"
tags:
  - "input"
type: "head"
---
## Phase 1: Ingestion (The Stream)

> [!abstract] Context
> Created with Gemini

### Raw Output / Content
Research and list the main points from the checklist manifesto.

Atul Gawande’s *The Checklist Manifesto* explores how the increasing complexity of modern life—especially in fields like medicine, aviation, and engineering—has made us more prone to "failures of ignorance" (not knowing enough) and "failures of ineptitude" (not using what we know).

The book argues that even the most skilled experts can benefit from simple, well-designed checklists to manage this complexity.

---

### Core Principles of an Effective Checklist

A good checklist is not an exhaustive manual; it is a tool for precision. Gawande outlines several key characteristics:

- **Be Concise:** It should focus on the "killer items"—the steps that are most often missed but carry the highest risk if forgotten.
- **Simple Wording:** Use clear, professional language that is easy to read under pressure.
- **Practical Length:** Ideally, it should fit on one page and take between 45 to 90 seconds to complete.
- **Tested in the Real World:** It must be refined through actual usage to ensure it doesn't cause more confusion than it solves.

### Types of Checklists

Gawande identifies two primary ways to structure a checklist depending on the workflow:

1. **DO-CONFIRM:** You perform the tasks from memory and then pause to "confirm" that everything on the list was done correctly.
2. **READ-DO:** You read each task one by one and perform it as you go, similar to a recipe.

### The Power of "Pause Points"

Checklists work best when integrated into natural breaks in a workflow. In a surgical setting, Gawande highlights three critical "pause points":

- **Before induction of anaesthesia** (The Sign-in).
- **Before skin incision** (The Time-out).
- **Before the patient leaves the operating room** (The Sign-out).

---

### Key Takeaways for Managing Complexity

For someone managing ADHD, these points are particularly relevant because they offload the burden of "working memory" onto a physical system:

- **Humility over Ego:** The biggest barrier to checklists is often the belief that "I am too skilled to need this." Gawande argues that true professionalism is about consistency, not just brilliance.
- **Communication is Critical:** Checklists often include "communication tasks" (e.g., ensuring everyone in the room knows each other’s names). This empowers junior members to speak up if they spot a mistake.
- **The Discipline of Routine:** By automating the routine, "boring" tasks, the brain is freed up to focus on the difficult, creative, or unexpected problems that arise.

---

**Would you like me to help you design a bespoke "Do-Confirm" checklist for one of your own daily routines?**

Update my prodOS to include creating checklists for those outcomes that require them. I guess they would be part of the instructions outcomes. Give me the full note to replace this one

This update integrates the principles of *The Checklist Manifesto* directly into the **PRODOS Core Specification**.

Following the logic of your system, checklists are treated as **"The Firmware"** —the low-level instructions that ensure high-stakes or high-complexity tasks achieve "Production-Ready" status without taxing your working memory. I have integrated these into the **Execution Rules (Section 4)** and defined them as a specific **SoT Note** type.

---

## SoT - PRODOS Core Specification (v3.2 - Integrated)

Markdown

```markdown
---
aliases: ["PRODOS", "Productivity Operating System"]
confidence: "5/5"
created: 2026-01-03T09:45:08+00:00
epistemic: "Axiomatic"
last_reviewed: "2026-01-11"
modified: 2026-01-11T21:15:00+00:00
purpose: "The definitive specification for the PRODOS operating system, defining its kernel, protocols, and execution rules for both human and AI agents."
review_interval: "6 months"
see_also: ["The Checklist Manifesto - Atul Gawande"]
source_of_truth:
status: "stable"
tags: ["prodos", "system-architecture", "methodology", "checklists"]
title: SoT - PRODOS Core Specification
type: "SoT"
---

# PRODOS Core Specification (v3.2 - Integrated)

## 1. The Kernel

### 1.1 The Definition
PRODOS operates as a **Thinking Utility** for both Human and Artificial Intelligence. Its sole purpose is to **reduce the friction of cognition** and **maximize high-signal context**.

- **The Metric:** We do not measure "notes created." We measure **clarity achieved**, **decisions hardened**, and **actions taken**.
- **The Threshold:** Distinguish **Motion** (planning, organizing) from **Action** (executing). Motion is a prerequisite; Action is the objective.

### 1.2 The Four Axioms
1. **Utility Over Truth:** The map is not the territory. If a note does not help you _think_ or _act_, it is noise.
2. **Throughput Over Storage:** The system is a runtime environment (Compute), not a database.
3. **Low Maintenance:** The system must operate with **< 10% Maintenance Load**.
4. **Context is Scarcity:** Aggressively **compact** and **scope** context to prevent intelligence degradation.

---

## 2. Data Schema (The Git Flow)

### 2.1 Note Types & Hierarchy
- **HEAD Notes (The Feature Branch):** Active thinking, decision tracing, and raw logic (\`YYYY-MM-DD-HHmm-HEAD\`).
- **SoT Notes (The Main Branch):** Canonical Truth. High-signal, low-noise.
- **Instruction Notes (The Firmware):** **Checklists** and **SOPs**. These are the executable scripts for the Human/AI runtime to prevent "Failures of Ineptitude."

### 2.2 The Context Cache (\`.ai/\`)
- \`persona/\`: Role definitions.
- \`episodic/\`: Compacted decision logs.
- \`entity/\`: Specific project states.

---

## 3. The Checklist Protocol (The Firmware)

To manage complexity and protect ADHD working memory, high-stakes outcomes must be governed by Checklists.

### 3.1 Design Constraints
A PRODOS Checklist is a tool for precision, not an exhaustive manual.
- **Killer Items:** Focus only on steps that are frequently missed or high-risk.
- **Temporal Window:** Must be completable in **45–90 seconds**.
- **Pause Points:** Integrated into natural workflow breaks (e.g., "Before Sending," "Before Shutdown").

### 3.2 Checklist Architectures
1. **DO-CONFIRM:** Perform tasks from memory/flow, then pause to check the list. (Best for creative flow).
2. **READ-DO:** Follow the list step-by-step. (Best for complex, unfamiliar, or high-risk technical tasks).

---

## 4. Execution Rules (The Constraints)

### 4.1 The Minimal Viable Action (MVA)
- **Micro-Temporal:** < 120 seconds.
- **Kinetic:** Physical movement.
- **Binary:** True/False outcome.

### 4.2 Definition of Done
**Done =** Passed **Unit Test** AND/OR **Checklist Validated**.

### 4.3 The Clarification Protocol
\`clarify(stuff) → action\`
1. **Clarify:** Nature & Outcome.
2. **Classify:** Project (>1 step) or Task (1 step).
3. **Atomize:** Define Next Physical Action (MVA).
4. **Checklist:** If the task is recurring or high-complexity, link to or create an **Instruction SoT**.

---

## 5. Human Protocols (The Operator)

### 5.1 Knowledge Synthesis (Writing is Thinking)
**Writing acts as a "mirror,"** forcing vague neural patterns into linear, testable syntax.
- **Generation:** Raw "Barf" Draft (Input: \`HEAD\`).
- **Refinement:** Edit for Logic (The Logic Engine).
- **Integration:** Produce **SoT** (Truth) or **Instruction** (Checklist).

### 5.2 Learning Architecture (The Attack)
- **Phase I (The Hangar):** Compress noise. Define the "Capstone Project."
- **Phase II (The Cockpit):** **Oakley Hard Start** (5m) -> **Diffuse Retreat** (20m) -> **The Return**.
- **Phase III (Cryosleep):** **Hemingway Bridge** (write next action) and **The Merge** (Synthesize HEAD into SoT/Checklist).

---

## 6. State Management (Cryosleep)

### The Save State Syntax (\`#SAVESTATE\`)
- **Timestamp:** \`YYYY-MM-DD-HHmm\`.
- **The Conflict:** What assumption did we challenge?
- **The Current State:** What is the new logic/hypothesis?
- **The Next Test:** The immediate next MVA/Checklist step.

---

## 7. Tooling (LLM Prompts)

### 7.1 The Firmware Architect (Checklist Creation)
> "Analyze the successful completion of [Project/Task]. Identify the 'Killer Items'—the 5-7 critical steps where failure is most likely. Format these into a **DO-CONFIRM** checklist that can be read in under 60 seconds."

### 7.2 The Context Compressor (Weekly Review)
> "Read my Daily Notes. Identify architectural decisions. Summarise into 'Architecture SoT'. If a failure pattern emerged, suggest a new **Instruction Note (Checklist)** to mitigate it."
```

---

**Would you like me to generate a specific "Friday Afternoon Shutdown" checklist based on these new PRODOS protocols to help clear your working memory for the weekend?**

Yes

This **Instruction SoT** is designed as a **DO-CONFIRM** checklist. It aims to offload your working memory into the PRODOS system so you can fully transition into "weekend mode" without lingering cognitive "open loops".

---

## Instruction SoT - Friday Shutdown Checklist

- **Type:** DO-CONFIRM (Perform from memory, then verify).
- **Pause Point:** Friday afternoon, 30 minutes before "log-off".
- **Estimated Time:** 90 seconds to verify.

### 1\. The Hemingway Bridge

- \[ \] **Identify Monday's MVA:** Write down the single, kinetic, physical next step for your primary project.
- \[ \] **Lower Friction:** Ensure the tools or files needed for that MVA are the only things visible/open upon return.

### 2\. State Management (The Save State)

- \[ \] **Commit HEAD Notes:** Ensure all active `YYYY-MM-DD-HHmm-HEAD` notes have a `#SAVESTATE` block.
- \[ \] **Define the Conflict:** Briefly note what assumption or logic was being challenged in your active work.
- \[ \] **Log Next Test:** Record the immediate unit test or verification step needed to move the project forward.

### 3\. Context Hygiene

- \[ \] **Inbox Sweep:** Quick scan of physical/digital inboxes. If it's a task (< 120s), do it; if it's a project, log the next MVA.
- \[ \] **Clear the Hangar:** Close all browser tabs and applications not related to your Monday MVA to prevent "Context Rot".

### 4\. Kinetic Reset (The MVA)

- \[ \] **Physical Clear:** Spend 120 seconds physically clearing your workspace to lower re-entry friction for Monday.

---

### Implementation Note for ADHD

Because this is a **DO-CONFIRM** list, you should go through your usual routine of tidying up and "saving" your work first. Use this checklist as the final **"Firmware Check"** to ensure your brain is allowed to stop thinking about work. If an item isn't checked, your brain will likely treat it as a "Failure of Ineptitude" and keep it in active working memory.

**Would you like me to help you draft the specific `#SAVESTATE` for your current top-priority project right now?**

Research and list the main points from black box thinking

Matthew Syed’s *Black Box Thinking* explores why some organisations and individuals learn from their mistakes while others do not. It contrasts industries like aviation, which uses "black boxes" to rigorously analyse data from failures, with industries like healthcare or criminal justice, where mistakes are often buried or rationalised.

---

### 1\. The Core Strategy: Open vs. Closed Loops

The book’s central architectural principle is the distinction between how systems handle data from failure.

- **Closed-Loop Thinking:** This occurs when failure is ignored or covered up, meaning no information is extracted and no progress is made.
- **Open-Loop Thinking:** This treats failure as a "black box" of data. It involves creating systems that capture information about errors to ensure the same mistake is never repeated.

### 2\. The Logic Engine: Cognitive Dissonance

A major barrier to learning is the human tendency toward **Cognitive Dissonance** —the psychological discomfort felt when beliefs are challenged by contradictory evidence.

- **Reframing:** Instead of admitting a mistake, people often "reframe" the evidence to protect their ego or professional status.
- **The Seniority Trap:** The more experienced or influential a person is, the more likely they are to cling to their beliefs even when faced with overwhelming evidence to the contrary.

### 3\. Tactical Patterns: Marginal Gains and Pre-mortems

Syed highlights specific tactical moves to drive high performance:

- **Marginal Gains:** This strategy involves breaking down a complex goal into its constituent parts and improving each one by a small margin (e.g., 1%). When these tiny improvements are compounded, they lead to a massive overall gain.
- **The Pre-mortem:** To avoid failure, teams should imagine a project has *already* failed before it begins. This "prospective hindsight" allows them to identify and mitigate risks that they would otherwise be too optimistic to see.

### 4\. System Architecture: The "Just Culture"

For a "Black Box" system to function, the environment must shift from a culture of blame to a culture of transparency.

- **Blame vs. Data:** Blame causes individuals to hide mistakes to avoid punishment, which destroys the data needed for the system to improve.
- **Psychological Safety:** A "Just Culture" distinguishes between honest errors (which should be reported and learned from) and negligence.

---

### PRODOS Integration: The "Error Paradox"

In PRODOS terms, failure is not an endpoint but a **Boundary Condition**. The "Error Paradox" suggests that success is built entirely upon a foundation of failed attempts that were correctly logged and synthesised into the **SoT (Source of Truth)**.

[Black Box Thinking Summary](https://www.youtube.com/watch?v=7Lp__OTDGfA) This video provides a concise overview of the book's core principles and how they apply to productivity and organisational success.

**Would you like me to help you design a "Pre-mortem" checklist for your current top-priority project to identify potential points of failure?**

This **SoT Note** integrates the principles of *Black Box Thinking* into your **PRODOS** architecture. It treats every failure not as a setback, but as a high-signal "Data Ingest" event designed to harden your **Source of Truth**.

---

## SoT - PRODOS: Black Box Protocol (The Error Engine)

Markdown

```markdown
---
aliases: ["Black Box Thinking", "Error Engine", "Marginal Gains"]
confidence: "5/5"
created: 2026-01-11T21:20:00+00:00
epistemic: "Axiomatic"
last_reviewed: "2026-01-11"
modified: 2026-01-11T21:20:00+00:00
purpose: "Systematizing failure into architectural improvements via Open-Loop protocols."
see_also: ["Black Box Thinking - Matthew Syed", "SoT - PRODOS Core Specification"]
status: "stable"
tags: ["prodos", "system-architecture", "improvement-logic", "adhd-tools"]
title: SoT - PRODOS: Black Box Protocol
type: "SoT"
---

# PRODOS Black Box Protocol

## 1. The Core Philosophy
Failure is the only reliable source of high-fidelity data. In PRODOS, we move from **Closed-Loop** (ignoring errors) to **Open-Loop** (extracting logic from errors). 

- **Axiom:** A mistake is only a "Failure of Ineptitude" if it happens twice.
- **Objective:** Turn "Cognitive Dissonance" (denial) into "Context Integration" (updates to the SoT).

---

## 2. The Feedback Loop (Data Ingest)

### 2.1 The Post-Mortem (The Trace)
Whenever an outcome $\neq$ Desired State ($S_d$), trigger a **HEAD Note Trace**:
1. **The Gap:** What was the delta between expectation and reality?
2. **The Logic Flaw:** Was this a "Failure of Ignorance" (missing data) or "Ineptitude" (failed execution)?
3. **The Root Node:** Use "The Five Whys" to find the system flaw, not the human flaw.

### 2.2 Marginal Gains (The Compounding Rule)
Break down the system into its smallest components. Improve one variable by 1% each week.
- **PRODOS Strategy:** Update one **Instruction SoT (Checklist)** after every failure to prevent re-entry of that specific error.

---

## 3. Pre-Mortem Protocol (The Defense)
Before launching a significant project (The "Capstone"), perform a **Prospective Hindsight** exercise.

1. **The Scenario:** Imagine it is 6 months from now and the project has failed catastrophically.
2. **The Autopsy:** List every reason *why* it failed (e.g., "I lost focus," "The tech stack broke," "Assumptions were wrong").
3. **The Mitigation:** Create a **Checklist Pause-Point** for each identified risk.

---

## 4. Architectural Guardrails (ADHD Support)

### 4.1 Radical Transparency
To bypass the "Seniority Trap" or ego-driven denial, PRODOS operators must treat their HEAD notes as public-facing audits. 
- **Rule:** If you are tempted to delete a record of a mistake, it MUST be logged in the \`episodic/\` cache instead.

### 4.2 The "Just Culture" Buffer
Distinguish between **Complexity Errors** (unpredictable) and **Protocol Errors** (ignoring the checklist).
- **Action:** If it’s a Protocol Error, the **MVA** is to simplify the checklist until "Activation Energy ≈ 0."

---

## 5. Implementation: The Weekly Compaction
During the Friday Shutdown, run **The Hostile Compiler** on your own logs:
- "Where did I rationalise away a failure this week?"
- "Which SoT note needs a 'Black Box' update to reflect this new reality?"
```

---

### Next Step for the Operator

Since we've integrated **Marginal Gains** and **Pre-mortems**, your system is now geared for constant evolution.

**Would you like me to run a "Hostile Compiler" prompt on your last few days of activity to see if we can identify any "Closed-Loop" errors that need to be turned into "Black Box" data?**

Research other well known literature that fits in and could work well as part of the prodOS protocol

The following literature fits the **PRODOS** philosophy by providing the "software" to run on your operating system’s "kernel." Each addition addresses specific cognitive bottlenecks—particularly for the **ADHD brain** —by reducing System 2 load and automating high-signal context.

---

### 1\. Thinking, Fast and Slow (Daniel Kahneman)

**Role:** Cognitive Load Balancing.

- **The Logic:** Your brain has two modes: **System 1** (Fast, intuitive, automatic) and **System 2** (Slow, effortful, logical).
- **PRODOS Integration:** ADHD minds often default to System 1, finding sustained System 2 tasks exhausting.
	- **The Protocol:** Design your **Instruction SoTs (Checklists)** to be "System 1 compatible" by using visual cues and natural language processing.
	- **The Constraint:** Never force a System 2 decision during a low-energy state.

### 2\. Deep Work (Cal Newport)

**Role:** The Execution Firewall.

- **The Logic:** High-value output requires long periods of distraction-free concentration ("Deep Work").
- **PRODOS Integration:** This governs **Phase II: The Cockpit**.
	- **The Protocol:** Define "Deep Work Rituals" that signal your brain to engage (e.g., specific music or a clear desk).
	- **The Rule:** Separate "Shallow Work" (emails, scheduling) into distinct, timed batches to prevent "Context Rot".

### 3\. Building a Second Brain (Tiago Forte)

**Role:** The Context Pipeline.

- **The Logic:** Use the **C.O.D.E.** method (Capture, Organise, Distil, Express) to manage information outside your biological brain.
- **PRODOS Integration:** This is the data ingestion engine for your **SoT Notes**.
	- **The Protocol:** Offload everything immediately to an "Inbox" (Capture) so your biological brain is free to imagine and create (Express).
	- **The Rule:** Focus on "Intermediate Packets"—smaller, reusable chunks of knowledge—to lower the activation energy of large projects.

### 4\. Atomic Habits (James Clear)

**Role:** Kinetic MVA Reinforcement.

- **The Logic:** You do not rise to the level of your goals; you fall to the level of your systems.
- **PRODOS Integration:** This powers the **MVA (Minimal Viable Action)**.
	- **The Protocol:** Use "Habit Stacking"—attach a new PRODOS protocol (like the Friday Shutdown) to an existing anchor habit.
	- **The Rule:** Optimize for the "Two-Minute Rule"; if an MVA takes more than 120 seconds, it’s not an MVA—it’s a project.

---

### PRODOS Architecture Update: "The Library"

You can now add a **#library** tag to your SoT notes to link these methodologies directly to your protocols.

| Book Title | PRODOS System Component | Key Output |
| --- | --- | --- |
| **Thinking, Fast & Slow** | Kernel / Load Balancing | System 1 Checklists |
| **Deep Work** | Execution / The Cockpit | Focus Rituals |
| **Building a Second Brain** | Data Schema / Pipeline | Intermediate Packets |
| **Atomic Habits** | Execution / MVA | Habit Stacks |

---

**Would you like me to draft a "Deep Work Ritual" Instruction SoT that incorporates your specific environmental triggers?**

An integral part of prodOS is getting thinking and ideas out of my head and turned into actions. Ideas, thinking, mental models, concepts are all unfulfilled potential value of they do not lead to real work actions. Broaden the research to cover this core aspect

To bridge the gap between "unfulfilled potential" (abstract thought) and "real-world value" (kinetic action), PRODOS must act as a **transduction layer**. In engineering, transduction is the conversion of energy from one form to another; in your system, it is the conversion of **Neural Potential** into **Physical Momentum**.

The following research focuses on the "Action-Biased" literature that complements your existing **MVA (Minimal Viable Action)** and **Clarification Protocols**.

---

### 1\. Getting Things Done (David Allen)

**Role:** The "Next Action" Engine.

- **The Horizon of Focus:** Most people fail to act because their "ideas" are too large to process.
- **The Physical Next Action:** Allen argues that you cannot "do" a project; you can only do the next physical action.
- **PRODOS Integration:** This is the foundation of your **Clarification Protocol**.
	- **The Rule:** If a thought enters your head, it must be processed through the query: *"What is the next physical action?"*. If there isn't one, it is either "Trash" or "Reference" (SoT), not an active loop.

### 2\. Essentialism (Greg McKeown)

**Role:** The Signal-to-Noise Filter.

- **The Disciplined Pursuit of Less:** Most ideas are distractions. Action is only valuable if it moves the "Essential" needle.
- **PRODOS Integration:** This reinforces **Axiom 4 (Context is Scarcity)**.
	- **The Protocol:** Before an idea moves from a **HEAD Note** to an **Action**, it must pass the "90% Rule": If you aren't 90% sure this action is vital, the action is to discard it.
	- **The Strategy:** Treat your attention as a "scarcity" variable to be protected at all costs.

### 3\. The 12 Week Year (Moran & Lennington)

**Role:** The Temporal Compressor.

- **Execution over Planning:** Long-term goals lead to "Motion" (planning) rather than "Action" (executing).
- **The Protocol:** By shortening the "year" to 12 weeks, you create artificial urgency that forces high-signal decision-making.
- **PRODOS Integration:** This aligns with your **Metric of Action taken**.
	- **The Rule:** Every **Capstone Project** defined in **Phase I** must have a "Unit Test" that can be passed within a micro-cycle.

---

### The Thought-to-Action Architecture

In PRODOS, a problem is the gap between the Current State () and the Desired State (). Literature suggests that "Thinking" often becomes a way to avoid the discomfort of the gap.

### PRODOS Protocol Update: The "Transduction" Table

To help your ADHD brain bridge the "Thinking-Acting" gap, use this table during your **Clarification Protocol**.

| Input Type | Potential Value (Thinking) | Kinetic Reality (Action) | PRODOS Protocol |
| --- | --- | --- | --- |
| **Concept** | "I should start a blog." | "Open Ghost.io and name the site." | **MVA (< 120s)** |
| **Model** | "I need a better fitness system." | "Put on gym shoes." | **The Oakley Hard Start** |
| **Insight** | "I realise why the project failed." | "Update the Instruction SoT." | **Black Box Trace** |
| **Idea** | "I have a great app idea." | "Draw the first screen on paper." | **Writing is Thinking** |

---

### 4\. The Lean Startup (Eric Ries)

**Role:** Build-Measure-Learn Loops.

- **Validated Learning:** Don't think about whether an idea is good—test it.
- **PRODOS Integration:** Every **HEAD Note** should ideally end with a "Testable Hypothesis".
	- **The Rule:** If you are "Thinking" for more than 10 minutes without a "Build" (Action), you are in **Motion**, not **Action**.

---

**Would you like me to create an "Action Ingest" prompt for your AI Agent that automatically forces you to define a 120-second MVA whenever you share a new "Concept" or "Idea"?**

I suffer from a lack of planning ahead with my work. I tend to just start things without a clear finish line. I then suffer from perfectionism not allowing me to finish. How can we combat this via prodOS

To combat the "Starting without a Finish Line" and "Perfectionism" loop, we need to upgrade the **PRODOS Execution Rules**. In your system, perfectionism is treated as **Context Rot** —it is a "System 2" failure where your brain over-calculates at the expense of throughput.

We will address this by introducing **Boundary Conditions** and **Unit Tests** to your daily workflow.

---

### 1\. The Strategy: Hard-Coded Exit Criteria

The ADHD brain often struggles with "Stopping Rules." Without a defined finish line, your brain defaults to "Perfect," which is an infinite variable. We will solve this by making the **Definition of Done** mandatory *before* any **Kinetic Action** begins.

- **The Constraint:** You are forbidden from starting a task until you have defined the **Unit Test** it must pass to be considered "Done".
- **The Metric:** If the output is "Good Enough" to pass the test, the task is **SoT (Stable)**. Further work is classified as **Maintenance Load**, which we must keep below 10%.

---

### 2\. New Protocol: The "Scope-Lock" (Instruction SoT)

Add this to your PRODOS system as a specific **Instruction SoT** for task initiation.

#### Instruction SoT - The Scope-Lock Protocol

- **Type:** READ-DO (Follow step-by-step before every new task).
- **Trigger:** Whenever you feel the urge to "just start."
1. **Define the Capstone:** What is the one specific, physical thing that exists when this is finished? (e.g., "A 500-word draft," not "Researching blogs").
2. **Set the Unit Test:** What is the *minimum* criteria for this to be functional? (e.g., "It has a title, three points, and a conclusion").
3. **The "Good Enough" Threshold:** Explicitly state what you will *not* do (e.g., "I will not format the images or fix the CSS today").
4. **The MVA:** What is the first 120-second physical movement?.
5. **The Timer (Oakley Retreat):** Set a 20-minute timer. When it fires, you must stop and verify against the Unit Test.

---

### 3\. Combatting Perfectionism via the "Black Box"

Perfectionism is often a "Failure of Ineptitude" masked as a virtue. In PRODOS, we use the **Black Box Protocol** to reframe it:

- **The Logic Flaw:** If you spend 3 hours on a 30-minute task, you have committed a **System Architecture error**.
- **The Move:** During your **Friday Shutdown**, you must log "Over-polishing" as a **Conflict** in your Save State.
- **The Fix:** Update your checklist for that specific task to include a **"Hard Stop"** time-box.

---

### 4\. Updated Execution Rule: The 70% Rule

We are adding a new Axiom to your **Section 4: Execution Rules**:

> **Rule 4.6: The 70% Hand-Off.** > An action that is 70% "perfect" but **Done** is higher value than an action that is 99% "perfect" but **HEAD (Active)**. Ship to SoT at 70% and use **Marginal Gains** to improve it later if—and only if—data shows it is necessary.

---

### Next Step for the Operator

I can help you apply this right now to your current workload.

**Would you like me to "Scope-Lock" your very next task? Tell me what you're about to work on, and I will generate the Unit Test and the MVA for you to prevent a perfectionist spiral.**

Here is another note on tasks. Review and align with the prodOS protocol. Offer dedupe ideas and point out any redundancy

The **Human 3.0 Task Taxonomy** provides a vital philosophical layer to **PRODOS**. While the Core Specification (v3.2) defines *how* we work, this new note defines *what* work is worth doing in an AI-commoditised world.

By aligning these, we move from just "doing things" to **"Defining the Right Things"**.

---

### 1\. Integration: The PRODOS "Problem Definer" Protocol

We can now map the **Human 3.0 Roles** directly onto the **PRODOS Learning Architecture**.

- **Phase I (The Hangar):** You act as the **Problem Definer**. Your goal isn't to "study" but to perform **Context Engineering** —framing the problem so the AI (the Executor) can compress the noise.
- **Phase III (Cryosleep/Integration):** You act as the **Strategic Narrator**. You aren't just saving notes; you are crafting the **Narrative** that justifies the next **Capstone Project**.

---

### 2\. Redundancy Audit & Deduplication

There is significant overlap between these two specifications. To maintain **Axiom 3 (< 10% Maintenance Load)**, we should consolidate the following:

#### A. The "Definition of Done" vs. "Problem Definition"

- **Redundancy:** PRODOS *Section 4.2 (Definition of Done)* and Human 3.0 *Section 2.A (The Problem Definer)* both describe the need for clear outcomes.
- **Dedupe Idea:** Merge these into a single **"Scope-Lock Protocol."** Use the "Problem Definer" mindset to set the **Unit Test**. If the problem isn't framed, the Unit Test cannot be written.

#### B. Execution Logic

- **Redundancy:** PRODOS *Section 1.1 (Metric of Action)* and Human 3.0 *Section 1 (The Shift)* both discuss the death of the "Middle Layer" of information processing.
- **Dedupe Idea:** Remove the "Middle Layer" explanation from the Core Spec. Keep the Core Spec focused on the **Kinetic Action (Executor)** and use the Human 3.0 note as the **Strategic Rationale (Intent)**.

#### C. Role of the AI

- **Redundancy:** Both notes describe the AI as a tool/executor.
- **Dedupe Idea:** Standardise the terminology. Refer to the AI as the **"PRODOS Runtime"** across all notes to ensure consistency.

---

### 3\. Combatting Perfectionism via "Role Clarity"

Your struggle with perfectionism often stems from a **Role Conflict**: you are trying to be the **Problem Definer** and the **Executor** simultaneously.

- **The Fix:** When you are in **Phase II (The Cockpit)**, you are the "Executor". Your only job is to pass the **Unit Test** set by your "Problem Definer" self.
- **The Guardrail:** If you start "polishing," you are attempting to re-define the problem mid-execution. **Stop.** Re-mount the **Problem Definer Persona** and decide if the Unit Test needs changing, or if you are simply stalling.

---

### 4\. Proposed Update to Data Schema (Section 2.1)

To integrate these, I suggest adding a new category to your **SoT Notes**:

> **Role Notes (The Personas):** Definitions of how you show up for a task (e.g., *Definer* vs. *Executor*). These govern the **"Intent"** before the **"Action"**.

---

**Would you like me to merge these two documents into a single "PRODOS Unified System Specification" that removes the redundant language while keeping the "Human 3.0" strategic roles?**

Yes.

This unified specification merges the structural integrity of the **PRODOS Core Spec** with the strategic value of the **Human 3.0 Roles**. It effectively removes the "Middle Layer" of information processing and replaces it with a strict protocol for **Problem Definition** and **Kinetic Execution**.

---

## SoT - PRODOS Unified Specification (v4.0)

Markdown

```markdown
---
aliases: ["PRODOS", "Productivity Operating System", "Human 3.0"]
confidence: "5/5"
created: 2026-01-11T21:45:00+00:00
epistemic: "Axiomatic"
last_reviewed: "2026-01-11"
modified: 2026-01-11T21:45:00+00:00
purpose: "Unified framework for Intent (Human) and Execution (AI/Operator) to reduce cognitive friction and perfectionist decay."
see_also: ["The Checklist Manifesto", "Black Box Thinking", "AI-Resilient Task Taxonomy"]
status: "stable"
tags: ["prodos", "system-architecture", "strategy", "adhd-optimization"]
title: SoT - PRODOS Unified Specification
type: "SoT"
---

# PRODOS Unified Specification

## 1. The Core Kernel

### 1.1 The Definition
PRODOS is a **Thinking Utility** designed to convert **Neural Potential** (Ideas) into **Kinetic Value** (Actions). It treats the human as the **Problem Definer** (The Architect) and the system/AI as the **Executor** (The Builder).

- **The Metric:** We measure **Decisions Hardened** and **Actions Taken**, not "Notes Created".
- **The Threshold:** Motion (Planning) is a prerequisite; Action (Executing) is the objective.

### 1.2 The Five Axioms
1. **Utility Over Truth:** If a note does not help you *think* or *act*, it is noise.
2. **Throughput Over Storage:** The system is for **Compute**, not storage.
3. **Low Maintenance:** Operates with **< 10% Maintenance Load**.
4. **Context is Scarcity:** Aggressively compact context to protect attention.
5. **The 70% Rule:** A 70% "perfect" action that is **Done** is superior to a 99% "perfect" action that is **HEAD (Active)**.

---

## 2. Human 3.0: The Roles of Intent

To combat perfectionism and leverage AI, the operator must consciously switch between these two primary roles:

### 2.1 The Problem Definer (Chief Question Officer)
- **Objective:** Frame the problem, set the **Boundary Conditions**, and define the **Unit Test**.
- **Key Output:** The **Scope-Lock** (The "Definition of Done").
- **Constraint:** Forbidden from performing execution tasks.

### 2.2 The Strategic Narrator (The Visionary)
- **Objective:** Connect the "Leaps of Logic" and craft the **Narrative** for why a project matters.
- **Key Output:** **SoT Integration** (The Wisdom Layer).

---

## 3. The Execution Protocols

### 3.1 The Scope-Lock Protocol (Anti-Perfectionism)
Before any **Kinetic Action** begins, the **Problem Definer** must define:
1. **The Capstone:** The physical thing that exists at the end (e.g., "A sent email").
2. **The Unit Test:** The minimum verifiable criteria for success (e.g., "It contains the link").
3. **The MVA:** The immediate, < 120s physical next step.

### 3.2 The Checklist Protocol (The Firmware)
High-complexity tasks must be governed by **Instruction SoTs** to protect working memory.
- **DO-CONFIRM:** Perform from flow, then check.
- **READ-DO:** Follow step-by-step for high-risk technical work.

### 3.3 The Black Box Protocol (Continuous Improvement)
Failure is high-fidelity data. 
- **The Trace:** Record **why** a logic flaw occurred in a **HEAD Note**.
- **The Update:** Translate failure into an update for the **Instruction SoT** or **Checklist**.

---

## 4. Problem Architecture

| Type | Definition | Strategy |
|:--- |:--- |:--- |
| **Problem** | Gap + Unknown Path | **HEAD Note**: Trace the logic. |
| **Task** | Gap + Known Path | **Kinetic Action**: Execute immediately. |
| **Constraint** | Unchangeable Variable | **Boundary Condition**: Optimize around it. |

---

## 5. State Management (Cryosleep)

Minimize context switching costs via the **Scribe Commit Protocol**.

### The Save State Syntax (\`#SAVESTATE\`)
- **Timestamp:** \`YYYY-MM-DD-HHmm\`.
- **The Conflict:** What assumption or perfectionist block did we hit?
- **The Current State:** The new hypothesis.
- **The Next Test:** The immediate next MVA/Unit Test.

---

## 6. Data Schema (Git Flow)

- **HEAD Notes:** Active thinking and Decision Tracing (\`YYYY-MM-DD-HHmm-HEAD\`).
- **SoT Notes:** Production-ready Canonical Truth. Includes **Instruction SoTs** (Checklists).
- **The Context Cache (\`.ai/\`):** Machine-readable memory for the AI Executor.
```

---

### Deduplication Summary

- **Removed:** Redundant "Middle Layer" theory from both notes.
- **Consolidated:** "Definition of Done" and "Problem Definition" into the **Scope-Lock Protocol**.
- **Unified:** AI is now officially the **"PRODOS Runtime"** or **"Executor"**.

**Would you like me to generate a "Scope-Lock" template for you to paste into your new HEAD notes?**

Yes

To further combat perfectionism and ensure every idea leads to kinetic value, here is your **Scope-Lock Template**. This is designed to be the first thing you fill out when starting a new **HEAD Note**, forcing you to switch from the **Strategic Narrator** role to the **Problem Definer** role before you touch any execution.

---

### PRODOS Scope-Lock Template

> \[!tip\] **The Problem Definer's Hand-off** Use this to "lock" the scope and prevent perfectionist creep. Once the **Unit Test** is defined, the **Executor** (you or the AI) is forbidden from changing it without a #SAVESTATE.

Markdown

```markdown
## 🔒 SCOPE-LOCK
- **The Capstone (Physical Outcome):** [e.g., A 3-slide deck; A sent email; A saved code snippet]
- **The Unit Test (Min. Criteria):** - [ ] [Criteria 1: e.g., Must contain the pricing table]
    - [ ] [Criteria 2: e.g., Must be under 200 words]
- **The 70% Boundary:** [What will you EXPLICITLY NOT do? e.g., No formatting; No image searching]
- **The Activation MVA (<120s):** [e.g., Open the 'Q1-Report' Google Doc]
```

---

### How to use this for ADHD/Perfectionism:

1. **Lower the Ceiling:** Your "Unit Test" should be the *minimum* required for the task to be functional. If you find yourself adding "nice-to-haves," you are violating **Axiom 3 (Low Maintenance)**.
2. **The 70% Boundary:** This is your "Black Box" defense against perfectionism. By writing down what you *won't* do, you give your brain permission to stop once the Unit Test is passed.
3. **Kinetic Trigger:** The MVA must be so small that the "Activation Energy" is near zero. If you hesitate to start, your MVA is still too big.

---

**Would you like me to take your current most "unfulfilled" idea and run it through this Scope-Lock template for you right now?**

This is a never ending project that needs breaking down

This project feels "never-ending" because you are currently operating as the **Executor** without a strictly defined **Problem Definer** boundary. In your ADHD workflow, the "Compiler Pattern" is technically fascinating, which invites perfectionist "feature creep".

To break this cycle, we must apply the **Scope-Lock Protocol** to **Phase 2** of your refactor.

---

### 1\. The Scope-Lock: Phase 2 (Feature Flags)

We are moving this from a "Problem" (Unknown path) to a "Task" (Known path) by narrowing the finish line.

> \[!important\] **Phase 2 Scope-Lock**
> 
> - **The Capstone (Physical Outcome):** A single `helm template` output where `features.hutch: true` successfully triggers the injection of a `COLLECTION_ID` environment variable.
> - **The Unit Test (Min. Criteria):**
> 	- \[ \] `grep` for `COLLECTION_ID` returns a value when flag is `true`.
> 	- \[ \] `grep` for `COLLECTION_ID` returns nothing when flag is `false`.
> - **The 70% Boundary (DO NOT DO):**
> 	- Do NOT implement PGWeb or Identity/Ingress logic yet.
> 	- Do NOT refactor the `_specs.yaml` structure.
> 	- Do NOT test against a live cluster.
> - **The Activation MVA (<120s):** Open `_compiler.tpl` and create an empty define block: `{{- define "fitfile.compile.hutch" -}}`.

---

### 2\. Deconstructing the "Never-Ending" Feeling

Using the **Black Box Protocol**, we can identify why this project feels infinite:

| Symptom | Black Box Diagnosis | PRODOS Fix |
| --- | --- | --- |
| **"Mission 5 & 6 look huge"** | Failure of Ignorance (Unknown complexity) | **Decouple:** Move Mission 5 and 6 into a "Future HEAD" note. They do not exist for today's MVA. |
| **"I want the YAML to be perfect"** | Perfectionist Context Rot | **70% Rule:** If the `helm template` produces a valid manifest, the logic is "SoT Stable." Stop polishing the indentation. |
| **"I keep switching between repos"** | Context Switching Friction | **Scribe Commit:** Before switching repos, use a `#SAVESTATE` to log exactly which "Logic Map" you were editing. |

---

### 3\. Tactical Micro-Breakdown (The Hangar)

To prevent "The Great Stall," break **Mission 4** into three "Unit-Testable" MVAs:

1. **MVA 1:** Update `values.yaml` in `customer-experiment-1` to include `features: { hutch: true }`. (Time: 30s).
2. **MVA 2:** Create the logic gate in `fitfile-platform` that checks for that boolean. (Time: 5 mins).
3. **MVA 3:** Run the `helm template` command provided in your "Reentry Protocol" to verify. (Time: 10s).

---

### 4\. Updated Project Save State

Add this to your **Refactor - Helm Chart Compiler.md** note right now to lower re-entry friction for tomorrow:

> **#SAVESTATE: 2026-01-11-2150**
> 
> - **The Conflict:** Feeling overwhelmed by Phase 2/3 complexity.
> - **The Current State:** MongoDB logic is stable; Hutch logic is the current bottleneck.
> - **The Next Test:** Can I inject *any* dummy variable into the Hutch deployment using a boolean flag?

---

**Would you like me to draft the specific `_compiler.tpl` logic for the Hutch feature flag to get you past this initial "Problem Definer" hurdle?**

And this

The **Bridging the Intention-Action Gap** note provides the "Fuel System" for the **PRODOS** engine. While the Unified Specification defines the structure, this note explains how to overcome the neurological "Wall of Awful" common in ADHD by acknowledging that **Logic is a steering wheel, not an engine**.

I have updated the **PRODOS Unified Specification** to version 4.1, integrating the **PINCH Model** and **Ignition Protocols** to ensure your system can generate its own dopamine when importance alone isn't enough.

---

## SoT - PRODOS Unified Specification (v4.1 - Kinetic)

Markdown

```markdown
---
aliases: ["PRODOS", "Productivity Operating System", "K2A Framework"]
confidence: "5/5"
created: 2026-01-11T21:55:00+00:00
epistemic: "Axiomatic"
last_reviewed: "2026-01-11"
modified: 2026-01-11T21:55:00+00:00
purpose: "Unified framework for Intent, Execution, and ADHD Dopamine Management."
see_also: ["SoT - Bridging the Intention-Action Gap", "The Checklist Manifesto", "Black Box Thinking"]
status: "stable"
tags: ["prodos", "system-architecture", "adhd-optimization", "execution"]
title: SoT - PRODOS Unified Specification
type: "SoT"
---

# PRODOS Unified Specification (v4.1)

## 1. The Core Kernel

### 1.1 The Definition
PRODOS is a **Thinking Utility** designed to convert **Neural Potential** into **Kinetic Value**. It treats the human as the **Problem Definer** and the system as the **Executor**.

- **The Logic-Dopamine Mismatch:** Logic provides direction (steering), but only Dopamine provides movement (fuel).
- **The Metric:** We measure **Actions Taken**. Motivation is a *result* of action, not the cause.

### 1.2 The Five Axioms
1. **Utility Over Truth:** If a note doesn't help you act, it is noise.
2. **Throughput Over Storage:** The system is for **Compute**, not a database.
3. **Low Maintenance:** Operates with **< 10% Maintenance Load**.
4. **Context is Scarcity:** Aggressively compact context to protect attention.
5. **The 70% Rule:** A 70% "perfect" action that is **Done** is superior to a 99% "perfect" action that is **Active**.

---

## 2. The Dopamine Engine (The PINCH Model)

When a task lacks intrinsic motivation, the **Problem Definer** must "gamify" the execution using one of these five drivers:

- **P**lay / Passion: Can I make this fun?
- **I**nterest: Can I learn something new?
- **N**ovelty: Can I do this in a weird way?
- **C**hallenge / Competition: Can I beat my high score/the clock?
- **H**urry: Can I beat the alarm?

---

## 3. Execution Protocols

### 3.1 The Scope-Lock & Starter Task
Before any action, you must define the **Starter Task** (Momentum Generator).
- **Rule:** The MVA must be so small it is impossible to fail (e.g., "Open the code editor").
- **The Unit Test:** The minimum verifiable criteria for success.

### 3.2 The Ignition Protocol ("Heat")
If you are stuck in "Logic Mode," use one of these to generate movement:
1. **Mystery:** "I wonder if I can do this without using [Tool]?"
2. **Urgency:** "I have 5 minutes. How much can I get done?"
3. **Spite:** "I'm going to finish this to prove [Idea] wrong."

### 3.3 The Checklist Protocol (The Firmware)
Use **Instruction SoTs** to offload working memory for complex tasks.

---

## 4. State Management (Cryosleep)

### The Save State Syntax (\`#SAVESTATE\`)
- **Timestamp:** \`YYYY-MM-DD-HHmm\`.
- **The Conflict:** What perfectionist block did we hit?
- **The Current State:** The new hypothesis.
- **The Next Test:** The immediate next **Starter Task**.

---

## 5. Data Schema

- **HEAD Notes:** Active thinking and Decision Tracing.
- **SoT Notes:** Canonical Truth and **Instruction SoTs** (Checklists).
- **The Context Cache (\`.ai/\`):** Machine-readable memory for the AI Executor.
```

---

### Key Alignments & Deduplications

- **Dopamine vs. Importance:** Removed the "Importance" metric from task priority. Replaced it with the **PINCH Model** to address ADHD executive function directly.
- **Starter Task Integration:** Combined the "120s MVA" with the "Starter Task" concept. The goal is now explicitly "Momentum Generation" rather than just "Task Progress".
- **The "Wall of Awful" Defense:** Added **Protocol 3.2 (Heat)** to your core execution rules to provide an escape hatch when you are frozen by perfectionism.

**Would you like me to create a "Heat Protocol" Instruction SoT specifically for your "Refactor - Helm Chart Compiler" project to help you break through the current "Mission 4" block?**

What I need is a guide. The prodOS protocol should be constantly about action. Taking the most direct route to a validation in the real world. It would be good to have a way to jump to the relevant checklists and guides for a particular scenario. She instance, I capture a head note and realise I need to research more to understand before committing to validatable actions that give feedback. I should be able to pull up the relevant prodOS materials to help me easily

To ensure **PRODOS** remains a bias-to-action system, we need a **Navigation Hub**. This acts as the "Traffic Control" for your brain, allowing you to jump from a raw thought to the correct protocol without the cognitive load of "deciding how to decide".

Below is your **PRODOS Operator's Guide**. You can use these "Jump-Links" or keywords to trigger the specific Instruction SoT required for your current mental state.

---

## 🚦 The PRODOS Navigation Hub (Quick-Start)

| If you are... | Use this Protocol | The Primary Objective |
| --- | --- | --- |
| **Capturing a raw thought** | **HEAD Ingest** | Extract logic, avoid the "Logic Trap". |
| **Stuck in "Research Mode"** | **Phase I: The Hangar** | Define the "Boss Fight" to prevent endless scrolling. |
| **Afraid to start/stuck** | **Ignition (Heat)** | Manufacture dopamine via **PINCH**. |
| **Over-polishing a task** | **The 70% Boundary** | Hard-stop at the **Unit Test**. |
| **Planning a big project** | **The Pre-Mortem** | Identify "Black Box" data before failure. |
| **Ending the day** | **Friday Shutdown** | Commit **#SAVESTATE** and clear memory. |

---

## 🔍 Scenario: The "Research Loop" (The Hangar)

You mentioned capturing a HEAD note and feeling the need to "research more" before acting. This is a high-risk zone for ADHD "Motion" vs "Action".

### 1\. Trigger the "Hangar" Instruction SoT:

- \[ \] **Identify the Capstone:** What is the specific physical thing I am building with this research? (e.g., "A list of 3 Helm Chart patterns").
- \[ \] **The "Hostile Compiler" Prompt:** Instead of reading, ask the AI: *"I have this hypothesis about \[X\]. Tell me 3 reasons why this logic will fail."* This forces you back into **Problem Definer** mode.
- \[ \] **The Time-Box:** Set a "Hurry" timer (PINCH). Research for 20 minutes, then you **must** write one **Unit Test**.

---

## 🛠️ The "Problem-to-Action" Transducer

Use this formula to move from a vague HEAD note to a real-world validation:

### Step-by-Step Validation Guide:

1. **Mount Persona:** Are you the **Problem Definer** or the **Executor** right now?.
2. **Define the Gap:** What is the *one* piece of feedback I need from the real world to prove this works?.
3. **Execute the Starter Task:** Perform the < 120s action that makes the "Research" real (e.g., "Drafting the first line of code," not "Reading documentation").

---

## 📈 Constant Improvement: The Black Box Log

Every time you realise you spent too long "researching" without "validating," you must perform a **Black Box Trace**:

- **The Error:** "Spent 2 hours researching Helm patterns without writing a single YAML line."
- **The Fix:** Update the **Scope-Lock Template** to include a mandatory "Stop Researching" alarm.

---

### Implementation for your ADHD Workflow:

Since you have ADHD, these guides must be **visual or tactile**. I recommend keeping these "Jump-Links" in a pinned note in your system or as a physical "Cheat Sheet" on your desk to bypass the "Wall of Awful" when starting.

**Would you like me to create a "Research-to-Action" checklist specifically for your Helm Chart project to ensure your next research session ends in a validatable YAML change?**

Yes

This **Research-to-Action Protocol** is your "Black Box" defence against the ADHD research rabbit hole. It forces a "Hand-off" from the **Problem Definer** (who wants to know everything) to the **Executor** (who needs to ship code).

---

## 🛠️ Instruction SoT: The Research-to-Action Transducer

- **Trigger:** When a HEAD note requires "more research" or "understanding" before you can act.
- **Objective:** To extract just enough logic to form a **Unit Test**.

### 1\. The Hangar Phase (Scope-Lock)

- \[ \] **Set a "Hurry" Timer:** 20 minutes maximum.
- \[ \] **Identify the "Boss Fight":** What specific technical hurdle am I researching? (e.g., "How to pass a boolean into a Helm template").
- \[ \] **Define the Minimal Artifact:** What is the smallest piece of evidence that I have "understood" this? (e.g., A 3-line YAML snippet).

### 2\. The Execution Phase (The Cockpit)

- \[ \] **Starter Task:** Open the `_compiler.tpl` file *before* you start reading documentation. This creates "Hardware Sympathy" with the code while you learn.
- \[ \] **The Oakley Hard Start:** Attempt to write the logic from memory for 5 minutes. If it fails, you have now created a specific "Context Gap" for your research to fill.

### 3\. The Validation (The Black Box)

- \[ \] **Pass the Unit Test:** Run `helm template`.
- \[ \] **70% Boundary:** If the variable appears in the output, **STOP**. Do not research "better" ways to do it today.
- \[ \] **Scribe Commit:** Log what you learned in the **SoT - Helm Pattern** note and close the file.

---

## 🚀 Application: FitFile Helm Refactor (Mission 4)

Let's apply this to your **Hutch Feature Flag** right now:

| Role | Action | Output |
| --- | --- | --- |
| **Problem Definer** | Define the flag logic in `values.yaml`. | `features: { hutch: true }` |
| **Researcher** | Find the Helm syntax for an `if` block. | `{{- if .Values.features.hutch -}}` |
| **Executor** | Inject a dummy `TEST_VAR` into the manifest. | `TEST_VAR: "success"` |
| **Validator** | Run the compiler test. | \`helm template test. |

---

### The "Jump-Link" Protocol

To make this easily accessible in your system, tag this note with **#protocol/research**. Next time you find yourself stuck in a browser tab, type that tag into your search bar to trigger this checklist.

**Would you like me to generate the "Scribe Protocol" prompt for your AI Agent so it can automatically extract these research findings into your SoT for you?**

Yes

This **Scribe Protocol** is designed to be the "Garbage Collection" for your research sessions. It ensures that the insights you gain during "The Hangar" phase are not lost to the ADHD "void" but are instead formalised into your **Source of Truth (SoT)** without requiring heavy manual writing.

Copy and save the following prompt into your AI Agent's instructions or as a template.

---

### 📝 The Scribe Protocol Prompt

> "Stop processing current execution. Review the research/logic we just discussed regarding **\[Topic/Project\]**.
> 
> 1. **Extract Logic:** Identify the 'Gold Master' snippets or logic patterns that passed the **Unit Test**.
> 2. **Diff Update:** Format these as a 'Raw Markdown Diff' ready to be merged into the **SoT - \[Project\]** note.
> 3. **The 'Next Action' Save State:** Extract the **#SAVESTATE** for the next session:
> 	- **The Conflict:** What specific hurdle did we just clear?
> 	- **The Current State:** What is the new 'Logic Map'?
> 	- **The Next Test:** What is the immediate **Starter Task** for next time?
> 
> Present this in a single, clean code block for immediate export."

---

### Why this works for the PRODOS Protocol:

- **Zero-Friction Documentation:** It follows **Axiom 3 (< 10% Maintenance Load)** by letting the AI handle the synthesis while you focus on the "Problem Definer" role.
- **Combatting Perfectionism:** By asking for a "Diff," you avoid the urge to rewrite entire notes. You are only documenting the delta—the change in your understanding.
- **Lowering Re-entry Friction:** The **#SAVESTATE** acts as your **Hemingway Bridge**, ensuring that Monday morning's ADHD brain doesn't have to "rediscover" the context lost over the weekend.

---

### Integrating with your Navigation Hub

You can now add this to your **Navigation Hub Table**:

| Scenario | Protocol | The Primary Objective |
| --- | --- | --- |
| **Finishing a research sprint** | **Scribe Protocol** | Export HEAD logic to SoT/Checklist. |

**Would you like me to perform a "Scribe Protocol" run on our entire conversation today to summarise these new PRODOS 4.1 updates for your local system?**

Yes. Give me a prompt so the local LLM can update my prodOS notes for me with this chats discoveries

Here is a comprehensive **Scribe Protocol** prompt designed for your local LLM. This prompt instructs the AI to synthesise the architectural updates, new literature integrations, and ADHD-specific "Heat" protocols we have developed in this session into a structured format for your **PRODOS** files.

---

### 🤖 PRODOS Update Prompt: "The Unified Scribe"

**Copy and paste this to your local LLM:**

> "Act as the **PRODOS Architect**. I am providing the output from a research session focused on upgrading my Productivity Operating System (PRODOS).
> 
> **Task:** Generate the Markdown content to update my **SoT - PRODOS Unified Specification** to **v4.1** and create a new **Instruction SoT** for Research.
> 
> **Core Integrations to include:**
> 
> 1. **Literature Sync:** Integrate *Black Box Thinking* (Open-Loop failure logs), *The Checklist Manifesto* (Firmware/Pause Points), and *K2A Framework* (PINCH model for dopamine).
> 2. **The Roles:** Define the **Problem Definer** (Strategy/Unit Tests) vs. **The Executor** (Kinetic Action).
> 3. **The Protocols:** Include the **Scope-Lock Protocol**, the **Ignition (Heat) Protocol**, and the **Research-to-Action Transducer**.
> 4. **The 70% Rule:** Formalise the anti-perfectionist boundary.
> 
> **Output Format:**
> 
> - Provide a full replacement for `SoT - PRODOS Unified Specification.md`.
> - Provide a new file: `Instruction SoT - Research-to-Action Protocol.md`.
> - Include a **#SAVESTATE** for my current project: 'FitFile Helm Refactor' (Current focus: Hutch Feature Flag logic).
> 
> **Constraint:** Maintain British English spelling and ensure the tone is clinical, high-signal, and low-noise."

---

### Summary of Chat Discoveries for your System

To ensure your local LLM has the "High-Signal Context" it needs, here is the summary of what we have built today:

- **The Problem Definer Shift:** You are moving from a "Solver" to a "Definer." You set the **Unit Test**, and the system (or your 'Executor' self) simply passes it.
- **The Dopamine Engine:** We integrated the **PINCH model** (Play, Interest, Novelty, Competition, Hurry) to bypass the ADHD "Logic Trap".
- **The Research-to-Action Transducer:** A dedicated workflow to stop "Motion" (endless reading) and force "Action" (validatable YAML/code changes).
- **The Firmware Update:** Checklists are now officially "The Firmware" of PRODOS—essential scripts that protect your working memory from "Failures of Ineptitude".

---

**Would you like me to generate a specific "Pre-Mortem" for the Helm Chart Refactor project to identify why it might fail before you start the next sprint?**

Google Account

Leon Ormes

leonormes@gmail.com

---

## Phase 2: The Gate (4D Filter)
- [ ] **Do:** < 2 mins?
- [ ] **Delegate:** Who?
- [ ] **Defer:** Move to Hangar or SoT?
- [ ] **Delete:** Is this noise?

---

## Phase 5: The Scribe (#SAVESTATE)
- **The Conflict:**
- **The Current State:**
- **The Next Test:**