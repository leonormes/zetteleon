---
created: 2026-01-30T17:54:41+00:00
modified: 2026-02-05T19:59:36+00:00
title: AGENTS
---

## AGENTS.md

This file provides context about this Obsidian vault for AI agents.

### Vault Overview

This vault serves as a highly structured 'Life OS' and technical knowledge base, primarily focused on cloud infrastructure, systems architecture, and software engineering. It functions as both a professional workbench for DevOps projects and a deep Zettelkasten for conceptual learning and personal development.

The vault integrates technical expertise in high-scale infrastructure with personal productivity frameworks, including GTD and ADHD-specific management strategies, creating a unified environment for professional output and personal growth.

### Organization

The vault is organized using a numerical prefix system that separates active intake and thinking from permanent reference material. It employs a sophisticated 'Source of Truth' (SoT) and 'Map of Content' (MoC) framework to manage high-density technical information.

- 00_Inbox & 20_Thinking: Used for initial capture and active 'Workbench' drafting. The `21_Workbench` subfolder is where reports, plans, and technical deep-dives (e.g., Grafana upgrades, AWS VPC explanations) are developed before being moved to the library.
- 01_journals: Contains a consistent daily logging practice (`Dailies`) for tracking tasks, progress, and interlinking daily activities with project notes.
- 10_System: Houses the vault's 'engine', including a significant collection of specialized LLM prompts (e.g., 'Principal GTD Logic Engine', 'Helm Platform Review Prompt'), templates, and metadata schemas.
- 30_Library: The primary repository, split into atomic conceptual notes (`100_zettelkasten`), categorized Projects (`200_projects`), and structural indexes. It specifically separates 'Source of Truth' (SoT) notes—which act as definitive protocols—from 'Maps of Content' (MoC) which serve as navigational hubs.
- 02_bases & 400_indexes: Contain high-level dashboards like the 'Life OS Dashboard' and 'All Tasks' list, facilitating a top-down view of the vault's contents.

### Key Topics

- Cloud Infrastructure & DevOps: Extensive focus on AWS (ALB, VPC), Kubernetes networking, Helm charts, and cross-cloud hybrid debugging.
- Observability: Detailed documentation on Grafana stacks, monitoring optimizations, and observability patterns.
- Software Engineering & Data Modeling: Specific interests in Rust, CUE data architecture, Type Theory, and security hardening.
- Personal Knowledge Management: Advanced use of Zettelkasten, MoCs, and 'Source of Truth' (SoT) patterns to manage information lifecycle.
- Psychology & Productivity: Exploration of ADHD emotional reasoning, virtue ethics, GTD (Getting Things Done) methodologies, and personal project management (e.g., career search, home renovation).
- Mathematics: Theoretical topics including Type Theory and general mathematical analogies applied to engineering.

### User Preferences

The user demonstrates a strong preference for high-precision, structured, and authoritative documentation. The existence of the 'Source of Truth' (SoT) folder and the 'fileClasses' system suggests that information should be treated as definitive and structured once it reaches the library. The user values technical accuracy and architectural consistency over casual summaries.

Responses should be analytical and professional, mirroring the user's own tendency to create 'Protocols' and 'Instruction SoTs'. The user appears to value modularity, often moving notes from a 'Workbench' phase to a 'Permanent' library status, suggesting that suggestions for new content should consider where it fits in the existing organizational lifecycle. There is also a clear preference for using LLMs as 'Logic Engines' to assist with complex task management and technical reviews.

### Custom Instructions

- Reference SoTs: When providing technical advice, check for existing 'SoT' or 'Protocol' notes in `30_Library/SoT/` to ensure consistency with the user's established 'Source of Truth'.
- Link via MoCs: Always suggest or look for relevant 'Maps of Content' (MoCs) in `30_Library/MoC/` or `30_Library/400_indexes/` to maintain the vault's interconnected structure.
- Distinguish Note Types: Maintain the distinction between atomic, conceptual Zettelkasten notes (`100_zettelkasten`) and action-oriented Project notes (`200_projects`).
- Technical Specificity: Use domain-specific terminology (e.g., 'CUE Data Architecture', 'Helm Platform Review', 'VPC Peering') as the user is a subject matter expert in DevOps and systems engineering.
- Workflow Awareness: Recognise that notes in `20_Thinking/21_Workbench` are in-progress and may require refinement or consolidation into the `30_Library` using the user's established templates.
