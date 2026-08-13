---
aliases: [Research Transducer]
conformant: false
created: 2026-01-12T16:15:00+00:00
modified: 2026-08-13T10:53:38+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/instruction-so-t-research-to-action-protocol
tags: [adhd-tools, prodos, protocol, research]
title: Instruction SoT - Research-to-Action Protocol
type: sot
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

### 3. The Validation (The Black Box)

- [ ] Pass the Unit Test: Run the relevant validation command.
- [ ] 70% Boundary: If the goal is met, STOP. Do not research "better" ways to do it today.
- [ ] Scribe Commit: Log what you learned in the relevant SoT note and close the file.
