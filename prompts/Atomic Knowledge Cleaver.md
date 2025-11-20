---
aliases: []
confidence:
created: 2025-10-29T04:23:37Z
epistemic:
last_reviewed:
modified: 2025-10-30T14:04:40Z
purpose: Deconstructs a long hybrid note into atomic facts and a contextual structural map, while also providing a secondary prompt for synthesizing multiple notes into consolidated concepts.
review_interval:
see_also: []
source_of_truth: []
status:
tags: []
title: Atomic Knowledge Cleaver
type: prompt
uid:
updated:
version: "1"
---

## ROLE: Atomic Knowledge Cleaver

## OBJECTIVE

Your task is to deconstruct a single, long-form "hybrid" note provided in `[INPUT TEXT]`. This note contains a mix of objective facts and subjective context (narrative, opinions, arguments).

Your goal is to perform a "cleaving" process:

1. **Extract** all standalone, objective facts into new, pure **Atomic Notes**, adhering to the Canonical Schema V1.
2. **Rewrite** the original text into a single **Structural Note** (specifically a `type: map`) that replaces the extracted facts with `[[wikilinks]]` to the new or existing atomic notes, preserving the original narrative and argument.

---

## CORE PRINCIPLES (Re-emphasized)

1. **Binary Category Invariant:** Maintain a strict separation:
    - **Atomic Notes (bricks):** Must be context-free, containing one single, indivisible idea (e.g., definitions, technical specs, verifiable statements). They *never* create context.
    - **Structural Notes (architecture/hubs):** Exist *to create context* by linking and organizing atomic notes (e.g., narratives, arguments, comparisons, sequences).
2. **Atomicity:** Each new Atomic Note must contain only *one* idea, as per your "LLM Note Processing Mandate."
3. **Linked Structure & Typed Links:** The new Structural Note provides the explicit context for *why* and *how* the new Atomic Notes are related. Use `[[wikilinks]]` with inline fields to add semantic meaning (e.g., `[[Atomic Note]] rel:: supports`).
4. **Epistemic Clarity:** Every atomic note must have a clear `epistemic` status (fact, axiom, principle, opinion, hypothesis).

---

## PROCESS

You must follow this three-phase process to ensure no duplicate facts are created and to adhere to the Canonical Schema V1.

### Phase 1: Analysis and Deconstruction

1. **Analyse** the `[INPUT TEXT]`.
2. **Identify** all discrete, atomic **facts** that can be extracted.
3. **Identify** the remaining **contextual narrative** that links these facts.

### Phase 2: Deduplication and Planning

For each fact identified in Phase 1, you must perform the following:

1. **Formulate a Search Query:** Create a concise, semantic search query that captures the core meaning of the fact.
2. **Search Existing Notes:** Execute a semantic search against the user's existing notes with this query.
3. **Analyze Search Results:**
    - **If a highly similar note exists:** Mark this fact as a **"consolidation"**. Note the existing file's name.
    - **If no similar note exists:** Mark this fact as a **"new note"**.
4. **Generate a Plan:** Create a final plan detailing the actions for each fact (create, consolidate, or skip) and the title for the new Structural Note. The plan should clearly list which existing notes will be used or updated.

### Phase 3: Generation and Consolidation

Execute the plan by generating and updating the necessary notes, strictly adhering to the provided templates and schema.

**1. For each "Fact" identified:**
    ***If it's a "new note":**
        * Create a new Atomic Note using the appropriate template below (e.g., `concept`, `strategy`).
        *The title must be a clear, declarative statement about the fact.
        * Rewrite the fact in your own words, ensuring it is self-contained and context-free.
        *Ensure all required YAML frontmatter fields are populated.
    * **If it's a "consolidation":**
        *Read the content of the existing note.
        * Compare the information from the `[INPUT TEXT]` with the existing note's content.
        *If the new information adds value (e.g., provides more detail, a new example, or a clarifying perspective), **append and merge** it into the *existing note*. Do not simply tack it on; integrate it smoothly.
        * If the new information is purely duplicative, do nothing with the existing note.
    * The `[[wikilink]]` used in the Structural Note will always point to the **existing note's title**.

**2. Create *one* Structural Note for the "Context":**
    ***Format:** Use the `map` template below.
    * **Title:** Use the original note's title, prefixed with "MOC" (Map of Content) (e.g., "MOC - Understanding Cloud Networking").
    * **Content:** Rewrite the *original* narrative from `[INPUT TEXT]`. Where a fact used to be, insert the `[[wikilink]]` to either the newly created Atomic Note or the pre-existing, consolidated one. Use **typed links** (e.g., `[[Atomic Note]] rel:: supports`) to add semantic meaning. The resulting text should read as a coherent piece of analysis, with the atomic facts now acting as linked references.

---

## OUTPUT FORMAT

Present your output as a series of new files, strictly following the Canonical Schema V1.

### Canonical Schema V1 (type-safe & enforceable)

Below are **required/optional** fields by type. Keep the **binary category invariant**: atomic never creates context; structural exists to create context.

#### Global (all notes)

```yaml
---
uid: [YYYY-MM-DDTHH:MM:SSZ]   # ISO UTC; unique
created: [YYYY-MM-DDTHH:MM:SSZ]
updated: [YYYY-MM-DDTHH:MM:SSZ]
type: <atomic|structural subtype>
aliases: []
tags: []
---
```

#### Atomic Types (bricks)
**Common required:** `status`, and for (concept|strategy|definition) also `epistemic`, `purpose` (or `purpose: NA`).

```markdown
# concept | strategy | definition
---
uid: [YYYY-MM-DDTHH:MM:SSZ]
created: [YYYY-MM-DDTHH:MM:SSZ]
updated: [YYYY-MM-DDTHH:MM:SSZ]
type: concept
status: seedling|growing|evergreen
epistemic: fact|axiom|principle|opinion|hypothesis|NA
purpose: "One-line 'what this model is for' (or 'NA')."
confidence: 0.5
last_reviewed: [YYYY-MM-DD]
review_interval: 90
see_also: []         # only atomic notes
source_of_truth: []  # optional: canonical sources
aliases: []
tags: []
---

# [Declarative Title of Fact]

**Summary:** One-sentence, context-free definition.

**Details:** 2–4 sentences max. No application stories.

> **Status gates**
> - seedling → growing: has summary + details + at least 1 inbound link.
> - growing → evergreen: has 2+ inbound links from structural notes, purpose set, confidence justified, 1–3 `see_also`.
```

```markdown
# instructional
---
uid: [YYYY-MM-DDTHH:MM:SSZ]
created: [YYYY-MM-DDTHH:MM:SSZ]
updated: [YYYY-MM-DDTHH:MM:SSZ]
type: instructional
status: seedling|growing|evergreen
epistemic: NA
purpose: "Checklist to accomplish X."
last_reviewed: [YYYY-MM-DD]
review_interval: 180
aliases: []
tags: []
---

# [Instructional Title]

**What:** One-line tactic.
**How:** 3–5 bullet steps.
**Failure modes:** Bullets.
**Example (1 max):** Short.
```

```markdown
# question
---
uid: [YYYY-MM-DDTHH:MM:SSZ]
created: [YYYY-MM-DDTHH:MM:SSZ]
updated: [YYYY-MM-DDTHH:MM:SSZ]
type: question
status: seedling|growing|evergreen
epistemic: NA
last_reviewed: [YYYY-MM-DD]
review_interval: 90
aliases: []
tags: []
---

# [Question Title]
```

```markdown
# quote
---
uid: [YYYY-MM-DDTHH:MM:SSZ]
created: [YYYY-MM-DDTHH:MM:SSZ]
updated: [YYYY-MM-DDTHH:MM:SSZ]
type: quote
status: evergreen
epistemic: fact
source: "[[Source Title]]"
loc: "Ch. 5, p. 123"  # or timestamp for video/podcast
aliases: []
tags: []
---

# [Quote Title]
```

```markdown
# person
---
uid: [YYYY-MM-DDTHH:MM:SSZ]
created: [YYYY-MM-DDTHH:MM:SSZ]
updated: [YYYY-MM-DDTHH:MM:SSZ]
type: person
status: evergreen
epistemic: fact
affiliation: ""
role: ""
links: []
aliases: []
tags: []
---

# [Person Name]
```

> **Atomic rule:** no links to **structural** notes from atomic notes. `see_also` must be atomic.

#### Structural Types (architecture/hubs)

```markdown
# map
---
uid: [YYYY-MM-DDTHH:MM:SSZ]
created: [YYYY-MM-DDTHH:MM:SSZ]
updated: [YYYY-MM-DDTHH:MM:SSZ]
type: map
scope: "What belongs here."
exclusions: "What does not."
criteria: "Inclusion criteria for adding links."
tags: [map]
aliases: []
---

# MOC - [Original Note Title]

> **Inclusion criteria:** Atomic only; must be evergreen or growing.

## Core Patterns
- [[Atomic Note Example]] rel:: part-of
- [[Another Atomic Note]] rel:: example-of

## Meta-Cognition
- [[Atomic Concept]] rel:: mitigates strategy:: "Use error budgets"
```

```markdown
# comparison
---
uid: [YYYY-MM-DDTHH:MM:SSZ]
created: [YYYY-MM-DDTHH:MM:SSZ]
updated: [YYYY-MM-DDTHH:MM:SSZ]
type: comparison
subject: "[[Thing A]] vs [[Thing B]]"
criteria: ["Latency","Auth","Rate limiting","Ops burden"]
tags: [comparison]
aliases: []
---

# [Thing A] vs [Thing B]

| Criterion     | Thing A | Thing B | Notes |
|---------------|---------|--------------------|-------|
| Latency       |             |                    | [[Benchmark XYZ]] rel:: supports |
| Auth          |             |                    |      |
| Rate limiting |             |                    |      |
| Ops burden    |             |                    |      |
| Cost          |             |                    |      |

**Context:** Choose based on NFR priorities; not mutually exclusive.
```

```markdown
# sequence
---
uid: [YYYY-MM-DDTHH:MM:SSZ]
created: [YYYY-MM-DDTHH:MM:SSZ]
updated: [YYYY-MM-DDTHH:MM:SSZ]
type: sequence
goal: "Outcome of the sequence"
tags: [sequence]
aliases: []
---

# [Sequence Title]
```

```markdown
# argument
---
uid: [YYYY-MM-DDTHH:MM:SSZ]
created: [YYYY-MM-DDTHH:MM:SSZ]
updated: [YYYY-MM-DDTHH:MM:SSZ]
type: argument
claim: "Concise, falsifiable statement."
tags: [argument]
aliases: []
---

# [Argument Title]

## Evidence
- [[Supporting Atomic Note]] rel:: supports strength:: 0.6
- [[Another Supporting Note]] rel:: supports

## Objections
- [[Contradicting Atomic Note]] rel:: contradicts

## Next step
- Run [[Experiment to Test Claim]]
```

```markdown
# project
---
uid: [YYYY-MM-DDTHH:MM:SSZ]
created: [YYYY-MM-DDTHH:MM:SSZ]
updated: [YYYY-MM-DDTHH:MM:SSZ]
type: project
start: [YYYY-MM-DD]
due: [YYYY-MM-DD]
status: planned|in-progress|blocked|done
outcomes: []
tags: [project]
aliases: []
---

# [Project Title]
```

```markdown
# timeline
---
uid: [YYYY-MM-DDTHH:MM:SSZ]
created: [YYYY-MM-DDTHH:MM:SSZ]
updated: [YYYY-MM-DDTHH:MM:SSZ]
type: timeline
scope: "Event scope"
tags: [timeline]
aliases: []
---

# [Timeline Title]
```

```markdown
# source
---
uid: [YYYY-MM-DDTHH:MM:SSZ]
created: [YYYY-MM-DDTHH:MM:SSZ]
updated: [YYYY-MM-DDTHH:MM:SSZ]
type: source
authors: ["Author"]
year: 2023
kind: book|paper|post|video|podcast
citekey: doe2023example   # optional (Zotero/Citations)
read_status: to-read|in-progress|processed
tags: [source]
aliases: []
---

# [Source Title]
```

```markdown
# experiment
---
uid: [YYYY-MM-DDTHH:MM:SSZ]
created: [YYYY-MM-DDTHH:MM:SSZ]
updated: [YYYY-MM-DDTHH:MM:SSZ]
type: experiment
tests: ["[[Hypothesis to Test]]"]
design: "Protocol; metrics; success criteria."
start: [YYYY-MM-DD]
end: [YYYY-MM-DD]
outcome: pending|success|fail|inconclusive
brier_score: 0.24    # optional when making forecasts
tags: [experiment]
aliases: []
---

# [Experiment Title]

## Protocol
- (to fill)

## Results
- (to fill)

## Conclusion
- (to fill)
```

```markdown
# decision
---
uid: [YYYY-MM-DDTHH:MM:SSZ]
created: [YYYY-MM-DDTHH:MM:SSZ]
updated: [YYYY-MM-DDTHH:MM:SSZ]
type: decision
context: "Problem + constraints."
decision: "What we chose."
alternatives: ["[[Option A]]","[[Option B]]"]
consequences: ["Pro","Con"]
date: [YYYY-MM-DD]
tags: [decision, ADR]
aliases: []
---

# [Decision Title]
```

---

## Quality Gates & Automation (for LLM Awareness)

To maintain the integrity and utility of the vault, the following are important:

- **Linting & Schema Enforcement:** Adherence to frontmatter schema and field ordering.
- **Dataview Checks:** Queries to identify violations (e.g., atomic notes linking to structural notes, untested hypotheses, orphaned atomics).
- **Cleaving Process (Operationalized):**
  - **When to cleave:** Notes exceeding 250 words, having more than 12 outlinks, or containing contextual sections (e.g., "Use cases", "When not to use").
  - **How:** Trim atomic notes to a crisp definition + minimal example. Create a `type: map` or `type: comparison` for use-cases, trade-offs, and typed links. Add `see_also` from the atomic to other **atomic** notes only.

---

## [INPUT TEXT]

(Paste your long-form hybrid note here)

### Secondary Prompt: Atomic Note Synthesiser (Consolidation)

Your notes (especially `LLM Prompt for Note Synthesis.md` and `zettelkasten-consolidation-prompt.md`) also describe a separate, equally important task: **Synthesis**. This is *not* deconstructing one note, but consolidating *many* notes. As per your instructions, I have formulated this as a distinct, secondary prompt.

## ROLE: Atomic Note Architect

## OBJECTIVE

Your task is to analyse a collection of my personal Markdown notes, all related to a single subject, provided in `[INPUT DATA]`. Your goal is to identify the core, "atomic" concepts discussed across these notes, and then to **synthesise** all information about each concept into a *single*, new, comprehensive, and de-duplicated note.

This is a **many-to-few** consolidation task.

---

## PROCESS

You must follow this three-phase process:

### Phase 1: Analysis and Concept Identification

1. **Read and analyse** all provided notes in the `[INPUT DATA]` section.
2. **Identify** the primary, recurring, and atomic themes or concepts.
3. **Generate** a list of these concepts.

### Phase 2: Information Extraction and Grouping

1. **For each atomic concept** you identified, go back through *all* the source notes.
2. **Extract** every sentence, paragraph, bullet point, or section that discusses that specific concept.
3. **Group** all these extracted snippets together, associating them with their parent concept.

### Phase 3: Synthesis and Consolidation

This is the most critical phase. For each concept, you will create *one* new, consolidated note. You must:

1. **Synthesise, not just copy:** Read all the extracted snippets for the concept.
2. **De-duplicate:** Remove redundant information or repeated definitions.
3. **Merge & Reconcile:** Combine partial explanations from different notes to create a complete, holistic description. If notes have slightly different takes, synthesise them into a more nuanced view.
4. **Rewrite:** Re-write all the disparate information into a *single*, coherent, well-structured, and easy-to-read narrative. The final note should read as if it were written from scratch.
5. **Format:** Structure the new note logically using Markdown (headings, bullet points, etc.) and add the YAML template below.

---

## OUTPUT FORMAT

You must present your output as follows:

1. First, provide the list of atomic concepts you identified.
2. Then, for each concept, provide the newly synthesised note. Use a clear filename-style marker for each new note.

### Synthesised Note Template

**File:** `[Concept Name].md`

```markdown
---
created: [YYYY-MM-DDTHH:MM:SS]
type: concept
epistemic: [fact|principle|hypothesis]
status: growing
tags: [synthesised]
---

# [Concept Name]

(Your fully synthesised, de-duplicated, and rewritten note on this concept goes here. This should be a comprehensive text combining all knowledge from the source notes.)

## Connections

- (Add relevant `[[wikilinks]]` or `related::` links to other major concepts synthesised in this session.)
````

## [INPUT DATA]

(Paste all your source Markdown notes for synthesis here)

***

## 2. Elaboration and Best Practices

Here is the explanation of my structural choices and best practices for using these prompts.

### Elaboration on Prompt Structure

- **Primary Prompt (Deconstructor):**
  - **The "Cleaving" Metaphor:** I built this prompt around the "Cleaving Process" from your `Personal Knowledge Management.md` note. This is the most powerful and precise metaphor for the task you want to perform.
  - **Fact/Context Solution:** The prompt solves your "Fact vs. Context" separation requirement by creating two distinct *types* of notes, a solution derived directly from your `PKM.md` file (Atomic vs. Structural notes) and `I have an obsidian markdown...md` (Layer 1 Fact vs. Layer 2 Concept).
  - **Linking:** The prompt solves the "Linking" requirement in the most robust way possible. Instead of just "link dumping," it instructs the LLM to weave the `[[wikilinks]]` *into the narrative* of the new `type: map` note. This *is* the link context, fulfilling the "eufriction" principle from your `LLM Note Processing Mandate.md`.
- **Secondary Prompt (Synthesiser):**
  - **Task Distinction:** Your provided notes described two conflicting tasks: deconstruction (1-to-Many) and synthesis (Many-to-Few). As per your instructions, I evaluated this and determined they are genuinely separate, high-value tasks that require distinct prompts.
  - **Consolidation:** This prompt is a direct synthesis of your `LLM Prompt for Note Synthesis.md` and `zettelkasten-consolidation-prompt.md` files, taking the best of both (the 3-Phase process from one, the de-duplication focus from the other).

### LLM Context Best Practices for Deconstruction

1. **Managing Large Notes (Chunking):**
    - If your input note is extremely long (e.g., >10,000 words), it may exceed the LLM's context window or lead to errors.
    - **Solution:** Use a multi-step approach.
        1. **Step 1:** Paste the *entire* note and ask the LLM *only* to perform `Phase 1: Analysis and Deconstruction` (i.e., just output the *plan*).
        2. **Step 2:** For each "Fact Note" in the plan, start a new chat turn. Paste the plan and *only the relevant paragraph(s)* from the source text, and ask it to generate that *one* Atomic Note.
        3. **Step 3:** Finally, ask it to generate the `type: map` (Context) note, using the plan and all the new note titles.
2. **Metadata and Formatting (YAML):**
    - The YAML block I included is a synthesis of the best practices from your notes (`PKM.md`, `I have read...smart notes.md`).
    - `type: [concept|map]`: This is the most crucial field, defining the note's role as per your `PKM.md` system.
    - `epistemic: fact`: This explicitly flags the extracted notes as objective, fulfilling a key requirement.
    - `status: seedling`: This is a vital workflow tag from your `PKM.md` file. It marks all LLM-generated notes as "drafts" that require your personal review before being promoted to "evergreen."
    - `source: "[[...]]"`: This creates the essential backlink from the "Fact Note" to the "Context Note," ensuring no information is orphaned.

3. **Ensuring Consistency and Accuracy:**
    - **Strict Templates:** The prompts provide rigid `## ROLE`, `## OBJECTIVE`, `## PROCESS`, and `## OUTPUT FORMAT` sections. This strict formatting significantly reduces LLM "drift" and ensures the output is predictable and machine-readable (i.e., you get actual file blocks).
    - **Two-Phase Process:** By forcing the LLM to first *Analyse and Plan* (Phase 1) before *Generating* (Phase 2), you prevent it from rushing, missing facts, or confusing context.
    - **Human-in-the-Loop:** The `status: seedling` tag is your most important quality control tool. The LLM's job is to do the 80% of deconstruction and formatting. Your job is the final 20% of refinement and integration, which solidifies the knowledge in your own mind.
