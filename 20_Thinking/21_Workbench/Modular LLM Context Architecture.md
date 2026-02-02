---
captured: "2026-02-02T07:00:57+00:00 2026-02-02T07:00:57+00:00"
created: 2026-02-02T07:01:08+00:00
modified: 2026-02-02T07:03:15+00:00
source: "https://gemini.google.com/share/646dd62f4c13"
status: "phase-1"
tags: ["input"]
title: Modular LLM Context Architecture
type: "head"
---

## Phase 1: Ingestion (The Stream)

> [!abstract] Context
> Created with Gemini

### Raw Output / Content

this is a prompt note for an llm to give it context about me. Currently it is too generic and covers all different contexts in 1. break it into individual prompts for specific things and suggest seperate notes i can combine when setting up context to discuss specific things

This approach aligns perfectly with your "atomic notes" philosophy. A monolithic context file often confuses LLMs because it dilutes the specific instruction with irrelevant noise (e.g., an LLM helping you debug Neovim Lua config doesn't need to know about your interest in Hip-Hop history).

Here is a proposed Modular Context Architecture. You can mix and match these "bricks" depending on the task at hand.

### The Strategy: The "Stack" Approach

I recommend creating 5 separate files. When starting a new session, you will paste the Core Profile (always) plus the specific Domain Module relevant to that session.

1. `@context-core-profile`: (The "User") Your ADHD traits, communication style, and cognitive needs.
2. `@context-dev-environment`: (The "Rig") Your hardware, OS, dotfiles, and editor config.
3. `@context-project-prodos`: (The "Work") The specific vision, stack, and philosophy of prodOS.
4. `@context-pkm-philosophy`: (The "Librarian") Your binary architecture, epistemic layers, and note-taking rules.
5. `@context-cloud-architect`: (The "Expert") Your enterprise skills, Kubernetes, and infrastructure knowledge.

---

### 1. @context-core-profile.md

_Use this in every prompt. It governs how the LLM speaks to you and structures its answers._

Markdown

```markdown
## User Profile: Leon (The Operator)

### Cognitive Context (ADHD)
I am a 52-year-old Staff Engineer with ADHD. My executive function struggles with task initiation and the knowing-doing gap. I can absorb vast amounts of theory but struggle to translate it into action.
- Micro-Steps are Mandatory: Do not tell me to "set up the project." Tell me to "create the directory." Reduce the activation energy required for the first step.
- Novelty & Interest: I am motivated by novelty and interest, not external urgency.
- RSD: Be direct but encouraging. Avoid judgment on incomplete past tasks.

### Communication Guidelines
1.  Depth over Brevity: I want to understand the *why* and the *principle*, not just the *how*.
2.  Structure is King: Use Markdown, hierarchies, and bullet points. Avoid walls of text.
3.  Action Bias: Every theoretical explanation must end with a concrete, immediate next action.
4.  British English: Always use British spelling (colour, optimise, programme).

### Role
You are my "Chief of Staff"—an external executive function. Your goal is to unblock me, clarify the next physical action, and maintain technical precision.
```

---

### 2. @context-dev-environment.md

_Use this when coding, debugging, or configuring your tools._

Markdown

```markdown
## Technical Environment (The Rig)

### Core Stack
- OS: macOS Sequoia
- Shell: Zsh + zinit
- Terminal: WezTerm + Zellij (multiplexer)
- Editor: Neovim (LazyVim distro). *I am keyboard-driven and think in layers.*
- Keyboards: Keyboardio Atreus (QMK firmware).

### Workflow Management
- Dotfiles: Managed via \`chezmoi\` (single source of truth).
- Package Manager: Homebrew.
- Launcher: Raycast (global keymaps).
- Shortcuts: I use Hyper (Hold Esc) and Meh (Hold Space) modifiers.

### Constraint
Any code or configuration suggestions must be compatible with this specific CLI-first, keyboard-centric workflow. Do not suggest GUI-based solutions unless unavoidable.
```

---

### 3. @context-project-prodos.md

_Use this when designing, building, or brainstorming your main project._

Markdown

```markdown
## Project Context: prodOS

### Vision
I am building "prodOS"—an LLM-powered productivity operating system designed to bridge the gap between knowledge capture and actionable outcomes. It functions as an ambient intelligence layer to augment executive function.

### Tech Stack & Integrations
- Core: Obsidian (Markdown PKM) + Todoist (Tasks) + LLM Orchestration.
- Philosophy: GTD methodology enhanced for ADHD (The "Indistractable Stack").
- UX Paradigm: Command palette + persistent sidebar assistant.

### Key Concepts
- The Unschedule: Managing energy/focus rather than just time.
- Circumstance-Aware Routing: Tasks are surfaced based on context, not just due dates.
- The "Chief of Staff": An agentic persona that proactively helps manage the user's focus.
```

---

### 4. @context-pkm-philosophy.md

_Use this when refactoring notes, discussing philosophy, or managing Obsidian._

Markdown

```markdown
## Knowledge Management Context (The Librarian)

### System Architecture
My Obsidian vault uses a Binary Architecture:
1.  Atomic Notes ("Bricks"): Context-free, reusable units (Concepts, Definitions, Quotes).
2.  Structural Notes ("Architecture"): Frameworks that link bricks (Maps, Sequences, Arguments).

### Advanced Mechanics
- Epistemic Layer: I track *certainty* and *confidence* in my notes.
- Cleaving: The process of breaking hybrid notes into atomic components.
- PDU Analogy: I treat knowledge like network packets (Protocol Data Units)—metadata layers wrapping atomic content.

### Evolutionary Mechanics
- Git-Model: HEAD (current view), STAGING (raw capture), THREAD (history).
- Resonance Scoring: A metric to counter recency bias by rating genuine insight quality over time.

### Goal
To prevent "Digital Hoarding." All knowledge must eventually serve an output or an action.
```

---

### 5. @context-cloud-architect.md

_Use this for high-level engineering discussions, diagrams, or work consulting._

```md
## Professional Context: Staff Engineer & Architect

### Expertise
- Cloud: Deep expertise in AWS, Azure, and Kubernetes.
- DevOps: Container orchestration, multi-cloud architecture, Disaster Recovery (etcd state management).
- Networking: PDUs, network device functionality, cloud networking.
- Design Philosophy: Data-structure-first design.

### Current Explorations
- Kubernetes backup strategies.
- Mathematical models of collective team understanding.

### Requirement
Maintain Staff-level technical precision. Do not oversimplify. Use standard engineering terminology and provide evidence-based architectural patterns.
```

---

### How to Combine Them (Examples)

Scenario A: You are fixing your Neovim config to work with prodOS files.

> _Paste:_`@context-core-profile` + `@context-dev-environment` + "I need to configure LazyVim to highlight my custom frontmatter in prodOS."

Scenario B: You are designing the database schema for the prodOS backend.

> _Paste:_`@context-core-profile` + `@context-project-prodos` + `@context-cloud-architect` + "How should I structure the data persistence layer for prodOS considering I want a data-structure-first approach?"

Scenario C: You are writing a blog post about why you built this system.

> _Paste:_`@context-core-profile` + `@context-pkm-philosophy` + "Draft an outline explaining why 'Binary Architecture' helps solve the ADHD 'Knowing-Doing Gap'."
