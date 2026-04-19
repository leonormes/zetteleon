---
captured: "2026-04-09T12:08:54+01:00 2026-04-09T12:08:54+01:00"
created: 2026-04-09T11:09:10+00:00
modified: 2026-04-19T18:30:45+00:00
source: "https://gemini.google.com/app/e381d02fa9bf81fe"
status: "processing"
tags: ["input"]
title: HEAD The Compiler Analogy
type: "head"
---

## Raw Output / Content

You

review this video and summarise the instructions so I can do the same thing. <https://youtu.be/7huCP6RkcY4?si=dQZ0aoDJbi-4l8fW>

Create a llm prompt for my local coding assistant to give it full context of the plan

---

Gemini

This system transforms a coding assistant into a self-evolving knowledge base by applying a "compiler analogy" to internal conversation data. Instead of just searching a static codebase, the assistant maintains and updates a wiki of its own decisions, lessons learned, and architectural plans.

### System Architecture: The Compiler Analogy

The core of this workflow treats knowledge exactly like source code to ensure data integrity and accessibility for an agent.

- Source Data (Raw): This stage involves capturing raw conversation transcripts or external articles. In this implementation, the system focuses on "internal data"—saving every session log from your coding interactions as raw Markdown files \[[03:16](http://www.youtube.com/watch?v=7huCP6RkcY4&t=196)\].
- The Compiler Stage: An LLM processes these raw logs to extract key takeaways, summaries, and action items. It organises information by identifying concepts and cross-linking related notes \[[03:23](http://www.youtube.com/watch?v=7huCP6RkcY4&t=203)\].
- The Executable (Wiki): The final output is a structured Obsidian vault. This is the "executable" knowledge base that the assistant queries to retrieve context from previous sessions \[[03:49](http://www.youtube.com/watch?v=7huCP6RkcY4&t=229)\].
- The Runtime: When you start a new session, the assistant reads a central index file to understand what knowledge is available, allowing it to navigate the wiki without needing expensive semantic search or vector databases \[[05:34](http://www.youtube.com/watch?v=7huCP6RkcY4&t=334)\].

### Step-by-Step Implementation Instructions

1. Initialise the Canvas: Create a dedicated project folder and open it as an Obsidian vault to visualise the memory graph and connections \[[11:15](http://www.youtube.com/watch?v=7huCP6RkcY4&t=675)\].
2. Define Global Rules: Create an `agents.mmd` file in the root directory. This file should describe the entire memory system, folder structure, and indexing rules so the assistant understands its own "meta-reasoning" \[[07:20](http://www.youtube.com/watch?v=7huCP6RkcY4&t=440)\].
3. Configure Session Hooks: Set up lifecycle hooks in your local coding environment (such as `settings.json` for Claude Code) to automate data flow \[[12:36](http://www.youtube.com/watch?v=7huCP6RkcY4&t=756)\]:
	- Session Start: Automatically load the `index.mmd` and `agents.mmd` files so the assistant is fully briefed on current project context \[[12:46](http://www.youtube.com/watch?v=7huCP6RkcY4&t=766)\].
		- Pre-compact & Session End: Trigger a separate LLM process (using an SDK or API) to summarise the current conversation transcript before the session closes \[[14:52](http://www.youtube.com/watch?v=7huCP6RkcY4&t=892)\].
4. Automate Knowledge Promotion: Implement a "flush" script that periodically moves information from raw logs into the structured `wiki/concepts` and `wiki/connections` folders \[[15:58](http://www.youtube.com/watch?v=7huCP6RkcY4&t=958)\].
5. Maintain the Index: Ensure the assistant updates a central `index.mmd` file after every session. This file acts as a map, allowing the agent to point to specific articles in response to your queries \[[13:48](http://www.youtube.com/watch?v=7huCP6RkcY4&t=828)\].

### LLM Context & System Prompt

To have your local coding assistant build this system for you, provide it with the following Product Requirement Document (PRD) prompt:

---

System Architect Prompt: Self-Evolving Memory System

"Act as a system architect. I want to implement a self-evolving memory system for this codebase based on the 'compiler analogy' for LLM knowledge bases.

Objective: Create a system that captures my coding sessions, summarises them, and organises them into a searchable Markdown wiki.

Requirements:

1. Directory Structure: Create a `memory/` directory with subfolders for `raw_logs/` (unprocessed session transcripts) and `wiki/` (structured articles, concepts, and connections).
2. Metadata & Rules: Create an `agents.md` file that defines this system's architecture and a central `index.md` file to track all wiki articles.
3. Automation Scripts:
	- Write a Python script for 'Session Start' that reads the index and global rules into the current LLM context.
		- Write a script for 'Session End' that takes the current conversation transcript, uses an LLM to summarise it into lessons learned and technical decisions, and saves it to `raw_logs/`.
		- Write a 'Promotion' script to parse `raw_logs/` and update the `wiki/` and `index.md` files with new cross-referenced content.
4. Integration: Provide instructions on how to hook these scripts into my local coding assistant's lifecycle settings.

Start by initialising the directory structure and drafting the `agents.md` and `index.md` templates."

---

You can find the full details of this architecture in the video: [https://youtu.be/7huCP6RkcY4?si=dQZ0aoDJbi-4l8fW](https://youtu.be/7huCP6RkcY4?si=dQZ0aoDJbi-4l8fW)

---

### Deconstruction Report: Automated Personal Knowledge Bases

The content provided outlines a workflow for creating a personal knowledge base (referred to as an "LLM Wiki") using a specific prompt published by Andrej Karpathy. The presentation frames this as a "PhD-level" research system designed to overcome the limitations of standard Large Language Model (LLM) interfaces, which often struggle with maintaining context across vast datasets or performing deep comparative analysis.

#### Core Thesis

The foundational argument is that individual research productivity is maximised when the user offloads the "bookkeeping" of information—categorisation, cross-referencing, and indexing—to an LLM agent, while the human researcher focuses exclusively on source curation and high-level synthesis. This is achieved by creating a local, structured repository of Markdown files that an LLM can query and maintain autonomously.

#### Filtered Substance: Actionable Concepts

Stripping away the promotional rhetoric regarding "breaking the internet" and "scaling businesses," the technical workflow consists of the following components:

1. Data Ingestion: Utilising tools such as a browser-based web clipper to capture web content or manually adding PDFs and text files into a local directory.
2. Orchestration Layer: Using a local agentic coding tool (e.g., Claude Code) to execute a specific system prompt (the "LLM-Wiki prompt"). This prompt instructs the agent to act as a librarian and researcher.
3. Knowledge Management (The IDE): Using Obsidian, a local-first Markdown note-taking application, as the interface to visualise data connections through its "Graph View" and to store the processed knowledge.
4. Automated Maintenance (Linting): The agent is tasked with "linting" the wiki—identifying stale data, correcting broken links, and updating summaries as new information is added.
5. Querying: The user interacts with the agent via the terminal or interface to ask complex questions based strictly on the ingested local data, rather than the model's general training data.

#### Grounding in Reality

The "novelty" of this system lies in the packaging and the specific prompting strategy provided by Karpathy, rather than a breakthrough in AI technology.

- RAG (Retrieval-Augmented Generation): This system is essentially a manual, local implementation of RAG. While industry-standard RAG usually involves vector databases and semantic search, this method uses a "map-reduce" style approach where the LLM reads and indexes local files.
- Zettelkasten Method: The use of Obsidian and back-linking is a digital adaptation of the Zettelkasten method, a decades-old knowledge management system.
- Standard Practice: The "agentic" nature of the setup—where the LLM has permission to read and write to a local file system—is a standard feature of modern developer tools like Claude Code or Aider.

#### The Verdict

Signal-to-Noise Ratio: 35% Signal, 65% Noise

Assessment: The informational density is moderate. The "noise" primarily consists of personal anecdotes, repetitive calls to join a community, and hyperbolic claims regarding the "PhD-level" nature of the output. However, the practical value is significant for users seeking a low-cost, local-first alternative to commercial "AI second brain" applications. It offers a transparent, hackable method for researchers to organise data without relying on proprietary cloud databases. The primary utility is the automation of the "bookkeeping" tasks inherent in complex research projects.
