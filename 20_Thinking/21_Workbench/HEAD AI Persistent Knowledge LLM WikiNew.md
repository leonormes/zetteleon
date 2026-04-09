---
title: "You said https://youtu.be/Mb5N08xcxtg?si=1OjdqgjeO..."
source: "https://gemini.google.com/app/8bd8e6ed34436677"
captured: "2026-04-09T13:32:54+01:00 2026-04-09T13:32:54+01:00"
status: "processing"
tags:
  - "input"
type: "head"
---
## Raw Output / Content
**You**

https://youtu.be/Mb5N08xcxtg?si=1OjdqgjeO1aBpcBW

---

**Gemini**

The video explores the integration of two powerful AI tools: **Hermes Agent** from Nous Research and Andrej Karpathy’s **LLM Wiki** concept, published around April 2026. This combination is designed to solve the problem of "memory loss" in AI sessions, where research and insights are typically lost once a chat ends.

### The Core Concept: LLM Wiki

Andrej Karpathy's "LLM Wiki" moves away from traditional Retrieval-Augmented Generation (RAG). Instead of the AI searching raw documents from scratch every time you ask a question, it builds and maintains a **persistent, structured knowledge base** of markdown files.

- **Compounding Knowledge:** When you add a new source, the AI reads it, extracts key information, and integrates it into the existing wiki—updating pages, revising summaries, and flagging contradictions \[[01:41](http://www.youtube.com/watch?v=Mb5N08xcxtg&t=101)\].
- **The Programmer Metaphor:** Karpathy describes the LLM as the "programmer" and the wiki as the "codebase" \[[02:06](http://www.youtube.com/watch?v=Mb5N08xcxtg&t=126)\].
- **Maintenance:** The AI handles the "tedious bookkeeping" like cross-referencing and updating indices, which is usually why human-led wikis fail over time \[[06:22](http://www.youtube.com/watch?v=Mb5N08xcxtg&t=382)\].

### Hermes Agent Integration

Hermes Agent is an open-source AI agent known for its "learning loop," meaning it creates and improves skills based on experience.

- **Built-in Skill:** The latest update to Hermes Agent includes the LLM Wiki as a built-in skill. Users can trigger it using the command `/LLM wiki` followed by a research topic \[[03:04](http://www.youtube.com/watch?v=Mb5N08xcxtg&t=184)\].
- **Flexibility:** It supports over 200 models via OpenRouter and can connect to platforms like Telegram, Discord, and Slack \[[02:44](http://www.youtube.com/watch?v=Mb5N08xcxtg&t=164)\].

### How the System Works

The workflow is divided into three distinct layers and three core operations:

| Layer | Function |
| --- | --- |
| **Raw Sources** | Immutable documents (articles, papers) that the AI reads but never changes \[[04:07](http://www.youtube.com/watch?v=Mb5N08xcxtg&t=247)\]. |
| **The Wiki** | AI-generated markdown files (summaries, concept pages) that the AI owns and updates \[[04:12](http://www.youtube.com/watch?v=Mb5N08xcxtg&t=252)\]. |
| **The Schema** | The "rulebook" or configuration that tells the AI how to structure and maintain the wiki \[[04:35](http://www.youtube.com/watch?v=Mb5N08xcxtg&t=275)\]. |

**Core Operations:**

1. **Ingest:** Dropping a source for the AI to process. A single source may update 10–15 different pages simultaneously \[[05:00](http://www.youtube.com/watch?v=Mb5N08xcxtg&t=300)\].
2. **Query:** Asking questions where the AI synthesises answers from the wiki. These answers can then be "filed back" into the wiki as new pages \[[05:14](http://www.youtube.com/watch?v=Mb5N08xcxtg&t=314)\].
3. **Lint:** A "health check" where the AI looks for stale information, orphan pages, or contradictions \[[05:36](http://www.youtube.com/watch?v=Mb5N08xcxtg&t=336)\].

### Practical Tips for Implementation

- **Viewing:** Use **Obsidian** to view the wiki. Its "graph view" is particularly useful for seeing how concepts connect and identifying "hubs" or "orphans" in your knowledge \[[06:56](http://www.youtube.com/watch?v=Mb5N08xcxtg&t=416)\].
- **Collection:** Use the Obsidian Web Clipper to grab articles and drop them into your raw sources folder for the agent to ingest \[[07:10](http://www.youtube.com/watch?v=Mb5N08xcxtg&t=430)\].
- **Navigation:** The system uses an **Index** (catalog of pages) and a **Log** (chronological record of actions) to help the agent and the user navigate the growing data \[[07:16](http://www.youtube.com/watch?v=Mb5N08xcxtg&t=436)\].

This system is particularly useful for long-term research, developers managing codebases, or business teams tracking meeting transcripts and Slack threads \[[06:09](http://www.youtube.com/watch?v=Mb5N08xcxtg&t=369)\].[Julian Goldie SEO · 6.1k views](http://www.youtube.com/watch?v=Mb5N08xcxtg)
