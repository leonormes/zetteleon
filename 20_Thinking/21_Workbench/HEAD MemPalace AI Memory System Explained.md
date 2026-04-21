---
captured: "2026-04-09T13:28:59+01:00 2026-04-09T13:28:59+01:00"
created: 2026-04-09T12:29:04+00:00
modified: 2026-04-20T13:21:27+00:00
source: "https://gemini.google.com/app/091c9a883284ce43"
status: "processing"
tags: ["input"]
title: HEAD MemPalace AI Memory System Explained
type: "head"
---

## Raw Output / Content

You

<Https://youtube.com/watch?v=4RHgCJVcdQM&si=StbOWCZ>\_8vkH9kbI

---

Gemini

Here is a summary of the video based on the provided link:

### Claude Code + Milla Jovovich = Ultimate Memory System?

In this video, creator Mansel Scheffel explores MemPalace, a brand new, locally hosted, open-source AI memory system. The tool is designed to solve the limitations of standard vector databases by highly organising conversational data, allowing AI assistants (like Claude) to recall past facts, decisions, and context with incredible accuracy.

Here is a breakdown of how the system works and the results of the creator's testing:

How MemPalace Organises Data To stop the AI from returning irrelevant search results, MemPalace categorises all information into specific labels before running a semantic search \[[01:26](http://www.youtube.com/watch?v=4RHgCJVcdQM&t=86)\]:

- The Wing (The "Who"): This top-level label filters data by client, person, or project (e.g., limiting a search only to conversations about a specific client named "Sarah") \[[01:43](http://www.youtube.com/watch?v=4RHgCJVcdQM&t=103)\].
- The Room (The "Topic"): Inside a Wing, data is further divided into topics, such as "website", "emails", or "payments" \[[02:23](http://www.youtube.com/watch?v=4RHgCJVcdQM&t=143)\].
- The Hall (The "Type"): This categorises the _nature_ of the memory, filtering by facts/decisions, milestones/events, preferences/habits, or advice \[[03:09](http://www.youtube.com/watch?v=4RHgCJVcdQM&t=189)\].

Storage and Token Compression Inside each "Room", MemPalace uses a dual-storage system to save on AI token costs \[[03:53](http://www.youtube.com/watch?v=4RHgCJVcdQM&t=233)\]:

- Closets (Triple AK Compression): A token-efficient, rule-based shorthand dialect that compresses large paragraphs into a dense format that AI models can read natively.
- Drawers: The original, uncompressed text stashed alongside the compressed version, just in case the AI needs the full, raw context later.

The Tech Stack & Knowledge Graph Under the hood, the system is completely free and runs locally \[[09:08](http://www.youtube.com/watch?v=4RHgCJVcdQM&t=548)\]. It stores the "Drawers" in Chroma DB (a vector database for semantic search) and uses SQLite to maintain a Knowledge Graph. This graph tracks "temporal entity triples"—meaning it understands _when_ a fact stops being true (e.g., if you change jobs, it won't mistakenly recall your old job as your current one for new queries) \[[09:43](http://www.youtube.com/watch?v=4RHgCJVcdQM&t=583)\].

Real-World Testing Scheffel uses Claude Code to install the system and mine his historical JSONL conversation files (over 186 conversations) \[[13:28](http://www.youtube.com/watch?v=4RHgCJVcdQM&t=808)\]. When tested, the system successfully pulled up the exact technical nuances of a past plugin error \[[15:23](http://www.youtube.com/watch?v=4RHgCJVcdQM&t=923)\]. Furthermore, when asked to recall his personal profile, MemPalace accurately summarised his 12-year consulting career, locations, and current AI operating system projects without hallucinating \[[16:35](http://www.youtube.com/watch?v=4RHgCJVcdQM&t=995)\].

Conclusion The creator concludes that for a version 1 release, MemPalace is highly impressive and accurate for autonomous AI workflows. While humans who are visual thinkers might still prefer tools like Obsidian for viewing their notes, MemPalace provides a brilliant semantic search backend that AI agents can query directly \[[19:41](http://www.youtube.com/watch?v=4RHgCJVcdQM&t=1181)\].

Link to video: [https://www.youtube.com/watch?v=4RHgCJVcdQM](https://www.youtube.com/watch?v=4RHgCJVcdQM)[Mansel Scheffel · 8.2k views](http://www.youtube.com/watch?v=4RHgCJVcdQM)
