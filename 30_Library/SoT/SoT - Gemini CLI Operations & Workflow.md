---
aliases: ["Gemini Guide", "Gemini Workflow"]
confidence: "4/5"
created: 2025-12-21T00:00:00Z
epistemic: "Synthesized from multiple video tutorials and hands-on use."
last_reviewed: "2025-12-21"
modified: 2025-12-25T11:40:21+00:00
purpose: "To provide a practical, actionable guide to the core operations and workflows of the Gemini CLI."
review_interval: "1 month"
see_also: []
source_of_truth: []
status: "evolving"
tags: ["gemini-cli", "guide", "tools", "workflow"]
title: SoT - Gemini CLI Operations & Workflow
type: "SoT"
uid: 
updated: 
---

1. **Runtime: "** Requires **Node.js v20** or higher."
2. **Installation: "** `npm install -g @google/gemini-cli@latest`"
3. **Verification: "** `gemini -v` (ensure v0.20.0 or higher for session management)."
4. **Authentication (Crucial for Economics): "**"
- This grants access to the free tier: "**Gemini 1.5 Pro with up to 1,000 requests per day** and a 1-million-token context window."

## 2. Core Concepts: Providing Context

The CLI's power comes from its ability to ingest context from your local environment.

- **The Master Prompt (`gemini.md`):** A file in your project root that acts as a global system prompt. It should define the agent's role, high-level architecture, and development standards. Use `/init` to generate an initial version based on your codebase.
- **File References (`@`):** To provide specific file context for a single prompt, use the `@` symbol (e.g., `Refactor this function based on the patterns in @utils/helpers.ts`).
- **Shell Injection (`!`):** To provide context from a shell command, use the `!` prefix (e.g., `Summarize the current changes:!git diff --staged`).

---

## 3. State & Session Management

The CLI automatically persists sessions, preventing context loss.

- **Resume Latest Session:** `gemini-res`
- **List All Sessions:** `gemini-list sessions`
- **Resume Specific Session:** `gemini-res [ID]` (or use the interactive browser).
- **Session Branching:** Use `/chat save [name]` and `/chat resume [name]` to manage non-linear conversational forks, similar to Git branches.
- **Persistent Memory:** Use `/memory add "[fact]"` to store long-term rules and decisions (e.g., `/memory add "Always use FastAPI for new Python services."`).
- **Context Compression:** If a session becomes too large, use `/compress` to reduce token usage by up to 90%.

---

## 4. Execution & Agency

You can control how much autonomy the agent has.

- **Default Mode (Manual):** Requires manual approval (`y` or `n`) for every file edit or shell command.
- **Auto-Edit Mode:** Automatically approves file modifications but still requires confirmation for shell commands. Toggle with `Shift + Tab`.
- **YOLO Mode (`--yolo`):** Grants full autonomy for all tool calls. Use with caution.
- **Checkpoints & Rollback:**
    - Enable with the `--checkpointing` flag.
    - The CLI will take a project snapshot before potentially destructive operations.
    - If an error occurs, use `/restore` to roll the entire project state back to the last known good checkpoint.

---

## 5. Advanced Workflows & UX

- **Test-Driven Development (TDD):** Instruct the agent to write tests *before* writing the feature code. This enforces a "Red-Green" loop and results in more reliable code.
- **Multimodal Debugging (Vision):** For UI bugs or visual errors, pass a screenshot directly to the CLI. Vision-enabled models are significantly more effective at fixing non-crashing UI issues.
- **Concurrent Contexts (`tmux`):** Use a terminal multiplexer like `tmux` to run multiple, independent Gemini CLI instances in parallel panes for different tasks (e.g., bug fixing, documentation, feature development).
- **Interactive Focus (`Ctrl+F`):** If the agent is waiting for manual input in a tool (e.g., a `git commit` message), press `Ctrl+F` (or `Cmd+F`) to jump focus directly to the input prompt.
- **Mouse Navigation:** The UI supports mouse-based scrolling and navigation within the terminal.
- **IDE Integration:** Use the **Gemini CLI Companion** extension for VS Code/Cursor to automatically provide context (recent files, cursor position) and sync CLI-generated changes back to the IDE.
