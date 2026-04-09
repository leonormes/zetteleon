---
title: "You said Https://youtu.be/7n5EVMtYA4I?si=32bmVRtP2..."
source: "https://gemini.google.com/app/f55091dba10c5c82"
captured: "2026-04-09T10:03:23+01:00 2026-04-09T10:03:23+01:00"
status: "processing"
tags:
  - "input"
type: "head"
---
## Raw Output / Content
**You**

Https://youtu.be/7n5EVMtYA4I?si=32bmVRtP2bEfIWq0

---

**Gemini**

Here is a summary of the video **"SuperIntelligence: Why the Future of AI is a File System (CORAL)"** by Discover AI (URL: [http://www.youtube.com/watch?v=7n5EVMtYA4I](http://www.youtube.com/watch?v=7n5EVMtYA4I)):

The video explores a new perspective on artificial intelligence research, suggesting that the next leap in capability won't come from updating the internal weights of Large Language Models (LLMs), but rather from developing sophisticated, multi-agent file systems around them \[[00:38](http://www.youtube.com/watch?v=7n5EVMtYA4I&t=38)\]. The presenter refers to this approach as "Advanced Intelligence" (ADI), as the core LLM remains frozen while the surrounding infrastructure handles the open-ended complexity \[[01:15](http://www.youtube.com/watch?v=7n5EVMtYA4I&t=75)\].

**The CORAL Framework** The core subject of the video is **CORAL**, a newly published autonomous multi-agent infrastructure developed by researchers from MIT, Stanford, Meta, Microsoft, and others \[[01:44](http://www.youtube.com/watch?v=7n5EVMtYA4I&t=104)\]. Instead of relying on probabilistic neural networks to learn new skills directly, CORAL outsources the intelligence to a highly deterministic, hierarchical file system \[[03:22](http://www.youtube.com/watch?v=7n5EVMtYA4I&t=202)\].

Key features of the CORAL infrastructure include:

- **Parallel Git Workspaces:** Between four and eight homogeneous agents run in parallel, each operating within an isolated local Git work tree using Bash commands and Python \[[03:50](http://www.youtube.com/watch?v=7n5EVMtYA4I&t=230)\].
- **Shared Persistent Memory:** Global coordination between agents is achieved implicitly through a shared public directory, rather than direct communication \[[04:10](http://www.youtube.com/watch?v=7n5EVMtYA4I&t=250)\]. This directory is categorised into three main elements:
	- **Attempts:** A ledger of all function evaluations across the agents, keyed by commit hashes \[[04:16](http://www.youtube.com/watch?v=7n5EVMtYA4I&t=256)\].
		- **Notes:** Simple markdown files where agents write textual hypotheses about what is or isn't working \[[04:22](http://www.youtube.com/watch?v=7n5EVMtYA4I&t=262)\].
		- **Skills:** Reusable, executable code modules abstracted from successful, localised evaluation runs \[[04:46](http://www.youtube.com/watch?v=7n5EVMtYA4I&t=286)\].

**Overcoming Local Minima** To prevent the autonomous agents from getting trapped in local extrema (repeating the same failed approaches), CORAL introduces a **Heartbeat Intervention Protocol** \[[05:42](http://www.youtube.com/watch?v=7n5EVMtYA4I&t=342)\]. This background runtime manages asynchronous interrupts using two distinct triggers:

- **Interval Triggers:** Forces an agent to pause and synthesise its raw markdown notes into abstracted skills \[[06:13](http://www.youtube.com/watch?v=7n5EVMtYA4I&t=373)\].
- **Plateau Triggers:** If an agent reaches a dead end, it is commanded to attempt a completely orthogonal mathematical approach, providing a "thermal noise" impulse to push it into new territory \[[06:46](http://www.youtube.com/watch?v=7n5EVMtYA4I&t=406)\].

**Cost and Practicality Warnings** While the framework provides highly structured and easily debuggable human-readable outputs (JSON and Markdown files), the presenter warns that it can become exceptionally expensive \[[28:14](http://www.youtube.com/watch?v=7n5EVMtYA4I&t=1694)\]. Because the agents run autonomously in continuous loops without human intervention, a single three-hour run for one agent can cost around $60, while a multi-agent setup can quickly exceed hundreds of dollars in a single day \[[28:34](http://www.youtube.com/watch?v=7n5EVMtYA4I&t=1714)\].

Ultimately, the video highlights a fascinating "sideways" evolution in the industry: leaning on traditional computer science principles, determinism, and structured file systems to manage AI orchestration, rather than attempting to brute-force a single model into becoming a superintelligence \[[32:05](http://www.youtube.com/watch?v=7n5EVMtYA4I&t=1925)\].
