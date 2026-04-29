---
captured: "2026-04-29T09:16:15+01:00 2026-04-29T09:16:15+01:00"
created: 2026-04-29T08:16:16+00:00
modified: 2026-04-29T08:46:57+00:00
source: "https://gemini.google.com/app/4e9696d74c063c57"
status: "processing"
tags: ["input"]
title: HEAD Harness Engineering
type: "head"
---

## Raw Output / Content

You

<https://youtu.be/uLWOLmeHOSE?si=LwTbwwuQOLOiw0UW>

---

Gemini

This video features a discussion between Thoughtworks experts Birgitta (Biga) Böckeler and Chris Ford regarding the concept of Harness Engineering for AI coding agents.

The core premise is that to get reliable results from AI agents (like Claude Code, Cursor, or GitHub Copilot), developers must build a "harness" around them—a combination of instructions and automated checks that ensure the AI remains within desired technical and architectural boundaries.

### Key Concepts and Frameworks

The speakers distinguish between two main components of a harness:

- Guides (Feed-Forward): These are the instructions provided _before_ the AI generates code. They typically include markdown files (e.g., `rules.md` or `.cursorrules`), coding conventions, and architectural principles. \[
	[05:09](http://www.youtube.com/watch?v=uLWOLmeHOSE&t=309)
	\]
- Sensors (Feedback): These are automated, often deterministic tools that provide feedback _after_ the code is generated. This allows the agent to self-correct before a human even reviews the work. \[
	[06:05](http://www.youtube.com/watch?v=uLWOLmeHOSE&t=365)
	\]

### The Role of Sensors

Biga highlights that while many developers focus on "the battle of markdown files" (guides), they underutilise computational sensors. These include:

- Static Analysis: Tools like ESLint or Semgrep to enforce code quality and complexity limits (e.g., cyclomatic complexity or maximum function arguments). \[
	[37:42](http://www.youtube.com/watch?v=uLWOLmeHOSE&t=2262)
	\]
- Structural Checks: Tools like Dependency Cruiser to ensure the AI doesn't violate architectural boundaries (e.g., preventing a domain layer from importing an external SDK). \[
	[48:41](http://www.youtube.com/watch?v=uLWOLmeHOSE&t=2921)
	\]
- Test Quality: Moving beyond simple code coverage to use Mutation Testing (changing code to see if tests fail) to identify "survivors" or missing assertions that the AI might have skipped. \[
	[44:03](http://www.youtube.com/watch?v=uLWOLmeHOSE&t=2643)
	\]

### Practical Insights from Experiments

Biga shares findings from a feature-building experiment comparing a "sensor-rich" environment to a "sensor-less" one:

- AI Design Fails: Without sensors, agents frequently forget to add tests, create overly complex functions, or ignore established folder structures. \[
	[30:42](http://www.youtube.com/watch?v=uLWOLmeHOSE&t=1842)
	\]
- Continuous Drift Detection: She recommends "garbage collection" sessions where sensors are run repeatedly to catch compounding technical debt that AI might introduce over months. \[
	[12:48](http://www.youtube.com/watch?v=uLWOLmeHOSE&t=768)
	\]
- Human Steering: The goal isn't necessarily 100% autonomy, but rather creating "higher abstraction loops" so humans can oversee the AI's health without reading every single line of a massive diff. \[
	[28:41](http://www.youtube.com/watch?v=uLWOLmeHOSE&t=1721)
	\]

### Future Outlook

The discussion concludes with the idea of Harness Templates—pre-configured sets of sensors and guides tailored to specific application types (e.g., a data dashboard vs. a CRUD service) that can be instantly instantiated to keep agents in check. \[

[54:37](http://www.youtube.com/watch?v=uLWOLmeHOSE&t=3277)

\]

Video Link:

[Harness engineering beyond skills: Using sensors to keep your coding agent in check](http://www.youtube.com/watch?v=uLWOLmeHOSE)
