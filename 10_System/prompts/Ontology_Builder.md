---
aliases: ["Ontology Prompts", "LLM Meta-Prompts"]
confidence: "High"
created: 2026-01-05
tags: ["prompts", "meta", "system", "llm"]
type: "System"
---

# Protocol: Ontology Maintenance

Use these prompts to maintain and expand the [[SoT - Knowledge Architecture (Associative Ontology)]].

## Protocol 0: The Architect (Vault Scan)

*Use this when you want to rebuild the entire map from scratch or analyze a large set of new folders.*

> **Role:** Systems Ontologist & Knowledge Architect.
> **Objective:** Map the user's "Intellectual Landscape" by converting a flat list of files into a **Layered Associative Ontology**.
>
> **Strategy (Map-Reduce):**
> 1.  **Phase 1 (Topography):** Scan filenames/tags in `@30_Library/SoT/` and `@30_Library/MoC/` to identify 5-7 "Primary Domains" (Clusters) without reading content.
> 2.  **Phase 2 (Deep Scan):** Read the 3 most central notes in each Domain to extract **1st Principles**.
> 3.  **Phase 3 (Mapping):** Define relationships using Typed Links:
>     *   **[Extends]:** Logic applied to a new field.
>     *   **[Catalyses]:** Fuel/Prerequisite.
>     *   **[Intersects]:** Shared boundary/principle.
>     *   **[Informs]:** Provides data/models.
>
> **Output:** A structured `SoT - Knowledge Architecture` note with Logical Layers, a Relationship Matrix, and a D2 Diagram.

## Protocol 1: The "New Interest" Scanner

*Use this when you have dumped a lot of new notes into `00_Inbox` or `20_Thinking` and want to see where they fit.*

**Role:** Systems Ontologist.
**Context:** I have a master [[SoT - Knowledge Architecture (Associative Ontology)]] that maps my interests into three layers: Core Logic, Engine (Cognition/Meaning), and Territory (Applied).
**Task:** Analyze the attached new notes.
1.  **Classify:** Which Layer/Domain do these notes belong to?
2.  **Extract:** What are the "First Principles" in these notes?
3.  **Link:** How do these new concepts connect to my existing domains? (Use: [Extends], [Intersects], [Catalyses], [Prerequisite]).
4.  **Update:** Propose a specific text update for the `SoT - Knowledge Architecture (Associative Ontology)` note to include this new field.

## Protocol 2: The "First Principles" Distiller

*Use this when you want to deepen your understanding of a specific domain (e.g., "Software") by finding its root axioms.*

> **Role:** First Principles Thinker.
> **Context:** I am analyzing the domain: **[Insert Domain, e.g., Data-Centric Engineering]**.
> **Task:** Read the core notes in this domain.
> 1.  **Strip:** Remove all "Syntax" (specific tools, languages, current events).
> 2.  **Identify:** What are the immutable "Laws of Physics" for this domain? (e.g., "Complexity is conserved," "Energy follows the path of least resistance").
> 3.  **Map:** Show how these laws are isomorphic to laws in **[Insert Another Domain, e.g., Biology or ADHD]**.
> **Output:** A concise list of axioms and cross-domain isomorphisms.

## Protocol 3: The "Graph Refresh" (D2 Diagram)

*Use this when the Ontology note text has changed, and you need to update the visual diagram.*

> **Role:** D2 Diagram Architect.
> **Input:** The current text content of [[SoT - Interest Ontology]].
> **Task:** Update the D2 diagram code block to reflect the new relationships described in the text.
> **Constraints:**
> *   Keep the 3-Layer structure (Clusters).
> *   Use the relationship types: `Catalyses`, `Extends`, `Intersects`, `Prerequisite`, `Informs`.
> *   Ensure the direction is `down`.
> *   Add tooltips to nodes for clarity.

## Protocol 4: The "Connection Seeker"

*Use this when you feel stuck or siloed in one topic.*

> **Role:** Interdisciplinary Researcher.
> **Task:** Find a hidden connection between **[Topic A]** and **[Topic B]**.
> **Method:**
> 1.  Look for shared vocabulary (e.g., "Protocol," "Latency," "Energy").
> 2.  Look for shared structural problems (e.g., "How to manage scale," "How to handle failure").
> 3.  Propose a "Bridge Note" title that would unify these two concepts.
