---
created: 2026-01-24T08:42:45+00:00
modified: 2026-02-04T07:27:51+00:00
tags: [llm-understanding]
title: LLM Codebase Understanding and Hierarchy of Representations
type: SoT
---

This note synthesizes key concepts regarding how Large Language Models (LLMs) "understand" a codebase, moving beyond simple text processing to structural and semantic reasoning.

## 1. The Core Challenge: Understanding vs. Processing

"Understanding" for an LLM is a probabilistic approximation of meaning. The goal is to bridge the "Semantic Gap" between the code's implementation (syntax) and its intent (domain).

"Understanding" for an LLM is simply having the right dependencies in the prompt.

- Without Graph: You might paste `calc_bonus`. The LLM changes it. But you forgot `Invoice` calls it, and now `Invoice` is broken.
- With Graph: The system pulls in `Invoice` (as a signature). The LLM sees the signature and thinks: _"Ah, I must ensure my change to `calc_bonus` still returns the data type `Invoice` expects."_

## 2. The Hierarchy of Representations

To represent a whole codebase, we must layer different types of structures. No single view is sufficient.

### A. The Tree: Abstract Syntax Tree (AST)

- Scope: Single file or code snippet.
- Function: Parses the grammatical structure (e.g., `VariableDeclaration`, `CallExpression`).
- Role: Acts as the "Structured Schema" for code.
- Limitation: It is parochial; unaware of other files or system-wide context.

The AST breaks a file down into nodes… It acts as the source of truth. It transforms code from unstructured text into a Knowledge Graph, enabling "Deterministic Retrieval" where relationships are known facts rather than probabilistic guesses.

### B. The Graph: Control Flow Graph (CFG)

- Scope: Single function or method.
- Function: Maps the order of execution (loops, branches).
- Role: Useful for understanding logic complexity (cyclomatic complexity).

A `while` loop creates a cycle in the graph. An `if/else` statement splits the graph into two paths that eventually merge back together.

### C. The Network: Code Property Graph (CPG) / Repository Intelligence Graph (RIG)

- Scope: The entire codebase ("The God View").
- Function: Connects ASTs via relationships (`calls`, `inherits_from`, `imports`).
- Role: Represents "Code-as-System" rather than "Code-as-Text".

The RIG represents a paradigm shift from "Code-as-Text" to "Code-as-System." … The RIG is a deterministic, evidence-backed architectural map derived from the build system itself.

### D. The Semantic Graph (Information Structure)

- Scope: The "Meaning" / Domain Intent.
- Function: Distorts "geography" (files) to show "topology" (logic/data flow).
- Role: Minimizes "noise" (syntax) to maximize "signal" (meaning).

The Semantic Graph is the Tube Map of your software. We strip the "streets" (syntax) so the LLM can see the "lines" (logic flow).

## 3. Strategies for Context & Understanding

### A. The "Linker's View" vs. The "Editor's View"

Humans need files to manage cognitive load ("Human Management Overhead"). Machines (and LLMs) prefer the "Linker's View"—a continuous stream of logic.

Imagine your entire codebase not as a folder of files, but as a single, infinite canvas where every function exists side-by-side.

- Imports are just wires.
- Files are just arbitrary boxes.

### B. Skeletonization (The Symbol Table)

Using the "Symbol Table" strategy (Signatures + Docstrings) allows us to send the "Machine Contract" and "Human Description" without the implementation details.

- The Docstrings/Comments represent the "Human Description" (Party A).
- The Function Signatures/Types represent the "Machine Contract" (Party B).
By feeding the LLM _both_ in a skeleton format, you are giving it the full picture of the negotiation without the noise.

### C. Data Lineage (The Maze)

For "Complex" systems (with state and side effects), static graphs fail. We need to track the "Path of the Mouse" (Data Lineage).

Instead of asking: _"What does this class do?"_ (which describes the walls), We represent the meaning by asking: _"Where does this specific piece of data go?"_

### D. Literate Programming as Context

Literate Programming (Knuth) is the ultimate format for LLMs because it orders code by _narrative intent_ rather than _compilation order_.

- Intent is Explicit: The prose explains _why_ the code exists before the code is even shown.
- Hierarchical Understanding: Chunks (e.g., `<<The Main Program Loop>>`) act as summaries. The LLM can understand the architecture from the chunks without needing the implementation details of every sub-chunk.
- Compression: Providing a "Weaved" document allows the LLM to skip the "Tangled" implementation details (syntactic noise) while retaining the full logic structure.

### E. Meta-Context & Domain Manifesto

To prevent "Perspective Drift" (LLM defaulting to average training data), we must inject a "Meta-Context" or "Domain Manifesto".

Meta-Context: Acts as the "Superego," preventing the generation of architecturally invalid code patterns.

Domain Manifesto: A structured block that defines the reality of the software (Core Entities, Allowed Flows, Strict Boundaries).

### F. Ubiquitous Language (Vector Anchoring)

Using consistent, domain-specific terminology anchors the LLM's latent space to the correct concepts.

If you use the word `Item`, the LLM is in the generic "Shopping" region of its brain.

If you use the word `SkuVariant`, you instantly drag the LLM into the "Professional E-commerce" region.

## 4. Advanced Tooling & Architectures

- Advanced Tooling: For a deep dive into the comparative architecture of modern tools, see [[SoT - Google Antigravity vs Tree-sitter]].
- Complexity Laws: For the underlying physics of software complexity, see [[SoT - Conservation of Complexity]] and [[SoT - LLM Reasoning Obeys the Complexity Conservation Law]].
- Tree-sitter: Used for "Chunk Twice, Retrieve Once"—extracting valid Semantic Entities (functions, classes) rather than arbitrary text chunks.
- HyDE (Hypothetical Document Embeddings): Generates hypothetical reasoning or code to bridge the semantic gap (finding the "why").
- Neuro-Symbolic Agents: Integrating Symbolic Execution (SMT Solvers) to provide mathematical guarantees on correctness.

## 5. Foundational Laws of Complexity

The strategies outlined in this note are grounded in two foundational laws:

1. Conservation of Complexity (Tesler's Law): Complexity cannot be removed, only moved. We choose to move it from dynamic logic (code) into static representation (data structures). See [[SoT - Conservation of Complexity]].
2. LLM Complexity Corollary: LLMs reason more effectively over structural constraints than procedural entropy. High-density context (Skeletons) reduces perplexity and prevents hallucination. See [[SoT - LLM Reasoning Obeys the Complexity Conservation Law]].

## 6. Summary: Information vs. Data

- Data: The raw facts (AST, syntax). High Entropy.
- Information: Data + Context (Symbol Table). Low Entropy.
- Goal: Reduce the "Entropy" of the prompt.

By converting your code into an Information Structure, you are literally reducing the entropy of the prompt. You are making the "meaning" inevitable rather than probable.

## 6. Mechanistic Understanding & Operational Strategies

### A. "Understanding" as Contextual Fidelity

Mechanistically, an LLM does not "understand" code. It has High Contextual Fidelity and Semantic Reachability.

- Context Window Saturation: "Understanding" is limited to what fits in RAM (the context window).
- Token Co-occurrence: "Understanding" is a function of probability. Standard patterns (React hooks) have sharp probability distributions; custom "magic" frameworks have high entropy (confusion).
- Symbol Resolution: True understanding requires tracing definitions. If a symbol's definition is not in the prompt, the model guesses (hallucinates).

The Verdict: An LLM understands a codebase only to the extent that you can fit the relevant dependency graph into its active context window.

### B. AI-Native Code Standards

To maximize Model Parseability, code should be written for agents, not just humans. See [[AI-Native Code Generator]] for the operational protocol.

1. Explicitness over Magic: Avoid "implicit" frameworks (e.g., Rails magic). Explicit imports and config anchor the model.
2. Strong Typing as Anchors: Types (TS Interfaces, Rust Structs) restrict the search space for the next token.
3. Atomic Context Units: Functions should fit in a single retrieval chunk (<40 lines).
4. Comments as System Prompts: Docstrings should define _Invariants_ and _Intent_, acting as mini-system prompts.

### C. The Cartographer & Dependency Subgraphs

The "Cartographer" is a role/agent that acts as a Graph Pruner. See [[The Code Cartographer]] for the specific system prompt.

- It does not dump the whole CFG (too noisy).
- It injects a Dependency Subgraph containing only nodes within 1-2 degrees of separation ("Impact Radius").
- It enforces Graph Integrity: checking upstream/downstream edges before modification.

## 7. The Problem of Context Rot

Simply increasing context windows (e.g., 1M tokens) fails due to Context Rot.

- Primacy/Recency Bias: Information in the middle of a large prompt is frequently lost.
- Distractors: Semantically similar but irrelevant code (e.g., mocks, legacy versions) confuse the attention mechanism more than random noise.

### Recursive Language Models (RLMs)

The solution is to move from "Linear Reading" to "Recursive Exploration". See [[SoT - Recursive Language Models]] for the detailed theory.

The Hybrid Loop:

1. Graph Navigation (Cheap): Agent queries the graph to find structure.
2. Vector/Text Inspection (Expensive): Agent loads _only_ the specific node's text into the context window.

This architecture requires a REPL loop where the agent can `THOUGHT` -> `ACTION` -> `OBSERVATION`. See [[The Recursive Architect]] for the system prompt.

## 8. Principal Architect Audit: Mechanistic Rigor

### A. Anthropomorphism Audit (Logic Falsification)

The following instances assign biological cognition to statistical engines and must be refactored:

1. "The LLM sees the signature and thinks…"
   - _Status:_ CRITICAL FAIL. Models do not "think".
   - _Correction:_ The presence of the signature increases the probability of token alignment with return type constraints.
2. "LLMs prefer the 'Linker's View'…"
   - _Status:_ FAIL. Machines possess no preferences.
   - _Correction:_ Flattened token streams minimize symbol resolution overhead, optimizing the Signal-to-Noise Ratio (SNR).
3. "Bridge the 'Semantic Gap' between intent…"
   - _Status:_ WARN. Intent is unobservable.
   - _Correction:_ The model maps statistical distance between natural language specifications (docstrings) and syntactic structures.

### B. Technical Definition: Codebase Comprehension

"Comprehension" is defined as:

1. The successful Isomorphism between the repository's Static Analysis Graph (RIG) and the Model's Transient Attention State.
2. A state where generated token streams satisfy a Verification Loop (AST validity + Type Safety) without violating pre-computed dependency constraints.
3. Measured inversely by the Hallucination Rate ($H_r$) of non-existent symbols per 1k tokens.

### C. Operational Critique: Attention Dilution

The "infinite canvas" model is mathematically dangerous due to Attention Dilution. As the context window ($N$) grows, the effective retrieval accuracy often degrades.

Mandatory Constraint: Implement a Minimum Viable Context (MVC) strategy. Do not feed the whole structure. Feed only the Dependency Subgraph $G'$ where all nodes $n$ are within distance $d \le 2$ of the target symbol.
