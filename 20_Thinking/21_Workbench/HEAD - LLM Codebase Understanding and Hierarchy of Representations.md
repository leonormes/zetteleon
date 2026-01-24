---
created: 2026-01-24T08:42:45+00:00
modified: 2026-01-24T09:44:22+00:00
title: HEAD - LLM Codebase Understanding and Hierarchy of Representations
---

This note synthesizes key concepts regarding how Large Language Models (LLMs) "understand" a codebase, moving beyond simple text processing to structural and semantic reasoning.

## 1. The Core Challenge: Understanding vs. Processing

"Understanding" for an LLM is a probabilistic approximation of meaning. The goal is to bridge the "Semantic Gap" between the code's implementation (syntax) and its intent (domain).

"Understanding" for an LLM is simply having the right dependencies in the prompt.

- Without Graph: You might paste `calc_bonus`. The LLM changes it. But you forgot `Invoice` calls it, and now `Invoice` is broken.
- With Graph: The system pulls in `Invoice` (as a signature). The LLM sees the signature and thinks: _"Ah, I must ensure my change to `calc_bonus` still returns the data type `Invoice` expects."_

[[HEAD Can a whole code base be represented as a data structure]]

## 2. The Hierarchy of Representations

To represent a whole codebase, we must layer different types of structures. No single view is sufficient.

### A. The Tree: Abstract Syntax Tree (AST)

- Scope: Single file or code snippet.
- Function: Parses the grammatical structure (e.g., `VariableDeclaration`, `CallExpression`).
- Role: Acts as the "Structured Schema" for code.
- Limitation: It is parochial; unaware of other files or system-wide context.

The AST breaks a file down into nodes… It acts as the source of truth. It transforms code from unstructured text into a Knowledge Graph, enabling "Deterministic Retrieval" where relationships are known facts rather than probabilistic guesses.

—[[Abstract Syntax Trees#1 The AST as a Structured Schema]]

### B. The Graph: Control Flow Graph (CFG)

- Scope: Single function or method.
- Function: Maps the order of execution (loops, branches).
- Role: Useful for understanding logic complexity (cyclomatic complexity).

A `while` loop creates a cycle in the graph. An `if/else` statement splits the graph into two paths that eventually merge back together.

—[[HEAD Can a whole code base be represented as a data structure#B The Graph Control Flow Graph CFG]]

### C. The Network: Code Property Graph (CPG) / Repository Intelligence Graph (RIG)

- Scope: The entire codebase ("The God View").
- Function: Connects ASTs via relationships (`calls`, `inherits_from`, `imports`).
- Role: Represents "Code-as-System" rather than "Code-as-Text".

The RIG represents a paradigm shift from "Code-as-Text" to "Code-as-System." … The RIG is a deterministic, evidence-backed architectural map derived from the build system itself.

—[[LLM Codebase Comprehension Roadmap#1 2 The Repository Intelligence Graph RIG Deterministic Grounding]]

### D. The Semantic Graph (Information Structure)

- Scope: The "Meaning" / Domain Intent.
- Function: Distorts "geography" (files) to show "topology" (logic/data flow).
- Role: Minimizes "noise" (syntax) to maximize "signal" (meaning).

The Semantic Graph is the Tube Map of your software. We strip the "streets" (syntax) so the LLM can see the "lines" (logic flow).

…

You are functioning as a Lossy Compression Algorithm (like JPEG).

- You throw away the pixel data (the syntax).
- You keep the edge data (the logic).

—[[HEAD Can a whole code base be represented as a data structure#3 The Visual Metaphor Topology over Geography]]

## 3. Strategies for Context & Understanding

### A. The "Linker's View" vs. The "Editor's View"

Humans need files to manage cognitive load ("Human Management Overhead"). Machines (and LLMs) prefer the "Linker's View"—a continuous stream of logic.

Imagine your entire codebase not as a folder of files, but as a single, infinite canvas where every function exists side-by-side.

- Imports are just wires.
- Files are just arbitrary boxes.

—[[HEAD Can a whole code base be represented as a data structure#2 The Mental Model "The Linker's View"]]

### B. Skeletonization (The Symbol Table)

Using the "Symbol Table" strategy (Signatures + Docstrings) allows us to send the "Machine Contract" and "Human Description" without the implementation details.

- The Docstrings/Comments represent the "Human Description" (Party A).
- The Function Signatures/Types represent the "Machine Contract" (Party B).
By feeding the LLM _both_ in a skeleton format, you are giving it the full picture of the negotiation without the noise.

—[[HEAD Can a whole code base be represented as a data structure#4 The Synthesis Code as a Negotiation]]

### C. Data Lineage (The Maze)

For "Complex" systems (with state and side effects), static graphs fail. We need to track the "Path of the Mouse" (Data Lineage).

Instead of asking: _"What does this class do?"_ (which describes the walls), We represent the meaning by asking: _"Where does this specific piece of data go?"_

—[[HEAD Can a whole code base be represented as a data structure#The "Data-Path" Representation]]

### D. Meta-Context & Domain Manifesto

To prevent "Perspective Drift" (LLM defaulting to average training data), we must inject a "Meta-Context" or "Domain Manifesto".

Meta-Context: Acts as the "Superego," preventing the generation of architecturally invalid code patterns.

…

Domain Manifesto: A structured block that defines the reality of the software (Core Entities, Allowed Flows, Strict Boundaries).

—[[LLM Codebase Comprehension Roadmap#3 1 The Layered Cognitive Model]]

—[[HEAD Can a whole code base be represented as a data structure#The "Domain Header" Strategy]]

### E. Ubiquitous Language (Vector Anchoring)

Using consistent, domain-specific terminology anchors the LLM's latent space to the correct concepts.

If you use the word `Item`, the LLM is in the generic "Shopping" region of its brain.

If you use the word `SkuVariant`, you instantly drag the LLM into the "Professional E-commerce" region.

—[[HEAD Can a whole code base be represented as a data structure#Level 3 Domain Terminology High Value]]

## 4. Advanced Tooling & Architectures

- Tree-sitter: Used for "Chunk Twice, Retrieve Once"—extracting valid Semantic Entities (functions, classes) rather than arbitrary text chunks. [[LLM Codebase Comprehension Roadmap#1 3 Tree-sitter and Syntactic Scope Awareness]]
- HyDE (Hypothetical Document Embeddings): Generates hypothetical reasoning or code to bridge the semantic gap (finding the "why"). [[LLM Codebase Comprehension Roadmap#2 1 HyDE Bridging the Semantic Gap in Code]]
- Neuro-Symbolic Agents: Integrating Symbolic Execution (SMT Solvers) to provide mathematical guarantees on correctness. [[LLM Codebase Comprehension Roadmap#4 2 Neuro-Symbolic Agents Beyond Probabilistic Generation]]

## 5. Summary: Information vs. Data

- Data: The raw facts (AST, syntax). High Entropy.
- Information: Data + Context (Symbol Table). Low Entropy.
- Goal: Reduce the "Entropy" of the prompt.

By converting your code into an Information Structure, you are literally reducing the entropy of the prompt. You are making the "meaning" inevitable rather than probable.

—[[HEAD Can a whole code base be represented as a data structure#5 The "Information Entropy" Argument]]

## 6. Mechanistic Understanding & Operational Strategies

### A. "Understanding" as Contextual Fidelity

Mechanistically, an LLM does not "understand" code. It has High Contextual Fidelity and Semantic Reachability.

- Context Window Saturation: "Understanding" is limited to what fits in RAM (the context window).
- Token Co-occurrence: "Understanding" is a function of probability. Standard patterns (React hooks) have sharp probability distributions; custom "magic" frameworks have high entropy (confusion).
- Symbol Resolution: True understanding requires tracing definitions. If a symbol's definition is not in the prompt, the model guesses (hallucinates).

The Verdict: An LLM understands a codebase only to the extent that you can fit the relevant dependency graph into its active context window.

—[[AI Code Understanding and Quality#Part 1 What is "Understanding" in an LLM?]]

### B. AI-Native Code Standards

To maximize Model Parseability, code should be written for agents, not just humans.

1. Explicitness over Magic: Avoid "implicit" frameworks (e.g., Rails magic). Explicit imports and config anchor the model.
2. Strong Typing as Anchors: Types (TS Interfaces, Rust Structs) restrict the search space for the next token.
3. Atomic Context Units: Functions should fit in a single retrieval chunk (<40 lines).
4. Comments as System Prompts: Docstrings should define _Invariants_ and _Intent_, acting as mini-system prompts.

### C. The Cartographer & Dependency Subgraphs

The "Cartographer" is a role/agent that acts as a Graph Pruner.

- It does not dump the whole CFG (too noisy).
- It injects a Dependency Subgraph containing only nodes within 1-2 degrees of separation ("Impact Radius").
- It enforces Graph Integrity: checking upstream/downstream edges before modification.

## 7. The Problem of Context Rot

Simply increasing context windows (e.g., 1M tokens) fails due to Context Rot.

- Primacy/Recency Bias: Information in the middle of a large prompt is frequently lost.
- Distractors: Semantically similar but irrelevant code (e.g., mocks, legacy versions) confuse the attention mechanism more than random noise.

### Hybrid "Just-in-Time" Architectures

The solution is a hybrid approach:

1. Graph Navigation (Cheap): Agent queries the graph to find structure.
2. Vector/Text Inspection (Expensive): Agent loads _only_ the specific node's text into the context window.
This combines the precision of the Graph with the semantic understanding of the LLM.

—[[LLM Codebase Interaction Validity Check#3 3 Hybrid "Just-in-Time" Architectures]]

## 8. Principal Architect Audit: Mechanistic Rigor

### A. Anthropomorphism Audit (Logic Falsification)

The following instances in this note assign biological cognition to statistical engines and must be refactored:

1. Section 1 (The LLM "Thinks"): "…the LLM sees the signature and thinks: 'Ah, I must ensure…'"
   - Status: CRITICAL FAIL. Models do not "think" or have obligations.
   - Correction: The presence of the signature in the context window increases the probability of token alignment with return type constraints via high-order correlations.
2. Section 3A (The "Linker's View"): "…LLMs prefer the 'Linker's View'…"
   - Status: FAIL. Machines possess no preferences.
   - Correction: Flattened token streams minimize symbol resolution overhead, optimizing the Signal-to-Noise Ratio (SNR).
3. Section 1 (The "Semantic Gap"): "…bridge the 'Semantic Gap' between… implementation and its intent."
   - Status: WARN. Intent is unobservable.
   - Correction: The model maps statistical distance between natural language specifications (docstrings) and syntactic structures.

### B. Mechanistic Rewrite: The Core Theory

Subject: Transitioning from "Understanding" to Latent Topological Mapping (LTM).

An LLM does not "understand" a codebase. It functions as a Predictive State-Transfer engine. It receives `State_A` (Current Code + Prompt) and predicts `State_B` (Modified Code). Reliability is achieved by biasing the context to render invalid states statistically improbable using deterministic invariants (ASTs, RIGs).

### C. Technical Definition: Codebase Comprehension

For a peer-reviewed context, "Comprehension" is defined as:

1. The successful Isomorphism between the repository's Static Analysis Graph (RIG) and the Model's Transient Attention State.
2. A state where generated token streams satisfy a Verification Loop (AST validity + Type Safety) without violating pre-computed dependency constraints.
3. Measured inversely by the Hallucination Rate ($H_r$) of non-existent symbols per 1k tokens.

### D. Operational Critique: Attention Dilution vs. Infinite Canvas

The "infinite canvas" model (Section 3A) is mathematically dangerous due to Attention Dilution. As the context window ($N$) grows, the effective retrieval accuracy often degrades despite $O(N^2)$ compute costs.

Mandatory Constraint: Implement a Minimum Viable Context (MVC) strategy. Do not feed the whole structure. Feed only the Dependency Subgraph $G'$ where all nodes $n$ are within distance $d \le 2$ of the target symbol.

### E. The Verification Loop (Final Guardrail)

To prevent "Perspective Drift," any neuro-symbolic agent must implement a binary gate:

1. Input: Request + Dependency Subgraph.
2. Output: LLM-generated code.
3. Verification: Run `ast-grep` or `tree-sitter` on the output. If a symbol is called that is not present in the RIG, the state is REJECTED and fed back into the loop as an error signal.
1. Anthropomorphism audit—3 concrete violations

(A) "The LLM sees the signature and thinks…"

This assigns deliberative cognition + obligation. Mechanistically, the signature's presence in the prompt increases the conditional probability mass on continuations consistent with the observed type/shape constraints. No "must," no internal goal state—just next-token likelihood shifts.

(B) "LLMs prefer the 'Linker's View'…"

"Prefer" implies an agent with utility. What's actually happening is: certain context layouts reduce symbol-resolution uncertainty and increase local coherence under attention constraints. It's an optimization artifact, not preference.

(C) "Bridge the Semantic Gap between implementation and intent"

"Intent" is not a repository-native observable. The only observables are code tokens + build artifacts + tests + comments + external specs. The model can form a Latent Topological Mapping between natural-language descriptions and code structures, but "intent" is an external hypothesis unless grounded by constraints.

---

1. Mechanistic rewrite of the core theory (systems-design language)

Core claim (reframed):

An LLM is not a codebase knower. It is a Predictive State-Transfer function:

f_\theta: (S_t, C_t) \rightarrow \hat{S}_{t+1}

Where:

 = current repository state (or a partial projection of it)

 = injected context (retrieved artifacts, constraints, policies)

 = predicted next state (patch, edit, explanation)

"Codebase comprehension" emerges only when the injected context contains sufficient constraint coverage over the repository's dependency surface so that invalid transitions become statistically unlikely and deterministically rejectable.

In practice, stability requires a hybrid controller:

Deterministic substrate: AST/CFG/CPG (your RIG) as the canonical constraint store.

Probabilistic generator: LLM proposes candidate state transitions.

Verification loop gate: compilation / typecheck / unit tests / graph-consistency checks reject invalid deltas.

This makes "comprehension" a property of the closed-loop system, not of the model in isolation.

---

1. Technically defensible definition of "Codebase Comprehension" (peer-review safe)

Avoid "understanding." Use an operational, falsifiable definition:

Definition (Codebase Comprehension):

A model exhibits codebase comprehension for a task over repository iff there exists a retrieval + control procedure such that the model's generated edits produce a repository transition satisfying:

1. Graph-consistency constraint
All referenced symbols in are resolvable in a static repository index (e.g., call graph / import graph / symbol table), i.e. no Hallucinated Dependencies.

2. Syntactic + structural validity
The edit preserves language well-formedness (AST-parseable) and respects structural constraints (e.g., type signatures, module boundaries).

3. Verification Loop success (mandatory determinism)
The edit passes a deterministic acceptance test suite (at minimum: parse + build/typecheck; ideally: unit/integration tests).

4. Bounded error rate under distribution shift
Under perturbations of context (partial retrieval, distractors, refactors), failure modes remain measurable via:

Hallucination Rate: nonexistent symbol references per k tokens or per patch

Regression Rate: failing tests introduced per accepted patch

In short: "comprehension" = the ability to produce verified, dependency-consistent state transitions using constrained context projections of the repo.

---

Required critique: RAG vs Long-Context + attention dilution (your note partially accounts for it)

You explicitly identify "Context Rot," primacy/recency bias, and distractors, which is the right direction.

But you should tighten the causal claim:

Long-context does not monotonically improve performance because attention allocation is not equivalent to perfect memory addressing. Even if compute grows, retrieval precision inside the window can degrade when semantically-similar distractors exist (Attention Dilution).

Your proposed solution ("Hybrid Just-in-Time architectures") is the correct systems move: treat the LLM as the generator inside a retrieval-controlled loop, not as a full-repo emulator.

---

Falsification demand: "it knows the code" must answer hallucinated dependencies

Your note says: "If a symbol's definition is not in the prompt, the model guesses (hallucinates)."

Push it harder:

> If the model emits a call to calc_bonus_v2() that does not exist in, your system must treat that as hard failure, not "low confidence."

That is the key difference between narrative framing and mechanistic rigor: invalid symbol resolution is not an opinion—it is a falsifiable error.

---

If you want, I can compress the rewritten definition into a thesis-ready paragraph, plus a metrics section (Hr, Rr, context-size sensitivity curves) that reads like a systems paper rather than an essay.

Below is a thesis-ready paragraph + a metrics/evaluation section written in systems-paper language, with your required terminology enforced.

---

Thesis-ready paragraph (drop-in)

In this work, "LLM codebase comprehension" is not treated as an intrinsic cognitive property of a model, but as an operational capability of a closed-loop system that couples a probabilistic generator with deterministic repository constraints. The LLM performs Predictive State-Transfer by proposing code edits conditioned on a bounded context projection of the repository, while a retrieval and indexing layer provides a structured constraint substrate (e.g., symbol tables, dependency graphs, and AST-derived representations). The model's apparent "understanding" is more precisely described as a Latent Topological Mapping between token sequences representing repository artifacts and token sequences representing intended edits, mediated by retrieval policy and attention allocation. Under this framing, success is measurable only through deterministic gates—static validation and executable tests—that reject invalid transitions such as unresolved references and type violations. Consequently, codebase comprehension is defined by the system's ability to generate dependency-consistent, verifiable repository state transitions under bounded context and distributional perturbations, rather than by any claim of global repository awareness.

---

Metrics & evaluation protocol (peer-review defensible)

1. Primary success criteria (hard gates)

A proposed patch is accepted iff it passes all gates in the Verification Loop:

1. AST Validity Gate

\text{parse}(\Delta) = \text{true}

1. Symbol Resolution Gate (anti-hallucination)
Let be a repository index (symbol table + import graph + call graph approximation).

\forall s \in \text{Refs}(\Delta): s \in \text{Symbols}(G_R)

1. Typecheck / Build Gate (language dependent)

\text{build}(R+\Delta)=\text{success}

1. Unit / Integration Test Gate

\text{tests}(R+\Delta)=\text{pass}

These gates force determinism: the model is never credited for "nearly correct" edits that cannot execute.

---

1. Quantitative metrics (reportable)

A. Verified Patch Rate (VPR)

Fraction of attempts producing an accepted patch:

\text{VPR} = \frac{\#\text{accepted patches}}{\#\text{total attempts}}

B. Hallucinated Dependency Rate (HDR)

Count nonexistent symbol references per patch (or per 1k generated tokens):

\text{HDR} = \mathbb{E}\left[\frac{\#\text{unresolved refs in }\Delta}{1}\right]

\text{HDR}_{1k}=\frac{\#\text{unresolved refs}}{\#\text{tokens}/1000}

C. Regression Introduction Rate (RIR)

Among accepted patches, how often new failures appear in non-target tests:

\text{RIR} = \frac{\#\text{patches that break previously passing tests}}{\#\text{accepted patches}}

D. Edit Locality / Blast Radius (BR)

Measures whether changes are tightly scoped or spread across the repo:

\text{BR}=\#\text{files changed} \quad\text{and}\quad \#\text{LOC changed}

E. Retrieval Sensitivity Curve (RSC)

Run the same task under varying retrieval budgets and measure VPR/HDR:

k \in \{5, 10, 20, 50, 100\}

VPR vs

HDR vs

This directly tests your RAG-vs-context hypothesis.

---

1. RAG vs long-context: explicit experiment design

Condition set

LC (Long-Context Only): shove as much as possible into the window.

RAG: retrieve topartifacts (signatures, call sites, tests, docs).

Hybrid: retrieve + also include "structural skeleton" (symbols + edges summary).

Measure Attention Dilution

You can operationalize Attention Dilution as the probability that a critical dependency is ignored despite being present.

Define critical evidence (e.g., the correct function signature, required import, or test expectation).

Log whether appears in the prompt, and whether the patch respects it.

\text{AD} = P(\text{violates }E \mid E \in C_t)

If AD increases with longer contexts (or with distractor injection), you've shown dilution empirically.

---

1. Negative controls (falsification, not vibes)

To prevent the work from becoming "it works because it works," add controlled sabotage:

A. Distractor Injection Test Include a near-duplicate symbol or outdated signature. Measure change in HDR and VPR.

B. Refactor Perturbation Rename internal modules, move files, alter import paths. Measure degradation.

C. Partial Retrieval Failure Drop a key file from retrieval. Quantify failure mode shifts:

more hallucinated dependencies?

more wrong call patterns?

more test mismatches?

This pins behavior to constraints and retrieval fidelity, not "understanding."

---

Short definition block (for the paper's Definitions section)

Codebase Comprehension (operational):

A system exhibits codebase comprehension on repository for task iff, using bounded context and deterministic verification, it produces repository transitions such that:

1. is syntactically valid,
2. all referenced symbols resolve in a static index of (no Hallucinated Dependencies), and
3. passes the Verification Loop (build/typecheck/tests) at a rate exceeding a baseline threshold under controlled perturbations.

---

If you want the next step: I can rewrite your entire note into a paper-style section structure ("Problem," "Model," "Failure Modes," "Evaluation," "Threats to Validity") while preserving your original ideas but stripping all anthropomorphic phrasing.
