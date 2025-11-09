---
aliases: []
confidence: 
created: 2025-05-20T11:11:58Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:15Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: "FFAPP-3770 Scale down EC2 node size at EOE "
type: project
uid: 
updated: 
version:
---

## Project: FFAPP-3770 Scale down EC2 Node Size at EOE

---

### 1. Why is This Important? (Purpose & Principles)

Keiran has requested we scale down costs where possible at EOE as it has become a line item on their internal governance calls (circa 2k per month spend).

Options include

- Resizing Workflow and System ec2 nodes.
- Resizing jumpbox node
- Powering off jumpbox manually when not needed

---

### 2. What Does Success Look Like? (Outcome Visioning)

*What's the desired end state? What would make you say "this is done" or "I understand this now"? Bullet points are great. This can be high-level initially.*

Keiran reports that costs have gone down enough.

---

### 3. Ideas & Brainstorming (How Could I Achieve this?)

*This is your sandbox. Dump all ideas, questions, potential resources, links, code snippets, and thoughts here. Don't censor or organise too much at this stage. Use extensively!*

- Initial thoughts on approach:
  - Turn off the jumpbox
  - Put max and desired size to 1
- Questions I have:
  - What happens to the hyve pods?
- Resources:
- Random ideas:

---

### 4. Organised Thoughts & Potential Steps (Organising)

*Review your Brainstorming section. Start to group related ideas, identify potential phases, or structure the information. This is where you bring some order to the chaos. Use headings (##, ###) and bullet points.*

---

### 5. Next Actions (What's the *very* next thing?)

*This is the most critical part for momentum. What is the \_absolute next, small, physical action* you can take to move this forward?

- [x] action [completion:: 2025-09-30]
