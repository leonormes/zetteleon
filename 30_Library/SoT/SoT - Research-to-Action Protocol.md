---
aliases: [Research Transducer]
created: 2026-01-12T16:15:00+00:00
modified: 2026-07-13T08:52:53+00:00
permalink: llmeon/30-library/so-t/so-t-research-to-action-protocol
tags: [adhd-tools, prodos, protocol, research]
title: SoT - Research-to-Action Protocol
type: Instruction
---

## Instruction SoT - Research-to-Action Protocol

- Trigger: When a HEAD note requires "more research" or "understanding" before you can act.
- Objective: To extract just enough logic to form a Unit Test.

### 1. The Hangar Phase (Scope-Lock)

- [ ] Set a "Hurry" Timer: 20 minutes maximum.
- [ ] Identify the "Boss Fight": What specific technical hurdle am I researching? (e.g., "How to pass a boolean into a Helm template").
- [ ] Define the Minimal Artifact: What is the smallest piece of evidence that I have "understood" this? (e.g., A 3-line YAML snippet).

### 2. The Execution Phase (The Cockpit)

- [ ] Starter Task: Open the relevant file _before_ you start reading documentation. This creates "Hardware Sympathy" with the code while you learn.
- [ ] The Oakley Hard Start: Attempt to write the logic from memory for 5 minutes. If it fails, you have now created a specific "Context Gap" for your research to fill.

### 3. The Commit (Exit & Persist)

If the Unit Test passes:

- [ ] 70% Boundary: If the goal is met, STOP. Do not research "better" ways to do it today.
- [ ] Scribe Commit: Log what you learned in the relevant SoT note and close the file.

If the Hurry Timer fires first:

- [ ] `#SAVESTATE`: Log the specific Context Gap you identified (what you now know you don't know).
- [ ] Set the Next Starter Task: Define the exact search query or doc page to open when you resume.
- [ ] Close the file. Do not "just five more minutes" it.


## Related

- [[MOC - ADHD Experiments & Protocols]]
- [[MOC - ADHD (The Master Map)]]
- [[MOC - ADHD Project Continuation Challenge]]
- [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]]

