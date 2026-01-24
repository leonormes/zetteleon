---
created: 2026-01-24T08:35:00+00:00
modified: 2026-01-24T08:35:27+00:00
title: Untitled
---

## LLM Agent Roles and Specialisations in Software Development

|**Agent Name**|**Primary Role**|**Mental Model**|**Key Insights and Responsibilities**|**Tools and Technologies**|**Layer (Inferred)**|**Source**|
|---|---|---|---|---|---|---|
|The Architect|Synthesis and strategy; Guardian of Architectural Integrity|The Grand Unifying Theory (GUT) / Type-Driven Onion|Consumes outputs from specialists to generate CONCENTRATE.md; defines constraints and 'Blast Radius'; ensures output matches philosophy (Anti-Parochial).|filesystem (write_file), memory.json schema, store_memory tool|Layer 4: Security & Boundaries|1, 2|
|The Scout (AST Scout)|Extracting structural skeleton and dependency mapping|Type-Driven Design|Maps data flow and dependencies; extracts Types, Interfaces, and Function Signatures without implementation details; defines the 'Blast Radius' of changes.|Tree-sitter (MCP), ripgrep (rg --json), fd, ast-grep (sg)|Layer 3: Data Transformations (Logic)|1-3|
|The Cartographer|Mapping the 'Territory' and tracking identity|The Filesystem is a Graph Database of Inodes|Responsible for structural awareness; tracks Inodes to distinguish between renames and atomic saves; identifies modules and layers; maps filesystem boundaries.|scan_inodes (Python), tree -J, stat, fd, filesystem (ls -R, find)|Layer 1: Types & Invariants / Layer 2: Data|1-3|
|The Librarian|Verification and memory curation|Self-Healing Memory via Citation Verification|Curates knowledge base; verifies 'facts' against live code using citations; prevents hallucinations by validating memory.json against reality.|tree-sitter get_symbols, verify_memory tool, Python|Layer 1: Types & Invariants|1, 4|
|The Historian|Providing narrative, intent, and temporal context|Git is a Transaction Log|Calculates 'Churn Rate' (volatility) to identify unstable vs calcified code; uses git blame to understand intent; correlates code changes with history.|git log, git blame, git diff, git ls-tree|Layer 5: Maintainability|1-3|
|PO Agent (Product Owner)|Document sharding and task decomposition|Agile-driven (BMAD Method)|Initialises the workflow; shards PRD and Architecture documents into manageable index chunks for incremental development.|BMAD core, shard doc command|Planning / Strategy|5|
|Scrum Master|Epic and story generation|Iterative Agile Delivery|Detects missing epics; breaks down sharded PRDs into epics and stories; tracks story status (Draft, Approved, Done).|draft method, create epic method|Planning / Strategy|5|
|Dev Agent|Modular feature implementation|Incremental Development|Implements specific stories; breaks tasks into subtasks; updates status to 'Ready for Review'.|IDE rule files (.cursorrules), development environment|Implementation / Logic|5|
|The Project Manager|Managing logistics and executive function|Task Dependency Graph / Working Memory|Manages work queue and task dependencies; uses the 'Land the Plane' protocol for clean session handovers; tracks blockers.|Beads (CLI), bd ready, bd create, SQLite|Operational / Orchestration|1|
|Triage Router|Request classification and delegation|Router Pattern (Complexity Classifier)|Classifies incoming prompts as 'Simple Fix' or 'Complex Flow'; directs tasks to either a simple coder or the full specialist team.|router.py, llama3.2:3b (small models), Python|Edge / Interface|1|
