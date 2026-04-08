---
created: 2026-04-06T17:58:36+00:00
modified: 2026-04-08T18:01:20+00:00
title: Incomplete Trigger Review from your Long-Term Memory
---

Here is an Incomplete Trigger Review from your Long-Term Memory and recent context, categorised using the Getting Things Done (GTD) methodology:

## Coding/Technical Tasks

- OMOP Data Generation:
    - Finish OMOP Stress Testing infrastructure (FTFL-476).
    - Complete the script to generate OMOP synthetic data (FTFL-475).
    - Create unit tests for `omop_generator` offset mathematics and SQL generation logic.
    - Rerun `omop etl-export` with `--reuse-db` and `--reuse-vocab` to verify speed increases.
    - Finalize DuckDB execution logic for streaming data to the "Golden" container.
    - Ensure `libomp` is correctly linked to prevent `data.table` failures.
    - Complete commit and push for `omop_generator` updates.
    - Monitor `feature/FFAPP-4566-OMOP-data-generation` branch for regressions.
    - Re-index Obsidian Vault in Khoj after swapping embedding model to `nomic-embed-text`.
    - Address "Critical" and "High" priority items in `fitConnectHosts` audit (e.g., adding "allowedorigin" to production environments).
    - Refine CLI integration: Finalize connection of `khoj-gemini` bridge to Gemini CLI config.
- Infrastructure as Code (IaC) & Dotfiles:
    - Split long Terraform `.tf` files into modules.
    - Investigate environment drift in Dev/Stage.
    - Refactor hardcoded values (e.g., AMI IDs, variables) in IaC.
    - Address Terraform provider version deprecation warnings.
    - Clean up orphaned resources in Terraform state files.
    - Refactor confusing `values.yaml` files in Helm charts.
    - Address image hygiene (e.g., `:latest` tags, old SHAs) in Kubernetes deployments.
    - Update deprecated Helm API versions.
    - Move secrets from code/configs to Vault/Secret Manager.
    - Execute prioritized refactoring plan for `chezmoi` templates.
    - Complete migration of remaining templates to consume new CUE `resolved_packages` structure.
    - Finalize "Housekeeping" phase of dotfiles refactor (duplicate entries, `zsh.dynamic_completions`).
    - Execute Infrastructure Refactoring Plan (remove `kubectl_manifest.vault_auth` from Terraform jumpbox template).
- Tooling & Environment:
    - Validate Todoist Context Bridge changes and ensure tasks sync correctly with Obsidian.
    - Test Tasks plugin integration with Todoist Context Bridge.
    - Finalize authentication for Todoist MCP (ensure `TODOIST_API_TOKEN` persistence).
    - Test the "Process my dump" command with `00_Inbox/dump.md`.
    - Address slow closing of `nvim` and fix internal routing for the front-end.
    - Restart Colima with increased RAM (6GB+) to resolve search engine and database crashes.
    - Refactor Neovim LazyVim configuration for quicker loading and efficient filetype management, specifically addressing the `:q` exit delay.
    - Build a Python script to generate embeddings for a sample folder (test Semantic Indexer).
- Monitoring & Automation:
    - Fix broken Grafana panels or alert channels.
    - Investigate logging blind spots where errors lack metrics.
    - Automate manual steps in the continuous delivery pipeline.

## Research/Learning Tasks

- Research `shiki-highlighter` for Obsidian and optimize.
- Explore further enhancements for Obsidian Tasks plugin and Dataview integration.
- Investigate the "NHS version" of Synthea for OMOP data work.
- Experiment with building a multi-step PKM research agent in Obsidian.
- Update "Magic Docs" implementation if applicable to personal documentation workflows.
- Map Wabi-Sabi principles (acceptance of imperfection) to system recovery protocols.
- Integrate "Circumstance-Aware Routing" and "The Unschedule" into [[MOC - Prodos]].
- Develop Atomizer Prompt (system instructions for breaking notes into atomic units).

## Administrative/Process Tasks

- Continue drafting `LLMeon README.md`.
- Review and finalize FITFILE Information Management and Communication Guidelines.
- Complete household tasks (bathroom light, Kefir, Fybrogel, Movicol).
- Update `GEMINI.md` to include "Autonomous Action" mandate.
- Ticket the ongoing OMOP data work.
- Develop a formal plan for Identity and Access Management (IAM) in Azure for the team.
- Schedule a security audit for current deployments.
- Define a "Rock" attribute and "resistance field" for task frontmatter.
- Confirm and book family cinema tickets for _Project Hail Mary_.
- Audit shame-triggers against current sprint bottlenecks.
- Define JSON Schemas for "Map" agents.
- Review passages surfaced by AI agent for stalled development tasks.
- Documentation Processing:
    - Process `Network Topography & fitConnectHosts` report: Add notes to Linux Networking MOC (Section 2: Container Networking) including Atomic Notes for Automated Loopback Injection, Internal Service URLs, Asymmetric Federation Config.
    - Process `mkuh Infrastructure refactoring plan`: Link to Infrastructure MOC (e.g., MOC - Infrastructure or MOC - GitOps), and create Atomic Notes for Architectural Bypasses in GitOps, Silent Data Loss in Infrastructure Contracts.
    - Move plugin documentation (`loop-detection.md`, `mcp-servers.md`) to `10_System/Docs/Agent/`.
- Operationalize "Customs Audit": Conduct the first "Customs Audit" session on a stalled strategic initiative.
