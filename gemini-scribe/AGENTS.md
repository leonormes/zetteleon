# AGENTS.md

This file provides context about this Obsidian vault for AI agents.

## Vault Overview

This vault functions as a highly structured 'Life OS' and technical operating manual, primarily focused on cloud infrastructure (AWS/Azure), systems architecture, and software engineering. It serves as both a professional workbench for complex DevOps deployments and a deep Zettelkasten for conceptual learning and personal development.

The system integrates high-level technical expertise in observability and generative infrastructure with personal productivity frameworks, specifically tailored for ADHD-specific management and GTD (Getting Things Done) methodologies. It is designed to move information from chaotic capture to definitive, authoritative 'Sources of Truth' (SoT).

## Organization

The vault uses a numerical prefix system to separate active intake and cognitive processing from permanent reference material. It is built around a sophisticated 'Source of Truth' (SoT) and 'Map of Content' (MoC) framework.

- **00_Inbox & 20_Thinking**: Used for initial capture and active drafting. The `21_Workbench` subfolder is the primary engine for current work, often using a `HEAD - [Timestamp]` or `Question - [Topic]` naming convention for active investigations (e.g., Grafana upgrades, Azure VNet debugging, HIE-NNUH forensics).
- **01_journals**: Contains a consistent daily logging practice (`Dailies`) for tracking tasks and progress, interlinking daily activities with project notes.
- **10_System**: Houses the vault's 'engine', including specialized LLM prompts (e.g., 'Technical Knowledge Engineer', 'Principal GTD Logic Engine'), templates (e.g., 'PRODOS Scope-Lock'), and metadata schemas in `fileClasses`.
- **30_Library**: The primary repository, containing over 1,500 files split into atomic conceptual notes (`100_zettelkasten`), categorised Projects (`200_projects`), and structural indexes. It distinguishes between 'Source of Truth' (SoT) notes—which act as definitive protocols—and 'Maps of Content' (MoC) which serve as navigational hubs.
- **02_bases & 400_indexes**: Contain high-level dashboards like the 'Life OS Dashboard' and 'All Tasks' list to facilitate a top-down view of the vault's contents.

Notes are heavily interlinked using a 'bottom-up' Zettelkasten approach that matures into 'top-down' MoCs and SoTs. Technical work in the `21_Workbench` is designed to be distilled into the Library once a 'Source of Truth' is established.

## Key Topics

- **Cloud Infrastructure & DevOps**: Deep focus on Azure (AKS Networking, VNet, Resource Manager) and AWS (ALB, VPC, Networking MOCs), including specific forensic analysis like FFNode and FITFILE deployments.
- **Observability & Networking**: Detailed documentation on Grafana stacks, network debugging protocols (HIE-NNUH), OpenSSL certificate operations, and scalable private connectivity standards.
- **Software Engineering & Data Modeling**: Specific interests in Rust, CUE data architecture, Type Theory, and security hardening (ACR Authentication, Secret Management, ArgoCD secrets).
- **Personal Knowledge Management**: Advanced use of Zettelkasten (900+ notes), MoCs, and 'Source of Truth' (SoT) patterns to manage information lifecycle.
- **Psychology & Productivity**: Exploration of ADHD emotional reasoning, virtue ethics, Schopenhauer, GTD methodologies, and 'Research-to-Action' protocols.
- **Systems Thinking**: Theoretical topics including 'Conservation of Complexity', 'Configuration Fragility', and mathematical analogies applied to engineering (e.g., 'Car Mechanic vs Engineer').

## User Preferences

The user demonstrates a strong preference for high-precision, structured, and authoritative documentation. Information is treated as definitive once it reaches the 'Source of Truth' (SoT) status. The user values technical accuracy, architectural consistency, and 'Scope-Locking' to prevent project drift.

Responses should be analytical, professional, and modular. The user employs LLMs as 'Logic Engines' or 'Technical Knowledge Engineers' to assist with complex task management and technical reviews. There is a clear preference for using established templates (like the 'HEAD_note' or 'PRODOS' templates) and following specific 'Protocols' for research and action.

The writing style is formal and intellectual, often drawing parallels between technical systems and philosophical concepts. The user relies on 'Structural Gates' and 'MVC Enforcement' when interacting with AI agents to ensure quality and consistency.

## Custom Instructions

- **Reference SoTs**: When providing technical advice, always check for existing 'SoT' or 'Protocol' notes in `30_Library/SoT/` (e.g., 'SoT - Kubernetes Networking' or 'Jira Dependency Management SoT') to ensure consistency with established truths.
- **Link via MoCs**: Suggest or look for relevant 'Maps of Content' (MoCs) in `30_Library/MoC/` or `30_Library/400_indexes/` to maintain the vault's interconnected structure.
- **Distinguish Note Types**: Maintain the strict distinction between atomic, conceptual Zettelkasten notes (`100_zettelkasten`) and action-oriented Project notes (`200_projects`).
- **Technical Specificity**: Use domain-specific terminology (e.g., 'CUE Data Architecture', 'Helm Platform Review', 'VPC Peering', 'Structural Gates') as the user is a subject matter expert.
- **Workflow Awareness**: Recognize that notes in `20_Thinking/21_Workbench` are in-progress. If assisting with these, suggest refinement or consolidation into the `30_Library` using the 'HEAD_note' or 'SoT' templates.
- **ADHD/GTD Context**: When assisting with productivity, refer to 'ADHD Emotional Reasoning' and 'Principal GTD Logic Engine' notes for context on the user's preferred cognitive frameworks.
- **Protocol Adherence**: Follow the 'Instruction SoT - Research-to-Action Protocol' for any research tasks to ensure they move from investigation to actionable items.
