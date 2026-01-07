---
aliases: []
tags:
  - head
  - workflow
  - ai
  - agentic
created: 2026-01-07T12:05:00
status: Active
---

# The Spark
Derived from "The creator of Claude Code just revealed his workflow" (Boris Cherny).
**Core Premise:** Treat AI not as an autocomplete, but as a "Fleet Commander" managing autonomous units.
**Key Tactic:** High-latency/High-intelligence models + Robust Context files + Recursive Verification.

# My Current Model (Adaptation)

| Cherny Concept | Gemini/ProdOS Adaptation |
| :--- | :--- |
| **5 Parallel Tabs** | Use multiple CLI sessions or parallel `delegate_to_agent` calls for background tasks. |
| **CLAUDE.md** | **`GEMINI.md`** (or per-project `.gemini/INSTRUCTIONS.md`). *Crucial:* The agent must update this file when it makes a mistake. |
| **Slash Commands** | Custom MCP tools or simple shell scripts wrapped in `run_shell_command`. |
| **Verification Loop** | **"No Input without Output."** Agent *must* run the build/test command before returning control. |

# The Tension
- My current `GEMINI.md` is static. It needs to be a "Living Document" of mistakes.
- I often just output code without running it to verify.

# The Next Test
- [ ] **Protocol Update:** Modify `GEMINI.md` to include a "Self-Correction" instruction (if I fail, I must update the docs).
- [ ] **Experiment:** Try a coding task where I strictly refuse to finish until I have executed a successful build command.
