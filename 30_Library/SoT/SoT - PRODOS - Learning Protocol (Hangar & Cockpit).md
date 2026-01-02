---
status: ""
purpose: ""
modified: 2026-01-02T09:47:23+00:00
last_reviewed: ""
review_interval: ""
see_also: []
epistemic: "Hangar & Cockpit Methodology"
source_of_truth: ["[[SoT - PRODOS (System Architecture)]]", "[[SoT - The Extended Mind]]"]
aliases: ["Learning Protocol", "Hangar and Cockpit", "Learning Workflow"]
confidence: "Stable"
created: 2026-01-02T09:30:15+00:00
tags: ["prodos", "protocol", "learning", "adhd", "workflow"]
title: "Stage 4: The Cockpit (Execution)"
type: "SoT"
---

## 1. The Prime Directive

> [!definition] The Golden Rule of Learning
> **No Input without Output.**
> You are forbidden from "studying" (reading/watching) until you have defined the specific **Unit Test** (Code/Essay/Project) that requires that information.

---

## 2. The Practical Workflow: From Spark to Action

Follow this pipeline for every new interest.

### Stage 1: The Spark (Capture & Think)

*Status: `20_Thinking/21_Workbench` | Context: "I just found this cool thing!"*

1. **The Trigger:** You find a new library, language, or hobby.
2. **The Action:** Create a **HEAD Note** (`YYYY-MM-DD-HHmm-HEAD`).
    * *The Spark:* Write down *what* it is.
    * *The Tension:* Write down *why* it matters or what problem it solves.
    * *Tag:* Add `#interest` to the note.
3. **The Rule:** **STOP.** Do not install the tool. Do not watch the 3-hour tutorial.
    * *Why:* The HEAD note captures the context so your brain can let go. Prevents "Rabbit Holes."

### Stage 2: The Gate (Filtering)

*Status: `Weekly Review` | Context: "Do I actually care?"*

1. **The Ritual:** During your Weekly Review, query for `tag:#interest` in your Workbench.
2. **The Decision:**
    * **Kill:** "This was just a dopamine spike." -> Delete/Archive the HEAD note.
    * **Incubate:** "Not now, but later." -> Move HEAD note to `Someday/Maybe` (or link in a Someday MOC).
    * **Activate:** "I am ready to commit resources to this." -> **Move to Stage 3.**

### Stage 3: The Hangar (Chartering)

*Status: `10_Actions/11_Projects` | Context: "Building the Flight Plan"*

1. **Create the Project Note:** Move the note to `11_Projects`. Apply the `Project Charter` template.
2. **Run the "Architect" Prompt:** Ask the LLM to generate the **Syllabus** (Concepts, Facts, Procedures).
3. **Define the Capstone:** What will you build to prove you finished this? (e.g., "A Traffic Light System in Rust").
4. **Define the First Unit Test:** What is the specific "Hello World" plus one? (e.g., "Write the Enum struct").

### Stage 4: The Cockpit (Execution)

*Status: `20_Thinking/21_Workbench` | Context: "Doing the Work"*

1. **Hard Start:** Open the project. Read the **Bridge Note** (Where did I leave off?).
2. **The IO Constraint:**
    * **Attempt:** Try to do the *Unit Test* immediately.
    * **Fail:** "I don't know the syntax."
    * **Fetch:** *Now* read the specific documentation to fix that error.
    * **Fix:** Complete the Unit Test.
3. **The Feedback Loop:** Paste your code/draft into the LLM with the **Hostile Compiler Prompt**.

### Stage 5: Cryosleep (Closing)

*Status: `Bridge Note` | Context: "Parking the Plane"*

1. **The Stop:** Your timebox ends.
2. **The Bridge:** Write the **Bridge Note** at the top of your Project file:
    * *Last State:* "Types are defined, but logic is missing."
    * *Next Physical Action:* "Write the `match` statement for the Red light."
    * *Hook:* "Once this works, the compiler does the safety checks for me."

---

## 3. The Toolset (LLM Prompts)

### The Architect (Stage 3)

> "Act as an expert in [Topic]. Create a syllabus split into **Concepts** (Mental Models), **Facts** (Memorization), and **Procedures** (Skills). For each Concept, define a 'Unit Test' (small project) to prove understanding. Finally, define a 'Capstone Project' for the whole course."

### The Hostile Compiler (Stage 4)

> "I am learning [Topic]. Here is my attempt at [Task]. Act as a strict code reviewer/critic. Find the logical flaws, edge cases, or misunderstandings in my work. Do not fix it for me; tell me *why* it fails."

### The Bridge Builder (Stage 5)

> "Summarize my current session into a 'Bridge Note'. Capture the current state, the exact next physical step, and a 'hook' to get me excited to return."

---

## 4. Maintenance & Rules

* **The "Active Only" Limit:** You may only have **1 Active Learning Project** in the Cockpit at a time. All others must be in `Someday/Maybe`.
* **The "Fluency" Check:** If you feel like you "understand" it but haven't built it, you are failing. Run a **Flight Simulator** session immediately.

# Stage 4: The Cockpit (Execution)

### Handling Gaps: The Drill Protocol (Recursion)

*Context: "I'm stuck because I don't know X."*

When you encounter a concept you don't understand (e.g., "What is a Trait?"):

1. **The Pause:** Stop the Main Project. Do not just read an explanation.
2. **The Stack:** Treat this as a "Sub-Quest."
3. **The Micro-Unit Test:** Define a tiny, isolated experiment to prove you can *use* the new concept.
    * *Bad:* "Read about Traits."
    * *Good:* "Write a script where a `Dog` and `Cat` both answer to a `speak()` function using a Trait."
4. **The Loop:** Read -> Write Code -> Compile -> Pop Stack.
5. **The Return:** Immediately apply the concept to the Main Project to cement the link.
