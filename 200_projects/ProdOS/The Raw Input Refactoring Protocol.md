---
aliases: []
confidence: 
created: 2025-12-05T13:54:30Z
epistemic: 
last_reviewed: 
modified: 2025-12-07T18:13:29Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [state/action, state/head, state/lib, type/bug, type/concept, type/conflict, type/design]
title: The Raw Input Refactoring Protocol
type: 
uid: 
updated: 
---

Here is the generalized **Refactoring Protocol** for raw inputs. This is the standard operating procedure for converting "unstructured data" (brain dumps) into "structured objects" (HEAD Notes).

Think of this process exactly like **Refactoring Legacy Code**: you are taking a monolithic block of "spaghetti text" and separating the concerns into defined functions.

## **The Raw Input Refactoring Protocol**

Input: A messy Daily Note entry, a rant, or a confused paragraph.  
Output: A structured HEAD Note with a "Next Test."

**Phase 1: Isolation (Sandboxing)**

Do not try to fix the thought inside the Daily Note. It is too noisy there.

1. **Extract:** Highlight the raw text.  
2. **Encapsulate:** Wrap it in \[\[HEAD \- Descriptive Title\]\].  
3. **Migrate:** Click to create the file and insert the **HEAD Template**.  
4. **Paste:** Paste the *entire* raw dump into the bottom of the note under a temporary header \#\# Raw Dump.

**Phase 2: Parsing (Separation of Concerns)**

Move pieces of the "Raw Dump" into the specific template slots. Do not rewrite yet; just move the data.

- **Move "Why am I writing this?"** $\\rightarrow$ \> \[\!abstract\] The Spark  
  - *Look for:* Emotional triggers, immediate frustrations, or "I just read X."  
- **Move "How I think it works"** $\\rightarrow$ \#\# My Current Model  
  - *Look for:* "I think," "I assume," "It seems like," or generalized statements.  
- **Move "What feels wrong"** $\\rightarrow$ \#\# The Tension  
  - *Look for:* "But," "However," "I'm worried that," or contradictions between sources.

*Delete the ## Raw Dump section once empty.*

**Phase 3: The Logic Linter (Debugging)**

Now that the text is in the right slots, run this "Linter" over your sentences to strip out cognitive bugs.

**Rule A: The "Fact vs. Assumption" Check**

- *If you wrote:* "The system is broken." (Vague assertion)  
- *Refactor to:* "The system failed to sync at 09:00." (Observation) \+ "I assume it is a timeout issue." (Hypothesis).

**Rule B: The "Emotion Strip" (Signal to Noise)**

- *If you wrote:* "I am so annoyed that the API docs are garbage."  
- *Refactor to:* "The API documentation lacks examples for Error 500." (The emotion is noise; the missing example is the signal).

**Rule C: The "Agency" Check (For Personal/Productivity notes)**

- *If you wrote:* "This project is dragging on." (Passive).  
- *Refactor to:* "I have not defined a 'Definition of Done' for this project." (Active/Systemic).

**Phase 4: The Compilation (The Next Test)**

A HEAD note is useless if it doesn't execute code. You must compile the confusion into a **Micro-Experiment**.

Ask: *"What is the smallest action that creates new data?"*

- **If it's Technical:** The test is a Code Snippet or CLI command.  
  - *e.g., "Run curl with the verbose flag to see the header."*  
- **If it's Personal/Productivity:** The test is a Rule Change or Conversation.  
  - *e.g., "Implement the 'No-Phone' rule for 2 hours and track mood."*

**Summary Checklist (The "Definition of Done")**

You know the Refactoring is complete when:

1. \[ \] **No "Spaghetti Text" remains:** The raw dump is deleted.  
2. \[ \] **The "Spark" is defined:** You know *why* you opened the ticket.  
3. \[ \] **Assumptions are labelled:** You know what is "Model" vs "Reality."  
4. \[ \] **Next Test is defined:** You have a physical action to perform.

## **⚡ Example: The "Before & After"**

**Raw Input (Daily Note):**

"I'm wasting so much time on email. It's ridiculous. I check it every 5 minutes and I never get any deep work done. I need to be more disciplined like I was last year."

**Refactored HEAD Note:**

- **Spark:** "I am interrupting deep work sessions to check empty inboxes."  
- **Model:** "I assume I check email because I am undisciplined (Character Flaw)."  
- **Tension:** "Actually, I check it mostly when I hit a hard problem in coding. It's not indiscipline; it's an **anxiety-relief ritual** (System Flaw)."  
- **Next Test:** "When I hit a hard problem, I will stand up and walk for 1 minute instead of opening Outlook. Does the urge subside?"

For an architect-mindset like yours, categorizing raw thoughts by topic (e.g., "Health," "Work") is a mistake. It leads to the "Granularity Dilemma" where you have 100 generic folders and no action.

Instead, you must categorize by Metabolic State (what does this thought need?) and Functional Class (what is this thought doing?).

Here is a categorization schema designed for your PRODOS system.

1. The Primary Triage (Metabolic State)
This is the "Router" level we discussed. Every raw thought falls into one of these three states.

| Category | Definition | Obsidian Tag | Action Required |
|---|---|---|---|
| Kinetic | A defined action or project. | #state/action | Move to Todoist / 10_Projects. |
| Static | A fact, reference, or finished spec. | #state/lib | Move to SoT / 30_Library. |
| Dynamic | An unresolved problem or insight. | #state/head | Keep in HEAD / 20_Thinking. |

2. The Functional Classes (For HEAD Notes)
When you are wrestling with a #state/head note (like "Bessie" or "Productivity"), you need to define what kind of thinking is required. Categorising by function tells you which "mental tool" to pick up.
A. The Debugger (Root Cause Analysis)
 - Definition: Something is broken or behaving unexpectedly.
 - The Prompt: "Why is X happening when I expected Y?"
 - Examples: "Why do I procrastinate?", "Why is the API latency high?", "Why is Bessie avoiding work?"
 - Tag: #type/bug
B. The Architect (Design & Strategy)
 - Definition: Creating a new structure or plan from scratch.
 - The Prompt: "How should X work?" or "What is the best way to structure Y?"
 - Examples: "Designing the PRODOS folder structure," "Planning the Kubernetes migration," "Creating a revision timetable."
 - Tag: #type/design
C. The Epistemic Gap (Concept Learning)
 - Definition: You lack the vocabulary or theory to understand a problem. You need to import external models.
 - The Prompt: "What does X actually mean?"
 - Examples: "What is Learned Helplessness?", "How does the Gateway API actually route traffic?", "Understanding identifying assumptions."
 - Tag: #type/concept
D. The Tension (Conflict Resolution)
 - Definition: You have two valid but opposing models. You need synthesis.
 - The Prompt: "Note A says X, but Note B says Y. Which is true?"
 - Examples: "Agency vs. Coercion in parenting," "GitOps Pull vs. Push models," "Speed vs. Reliability."
 - Tag: #type/conflict
3. Implementation in Obsidian
Do not over-engineer folders for these. Use Nested Tags in your HEAD notes. This allows you to slice your thinking queue by the type of work you feel like doing.
Example Frontmatter:

---

type: head

status: processing

tags:

  - state/head <-- It needs thinking
  - type/bug <-- It is a "Repair" job
  - topic/family <-- The domain

---

The "Architect's Triage" Cheatsheet

When you look at a raw thought in your Inbox, ask:

 - Is it a Bug? (Something is wrong \rightarrow Fix it)
 - Is it a Design? (Something is missing \rightarrow Build it)
 - Is it a Gap? (Something is unknown \rightarrow Learn it)
 - Is it a Conflict? (Something is contradictory \rightarrow Resolve it)
Recommendation: For your "Bessie" note, the category is #type/bug (diagnosing a behaviour) mixed with #type/conflict (Agency vs. Coercion). For the "Learned Helplessness" note, the category is #type/concept.
