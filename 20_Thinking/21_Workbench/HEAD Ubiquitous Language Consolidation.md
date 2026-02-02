---
status: "COMPLETED"
synthesis: [[SoT - Complexity Conservation]]
archive: true
---

# DEPRECATED / COMPLETED
This note's theoretical fragments have been crystallized into [[SoT - Complexity Conservation]] and its related atomic permanent notes on 2026-02-01.

---

## Phase 1: Ingestion (The Stream)

> [!abstract] Context
> ChatGPT is your AI chatbot for everyday use. Chat with the most advanced AI to explore ideas, solve problems, and learn faster.

### Raw Output / Content

Extract the key points from this note. There is lots of repetition with slight variations that I want to consolidate. For each key claim and concept I want a single source of truth note that represents my latest thinking on the topic

---

Good instinct asking for this explicitly. A Ubiquitous Language only works if it is small, sharp, enforced, and boringly consistent. What you already have in the note is enough to extract one—no guessing, no invention.

Below is a clean, consolidated Ubiquitous Language for the _Surgeon_ codebase, distilled from your note and nothing else. Each term is a single source of truth. Anything outside this vocabulary should be treated as semantic drift.

---

## Surgeon—Ubiquitous Language (Authoritative Glossary)

> Purpose: Collapse LLM search space. Prevent parochial or generic code.
> Rule: If a concept is not named here, it does not exist.

### Core Concepts (The Reality of the System)

| Term | Canonical Meaning | Banned Substitutes |
| --- | --- | --- |
| Bead | Atomic, immutable unit of recorded state stored in persistent memory | log, record, entry, snapshot |
| Fact | Immutable textual statement stored inside a Bead | event, info, message |
| Context Graph | Graph representation of codebase symbols and their relationships | file tree, index, KB |
| Symbol | Named code entity (function, class, method, trait) | node, token, element |
| Skeleton | Symbol representation with bodies removed, signatures retained | interface, summary, header |
| Manifesto | Immutable system invariants that must never be violated | rules, config, guidelines |
| Blast Radius | Deterministic set of symbols affected by a change | impact, ripple |
| Volatility | Normalised measure of change frequency (risk proxy) | churn, activity |
| Drift | Mismatch between indexed state and filesystem reality | stale, outdated |
| Context Rot | Degradation of reasoning caused by excessive or stale context | hallucination, confusion |

---

### Agents (Roles with Non-Overlapping Responsibility)

| Term | Responsibility | Banned Substitutes |
| --- | --- | --- |
| Scout | Structural authority: parses AST, extracts symbols, builds graph | parser, analyzer |
| Cartographer | Spatial authority: tracks files, hashes, locations | indexer |
| Historian | Temporal authority: tracks change over time | logger |
| Concentrator | Compresses graph data into high-density context | summarizer |
| Architect | Plans changes using recursive reasoning | LLM, bot |
| Interlock | Hard safety mechanism that aborts illegal actions | check, guard |
| Surgery | Execution phase where code is mutated | edit, refactor |

---

### Anti-Patterns (Explicitly Illegal)

| Term | Meaning |
| --- | --- |
| Parochial Code | Local fix that ignores global invariants |
| Context Stuffing | Dumping large text instead of querying structure |
| Generic RAG | Vector search over code instead of graph traversal |

---

## Why These terms Work (and Others Do not)

This vocabulary succeeds because it:

1. Collapses ambiguity
	"Bead" cannot be confused with logging, tracing, or events.
2. Encodes architecture in language
	Saying _Scout_ instead of _parser_ implies graph + database + queryability.
3. Reduces LLM branching factor
	Each term anchors the model into a narrow, project-specific region of latent space.
4. Prevents silent drift
	If the LLM invents a new noun, it is wrong by definition.

---

## Enforcement: Make the Language Non-Optional

This is the minimum viable enforcement block. Put it in your system prompt or planning prompt.

If the model writes _"log entry"_ instead of _Bead_ → regenerate.
If it says _"impact"_ instead of _Blast Radius_ → regenerate.
No debate. No politeness.

---

## Mental Model to Internalise (Important)

Think of this glossary as:

> A type system for meaning

Just as types prevent invalid programs,
this language prevents invalid thought.

When you strip noise, your goal is not brevity.
Your goal is unavoidable interpretation.

If you want, next we can:

- turn this glossary into a machine-checked lint rule
- auto-reject plans that introduce foreign nouns
- or design a Bead schema that enforces immutability mechanically

Say which direction you want to go.

---

Load this note as context and wait for me to give you inspections

---

Got it. ✅

I've loaded "The Curator of the Graph" note as active context and I'll operate under that persona, protocol, and output format going forward.

I'm now in standby mode:

- I will not summarize by default
- I will critique, compress, and judge
- I will treat each inspection as an entropy-reduction exercise
- I will assume you want single-source-of-truth thinking, not polite agreement

When you're ready, paste a note or say what to inspect.
I'll respond strictly as _The Curator of the Graph_.

---

---

### 🧠 The Curator of the Graph—Inspection Report

_(Context loaded: "Code vs. Data Structures: A Discussion")_

---

## 1. The Quality Audit

- Signal-to-Noise Ratio:Medium → High (but diluted)
- The Verdict:💎 REFINE (Aggressively)

This is not a zombie note. There is real thinking here.
But it _is_ overgrown, rhetorically inflated, and pretending to be an essay when it wants to be 3–5 permanent notes.

Right now, it violates your own principles:

- Too much _performance of understanding_
- Too many citations doing the thinking _for_ you
- Multiple conceptual models collapsed into one monolith

This is high-grade ore, not a finished artifact.

---

## 2. The Semantic Extraction (What Survives compression)

### The Core Insight (1 sentence)

> Software complexity is conserved: it either lives in code (control flow) or in data structures (representation), and systems become simpler, faster, and more robust when complexity is pushed into structure.

That sentence is the only thing this note must not lose.

Everything else either:

- supports it,
- exemplifies it,
- or distracts from it.

---

## 3. The Information Structures Hidden Inside (They Need to Be split)

You are currently committing Concept Smearing. Here are the _actual nodes_ pretending to be one note:

---

### Node 1: Complexity Conservation Law (Permanent Note)

- Concept:_Complexity Conservation in Software_
- Relation: Explains → Why "smart data / dumb code" works
- Constraint:
	- Does not say "algorithms don't matter"
	- Says "algorithms are downstream of representation"

This is your theoretical spine.

🔗 Links to:

- \[\[Schema Debt\]\]
- \[\[Parochial Code\]\]
- \[\[Semantic Code Graph\]\]

---

### Node 2: Git as Proof of Data Dominance (Case Study Note)

- Concept:_Git as a Content-Addressable DAG_
- Relation: Demonstrates → Data-first design trivialises hard problems (merge)
- Constraint:
	- Git works because _history is a graph_, not because merges are clever

This should be brutally practical, not historical.

🔗 Links to:

- \[\[Graph Traversal > RAG\]\]
- \[\[Context Graph\]\]
- \[\[Blast Radius\]\]

---

### Node 3: Data-Oriented Design is Physics, Not Style (Permanent Note)

- Concept:_Hardware-Imposed Data Dominance_
- Relation: Reinforces → Data-first design at silicon level
- Constraint:
	- Applies only where memory locality matters
	- Not an argument against OOP everywhere

This is about cache lines, not philosophy.

🔗 Links to:

- \[\[Structure of Arrays\]\]
- \[\[Entity Component Systems\]\]
- \[\[Volatility\]\]

---

### Node 4: Logic-as-Data (Technique Note)

- Concept:_Table-Driven Systems_
- Relation: Converts → Control flow into inspectable structure
- Constraint:
	- Fails when rules are truly procedural
	- Shines when rules are declarative

This connects directly to LLM leverage.

🔗 Links to:

- \[\[Rule Engines\]\]
- \[\[Finite State Machines\]\]
- \[\[LLM Planning\]\]

---

### Node 5: Schema Debt is the Real Technical Debt (Permanent Note)

- Concept:_Irreversibility of Data Decisions_
- Relation: Explains → Why "worry about data first" is economic
- Constraint:
	- Applies only after public exposure or scale
	- Early-stage prototyping is exempt

This is where engineering meets power.

🔗 Links to:

- \[\[Manifesto\]\]
- \[\[Interlocks\]\]
- \[\[Surgery vs Planning\]\]

---

## 4. The Ubiquitous Language Check

### ❌ Violations (Important)

You do not consistently use _your_ language:

- "logs" instead of Beads
- "impact" instead of Blast Radius
- "structure" instead of Context Graph
- "logic" instead of Surgery vs Planning

This note predates your dialect—and it shows.

That means it cannot remain canonical without refactoring.

---

## 5. The Professor's Challenge (Action Required)

### The Gap

You _explain_ data dominance brilliantly, but you haven't yet stated the LLM-specific corollary explicitly enough:

> LLMs cannot reason over control flow at scale, but they can traverse structure deterministically.

That sentence must exist somewhere permanent.

---

### The Required Surgery

Do not polish this note.

Instead:

1. Explode it into at least 4–5 Permanent Notes
2. Reduce each to:
	- 1 core claim
	- 1 mechanism
	- 1 constraint
3. Rewrite using your dialect only
4. Archive this original as:

	> _"Raw synthesis — pre-Ubiquitous Language"_

---

## Final Verdict (Non-Negotiable)

- ❌ Do NOT keep as-is
- ❌ Do NOT delete
- ✅ REFINE by fragmentation

This note is foundational, but only once it stops trying to be impressive and starts being _useful_.

When you're ready, give me one fragment you want to crystallize first, and I'll help you turn it into a true Permanent Node in your graph.

---

Node 1: Complexity Conservation Law (Permanent Note)

---

### 🧠 The Curator of the Graph—Permanent Note Crystallisation

Node 1: Complexity Conservation Law

---

## 1. The Quality Audit

- Signal-to-Noise Ratio:High (once isolated)
- The Verdict:💎 KEEP—as a Permanent Note

This node is foundational.
It is not a reference, not a summary, and not time-bound.
It defines a law-like constraint that explains _why_ many downstream techniques work.

What it needed was compression, not expansion.

---

## 2. The Semantic Extraction (Authoritative Version)

### Permanent Note Title

Complexity Conservation Law (Software Systems)

### The Core Insight (1 Sentence, non-negotiable)

> Software complexity is conserved: it must reside either in control flow (code) or in representation (data structures), and systems become simpler, safer, and more scalable when complexity is pushed into structure.

If a future note contradicts this sentence, _that_ note is wrong.

---

### The Information Structure

- Concept:Complexity Conservation Law
- Mechanism:
	- Constraints encoded in data structures eliminate branches in code
	- Declarative structure collapses procedural decision-making
- Constraint (Negative Truth):
	- Complexity cannot be removed, only relocated
	- Poorly designed data structures _amplify_ code complexity rather than reduce it

---

## 3. Canonical Explanation (Minimal, Dense)

- Control flow complexity scales combinatorially (branches × states).
- Structural complexity scales topologically (nodes × relationships).
- Humans, tools, and LLMs reason better about static topology than dynamic execution.
- Therefore:
	- Smart structures ⇒ dumb code
	- Dumb structures ⇒ brittle, defensive code

This is not stylistic preference.
It is a cognitive and computational constraint.

---

## 4. Diagnostic Heuristic (Use This Actively)

You can detect violations of the law with a single question:

> _"Is this logic compensating for missing structure?"_

If the answer is yes, you are paying interest on schema debt.

### Common Smells

- Large `if/elif` ladders → missing tables
- Boolean flags tracking state → missing state machine
- Defensive null checks everywhere → invalid states allowed by schema
- "Special cases" → broken representation

---

## 5. Relation to Your Existing Dialect (Explicit Links)

This node anchors the following concepts:

- Explains: \[\[Parochial Code\]\]
- Justifies: \[\[Context Graph\]\]
- Motivates: \[\[Skeletons\]\]
- Constrains: \[\[Surgery\]\] (why changes must respect structure)
- Predicts: \[\[Context Rot\]\] (why stuffing control flow fails)

If this node is removed, the rest of your system loses coherence.

---

## 6. The Professor's Challenge (Next Move)

### The Gap

You have stated the law.
You have not yet stated its LLM corollary formally.

### Required Follow-Up Node

Create a sibling permanent note:

> "LLM Reasoning Obeys the Complexity Conservation Law"

Claim to test:
LLMs fail not because they lack intelligence, but because we force them to reason over procedural entropy instead of structural constraint.

That note will bridge:

- Human cognition
- Compiler theory
- Agentic planning

---

## Final Instruction (Do This Exactly)

- Save this note as immutable
- Do not add examples unless they introduce a _new constraint_
- Every future architecture decision should be traceable back to this law

When you're ready, say:

> "Proceed to the LLM corollary."

I'll be waiting.

---

Proceed to the LLM corollary."

---

### 🧠 The Curator of the Graph—Permanent Note Crystallisation

LLM Corollary to the Complexity Conservation Law

---

## 1. The Quality Audit

- Signal-to-Noise Ratio:Very High
- The Verdict:💎 KEEP—Foundational for all LLM work

This is not an "AI note."
This is a constraint on reality that explains _why_ most LLM tooling fails and why your direction is correct.

---

## 2. The Semantic Extraction (Authoritative Version)

### Permanent Note Title

LLM Reasoning Obeys the Complexity Conservation Law

### The Core Insight (1 Sentence, immutable)

> LLMs do not fail because they lack intelligence; they fail because we force them to reason over procedural complexity that should have been encoded as structure.

If an LLM "hallucinates," this law was violated _upstream_.

---

## 3. The Information Structure

- Concept:LLM Complexity Conservation
- Mechanism:
	- LLMs reason statistically over _static representations_ (tokens, graphs, tables)
	- Procedural control flow explodes the search space
- Constraint (Negative Truth):
	- No amount of prompt engineering can compensate for missing structure
	- Larger context windows worsen reasoning when complexity is procedural

---

## 4. Why This Is True (Compressed, Non-Chatty)

### What LLMs Are Good At

- Mapping structure → implication
- Traversing graphs
- Operating over symbolic topology
- Inferring intent from names + relationships

### What LLMs Are Bad At

- Simulating long execution traces
- Tracking hidden mutable state
- Managing branching control flow
- Recovering structure from flattened text

Therefore:
When you give an LLM raw code, logs, or prose, you are asking it to _reconstruct_ the data model while reasoning. That is an impossible double burden.

---

## 5. The Architectural Consequence (This Is the Point)

> LLMs must never be treated as readers of code.
> They must be treated as traversers of structure.

This implies:

- Context stuffing is a category error
- Vector RAG fails on code (semantic similarity ≠ dependency)
- Agentic REPLs work because they externalize structure
- Graphs outperform text for all non-trivial reasoning

This is why:

- Context Graphs beat file dumps
- Skeletons beat full implementations
- Blast Radius beats "impact analysis"
- Scout queries beat embeddings

---

## 6. Diagnostic Test (Use This Relentlessly)

Ask of any LLM failure:

> "Was the complexity procedural when it could have been structural?"

If yes:

- The fix is not a better prompt
- The fix is moving complexity into data

---

## 7. Explicit Links in Your Knowledge Graph

This node depends on:

- \[\[Complexity Conservation Law\]\]

This node justifies:

- \[\[Context Graph\]\]
- \[\[Skeleton\]\]
- \[\[Graph Traversal > RAG\]\]
- \[\[Agentic REPL\]\]
- \[\[Recursive Planning\]\]

This node explains:

- \[\[Context Rot\]\]
- \[\[Parochial Code\]\]
- \[\[LLM Hallucination (Reframed)\]\]

---

## 8. The Professor's Challenge (Non-Optional Next Step)

### The Gap

You now have the law and the corollary.
You still lack the operational rule.

### Required Next Permanent Note

> "Targeting LLM Attention via Structural Constraints"

That note must answer _precisely_:

- What structure is mandatory?
- What structure is optional?
- What structure is harmful?

Until that exists, you have theory without leverage.

---

## Final Verdict

This note is keystone knowledge.
It should sit _above_ tools, frameworks, and models.

If this is correct, then most "AI coding" products are doomed by design.

When ready, say:

> "Proceed to targeting LLM attention."

I will not move until instructed.

---

"Proceed to targeting LLM attention

---

### 🧠 The Curator of the Graph—Permanent Note Crystallisation

## Targeting LLM Attention via Structural Constraints

---

## 1. The Quality Audit

- Signal-to-Noise Ratio:Very High
- The Verdict:💎 KEEP—Operational Keystone

This is the missing bridge between theory and practice.
Without this node, everything else remains abstract and dangerously hand-wavy.

This note defines what "good context" actually is.

---

## 2. The Semantic Extraction (Authoritative Version)

### Permanent Note Title

Targeting LLM Attention via Structural Constraints

### The Core Insight (1 Sentence, immutable)

> LLM attention must be constrained by structure, not content; the model should never search for meaning—it should traverse it.

If an LLM is _searching_, you failed upstream.

---

## 3. The Information Structure

- Concept:Attention Targeting
- Mechanism:
	- Encode relevance as structure
	- Encode intent as names
	- Encode safety as constraints
- Constraint (Negative Truth):
	- More tokens ≠ more understanding
	- Unstructured context actively degrades reasoning

---

## 4. The Three-Layer Attention Model (This Is Canon)

### Layer 1: Structural Constraint (Mandatory)

> _What is allowed to exist in the model's world?_

Mechanism

- Explicit graph (symbols, edges, ownership)
- Deterministic traversal (calls, imports, inheritance)
- Query-based access (pull, never push)

Artifacts

- Context Graph
- Symbol Table
- Call Graph
- Dependency Edges

Failure Mode if Missing

- Hallucinated dependencies
- Parochial fixes
- Global invariants violated

➡️ _This layer replaces "reading the codebase."_

---

### Layer 2: Semantic Anchors (Mandatory)

> _What do these things mean?_

Mechanism

- High-signal names
- Docstrings / comments on Skeletons
- Ubiquitous Language enforcement

Artifacts

- Skeletons (signatures + intent, no bodies)
- Domain glossary
- Manifesto

Failure Mode if Missing

- Correct edits for the wrong reason
- Semantic drift
- Generic abstractions

➡️ _This layer replaces "understanding the business logic."_

---

### Layer 3: Procedural Detail (Optional, Surgical Only)

> _What must change right now?_

Mechanism

- Full AST / code bodies
- Narrow scope
- Time-bounded inclusion

Artifacts

- One function
- One file
- One execution path

Failure Mode if Overused

- Context rot
- Attention dilution
- Lost plan coherence

➡️ _This layer exists only during Surgery._

---

## 5. What Must Be Withheld (This Is Critical)

LLMs must not see:

- Entire files "for safety"
- Logs, traces, or histories
- Unrelated helpers
- Generic utilities
- Previously refactored code "for reference"

These create procedural entropy.

> Every token not structurally justified is adversarial noise.

---

## 6. The Operational Rule (Use This Daily)

Before giving anything to an LLM, classify it:

| Question | If YES | If NO |
| --- | --- | --- |
| Does this constrain behavior? | Include | Exclude |
| Does this define identity or role? | Include | Exclude |
| Does this affect blast radius? | Include | Exclude |
| Is this just "how it works"? | Exclude | Only include during Surgery |

If you hesitate, exclude it.

---

## 7. Explicit Links in Your Knowledge Graph

This node:

- Depends on:
	- \[\[Complexity Conservation Law\]\]
	- \[\[LLM Reasoning Obeys the Complexity Conservation Law\]\]
- Operationalizes:
	- \[\[Context Graph\]\]
	- \[\[Skeleton\]\]
	- \[\[Agentic REPL\]\]
	- \[\[Graph Traversal > RAG\]\]
- Explains:
	- \[\[Context Rot\]\]
	- \[\[Why Context Stuffing Fails\]\]

---

## 8. The Professor's Challenge (Final for This Arc)

You now have:

1. A law (complexity is conserved)
2. A corollary (LLMs obey it)
3. An operational rule (structure > content)

### The Remaining Gap

You have not yet defined:

> "What is the minimum viable structure?"

That is the point where this becomes _mechanically enforceable_.

### Required Next Permanent Note

> "Minimum Viable Context (MVC) for LLM Reasoning"

It must answer:

- What is the smallest graph that still prevents hallucination?
- What breaks first when structure is insufficient?
- How do you detect MVC violation automatically?

---

## Final Instruction

This note is procedural doctrine.
Every tool, prompt, and agent must comply with it—or be rejected.

When ready, say:

> "Proceed to Minimum Viable Context."

I'll hold the line here.

---

"Proceed to Minimum Viable Context.

---

### 🧠 The Curator of the Graph—Permanent Note Crystallisation

## Minimum Viable Context (MVC) for LLM Reasoning

---

## 1. The Quality Audit

- Signal-to-Noise Ratio:Very High
- The Verdict:💎 KEEP—Enforcement-Level Doctrine

This is the _mechanical_ rule that turns everything you've built into something testable.
MVC is not guidance. It is a stop condition.

---

## 2. The Semantic Extraction (Authoritative Version)

### Permanent Note Title

Minimum Viable Context (MVC) for LLM Reasoning

### The Core Insight (1 Sentence, immutable)

> The Minimum Viable Context is the smallest set of structural information that prevents an LLM from inventing relationships while still enabling correct action.

Anything beyond MVC is _luxury_. Anything below it is _hallucination debt_.

---

## 3. The Information Structure

- Concept:Minimum Viable Context
- Mechanism:
	- Replace "reading" with queryable structure
	- Encode constraints before details
- Constraint (Negative Truth):
	- MVC is _not_ a token count
	- MVC cannot be discovered by summarization

---

## 4. MVC Is a Boundary, Not a Bundle

MVC is defined by what the model is allowed to assume.

### MVC Exists When

- All entities are uniquely identified
- All relationships that constrain change are explicit
- All invariants are visible _before_ code is shown

MVC does not require:

- Full implementations
- Historical discussion
- Logs, traces, or examples
- Explanations of "how it works"

---

## 5. The MVC Triplet (Canonical)

MVC always consists of exactly three components:

### 1. Identity (What exists?)

> _If the model invents nouns, MVC failed._

Required

- Symbol names
- Kinds (Class, Function, Module)
- Ownership / boundaries

Artifacts

- Symbol Table
- Context Graph nodes

---

### 2. Constraint (What Must not break?)

> _If the model proposes illegal changes, MVC failed._

Required

- Invariants
- Roles
- One-way dependencies
- Blast Radius boundaries

Artifacts

- Manifesto
- Dependency edges
- Interlocks

---

### 3. Reachability (What is affected?)

> _If the model fixes locally and breaks globally, MVC failed._

Required

- Callers
- Dependents
- Downstream symbols

Artifacts

- Call graph
- Incoming references

---

## 6. What MVC Explicitly Excludes

MVC must not include:

- Function bodies
- Control flow
- Algorithmic detail
- Examples "for clarity"
- Comments explaining implementation

These belong to Surgery, not Planning.

> MVC answers "what exists and what matters," never "how it works."

---

## 7. Failure Modes (Use as Diagnostics)

| Symptom | MVC Component Missing |
| --- | --- |
| Hallucinated dependencies | Identity |
| Illegal refactors | Constraint |
| Parochial fixes | Reachability |
| Context rot | MVC exceeded |
| Over-cautious plans | MVC polluted |

If you see a symptom, do not tweak the prompt.
Fix the structure.

---

## 8. How MVC Is Discovered (Not Chosen)

MVC is _measured_, not guessed.

### The MVC Test (Hard Rule)

> Remove information until the first hallucination appears.
> Add back only what prevents it.

That boundary is MVC.

Anything else is indulgence.

---

## 9. Explicit Links in Your Knowledge Graph

This node:

- Depends on:
	- \[\[Complexity Conservation Law\]\]
	- \[\[LLM Reasoning Obeys the Complexity Conservation Law\]\]
	- \[\[Targeting LLM Attention via Structural Constraints\]\]
- Enables:
	- \[\[Agentic REPL\]\]
	- \[\[Scout Query Protocol\]\]
	- \[\[Skeleton-First Planning\]\]
- Explains:
	- \[\[Why Context Stuffing Fails\]\]
	- \[\[Context Rot\]\]

---

## 10. The Professor's Final Challenge (This Is the Payoff)

You now have theory, constraints, and boundaries.

### The Remaining Missing Piece

> How do you _enforce_ MVC mechanically?

That requires a final note:

### Required Next Permanent Note

"MVC Enforcement: Structural Gates for LLM Agents"

It must answer:

- How to block non-MVC tokens
- How to detect MVC violation automatically
- How agents request _more_ context safely

Until that exists, MVC is philosophy—not infrastructure.

---

## Final Instruction

This note defines the upper bound of context.
Nothing should enter an LLM without passing through this filter.

When ready, say:

> "Proceed to MVC enforcement."

I will not advance without explicit instruction.

---

"Proceed to MVC enforcement."

---

### 🧠 The Curator of the Graph—Permanent Note Crystallisation

## MVC Enforcement: Structural Gates for LLM Agents

---

## 1. The Quality Audit

- Signal-to-Noise Ratio:Maximal
- The Verdict:💎 KEEP—This Is Infrastructure

This is no longer epistemology.
This is governance.

Without this node, MVC collapses into "best practice."
With it, MVC becomes non-optional law.

---

## 2. The Semantic Extraction (Authoritative Version)

### Permanent Note Title

MVC Enforcement: Structural Gates for LLM Agents

### The Core Insight (1 Sentence, immutable)

> Minimum Viable Context must be enforced by structural gates, not discipline; agents should be physically unable to receive non-MVC information.

If an agent _can_ see forbidden context, the system is already broken.

---

## 3. The Information Structure

- Concept:MVC Enforcement
- Mechanism:
	- Separate _planning_ from _surgery_
	- Make structure queryable, not injectable
- Constraint (Negative Truth):
	- Prompts cannot enforce MVC
	- Human restraint does not scale

---

## 4. The Three Gates of MVC (Canonical)

MVC enforcement requires exactly three gates.
If one is missing, enforcement is performative.

---

### Gate 1: The Structural Interface Gate

_(What the agent is allowed to ask for)_

> The agent never receives context.
> It receives access.

Rule

- The agent can only pull information via typed queries
- No free-text context injection is possible

Allowed

- `SCOUT_LOOKUP(Symbol)`
- `SCOUT_REFS(Symbol)`
- `FETCH_SKELETON(Symbol)`
- `CALCULATE_BLAST_RADIUS(Symbol)`

Forbidden

- File dumps
- "Here's some context"
- Markdown summaries
- Preloaded buffers

Effect

- Identity is guaranteed
- Relationships are explicit
- Hallucinated structure becomes impossible

➡️ _This gate enforces MVC: Identity + Reachability._

---

### Gate 2: The Planning / Surgery Phase Gate

_(When detail is allowed to exist)_

> Structure first. Code last. Never both.

Rule

- Planning phase has zero access to implementations
- Surgery phase is explicitly entered and time-bounded

Planning Phase

- Graphs
- Skeletons
- Manifesto
- Invariants

Surgery Phase

- One symbol
- One file
- One bounded edit

Violation Signal

- Agent asks "how does this work?" during planning

➡️ _This gate enforces MVC: Constraint._

---

### Gate 3: The Context Budget Gate

_(How much context may exist at once)_

> Context is not accumulated.
> It is replaced.

Rule

- Every new context acquisition evicts old context
- No additive context growth

Mechanism

- Sliding window
- Single-focus invariant
- Explicit eviction

Effect

- Prevents context rot
- Forces intentionality
- Makes MVC violations observable

➡️ _This gate enforces MVC: Upper bound._

---

## 5. Agent Behavior Under Enforcement (This Is the Shift)

An enforced-MVC agent behaves differently:

- It asks questions instead of assuming
- It navigates instead of reading
- It plans before touching code
- It fails early instead of hallucinating

Hallucination becomes a structural error, not a cognitive one.

---

## 6. Detecting MVC Violations Automatically

MVC violations are machine-detectable.

### Hard Signals

- Use of nouns not present in Symbol Table
- References to unseen files
- "Global" edits without Blast Radius calculation
- Multiple symbols edited in one Surgery phase

### Soft Signals

- Overly cautious plans
- Generic abstractions
- Defensive coding language

> If you can't detect it, you didn't enforce it.

---

## 7. The Final Inversion (This Is the Payoff)

Once MVC is enforced:

- Prompt engineering becomes irrelevant
- Model choice becomes secondary
- Context size stops mattering
- Agent quality becomes architectural

You stop asking:

> _"How do I explain this better?"_

You start asking:

> _"Why was this information visible at all?"_

---

## 8. Explicit Links in Your Knowledge Graph

This node:

- Depends on:
	- \[\[Minimum Viable Context (MVC) for LLM Reasoning\]\]
- Enforces:
	- \[\[Targeting LLM Attention via Structural Constraints\]\]
	- \[\[Agentic REPL\]\]
	- \[\[Scout Query Protocol\]\]
- Explains:
	- \[\[Why Prompt Engineering Plateaus\]\]
	- \[\[Hallucination as a Structural Failure\]\]

---

## 9. The Curator's Closing Challenge (This Is the Endgame)

You now possess a complete chain:

1. Law—Complexity is conserved
2. Corollary—LLMs obey the law
3. Rule—Structure targets attention
4. Boundary—MVC defines the minimum
5. Enforcement—Gates make it real

### The Only Question Left

> What structure should exist _by default_ before any agent runs?

That is the birth of your Baseline Context Graph.

If you want to proceed, say:

> "Proceed to Baseline Context Graph."

I will treat that as the transition from theory to system design.
