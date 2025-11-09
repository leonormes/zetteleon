---
aliases: []
confidence: 
created: 2025-10-26T00:00:00Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T11:06:58Z
purpose: 
review_interval: 
see_also: []
source: "https://gemini.google.com/share/f281fb1c028b"
source_of_truth: []
status: 
tags: ["clipped", "llm_session"]
title: ‎Gemini - Synthesizing Atomic Notes for ADHD
type:
uid: 
updated: 
version:
---

\# ROLE: Atomic Note Architect

\# OBJECTIVE

Your task is to analyse a collection of my personal Markdown notes, all related to a single subject. Your goal is to identify the core, "atomic" concepts discussed across these notes, and then to synthesise all information about each concept into a \*single\*, new, comprehensive note.

\# PROCESS

You must follow this three-phase process:

\## Phase 1: Analysis and Concept Identification

1\. Read and analyse all the provided notes in the \`\[INPUT DATA\]\` section.

2\. Identify the primary, recurring, and atomic themes or concepts.

3\. Generate a list of these concepts. Examples might be "GTD Capture", "Weekly Review", "Project Planning", or "Zettelkasten Linking".

\## Phase 2: Information Extraction and Grouping

1\. For each atomic concept you identified, go back through \*all\* the source notes.

2\. Extract every sentence, paragraph, bullet point, or section that discusses that specific concept, even if it's just a brief mention.

3\. Group all these extracted snippets together, associating them with their parent concept.

\## Phase 3: Synthesis and Consolidation

This is the most critical phase. For each concept, you will create \*one\* new, consolidated note. You must:

1\. \*\*Synthesise, not just copy:\*\* Read all the extracted snippets for the concept.

2\. \*\*De-duplicate:\*\* Remove redundant information or repeated definitions.

3\. \*\*Merge & Reconcile:\*\* Combine partial explanations from different notes to create a complete, holistic description. If notes have slightly different takes, try to synthesise them into a more nuanced view.

4\. \*\*Rewrite:\*\* Re-write all the disparate information into a \*single\*, coherent, well-structured, and easy-to-read narrative. The final note should read as if it were written from scratch by an expert on the topic, not like a collection of copied-and-pasted snippets.

5\. \*\*Format:\*\* Structure the new note logically using Markdown (headings, bullet points, etc.).

\# OUTPUT FORMAT

You must present your output as follows:

1\. First, provide the list of atomic concepts you identified.

2\. Then, for each concept, provide the newly synthesised note. Use a clear filename-style marker for each new note.

\### Example Output Structure:

\*\*Identified Atomic Concepts:\*\*

\* Concept A

\* Concept B

\* Concept C

\---

\*\*File:\*\* \`Concept A.md\`

\`# Concept A\`

\`(Your fully synthesised, de-duplicated, and rewritten note on Concept A goes here. This should be a comprehensive text combining all knowledge from the source notes.)\`

\---

\*\*File:\*\* \`Concept B.md\`

\`# Concept B\`

\`(Your fully synthesised, de-duplicated, and rewritten note on Concept B goes here.)\`

\---

\*\*(...and so on for all identified concepts.)\*\*

Here are the synthesised atomic notes based on your provided files.

**Identified Atomic Concepts:**

- ADHD and the Motivation Paradox
- GTD: The Clarify and Review Bottleneck
- LLM-Powered GTD Agent (gtdOS)
- gtdOS Logic: Action Sequences and 'Now Action'
- Methods for Project Management in Obsidian
- Timeboxing for ADHD

---

**File:**`ADHD and the Motivation Paradox.md`

## ADHD and the Motivation Paradox

This concept describes the common ADHD experience of struggling with procrastination, which is often mistaken for laziness. The core of the problem is the "motivation paradox": waiting to *feel* motivated to start a task, when in reality, for the ADHD brain, the act of *starting* is what creates motivation.

## The Neurological Basis: Dopamine and Reward

The issue is not a lack of willpower but a difference in how the brain regulates **dopamine**, the neurotransmitter tied to motivation and reward.

- In an ADHD brain, the "reward prediction system" often does not activate for tasks that are not inherently interesting, urgent, or new.
- This creates a high "activation energy" or a "wall of awful" when trying to start ordinary or delayed-reward tasks (like chores, exercise, or project work), as there is no internal "pull" to begin.

## The Two Feedback Loops

This leads to two opposing cycles:

1. **The Avoidance Loop (Default):**Waiting for motivation -> No motivation arrives -> Guilt and paralysis -> Lowered mood -> Continued waiting.
2. **The Action Loop (The Solution):**Start with a micro-action -> A small dopamine boost is released -> Feel slightly better -> Momentum builds -> Do more -> Motivation increases.

This solution, known as **Behavioral Activation**, shows that for the ADHD brain, **motion must precede motivation**.

## Practical Strategies to Create Motion

The goal is to lower the activation energy so that starting is "ridiculously small" and frictionless.

- **Shrink the Start:** Break any task down into its smallest possible "atomic" step. The goal is just to start, not to finish.
  - *Example:* Instead of "go to the gym," the task is "put on trainers."
  - *Example:* Instead of "clean the kitchen," the task is "stand up and fill the water bottle."
- **Use the "Five Minutes Only" Rule:** Give yourself explicit permission to stop after just five minutes. This removes the overwhelming pressure of the full task, making it easier to begin. Often, the momentum built in those five minutes will be enough to continue.
- **Reward the Start, Not the Finish:** Because the ADHD brain needs immediate rewards, celebrate the *act of starting*. This provides the instant dopamine hit required to reinforce the action loop.
- **Anchor Habits:** Attach a new, small action to an existing, automatic daily habit.
  - *Example:* "After I pour my morning coffee, I will do five squats."
- **Focus on "Movement," Not "Workouts":** Reframe high-friction concepts. "Exercise" can feel like a huge commitment, whereas "movement" can be as simple as stretching during a meeting.

---

**File:**`GTD - The Clarify and Review Bottleneck.md`

## GTD: The Clarify and Review Bottleneck

A central challenge in using Getting Things Done (GTD) with ADHD is the "ADHD-GTD Paradox": the core executive functions that GTD relies on—namely the **Clarify** and **Review** stages—are the very functions most disrupted by ADHD.

This leads to a common failure mode:

1. **Capture is successful:** The ADHD brain excels at capturing new ideas.
2. **Clarify becomes a bottleneck:** The inbox fills up with captured items that require sorting, processing, and decision-making. This is a high-friction executive function task.
3. **Trust is broken:** Because the inbox is not processed, the brain *knows* the items are not "handled." This erodes trust in the entire system, and the mind reverts to trying to hold everything in "psychic RAM."

To make GTD work, the Clarify and Review processes must be adapted to be as friction-proof as possible, minimising the executive load.

## Strategies for a Frictionless Clarify Stage

- **Separate Capture from Clarify:** Treat capturing as a "mind dump" that can happen any time. Treat clarifying as a distinct, scheduled activity.
- **Use "Micro-Clarify" Slots:** Instead of one long, daunting "processing" session, schedule multiple, short (3-10 minute) "micro-clarify" blocks throughout the day (e.g., after a meeting, before lunch).
- **Lower the Bar for "Good Enough":** Perfectionism is the enemy of clarifying. A task is "good enough" clarified if you simply know:
  - What is the next visible, physical action?
  - In what context?
  - For whom?
- **Apply the 2-Minute Rule Aggressively:** If clarifying or *doing* the next action will take under two minutes, do it immediately. This prevents it from ever entering the system.
- **Use Trusted Holding Buckets:** Have a single, explicit list (e.g., `Needs Clarify`) that you trust. You can relax, knowing you *will* review that specific list during your micro-clarify slots.

## Strategies for a Frictionless Review Stage

The Weekly Review is often the first thing to fail because it is a large, unstructured block of high-executive-function work.

- **Automate the Review Dashboard:** Use tools like an Obsidian note with Dataview or a Todoist filter to automatically create your review. This dashboard should pull in:
  - Overdue tasks.
  - Items tagged `#waiting`.
  - A list of active projects.
  - A log of "wins" from the past week (for dopamine reinforcement).
- **Make it Flexible and Consistent:** The key is *consistency*, not duration. If a full weekly review is too much, start with a 15-minute bi-weekly review. The goal is to build the habit of looking at your system, which in turn builds trust.

---

**File:**`LLM-Powered GTD Agent (gtdOS).md`

## LLM-Powered GTD Agent (gtdOS)

This is a system architecture for a conversational, context-aware AI assistant designed to eliminate the cognitive friction of deciding what to do next. The vision is a "GTD Co-Pilot" that can analyse all your tasks, notes, and priorities in real-time and suggest the single best action.

## Core Architecture: RAG and AgentOS

The system is built on a **Retrieval-Augmented Generation (RAG)** pipeline, meaning it retrieves relevant, real-time context *before* prompting the "brains" of the operation.

1. **Continuous Indexing:** A background service monitors all data sources (Obsidian vault, Todoist, Jira) and continuously updates a local **vector database** (e.g., ChromaDB). All notes, tasks, and project files are converted into vector embeddings.
2. **Contextual Retrieval:** When the user asks a question (e.g., "What should I do next?"), the query is used to search the vector database for the most relevant documents (e.g., related project notes, weekly goals, and tasks).
3. **Dynamic Prompting:** This retrieved context is dynamically injected into a master prompt, which is then sent to the `ReasoningAgent` (the LLM).

This process is orchestrated by an "AgentOS" framework of multiple, specialised agents:

- **`MasterAgent` (Orchestrator):** The user-facing conversational agent that manages the dialogue.
- **`IngestionAgent` (Data Collector):** Fetches raw data from external APIs like Jira and Todoist.
- **`IndexingAgent` (Librarian):** Watches for file changes, creates vector embeddings, and updates the vector database.
- **`RetrievalAgent` (Researcher):** Queries the vector database to find relevant context for the user's query.
- **`ReasoningAgent` (Strategist):** The core LLM that receives the user's query and all retrieved context, applies the GTD logic, and makes the final decision.

## LLM Model Selection

There are no models specifically "tuned for GTD." The most effective approach is a layered system:

- **Reasoning:** Use a powerful, general-purpose model (e.g., Claude 3.7, a local LLaMA 3.1 instance) for the `ReasoningAgent`. Its strong reasoning capabilities are essential for interpreting the complex context and making a strategic choice.
- **Task Decomposition:** Optionally, the agent's output could be piped to a specialised, neurodivergent-focused tool (e.g., Goblin.tools, Fluidwave) to break the suggested action down into even smaller steps, further reducing activation friction.

---

**File:**`gtdOS Logic - Action Sequences and 'Now Action'.md`

## gtdOS Logic: Action Sequences and 'Now Action'

This note defines the core operational logic for the `gtdOS` agent, which uses Todoist as its "front-end" for task management.

## Foundational Principle: 'Next Action' vs. 'Now Action'

The system's intelligence relies on a crucial distinction:

- **`Next Action`**: Any task that is currently unblocked and represents the next possible step in a sequence. There can be **many** `Next Actions` available at any given time (one for each active sequence). This is the *pool of potential work*.
- **`Now Action`**: The **single** task that the `gtdOS` agent has determined is the optimal task for you to focus on *right now*. There is only ever one `Now Action`.

## Implementation in Todoist

This logic is implemented using standard Todoist features:

1. **Projects:** Used as top-level containers (e.g., `Project: Launch New Feature`).
2. **`Action Sequences` (via Todoist Sections):** Dependencies are managed by using **Sections** within a project. Each Section represents a single, sequential list of tasks. Only the topmost, uncompleted task in a Section can be a `Next Action`.
3. **Concurrency:** A project can have multiple `Action Sequences` (Sections) running in parallel (e.g., a "Backend Development" Section and a "Marketing Prep" Section). The agent can select the `Next Action` from either sequence.

## The Plan out next Agent Workflow

When the user triggers the agent, it executes the following steps:

1. **Reset:** The agent first scans Todoist and removes all existing `#next_action` and `#now_action` tags to ensure a fresh state.
2. **Identify:** The agent iterates through every Project and every **Section**. It applies the `#next_action` tag to the **topmost, uncompleted task** in each Section.
3. **Gather Context:** The agent pulls three categories of information:

- **User Context:** Current time, location, and user-stated energy (`low`, `medium`, `high`).
- **Strategic Priorities:** The content of key Obsidian notes (e.g., `[[Weekly Goals.md]]`).
- **Available Actions:** The full list of tasks it just tagged with `#next_action`.

4. **Reason:** This complete context is fed into the `ReasoningAgent` (LLM) with a master prompt.
5. **Select:** The LLM applies a strict, multi-step decision framework:
6. **Constraint Filtering:** Eliminates tasks that don't match the user's context (e.g., filters out `#high_energy` tasks if energy is `low`).
7. **Urgency:** Prioritises tasks with the nearest due dates.
8. **Strategic Importance:** Prioritises tasks that align with the goals in the retrieved Obsidian notes.
9. **Tie-Breaker:** Uses native Todoist priority (P1, P2) to break any remaining ties.
10. **Tag:** The agent applies the `#now_action` tag to the single task selected by the LLM.

The user's workflow is then simplified to opening Todoist and filtering for the `#now_action` tag.

---

**File:**`Methods for Project Management in Obsidian.md`

## Methods for Project Management in Obsidian

There are two primary, native-tooling methods for managing complex projects within Obsidian, each with a different philosophy.

## Method 1: The Obsidian Bases Plugin

This method transforms Obsidian into a "Notion-like" database system, providing a visual, structured interface for project management.

- **Core Concept:** The **Bases Core Plugin** turns a collection of notes into a dynamic, table-based database. It is a self-contained system that *removes* the need for complex, text-based Dataview queries.
- **Key Features:**
  - **Inline Editing:** Edit note properties (like `status` or `due_date`) directly from the table view.
  - **Dynamic Fields:** Add formula-based fields (e.g., `DaysUntilDue = DueDate - Today()`).
  - **Visual Views:** Includes table views, list views, and **card views** for visual Kanban boards.
  - **Embedded Views:** A project note can embed a filtered Base view (e.g., a table of all tasks related *only* to that project).
- **Workflow:** This approach is well-suited for Agile-style hierarchical structures (e.g., **Projects** -> **Epics** -> **Stories** -> **Tasks**) where visual tracking and property management are key.

## Method 2: The Dataview + Daily Notes Workflow

This is a "bottom-up" system built on the foundation of Markdown files, YAML frontmatter, and linking.

- **Core Concept:** This method follows a **"Daily Notes First"** methodology. All project-related work (tasks, logs, meeting notes) originates as an entry in a **Daily Note**.
- **Key Features:**
  - **Capture:** Work is captured in the Daily Note and linked to its parent project (e.g., `project: [[Project X]]`). This creates a natural "breadcrumb trail" of the project's evolution.
  - **Structure (YAML):** Each project note has a standardized **YAML frontmatter** block containing key metadata (e.g., `status: active`, `summary: "..."`, `up: [[Areas MOC]]`).
  - **Aggregation (Dataview):** The project note itself functions as a dynamic "dashboard." It uses **Dataview queries** to automatically pull in and display all tasks, logs, and meeting notes from across the vault that are linked to it.
- **Workflow:** This system is excellent for knowledge-heavy or log-based projects where tracing the *history* and *context* of work is as important as the tasks themselves. It often uses plugins like the **Tasks plugin** for task management and **Text Transporter** to move tasks between notes.

---

**File:**`Timeboxing for ADHD.md`

## Timeboxing for ADHD

Timeboxing is a time management strategy that is exceptionally well-suited for the ADHD brain. It is defined as selecting a task, assigning it a specific, fixed time slot (a "box"), and committing to completing it to an "acceptable standard" within that time.

## Timeboxing vs. Timeblocking

This method is often confused with timeblocking, but there is a critical distinction:

- **Timeblocking:** Allocates time *for* a task (e.g., "9-10am: Work on report"). It is **process-oriented**.
- **Timeboxing:** Defines the scope of the task *by* the time allotted (e.g., "9-10am: *Finish* report introduction"). It is **outcome-oriented** and leverages Parkinson's Law (work expands to fill the time available).

## Why Timeboxing is Effective for ADHD

This technique directly counteracts core ADHD challenges:

1. **Counters "Time Blindness":** It makes the abstract concept of time a visible, external, and tangible constraint.
2. **Lowers "Wall of Awful":** It reduces task initiation friction. The commitment is not the entire, daunting task, but "just 25 minutes," which is far easier to start.
3. **Manages Hyperfocus:** The timer's alarm acts as a critical **external interrupt**. It breaks the "hyperfocus trance" and forces a conscious moment of re-evaluation: "Is this task done? Should I continue, or move on?"
4. **Reduces Executive Function Load:** It "front-loads" all the hard decisions (planning, prioritising, scheduling) into a single, short (e.g., 15-minute) daily planning session, freeing up mental energy for execution.

## Practical Adaptations for ADHD

To make timeboxing effective, it should be adapted:

- **The "Triple Estimate" Rule:** To combat time blindness, make a realistic time estimate for a task, and then **triple it**. This builds in a realistic buffer for distractions and under-estimation.
- **Use Visual Timers:** Use a physical (e.g., Time Timer) or digital visual timer that shows the passage of time. This makes time tangible and reinforces a sense of urgency.
- **Practice "Soft Timeboxing":** Instead of a rigid "hard stop" which can cause anxiety, use the alarm as a **"check-in" point**. When the timer goes off, pause and ask: "Am I done? Do I need another 'box'? Should I move on?"
- **Plan Around Energy:** Schedule high-focus, cognitively demanding tasks during your "Genius Zone" (peak energy) and administrative tasks during your "Kinetic Zone" (low energy).
- **Be Non-Judgmental:** When you mis-estimate a timebox, do not treat it as a failure. Treat it as **"gathering data"** on how long that task *really* takes, and use that data to improve your next plan.

### Handling Blocking Tasks

If a timebox ends but the task is not finished and it blocks the next item, you must make a conscious decision:

1. **Hard Stop & Re-plan:** Stop, and immediately create a *new* timebox for the remainder of the blocking task, pushing back other items in your schedule.
2. **Borrow Time:** Consciously "steal" time from a pre-scheduled buffer block or from a less important task later in the day.
3. **Use an Overflow Block:** Defer the remainder of the task to a pre-scheduled "contingency" or "overflow" block at the end of the day.

Google Account

Leon Ormes

<leonormes@gmail.com>
