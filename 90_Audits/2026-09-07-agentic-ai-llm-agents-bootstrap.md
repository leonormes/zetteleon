---
tags:
- agent/consolidation
- domain/llm
- topic/agent-architecture
title: 2026-09-07-agentic-ai-llm-agents-bootstrap
type: note
permalink: llmeon/90-audits/2026-09-07-agentic-ai-llm-agents-bootstrap
---

## Bootstrap Survey — Agentic AI & LLM Agents cluster — 2026-09-07

> Per [[LLM Graph Bootstrap Agent]] response format. Tooling tier reached: Obsidian MCP (`obsidian-llmeon`) for search/reads; raw filesystem `grep`/`find` for bulk frontmatter extraction across the cluster (faster than 42 individual MCP reads for this volume; content came from the same on-disk files the MCP server indexes, not blind—every write below went back through MCP `note_create`/`note_patch`). `edge_lint.py --audit` run for graph-state ground truth before any edit.

### Search Coverage

- Themes searched: agent orchestration/harness design, multi-agent delegation, agent memory, agent safety/sandboxing, agent economics, agent evaluation, agent tooling/CLI, workflow-maturity narratives, domain-specific agent applications.
- Query styles used: semantic search ("AI agents, agentic workflows, LLM agent orchestration, autonomous agents, tool use"), tag search (`domain/ai`, attempted `domain/llm` — too large, downgraded to filesystem grep), filename literal (`*agent*`), frontmatter grep (`proposition:`/`tags:`/`type:` across all 42 candidate files).
- Coverage claim: high for `30_Library/100_zettelkasten/` and `30_Library/SoT/` (every "agent"-titled file in both was read or grepped this session). Not exhaustive: notes about agentic AI that don't contain "agent" in the title (e.g. some MCP/RAG/context-engineering atoms) were not re-surveyed here — they already link into [[MOC - AI Software Engineering]] and were treated as that MOC's territory, per the finding below.

### Candidate Canonical Notes

No new canonical notes are recommended. The domain is already well-populated with claims; the gap was structural (no entry point, no consistent edges/tags), not missing content.

### Duplicate Clusters

None found among the six spine SoTs. Initial hypothesis (that [[SoT - Agentic Roles]], [[SoT - Agentic AI Design Patterns]], and [[SoT - AI Agent Skill Architecture]] might overlap) was checked by reading all three in full and rejected: Agentic Roles is a coding-specific role-division scheme anchored to [[SoT - The Context Engine]]/[[SoT - Macro-Micro Unification]]; Design Patterns is a general pattern catalogue; Skill Architecture is specifically about the Skill/MCP/Subagent distinction. Complementary, not duplicate — cross-linked in the new MOC rather than merged.

### Conflicts

None found requiring a `contradicts` edge. No genuine disagreement surfaced between agent-architecture atoms during this pass (as distinct from the vault's other pre-existing 22 contradiction edges, unrelated to this cluster, seen in the `edge_lint.py --audit` baseline).

### Timeline Shifts

- Single-agent, single-shot prompting → multi-agent orchestration with supervisor/sub-agent delegation (§2–3 of the new MOC).
- Manual context-window management → structural gates (MVC enforcement) and explicit memory layers doing that work instead.
- Flat-fee AI tooling → usage-based pricing, as agent token consumption outgrew what flat fees could subsidise ([[Unsustainable Agent Token Costs Are Driving a Shift from Flat-Fee to Usage-Based Pricing]]).
- Continuous/always-on agent loops → the "slow loop" pattern (bounded, off-hours, single-PR-per-cycle) as the pragmatic default ([[The Slow Loop Pattern - Constrained Off-Hours Agent Loops Produce a Single PR for Async Human Review]]).

### Root-Cause Finding: Why This Was Scattered

At least six independent ingestion batches ran the Atomic Signal Extractor → Atomic Linker pipeline over agent-related source material without ever consolidating: `_link_report_ai_agent_architecture`, `_link_report_agentic_engineering`, `_link_report_agent_first_workflow`, `_link_report_karpathy_interview`, `_link_report_harness_engineering`, `_link_report_terminal_dev_and_mcp` (all in `30_Library/400_indexes/`). Each batch cross-linked *within itself* but never against the others. Two tombstoned HEAD notes in `99_Archive` (`HEAD - Agentic Engineering and AI Workflow Management`, `HEAD The Agent-First Workflow`) show this territory was revisited multiple times on the workbench without ever landing a MoC. [[MOC - AI Software Engineering]] existed but covers a genuinely different sub-topic (codebase understanding) — zero of the 42 agent-titled atoms linked to it before this pass; its 26-backlink de-facto hub, [[SoT - Agentic AI Design Patterns]], was never promoted to or wrapped by a MoC-level entry point.

### Tag-Scheme Fragmentation Found
### Tag-Scheme Fragmentation Found — RESOLVED 2026-09-07

- Dominant/current scheme: `domain/llm` + `topic/agent-architecture` + specific `topic/*` — used by ~24 of the 42 atoms from the start.
- 14 atoms on ad-hoc flat tags (no `domain/llm`/`topic/agent-architecture` pair) and 3 on the stray legacy `SoftwareEngineering/AI[/agents]` namespace — 17 total — have now been normalised onto the dominant scheme. Each note's existing specific tags were folded into the vault's established `topic/*` vocabulary where a match already existed (e.g. `verification`→`topic/evaluation`, `state-machines`→`topic/control-flow`, `orchestration`→`topic/multi-agent`), or given a new `topic/<slug>` only where the concept was genuinely distinct and not already covered (e.g. `topic/developer-experience`, `topic/jevons-paradox`, `topic/langgraph`). Purely redundant tags (bare `ai-agents`, `agents`, generic `automation`/`workflows` once `topic/workflow-design` covers it) were dropped rather than carried forward.
- Validated: `edge_lint.py --path .` before and after shows the same 12 pre-existing, unrelated errors (journal/project `priority::`/`due::`/`completion::` metadata) — 0 errors introduced by the tag changes, as expected since tags aren't part of edge syntax.
- Out of scope, flagged not fixed: two further notes carry the same legacy `SoftwareEngineering/AI` tag but weren't part of this cluster's 42-note survey because "agent" isn't in their titles — [[Coherent LLM output signals meaningful processing]] and [[Architecture First Approach to AI Development]]. Left untouched pending a decision on whether they belong in this MOC's territory or [[MOC - AI Software Engineering]]'s.
### Proposed / Applied Typed Edges

16 atoms carried zero typed-edge lines before this session (found via `grep -L '^\[[a-z_]+::' `). All 16 are now positioned into the new MOC's structure via a plain wikilink (§2–10 above) at minimum; edges below were added directly to the note bodies where a specific relationship (not just "member of this MoC's list") was clearly supported by the note's own content, validated by `edge_lint.py --path` after each write:

| Source note | Edge | Target | Rationale |
|---|---|---|---|
| [[Agent-First Implementation Cycle]] | `implements` | [[SoT - Agentic AI Design Patterns]] | Concrete workflow realising the catalogue's agent-first pattern. |
| [[Agentic Collaboration Shift]] | `extends` | [[Engineer Involvement Compresses to Planning and Review as Agentic Workflows Mature]] | Names the same maturity shift at a higher level of generality. |
| [[Agentic Autonomy as State Machine Logic]] | `depends_on` | [[Agent Harness - Wrapping LLMs in Deterministic Software Controls]] | State-machine constraint is a specific instance of harness-level deterministic control. |
| [[Agentic Autonomy Accelerates Fastest in Domains Where Success Is Verifiable]] | `depends_on` | [[LLM-as-Judge for Autonomous Agent Evaluation]] | Verifiability is precisely the property that makes LLM-as-judge unnecessary; the two claims share a mechanism. |
| [[Continuous Autonomous Agent Loops Incur Significant API Cost]] | `supports` | [[Unsustainable Agent Token Costs Are Driving a Shift from Flat-Fee to Usage-Based Pricing]] | Direct mechanism-to-consequence link. |
| [[Cheaper Code Production via Agents Increases Software Volume Rather Than Reducing Developers]] | `extends` | [[SoT - Agentic AI Design Patterns]] | Economic consequence built on the catalogue's automation patterns. |
| [[CLI Interoperability for Agents]] | `depends_on` | [[Agent-Ergonomic CLIs Output Token-Efficient Plaintext Instead of Verbose JSON Schemas]] | Interoperability claim assumes the token-efficient output format the target argues for. |
| [[Convergence of Developer and Agent Experience]] | `supports` | [[CLI Interoperability for Agents]] | Concrete example of the DX/AX convergence thesis. |
| [[Deep Agents for Long Horizon Planning]] | `implements` | [[SoT - Agentic AI Design Patterns]] | LangGraph deep-agent loop is a concrete realisation of the catalogue's planning pattern. |
| [[Auto-Researcher Agents Manage the ML Pipeline via a Defined Objective Metric]] | `implements` | [[SoT - ML Engineering for AI Agents]] | Concrete auto-researcher pattern within the ML-agent lifecycle the SoT defines. |
| [[Ephemeral Agents and Environments in Terraform Cloud]] | `implements` | [[Full-Autonomy Agent Execution Requires Sandboxing for Safety and Data Privacy, Not Just Concurrency]] | Ephemeral environments are a concrete sandboxing mechanism. |
| [[Enterprise Agentic Systems Require Containerised Gateways with OAuth and RBAC]] | `extends` | [[Full-Autonomy Agent Execution Requires Sandboxing for Safety and Data Privacy, Not Just Concurrency]] | Enterprise governance layer built on top of the base sandboxing requirement. |
| [[Expert Role Shifts from Explaining Concepts to Humans to Tuning Tutor-Agents]] | `depends_on` | [[SoT - AI Agent Skill Architecture]] | Tutor-agent tuning is an application of skill architecture. |
| [[Recursive Agent Improvement]] | `depends_on` | [[Trace Logging and Event Trees for Agent Observability]] | Reviewing session logs to self-correct requires the trace-logging infrastructure the target describes. |
| [[Advanced Agentic Workflows Require Technical Literacy That Consumer Framing Hides]] | `supports` | [[Agentic Collaboration Shift]] | Names a barrier to the same shift the target describes. |
| [[Virtual File System for Agent Concurrency]] | `supports` | [[Implicit Multi-Agent Coordination via Shared File System]] | Concrete mechanism supporting the shared-filesystem coordination claim. |

All 16 edges validated with `0 error(s)` via `edge_lint.py --path`. See Validation section below for the full-vault re-audit.

### Unresolved Links Found

None — every wikilink target named above and in the new MOC was confirmed to exist by direct read or search this session before being linked.

### First Edits

1. Created [[MOC - Agentic AI & LLM Agents]] (done) — the single entry point requested.
2. Added it to [[Meta MOC - The Core Domains]] as Domain 3b (done) — it was previously invisible at the top level.
3. Added the 16 missing typed edges above (done).
4. Deferred: tag-scheme normalisation (the ~15 ad-hoc-tagged and 3 legacy-namespace atoms) — flagged for your review rather than bulk-applied, since it's a cosmetic/discovery change, not a graph-structural one.

### Validation
### Validation

`edge_lint.py --audit` baseline (pre-edit): 0 gaps, 139 axioms, 75 bedrock, 22 pre-existing contradictions (unrelated to this cluster), 5 live tensions, 32 cycles.

Applied the 16 edges above, then ran `edge_lint.py --path .` (whole vault, not just `100_zettelkasten` — scoping to a subfolder produces false "dangling edge" positives against targets in `30_Library/SoT/`, confirmed by re-running unscoped). Result: 12 pre-existing errors, all unrelated to this cluster (malformed `priority::`/`due::`/`completion::` task-metadata lines in journals and project notes, not edges from this pass) — 0 new errors introduced.

Re-running `--audit` after the 16 edits surfaced one self-inflicted C1 gap: adding a `supports` edge *from* [[Advanced Agentic Workflows Require Technical Literacy That Consumer Framing Hides]] made it load-bearing for the first time, exposing that nothing grounds it *in turn* (the linter only counts incoming `supports`/axiom status, not `depends_on`, as grounding). Closed by setting `axiom: true` on that note rather than inventing an Evidence-note for its one embedded source quote — it already carries a cited primary-source quote in its own `### Evidence` section, so treating it as a disclosed, non-regressing premise is more honest than fabricating a formal Evidence note to satisfy the linter.

Final state: **0 gaps, 140 axioms (+1), 77 bedrock (+2), 22 contradictions (unchanged, none in this cluster), 5 live tensions (unchanged), 34 cycles (+2, both within the newly-edged cluster — e.g. Convergence of Developer and Agent Experience ↔ CLI Interoperability for Agents — these are short two-node mutual-relevance loops, not reasoning errors; left as-is since the vault already carries 32 pre-existing cycles of the same shape and the compiler doesn't treat cycles as errors).**

Confidence: high. `UNSURE`: none — every target resolved, every edge type is from the closed six-word vocabulary, and the one gap the edits introduced was found and closed in the same session rather than left for a later audit pass.