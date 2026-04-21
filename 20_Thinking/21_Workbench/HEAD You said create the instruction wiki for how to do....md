---
captured: "2026-04-09T09:52:40+01:00 2026-04-09T09:52:40+01:00"
created: 2026-04-09T08:52:42+00:00
modified: 2026-04-21T09:51:56+00:00
source: "https://gemini.google.com/app/b68fb04d61e5ba5b"
status: "processing"
tags: ["input"]
title: HEAD You said create the instruction wiki for how to do...
type: "head"
---

## Raw Output / Content

You

create the instruction wiki for how to do this from the video <https://youtu.be/7huCP6RkcY4?si=7AOa4jg0rjtIu7Af>

---

Gemini

Here is an instructional wiki detailing the setup and architecture of the self-evolving Claude Code memory system, drawn from the provided video ([https://youtu.be/7huCP6RkcY4](https://www.google.com/search?q=https://youtu.be/7huCP6RkcY4)):

## Self-Evolving Claude Code Memory: Instruction Wiki

Overview This system adapts Andrej Karpathy's LLM Knowledge Bases to work natively with internal data \[[00:12](http://www.youtube.com/watch?v=7huCP6RkcY4&t=12)\]. By capturing and processing your coding sessions, it builds a continuously evolving, long-term memory for Claude Code, allowing your agent to understand past decisions and project context without requiring expensive codebase scans.

### Prerequisites

- Claude Code: The core AI agent operating within your codebase.
- Obsidian: A free markdown application used as the canvas to view your generated knowledge graph \[[00:48](http://www.youtube.com/watch?v=7huCP6RkcY4&t=48)\].

### Step 1: Initialise the Obsidian Vault

1. Install and open the Obsidian application.
2. Select the option to Open folder as vault \[[11:26](http://www.youtube.com/watch?v=7huCP6RkcY4&t=686)\].
3. Choose the local path to the codebase where you want to deploy the memory system.
4. _(Optional)_ Customise your viewing experience by clicking Settings (bottom left) -> Appearance -> Manage, and installing a dark theme such as obsidianite \[[11:45](http://www.youtube.com/watch?v=7huCP6RkcY4&t=705)\].

### Step 2: System Architecture & Folder Structure

Once the setup script is executed, it will generate a specific directory structure for your project to manage data flow:

- Daily Logs (`raw` equivalent): The entry point where unprocessed conversational transcripts and automated session summaries are dumped \[[13:58](http://www.youtube.com/watch?v=7huCP6RkcY4&t=838)\].
- Knowledge (`wiki` equivalent): The formalised area where processed data is stored \[[14:09](http://www.youtube.com/watch?v=7huCP6RkcY4&t=849)\]. This includes:
	- Concepts & Connections: Markdown files detailing distinct ideas and how they interrelate.
		- `index.mmd`: The most crucial file. It provides an actively maintained map of all folders and resources, allowing Claude to navigate your knowledge base directly without relying on complex semantic search or vector databases \[[05:34](http://www.youtube.com/watch?v=7huCP6RkcY4&t=334)\].
- `agents.mmd`: The global rules file. This outlines the entire LLM knowledge base system to the agent, ensuring it possesses the meta-reasoning to understand where its information comes from and how to navigate it \[[07:14](http://www.youtube.com/watch?v=7huCP6RkcY4&t=434)\].

### Step 3: Configuring the Claude Code Hooks

The automation is entirely driven by Claude Code hooks defined within your project's `settings.json` file \[[12:30](http://www.youtube.com/watch?v=7huCP6RkcY4&t=750)\]. No external integrations are necessary.

- `session_start` Hook: A script that runs when a new session begins. It automatically loads `agents.mmd` and `index.mmd` so the agent starts with complete awareness of the system and file structure \[[12:46](http://www.youtube.com/watch?v=7huCP6RkcY4&t=766)\].
- `pre_compact` & `session_end` Hooks: Whenever context is about to be lost (either by compaction or closing the session), these hooks capture the latest messages \[[14:52](http://www.youtube.com/watch?v=7huCP6RkcY4&t=892)\]. They trigger a separate background process via the Claude Agent SDK to summarise the conversation (e.g., lessons learned, decisions made) and save it to the daily logs \[[15:30](http://www.youtube.com/watch?v=7huCP6RkcY4&t=930)\].

### Step 4: The Flush & Compile Process

- To keep the wiki structured, a scheduled flush process runs in the background (typically once a day) \[[15:50](http://www.youtube.com/watch?v=7huCP6RkcY4&t=950)\].
- It extracts raw information from the daily logs, processes it, and generates formal concepts and connections to populate the `knowledge` folder.
- Customisation: You can manually navigate to the flush or compile scripts and alter the system prompt sent to the Claude Agent SDK, giving you full control over how your data is categorised and compiled \[[16:14](http://www.youtube.com/watch?v=7huCP6RkcY4&t=974)\].

### Step 5: Querying Your Second Brain

Once operational, you can simply ask Claude Code a project-specific question. Instead of reading the entire git log or running slow sub-agents, it will consult the `index.mmd`, search the relevant formal knowledge articles, and cross-reference daily logs to provide an immediate, highly contextualised answer \[[13:48](http://www.youtube.com/watch?v=7huCP6RkcY4&t=828)\].
