---
type: tmp_atoms
status: tmp
source_title: Shared Memory Layer for Agentic AI (Gemini conversation reviewing several
  multi-agent architecture videos)
source_url: unknown — see original archived file for individual video URLs
captured_utc: '2026-09-14T00:00:00Z'
signal_to_noise: 40% signal / 60% noise (the opening audit-prompt block is Leon's
  own tool output, not source content; several videos are thin/promotional)
permalink: llmeon/00-inbox/tmp-atoms-shared-memory-agentic-ai
---

## Not Atomised
- The opening "audit prompt" block — Leon's own generated output, not source content to extract claims from.
- Task-specific model routing to named commercial models (Qwen/GLM/Grok) — too tool/vendor-specific and ephemeral to be a durable atom; the general "routing" pattern is already covered by [[SoT - Agentic AI Design Patterns]].
- General multi-agent orchestration / group-chat coordination — largely a restatement of patterns already covered in this vault's Agentic AI domain.
- Retain/Recall/Reflect memory-service loop — a reasonable named pattern but close enough to this vault's existing tri-partite memory coverage that it's folded into Atom 002's Related section rather than a separate atom.

## Atoms

### Atom 001: A Medallion Architecture (Bronze/Silver/Gold) Applied to Agentic Knowledge Bases Stages Raw Capture Through Review Before Trusted Storage
- Kind: definition
- Statement: Borrowed from enterprise data engineering, a medallion architecture applied to an agent-maintained knowledge base separates raw, immutable source capture (bronze — transcripts, articles, clippings) from agent-generated review proposals awaiting human approval (silver — suggested edits, link creations, extractions) from the approved, interlinked trusted knowledge base itself (gold — the wiki).
- Scope & Conditions: Specifically a response to the risk that an autonomous agent writing directly to a persistent knowledge base can introduce memory poisoning, hallucinations, and false contradictions.
- Evidence: "Bronze (Raw): Ingestion of raw, immutable source materials... Silver (Review/Trust Layer): The agent parses the raw data and generates 'review proposals'... rather than modifying the wiki directly... Gold (Wiki): The approved, interlinked markdown files that form the trusted semantic knowledge base."
- Implications:
    - An agent that can write review proposals but never commit them directly to the gold layer cannot poison the trusted knowledge base, regardless of how confidently wrong a given proposal is.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [domain/llm, topic/agent-architecture, topic/knowledge-graph, domain/pkm]

### Atom 002: Transactional Belief Commit Prevents an Agent's Unverified Write From Immediately Becoming Actionable Truth
- Kind: mechanism
- Statement: A transactional belief-commit pattern stages an agent's writes inside a snapshot-isolated, tentative state that must be validated before being promoted to a committed, action-safe state — preventing an unverified observation from immediately becoming ground truth that other agents or downstream tool calls treat as fact.
- Scope & Conditions: Addresses a specific failure mode in shared agentic memory: without staging, one agent's hallucination or premature write can silently corrupt what every other agent in the system subsequently treats as established.
- Evidence: "It introduces a 'Tentative' staging state where unverified observations are isolated and must be validated before they reach the 'Committed' or 'Action-Safe' state within the shared memory layer."
- Implications:
    - The same staging discipline that prevents memory poisoning in a multi-agent system is the general pattern behind any human-in-the-loop review gate before a write becomes canonical.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [domain/llm, topic/agent-architecture, topic/agentic-autonomy, domain/pkm]

### Atom 003: Capability Pruning Restricts Each Agent's Tools to Its Role to Prevent Runaway Tool Calls and Hallucinated Requirements
- Kind: claim
- Statement: Deliberately restricting each specialised agent's available tools and skills to only what its role requires — e.g. a Researcher agent has no task-delegation or cron access, an Orchestrator has no web-browsing tool — reduces token consumption and prevents agents from hallucinating requirements for capabilities they don't actually have or need, and getting caught in expensive, endless tool-call loops.
- Scope & Conditions: A multi-agent design practice, distinct from simply giving every agent full tool access "in case it's needed" — the restriction is itself the safety and efficiency mechanism.
- Evidence: "A critical best practice for multi-agent setups is tightly restricting the tools and skills each bot can access... Disabling these prevents agents from hallucinating requirements and getting caught in expensive, endless loops."
- Implications:
    - When an agent starts making unexpected or repeated tool calls, checking whether its toolset is over-provisioned for its actual role is a cheap first diagnostic step.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [domain/llm, topic/agent-architecture, topic/agentic-autonomy, domain/pkm]