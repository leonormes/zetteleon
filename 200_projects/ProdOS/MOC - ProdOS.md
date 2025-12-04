---
aliases: []
confidence: 
created: 2025-12-04T14:38:32Z
epistemic: 
last_reviewed: 
modified: 2025-12-04T15:57:30Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: ProdOS MOC
type: 
uid: 
updated: 
---

## ProdOS - Map of Content

This note serves as a central index for the interconnected ideas, frameworks, and systems explored in the LLMPKM project. It organizes the notes into thematic clusters to provide a coherent overview and facilitate deeper understanding.

---

### 1. Core PKM Philosophy & Theory

This cluster deals with the fundamental principles of knowledge management, the nature of notes, and the "why" behind building a Zettelkasten-style system.

- **Foundational Concepts:**
  - [[Atomic vs Structural Notes]]: Defines the two primary note types in the system architecture.
  - [[Units of a PKM]]: A glossary of terms and concepts used throughout the PKM.
  - [[200_projects/ProdOS/The Problem of False Atoms]]: Explores the tension between atomic independence and the reality of interconnected ideas.
  - [[The why of my zettelkasten]]: A reflection on the purpose and motivation for maintaining the PKM.
- **The Nature of Thinking & Writing:**
  - [[200_projects/ProdOS/The Unified Writing to Think Process]]: A five-stage process for turning raw thoughts into synthesized knowledge.
    - [[Stage 1 Generate (The Goldberg Layer)]]
    - [[Stage 2 Clarify (The On Writing Well Layer)]]
    - [[200_projects/ProdOS/Stage 3 Understand (The Writing to Learn Layer)]]
    - [[Stage 4 Connect (The Zettelkasten Layer)]]
    - [[200_projects/ProdOS/Stage 5 Synthesise (The Outcome Layer)]]
  - [[Detailed Example From Spark to Synthesis]]: A practical walkthrough of the writing-to-think process.
  - [[What Organizing Your Thoughts Really Means]]: Discusses how a PKM helps evolve thinking from cyclical to cumulative.
  - [[Not a Final Thought]]: A key insight that notes are not final products but part of an evolving process.

### 2. ADHD, Mindset, and Learning Psychology

This section covers the cognitive and psychological aspects of learning, productivity, and knowledge work, with a strong focus on ADHD-aware strategies.

- **Cognitive Science of Learning:**
  - [[Our Unseen Mental Models]]: Explores naïve realism and the cognitive-emotional feedback loop in how we understand the world.
  - [[Learning Principles and Practices]]: A comprehensive overview of learning techniques like retrieval, interleaving, and the Feynman method.
  - [[Learning through First Principles]]: Discusses the drive to understand foundational concepts, especially in the context of ADHD and systems thinking.
  - [[Building Self Beyond Objective Truth]]: Tackles the challenge of building confidence and identity when "objective truth" is elusive.
- **ADHD-Specific Challenges & Strategies:**
  - [[Breaking the Creation Cycle]]: Addresses the ADHD challenge of restarting projects due to lost context and offers strategies like "State Snapshots."
  - [[Processing IS the Work, Not Prep for Work]]: Reframes the administrative "processing" of notes as a creative act to overcome ADHD-related executive dysfunction.
  - [[lower energy capacity]]: Outlines principles for a productivity system designed to function during periods of low energy.
  - [[Navigating PKM Challenge]]: A detailed user profile outlining the core struggles of an adult with ADHD trying to build a PKM.

### 3. Action & Productivity Frameworks (GTD & ProdOS)

This cluster focuses on practical systems for execution, task management, and aligning daily actions with broader goals.

- **Core Frameworks:**
  - [[Process Over Goals Actionable System]]: A detailed guide for shifting from outcome-based goals to process-based systems, with templates and examples.
  - [[Shifting Focus From Goals Outcomes to Systems Processes]]: A deep dive into the "why" of process primacy, drawing on habit-formation literature.
  - [[Complete Context ProdOS System]]: The master document outlining the vision, architecture, and principles of the "Productivity Operating System."
  - [[ProdOS System Overview and Development Progress]]: A summary of the ProdOS project, its current state, and future plans.
- **Tactical Methods:**
  - [[Action Sequences Form Directed Acyclic Graphs]]: Models workflows as a series of dependent and parallel tasks.
  - [[Context Tags Make Actions Location and Tool Specific]]: Explains the GTD concept of using context tags for efficient task batching.
  - [[Think Like a Man of Action]]: Strategies for breaking the "analysis paralysis" loop by focusing on Minimum Viable Actions (MVAs).
  - [[Day in the Life]]: A template for a process-driven day for a DevOps engineer, integrating timeboxing and reflection.
  - [[The War of Art]]: A summary of Steven Pressfield's concepts of "Resistance" and "Turning Pro."

### 4. LLMs as Thinking Partners

This section details strategies for using Large Language Models as tools for thought, synthesis, and cognitive augmentation, while avoiding common pitfalls.

- **Core Interaction Models:**
  - [[ADHD, LLMs, and PKM Balance]]: Introduces the "Human -> LLM -> Human Sandwich" and the use of convergent prompting.
  - [[LLM To the Extreme]]: A similar exploration of balancing self-thinking with LLM assistance for an ADHD brain.
- **Application in PKM:**
  - [[Chronos Synthesizer Workflow Summary and ADHD Evaluation]]: Designs and evaluates an LLM-driven workflow for maintaining a Source of Truth (SoT) in a PKM.
  - [[I Have a Vague Idea I Want to Capture My Understanding]]: A plan for using Obsidian and LLMs to build up mental models of technical topics like Kubernetes and Terraform.

### 5. Advanced PKM System Design

This cluster contains the technical and architectural thinking behind building a "smart" PKM, treating notes and links as programmable objects.

- **Core Models:**
  - [[Modelling Notes and Links as Objects]]: Introduces the concept of notes and links as objects with properties, using a TCP packet analogy.
  - [[NGSI-LD Report]]: Explores the NGSI-LD standard and JSON-LD for representing context information in a property graph.
  - [[PKM PDU]]: A deep-dive on the "Protocol Data Unit" analogy for PKM, exploring how metadata layers create a navigable knowledge network.
- **Implementation & Context:**
  - [[Capture the Context]]: Discusses the importance of capturing mental models, assumptions, and personal context, not just content.
  - [[Problem and Requirements Statement for Personal Knowledge Management]]: Articulates the core problem the PKM is trying to solve: the disconnect between generic notes and personal understanding.
  - [[Proven Organizational Methods for Managing a Large-Scale Knowledge Base in Obsidian]]: Analyzes various methods like PARA, Zettelkasten, and Faceted Classification for large vaults.
  - [[Key Principles & Mindset Shifts – Processing IS the Work]]: A mindset shift to treat note processing as the primary creative act.

### 6. Practical Application & Workflows

This section connects theory to practice with concrete examples.

- **Thinking & Writing:**
  - [[Elements of Effective Thinking]]: Outlines five habits for improving thinking.
  - [[200_projects/ProdOS/The Unified Writing to Think Process]]: A five-stage workflow for developing thoughts through writing.
- **Self-Reflection & Habit Change:**
  - [[Hansei]]: The Japanese concept of continuous reflection and improvement.
  - [[Powerful Identity]]: Explores the role of identity in habit formation, a key concept for process-oriented systems.
- **Project Example:**
  - [[Problem and Requirements Statement for Personal Knowledge Management]]: Uses the "Velero on Kubernetes" task as a real-world example to refine PKM strategies and prompts.
```dataview
LIST FROM #pkm OR #prodos OR #adhd OR #gtd OR #llm OR #productivity OR #system_design
SORT file.name ASC
```