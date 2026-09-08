---
aliases:
- Agentic AI MOC
- LLM Agents Index
- Agent Architecture MOC
created: 2026-09-07 00:00:00+00:00
modified: 2026-09-07 00:00:00+00:00
tags:
- domain/llm
- topic/agent-architecture
- moc
- map-of-content
title: MOC - Agentic AI & LLM Agents
permalink: llmeon/30-library/mo-c/moc-agentic-ai-llm-agents
---

Core Theme: How autonomous, tool-using LLM systems are designed, orchestrated, made safe, and made economical — as distinct from [[MOC - AI Software Engineering]], which covers the narrower "cognitive bridge" problem of LLMs understanding codebases. This is the single entry point for the vault's agentic-AI content, which prior to 2026-09-07 was scattered across ~50 notes produced by at least six separate, never-unified ingestion batches (see `_link_report_ai_agent_architecture`, `_link_report_agentic_engineering`, `_link_report_agent_first_workflow`, and siblings in `30_Library/400_indexes/`).

## 1. The Conceptual Spine (SoT Layer)

The design-pattern catalogue and role/skill architecture that the atomic claims below instantiate or extend.

- [[SoT - Agentic AI Design Patterns]] — _The pattern catalogue (multi-agent collaboration, RAG, tool-use, reflection) that most atoms in this MOC cite as their theoretical parent; the vault's de-facto hub for this domain._
- [[SoT - Agentic Roles]] — _Divides coding-agent cognitive load across specialised roles (Architect, Scout, Cartographer, Historian, Coder); also anchored under [[MOC - AI Software Engineering]] via its `implements` edge to [[SoT - The Context Engine]]. Its role/autonomy language ("the Architect enforces," "the Coder writes") is functional shorthand for a state machine, not a claim of literal cognition — see [[SoT - LLM Semantic-Statistical Mismatch]]'s Anthropomorphism Trap, which this MOC's operational vocabulary does not retract._
- [[SoT - AI Agent Skill Architecture]] — _Distinguishes Skills (behavioural recipes) from MCP servers (tools) and Subagents (isolated execution), and explains progressive-disclosure context loading._
- [[SoT - ML Engineering for AI Agents]] — _Domain-specific instance of skill architecture applied to the ML training/debugging lifecycle._
- [[MVC Enforcement Structural Gates for LLM Agents]] — _The three structural gates (interface, phase, context-budget) that keep an agent's context minimal and prevent hallucination from context overload._
- [[Protocol - Autonomous Action System]] — _Leon's own applied autonomous-agent protocol: an LLM Chief-of-Staff that routes GTD capture through Obsidian/Todoist MCP with no human in the loop between capture and action._

## 2. Architecture & Control Flow

How an agent's execution is structurally constrained rather than left to free-running inference.

- [[Agent Harness - Wrapping LLMs in Deterministic Software Controls]] — _A harness wraps probabilistic token prediction in deterministic software controls so the agent's behaviour stays bounded._
- [[Agentic Autonomy as State Machine Logic]] — _Perceived agent "autonomy" is functionally just traversal of a developer-defined state machine._
- [[Protocol Statelessness Relocates Agent State into Model-Visible Handles]] — _Removing protocol-level sessions relocates state into explicit, model-visible handles that can be composed across tools, which is a capability gain, not just a scaling fix._
- [[Agentic Loops Gain Turing-Complete Instability From Chained Reasoning and Tool Use]] — _Chaining reasoning and tool calls in a loop gives an agent Turing-complete power — and, without external deterministic constraints, no structural reason to halt or stay in scope._
- [[Code as Zero-Cost Deterministic Actor Alongside Engineers and Agents in Workflows]] — _Deterministic code is a third, zero-cost actor in agentic workflows alongside human engineers and probabilistic agents — the design question is which actor should own which step, not just human-vs-agent._
- [[Ground New Agent Ontologies in Established Semantic Web Taxonomies Rather Than Building From Scratch]] — _New agent-capability ontologies should extend existing semantic-web taxonomies rather than be invented from scratch._

## 3. Multi-Agent Orchestration & Delegation

- [[A Supervisor Agent Delegates to Repository-Specific Sub-Agents and Escalates Only Ambiguous Architectural Decisions]] — _A supervisor agent manages background sessions and only escalates genuinely ambiguous architectural calls to the human — attention management, not task delegation._
- [[Specialized Sub-Agent Roles Divide Research, Context Retrieval, and Code Editing]] — _Spec-driven development splits work across specialised sub-agents (research, retrieval, editing) instead of one agent vibe-coding the whole task._
- [[Implicit Multi-Agent Coordination via Shared File System]] — _Parallel agents can coordinate implicitly through a shared hierarchical file system instead of direct message-passing, giving deterministic audit trails and less communication overhead; `implements` [[SoT - Agentic AI Design Patterns]]._
- [[Software Factory Pattern - Specialized Sandboxed Agents Autonomously Own Feature, Bugfix, and Incident Lifecycles]] — _The end-state of workflow maturity: sandboxed specialist agents own entire feature/bugfix/incident lifecycles rather than one engineer directing one agent._
- [[Loop Engineering Is Built From Six Components - Automation, Worktrees, Skills, Plugins, Sub-Agents, and State]] — _Loop Engineering — removing the human from task initiation — decomposes into six components: automation, worktrees, skills, plugins, sub-agents, and state._
- [[Small Single-Purpose Agent Skills Outperform Monolithic Skill Design]] — _Agent skills should stay small and single-purpose rather than monolithic, for the same context-budget reasons as §1's MVC gates._

## 4. Memory & Continuity

- [[Tri-Partite Agent Memory - Procedural, Semantic, and Episodic]] — _Autonomous agents need three distinct memory stores — procedural, semantic, episodic — each serving a different recall function._
- [[Persistent Memory Layers Enable Multi-Session Agent Continuity]] — _Persistent memory layers (knowledge graphs, discovery logs, architectural decisions) let an agent's understanding compound across sessions instead of resetting each time._
- [[Agent Feedback Loops Require Bidirectional Memory Writes]] — _Learning across sessions requires agents to write to memory, not just read from it — retrieval alone doesn't close the loop._
- [[Recursive Agent Improvement]] — _Agents can review their own session logs and propose updates to their own skill definitions, improving procedure without human authorship._

## 5. Safety, Sandboxing & Governance

- [[Full-Autonomy Agent Execution Requires Sandboxing for Safety and Data Privacy, Not Just Concurrency]] — _Granting an agent full autonomy to execute any command requires sandboxing for safety and data privacy — concurrency isolation alone isn't the reason._
- [[Enterprise Agentic Systems Require Containerised Gateways with OAuth and RBAC]] — _Enterprise deployment of agentic systems needs containerised gateways enforcing OAuth and RBAC, not just capable models._
- [[Privacy Tombstones Mark Sensitive Files as Off-Limits to AI Agents]] — _Tombstone markers flag sensitive vault files as off-limits to agents, independent of folder-level permissions._
- [[Git Worktrees Provide Isolated, Low-Overhead Workspaces for Concurrent AI Agents]] — _Git worktrees give concurrent agents isolated workspaces without the overhead of full repo clones._
- [[Virtual File System for Agent Concurrency]] — _A virtual file system layer lets concurrent agents operate without colliding on shared state._
- [[Ephemeral Agents and Environments in Terraform Cloud]] — _Ephemeral, short-lived agents and environments reduce the blast radius of an agent's infrastructure access in Terraform Cloud._

## 6. Economics & Cost

- [[Agentic Tool Calls Compound Context Growth Multiplicatively]] — _Each tool call in an agentic loop compounds context growth multiplicatively, which is why agentic coding assistants cost far more than chatbots._
- [[Continuous Autonomous Agent Loops Incur Significant API Cost]] — _Letting an autonomous agent loop run continuously (vs. bounded/triggered runs) incurs API cost that scales with wall-clock time, not just task complexity._
- [[API Quota Limits, Not Just Cost, Drive Model Stratification in Agentic Workflows]] — _Provider quota limits, separate from raw cost, are an independent force pushing agentic workflows to stratify across model tiers._
- [[Unsustainable Agent Token Costs Are Driving a Shift from Flat-Fee to Usage-Based Pricing]] — _Flat-fee AI coding tools that subsidised heavy token use are being replaced by usage-based pricing as agent token consumption became unsustainable to subsidise._
- [[Cheaper Code Production via Agents Increases Software Volume Rather Than Reducing Developers]] — _A Jevons-paradox effect: cheaper agent-produced code increases total software volume/demand rather than shrinking the developer workforce._

## 7. Evaluation & Observability

- [[LLM-as-Judge for Autonomous Agent Evaluation]] — _Evaluating agent success requires either ground-truth labels or an LLM-as-judge, since most agent output has no simple pass/fail check._
- [[Trace Logging and Event Trees for Agent Observability]] — _Production agents must log every reasoning step and tool call as a tree of events, or debugging a failed run is impossible._
- [[Agentic Autonomy Accelerates Fastest in Domains Where Success Is Verifiable]] — _Agentic self-improvement accelerates fastest in domains where success is mechanically verifiable (e.g. code, math) — the same property that makes LLM-as-judge unnecessary there._

## 8. Tooling & the Developer/Agent Experience

- [[CLI Interoperability for Agents]] — _Small, Unix-philosophy CLI tools that pipe data between each other are what let agents compose capabilities without bespoke integration._
- [[Agent-Ergonomic CLIs Output Token-Efficient Plaintext Instead of Verbose JSON Schemas]] — _Tool-integration protocols (including some MCP servers) waste tokens on verbose JSON where token-efficient plaintext would do the same job for an agent caller._
- [[Convergence of Developer and Agent Experience]] — _The architectural and documentation bar for a good human developer experience is converging with what a good agent experience requires — DX and AX are becoming the same discipline._

## 9. Workflow Maturity & the Changing Role of the Engineer

- [[Engineer Involvement Compresses to Planning and Review as Agentic Workflows Mature]] — _As a workflow matures, engineer involvement doesn't vanish — it compresses to the two boundaries of the pipeline (initial planning, final review), with agent execution filling everything between._
- [[Agentic Collaboration Shift]] — _Software engineering is shifting from "AI-assisted autocomplete" to "agentic collaboration," changing what the engineer's moment-to-moment job actually is._
- [[Agent-First Implementation Cycle]] — _The agent-first workflow inverts the traditional implementation cycle — the agent drafts first, the human directs and reviews._
- [[The Slow Loop Pattern - Constrained Off-Hours Agent Loops Produce a Single PR for Async Human Review]] — _The pragmatic version of loop engineering: a constrained nightly agent loop fixing one anti-pattern, producing a single PR for asynchronous human review the next morning._
- [[Advanced Agentic Workflows Require Technical Literacy That Consumer Framing Hides]] — _Advanced agentic workflows demand a level of technical literacy that consumer-friendly marketing framing obscures, creating a real barrier to entry._

## 10. Domain-Specific Applications

- [[Auto-Researcher Agents Manage the ML Pipeline via a Defined Objective Metric]] — _An auto-researcher agent manages an entire ML pipeline against a single defined objective metric rather than a human tuning each stage._
- [[DocETL Framework - Declarative Pipelines with Agentic Optimization]] — _DocETL defines document-processing pipelines declaratively in YAML, then uses agentic optimisation to rewrite the pipeline for cost/accuracy._
- [[Expert Role Shifts from Explaining Concepts to Humans to Tuning Tutor-Agents]] — _Domain experts increasingly spend their time tuning tutor-agents' explanations rather than explaining concepts to students directly._
- [[Deep Agents for Long Horizon Planning]] — _LangGraph-based "Deep Agents" loop through planning and tool use for long-horizon tasks, rather than a single-shot plan._

---

## Related but Distinct

- [[MOC - AI Software Engineering]] — _Covers LLM codebase understanding, context rot, and the "cognitive bridge" between probabilistic models and deterministic architecture — a neighbouring domain, not a subset of this one. [[SoT - Agentic Roles]] and [[MVC Enforcement Structural Gates for LLM Agents]] sit at the seam between the two MOCs and are cross-listed._
- [[Protocol - Typed Answer Contract (TAC) for Vault Agents]] — _Governs how agents *working in this vault specifically* must format output; a PKM-governance protocol rather than a claim about agentic AI in general._

## Known Gaps (as of 2026-09-07 survey)

- 16 of the atoms above previously carried no typed-edge line at all; edges to this MOC's spine were added during positioning — see the bootstrap report for the full list.
- A meaningful minority of these atoms carried only ad-hoc flat tags (`ai-agents`, `automl`, `autonomous-agents`, etc.) rather than the dominant `domain/llm` + `topic/agent-architecture` scheme; three carried a stray, older `SoftwareEngineering/AI[/agents]` namespace. Tag normalisation is tracked as follow-up, not blocking this MOC's usefulness as an entry point.

---

Status: 🌱 Seedling — newly positioned as the domain's single entry point; typed-edge hygiene pass in progress.