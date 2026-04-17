# AGENTS.md

This file provides context about this Obsidian vault for AI agents.

## Vault Overview

This vault is a high-fidelity Personal Knowledge Management (PKM) system and digital garden, bridging deep theoretical research in mathematics and type theory with practical software engineering and operational protocols. It functions as a 'Second Brain' for Leon, integrating technical expertise, philosophical inquiry, and structured ADHD management strategies into a unified system of nearly 2,000 interlinked documents.

The vault serves as both a research laboratory for complex systems (distributed computing, formal methods) and a production environment for active engineering projects, such as synthetic health data pipelines (OMOP).

## Organization

The vault follows a modular structure blending Zettelkasten principles with functional hierarchies:

- **Capturing & Meta**: `00_Inbox` manages raw inputs (Readwise, AI exports), while `10_System` contains the vault's governing logic, including AI prompts and structural templates.
- **Temporal & Thinking**: `01_journals/Dailies` tracks daily progress. `20_Thinking/21_Workbench` hosts active 'HEAD' notes for iterative drafting and cognitive work.
- **The Library (Core Knowledge)**: The primary repository, subdivided into:
  - `100_zettelkasten`: Over 1,000 atomic, declarative notes with full-sentence titles.
  - `200_projects`: Categorised into active work (e.g., OMOP), Infrastructure, and Development.
  - `MoC`: Maps of Content serving as central hubs for complex topics.
  - `ops` and `SoT`: Definitive protocols and 'Sources of Truth' for technical and personal workflows.
- **Indexes**: `400_indexes` contains automated link reports and curated watchlists.

Notes are densely interconnected through bidirectional links and MOCs, facilitating a 'bottom-up' knowledge synthesis where atomic ideas are aggregated into higher-level frameworks.

## Key Topics

- **ADHD Management & Neurodivergent Productivity**: Executive function, dopamine-leveraged workflows, burnout prevention, and adapted GTD protocols.
- **AI Agent Development & Workflow**: Prompt engineering, MCP servers, MVC enforcement for agents, and 'Research-to-Action' protocols.
- **Health Data & Synthetic Pipelines**: NHS-OMOP synthetic data generation, patient pipeline architecture, and data-first IaC.
- **Software Engineering & DevOps**: Linux networking, Kubernetes, CUE migration, Identity Governance, and distributed systems (Paxos vs Raft).
- **Mathematics & Philosophy of Science**: Type theory, formal systems, effective theories, and the distinction between instrumentalism and realism.
- **Personal Knowledge Management**: Zettelkasten methodology, MOCs, and structured information architecture.
- **Philosophy & Resilience**: Stoicism, Miyamoto Musashi, and emotional regulation.

## User Preferences

Leon employs a highly systematic and intellectual approach, preferring declarative, full-sentence note titles that capture core insights (e.g., 'Sprint Journaling Prevents Overwhelm in ADHD'). There is a rigorous emphasis on establishing 'Sources of Truth' (SoT) and repeatable 'Operations' (ops), indicating a preference for precision and protocol-driven workflows over casual notes.

Responses should be technical, high-density, and provided in British English (en-GB). Leon values the distinction between active 'Thinking' (found in the Workbench with 'HEAD' prefixes) and the vetted knowledge in the 'Library'. When discussing projects, refer to the active context in `200_projects/00_Active_Projects`.

## Custom Instructions

- Always search `30_Library/ops/` or `30_Library/SoT/` before providing technical or procedural advice to ensure alignment with existing protocols.
- Use descriptive, declarative full-sentence titles for all new notes.
- Maintain the 'HEAD' prefix for active drafting files within `20_Thinking/21_Workbench`.
- Apply 'ProdOS' frontmatter metadata to all new or revised notes as specified in `30_Library/SoT/SoT - ProdOS Note Metadata (Frontmatter).md`.
- Prioritise 'MOCs' (Maps of Content) to provide context when synthesising broad topics.
- Strictly support the 'Research-to-Action' protocol by translating theoretical insights into actionable 'ops' or 'SoT' documents.
