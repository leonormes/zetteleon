---
type: tmp_atoms
status: tmp
source_title: "AI Agent Architecture and the Modern Tech Stack"
source_url: "https://gemini.google.com/app/509937047bd0b955"
captured_utc: "2026-04-08T16:03:57+01:00"
signal_to_noise: "35% signal / 65% noise"
---

- Discarded hypothetical corporate scenarios and repetitive coding tutorial narratives.
- Discarded line-by-line lab walk-throughs and virtual environment setup instructions.
- Discarded promotional language regarding LangChain as an "essential" foundation.

### Atom 1: LLM Context Constraints
- Kind: constraint
- Statement: Large Language Models are limited by a finite token-based context window that functions as short-term memory.
- Scope & Conditions: Expanding this window increases latency and cost, necessitating external memory solutions.
- Evidence: "LLMs are constrained by a context window (measured in tokens), which functions as short-term memory. Expanding this window increases latency and cost..."
- Implications:
    - Long-term information must be stored externally (e.g., vector databases).
    - Developers must prioritise and compress information to fit within token limits.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [llm, context-window, memory, tokens]

### Atom 2: Semantic Search via Embeddings
- Kind: mechanism
- Statement: Text is converted into numerical vectors that capture semantic relationships, allowing retrieval based on conceptual meaning rather than keyword matching.
- Scope & Conditions: Typically involves high-dimensional arrays (e.g., 1536 dimensions) and similarity scoring.
- Evidence: "Text is converted into numerical arrays (vectors...) that capture semantic relationships... allowing retrieval by conceptual meaning rather than exact keyword matching."
- Implications:
    - Enables "fuzzy" search for relevant context.
    - Requires document chunking with overlap to preserve context during vectorisation.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [embeddings, vector-database, semantic-search, nlp]

### Atom 3: Retrieval-Augmented Generation (RAG)
- Kind: mechanism
- Statement: RAG is a pipeline that dynamically injects relevant data from external sources into an LLM's prompt to ground the model in current or private information.
- Scope & Conditions: Bypasses the need for expensive fine-tuning of the underlying model.
- Evidence: "A pipeline that queries a vector database for relevant information and dynamically injects it into the LLM's prompt... without the need to fine-tune."
- Implications:
    - Connects static models to real-time or proprietary data.
    - Reduces hallucinations by providing verifiable source material.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [rag, llm, data-retrieval, grounding]

### Atom 4: Prompt Architecture Levels
- Kind: distinction
- Statement: Prompt engineering techniques range from zero-shot instructions to few-shot templates and chain-of-thought reasoning.
- Scope & Conditions: Used to restrict model behaviour and format outputs.
- Evidence: "Techniques to restrict model behaviour... range from zero-shot (direct instruction) to few-shot (providing templates...) and chain-of-thought (forcing sequential... reasoning)."
- Implications:
    - Increases predictability of model responses.
    - Enables complex task decomposition through step-by-step logic.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [prompt-engineering, zero-shot, few-shot, chain-of-thought]

### Atom 5: Graph-Based Orchestration
- Kind: mechanism
- Statement: Stateful, graph-based workflows enable loops, conditional routing, and persistent data states across multiple execution steps in AI applications.
- Scope & Conditions: Often implemented via frameworks like LangGraph.
- Evidence: "LangGraph extends this into stateful, graph-based workflows, enabling loops, conditional routing, and persistent data states across multiple execution steps."
- Implications:
    - Allows for complex, multi-turn agent logic.
    - Replaces linear chains with more flexible state machines.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [orchestration, langgraph, state-machines, ai-agents]

### Atom 6: Model Context Protocol (MCP)
- Kind: definition
- Statement: The Model Context Protocol is a standardised communication interface that allows AI agents to interact with external tools and databases using a uniform schema.
- Scope & Conditions: Functions as a universal "OpenAPI specification" for LLMs to interpret tools without bespoke integration code.
- Evidence: "A standardised communication interface... allows AI agents to interface with external tools... using a uniform protocol, bypassing the need for... bespoke integration code."
- Implications:
    - Standardises tool-calling across different LLMs and platforms.
    - Reduces the friction of integrating new external capabilities into agentic systems.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [mcp, interoperability, tool-calling, standards]

### Atom 7: Agentic Autonomy as State Machine Logic
- Kind: claim
- Statement: AI "agentic autonomy" is functionally constrained within programmatic control flows such as state machines and conditional edges.
- Scope & Conditions: Rebuttal to the perception of unconstrained AI decision-making.
- Evidence: "In reality, frameworks like LangGraph constrain this autonomy within rigid, programmatic control flows (state machines, conditional edges). The agent is simply an LLM executing decisions within a tightly defined logic loop."
- Implications:
    - Autonomy is limited by the developer-defined graph architecture.
    - Predictability is achieved through structural constraints rather than model "judgment."
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [ai-agents, autonomy, state-machines, control-flow]
