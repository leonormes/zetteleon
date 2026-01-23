---
created: 2026-01-17T15:29:38+00:00
modified: 2026-01-23T18:09:35+00:00
title: Grand Unifying Theory of Code Generation
---

Based on our conversation, here is the prioritized task list to operationalise your "Grand Unifying Theory" (GUT) of code generation.

I have prioritised these by Architectural Value: foundational "Database" mechanisms come first, followed by the "Intelligence" layers, and finally the "Orchestration" glue.

## 🚨 Phase 1: The "Database" Foundation (Critical Path)

Goal: Establish the Sources of Truth. Without these, the agents have "Context Dementia."

 - Deploy "Beads" (Executive Database)
   - Task: Install beads locally (npm install -g beads or binary).
   - Task: Initialize it in your target repo (bd init).
   - Value: Provides the "Working Memory" so agents know what to do.
 - Implement scan_inodes Tool (Spatial Database)
   - Task: Create the Python function (from our chat) that returns [{path, inode, mtime}].
   - Task: Verify it detects "Renames" (Same Inode) vs "Edits" (New Inode/Timestamp).
   - Value: Prevents "Context Rot" by giving agents a robust way to track file identity.
 - Define memory.json Schema (Semantic Database)
   - Task: Create the JSON structure for "Verified Facts" with Citations.
   - Value: The storage mechanism for the "Librarian" to prevent hallucinations.

## 🧠 Phase 2: The "Surgical Team" Tools (High Value)

Goal: Give the agents the specific sensors they need to query the databases.

 - Create the "Project Manager" Tool Wrapper
   - Task: Write the Python/LangChain tool that wraps bd ready --json and bd create.
   - Value: Allows the agent to query the work queue and "Land the Plane."
 - Create the "Librarian" Verification Tool
   - Task: Write the Python function that takes a {file, line_content} citation and returns True/False.
   - Value: Enables "Self-Healing Memory" (The blog post insight).
 - Create the "Historian" Tool
   - Task: Write the wrapper for git log and git blame to calculate "Churn Score."
   - Value: Stops agents from refactoring "calcified" legacy code without caution.
 - Setup Tree-sitter MCP (Scout)
   - Task: Ensure the Tree-sitter MCP server is running and can query for "Struct Definitions" (The Skeleton).
   - Value: Provides the "Macro View" of data flow without reading line-by-line code.

## ⚙️ Phase 3: The Orchestration (The Glue)

Goal: Wire the sensors into a decision-making graph.

 - Implement the Triage Router
   - Task: Write the router.py node with the binary classification prompt ("Complex Flow" vs "Simple Fix").
   - Value: Saves money/time by skipping the full GUT process for typos.
 - Write the "Architectural Manifesto" Prompt
   - Task: Finalise the System Prompt for the Architect Node (Anti-Parochial, No Trade-offs, Type-Driven).
   - Value: The "Soul" of the system; ensures the output matches your philosophy.
 - Wire the LangGraph
   - Task: Connect Router -> PM -> Librarian -> Cartographer/Scout -> Architect -> Coder.
   - Value: The runnable application.

## 🚀 Phase 4: Optimisation (Future Proofing)

 - Rust Migration (Performance)
   - Task: Rewrite scan_inodes and the Tree-sitter wrapper in Rust if Python latency > 2s.
   - Value: Speed and concurrency.
 - Visualisation
   - Task: Add a Mermaid.js generator tool for the Scout to draw the dependency maps it finds.
   - Value: Visual debugging for you.
Summary
Your immediate next action:
Run npm install -g beads and then write the project_manager_node python script. This gives you the "Executive Function" immediately.

## Related Implementation (2026-01-21)

The theoretical concepts here have been crystallized into specific Protocols and Source of Truth notes:

- [[SoT - Semantic Code Graph]] - The definition of the "Information Structure" replacing the raw "Data Structure".
- [[Protocol - Context Injection]] - The operational prompt ("The Cartographer") to enforce this theory.
