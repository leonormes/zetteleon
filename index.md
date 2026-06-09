---
created: 2026-04-28T00:00:00+00:00
modified: 2026-06-09T03:35:00+01:00
tags: [index, system]
title: index
---

## Vault Index

Hermes-maintained catalog of all wiki pages. One line per page.

Updated automatically on every Ingest. Do not edit manually.

---

### `wiki/people/`

_(empty—populated on first ingest)_

### `wiki/projects/`

- [[raw/2026-05-30-pieces-ftfl638-tolerations-permissive.md]]—FTFL-638 tolerations permissive confirmation
- [[wiki/projects/12 Million Patient Synthetic NHS-OMOP Pipeline]]—FITFILE synthetic NHS OMOP data generation & stress-test initiative (up to 12M patients, 5-node Parquet datasets).
- [[wiki/projects/Azure AKS Backup — FTFL]]—Azure Backup for AKS covering FTFL-596/599/615: vault, extension, RBAC, trusted access binding, Terraform dependencies; 9 validated components (private storage, PE subnet, DNS, vault, snapshot RG, extension, policy, trusted binding, backup instance); IaC action plan defined with Phase 1–3 roadmap and validation criteria; Terraform module review completed (2026-05-01) validating plan against manual CLI end-state, identifying import vs creation distinction, secrets configuration gaps, and security considerations.
- [[wiki/projects/Azure Backup Restore Runbook]]—FTFL-599: operational runbook documenting az dataprotection CLI sequences for backup initialization, validation, and restore operations.
- [[wiki/projects/Antigravity CLI Migration]]—Migration from Gemini CLI to Antigravity CLI (`agy`) before June 18, 2026 deadline; includes Claude Code prompt for chezmoi config migration (remove Gemini, install agy).
- [[wiki/projects/CoS-Work-Review-System]]—Automated Hermes cron job that queries Jira for open tickets, reviews against Obsidian PKM, and updates Source of Truth; built 2026-05-26 with curl-based jira-fetch.js workaround for Node.js fetch() proxy incompatibility on corporate VPN.
- [[wiki/projects/Future Roadmap Planning]]—team roadmap presentation meeting set up by WJ; preparing two topics.
- [[wiki/projects/MKUH Azure Backup]]—Azure Backup deployment for Milton Keynes University Hospital; part of EoE Data Providers program.
- [[wiki/projects/NNU Azure Backup]]—FTFL-596: Azure Backup configuration for Norfolk and Norwich University Hospital via private endpoint on private test cluster.
- [[wiki/projects/ProdOS-Workflow]]—AI Chief of Staff bridge between Todoist (action engine) and Obsidian (source of truth); Hermes Gateway periodically checks Jira + Microsoft Teams, updates Obsidian, keeps Todoist in sync; requirements + Hermes /goal prompt delivered 2026-05-26.
- [[wiki/projects/Security and Maintenance Roadmap]]—moving from annual pen tests to continuous security and maintenance as a first-class track.
- [[wiki/projects/Terraform IaC Modules]]—FTFL-596/615: Terraform modules for Azure Backup for AKS, handling Vault/AKS MSI role assignments and trusted access role bindings; LLM prompt created to audit module and produce implementable plan with current state inventory, gaps, proposed changes, migration steps, and git-friendly patch diffs.
- [[wiki/projects/Unified LLM Router Cockpit]]—unifying LLM tooling (Ollama, Hermes, Claude, Gemini, Pieces) into a deterministic chezmoi-managed workflow.
- [[wiki/projects/AWS SSM Session Troubleshooting]]—AWS Systems Manager session login failure diagnosis: missing `s3:GetEncryptionConfiguration` permission on SSM role preventing session log writes to S3 bucket.
- [[wiki/projects/Azure Entra ID IAM → IaC + PIM Migration]]—High-stakes project to migrate Entra ID configuration to Infrastructure as Code, implement Privileged Identity Management, and tidy stale policies; includes break-glass account blueprint prerequisite.
- [[wiki/projects/Execution Protocol for High-Friction Work]]—Personal execution protocol (Pre-Flight → Walking Skeleton → Unschedule → WIP Limits) for initiating large, ambiguous engineering projects.
- [[wiki/projects/GitOps Deployment Pipeline Optimisation]]—Incremental investigation and optimisation of a live GitOps deployment pipeline measured via Four Key Metrics; no big-bang replacements.
- [[wiki/projects/Hermes Config Production-Ready Audit]]—Config.yaml audit identifying redundancies, conflicts, and ~40% config reduction opportunity; produced 7-phase /goal instruction set for production-ready workstation convergence; comprehensive Discovery Report commissioned and delivered 2026-05-24 synthesising all LTM-captured configuration knowledge; detailed Cursor config validation (2026-05-28) confirmed all applied changes including approvals.mode: smart, delegation lockdown, MCP tool filters, 4 new infra skill files.
- [[wiki/projects/Hermes Integration — Provider Adapter Setup]]—concrete implementation project to wire Claude and Gemini as first-class providers within Hermes via provider adapters, keeping Hermes as orchestrator and PKM hub.
- [[wiki/projects/Hermes Iteration Limit Configuration]]—Debugging workstream resolving 10/10 turn freeze: identified confusion between `max_turns` (main chat loop) vs `max_iterations` (background delegation) configuration parameters.
- [[wiki/projects/Hermes-Model-Configuration]]—Diagnosis of `qwen/qwen3.5:cloud` invalid model ID error: traced stale reference to profile YAML files; both live and chezmoi configs already correct.
- [[wiki/projects/Hermes-TUI-Startup-Performance]]—Investigation into slow `hermes --tui` startup (30–40+ seconds); /goal prompt composed for self-diagnosis of config bottlenecks.
- [[wiki/projects/Starship-Performance-Tuning]]—Analysis and optimisation of Starship prompt config (starship.toml): identified critical bottlenecks including 2000ms command_timeout, unscoped k8s/azure/aws modules.
- [[wiki/projects/K8s Cluster Stress Testing with OMOP Data]]
- [[wiki/projects/Kubernetes-Cluster-Bootstrapping]]—Automating ArgoCD deployment on private K8s clusters after Terraform provisioning; exploring argocd-autopilot, Terraform Helm/K8s providers, CAPI, Flux, Crossplane patterns.—Summer project to validate distributed Kubernetes cluster stability under large OMOP clinical data loads; scoped via GTD Natural Planning Model.
- [[INSIGHTFILE_PIPELINE_REPORT]]—GitLab CI/CD automation research for FITFILE/Hermes: comprehensive search synthesis, 7-phase TRANSFER artifact, cursor-based pagination workflow (2026-05-18).
- [[FTFL-673 Grafana Deploy All Envs]] — FTFL-673: deploy fixed Grafana across all environments; extends FTFL-638 testing cluster upgrade with two-phase Hermes prompt (context gather → smarter model plan via OpenRouter).
- [[wiki/projects/Grafana Alloy Monitoring — FTFL-638]]—Kubernetes monitoring stack: Grafana/Alloy Helm deployment, Loki log labeling, values.yaml schema design, and testing cluster fix plan for FTFL-638/511/512; acceptance criteria include cue vet validation, job label alignment (namespace/container), and ArgoCD-synced Alloy-logs DaemonSet.
- [[wiki/projects/MCP Proxy Robustness and High Availability]]—Planning initiative to make mcp-proxy resilient across multiple AI consumers (Hermes, Claude, Cursor, Gemini); triggered by Hermes disabling four MCP servers without approval; 10-server restoration plan and chezmoi-config-guardrails.
- [[wiki/projects/Pieces-LTM]]—Pieces LTM (Long-Term Memory) serves as the primary sensory input for the Obsidian PKM system, capturing snippets, terminal commands, open files, and annotations.
- [[wiki/projects/Obsidian-PKM]]—Obsidian-based PKM vault following the AGENTS.md schema with three-layer memory architecture (raw/, wiki/, output/) for structured knowledge management.
- [[wiki/projects/Token-Usage]]—Tracking and optimisation of LLM token consumption across sessions, including cost analysis and context compression strategies.
- [[wiki/projects/Status-Reports]]—Structured status reporting and reflection workflow using numbered reflections and checklist-based task completion tracking.
- [[wiki/projects/Chezmoi]]—Dotfile management using chezmoi for version-controlled configuration across systems with source directory at ~/.local/share/chezmoi/.
- [[wiki/projects/LLMeon]]—LLMeon is the name of the Obsidian vault instance located at /Volumes/DAL/Zettelkasten/LLMeon, serving as the personal knowledge base.
- [[wiki/projects/CUH-DP AKS Backup — Terraform]]—Production Terraform remediation for Azure AKS Backup on CUH-DP cluster (aks-ff-uks-gp-01): module v1.0.5→v1.2.6 upgrade, destructive plan fixes (backup RG deletion, storage LRS override, AKS cluster replacement risk), variable interface changes, FTFL-615 subnet errors; AKS backup extension conflict resolution (azure-aks-backup vs azbkuextension name conflict, delete-and-recreate workflow); RBAC permissions thread with Sean Donnelly (CUH), SP confirmation (c3791fe2), resource group naming corrections, sprint impact analysis.
- [[wiki/projects/HIE AWS Cluster — RDP via Jumpbox]]—Operational runbook for accessing the HIE AWS cluster via RDP through an EC2 jumpbox using SSM port-forward tunnel (localhost:3389).
- [[wiki/projects/gcx CLI — FITFILE Grafana Stacks]]—Setting up and authenticating the gcx CLI tool for both FITFILE Grafana Cloud stacks (fitfileprod and fitfiletest) under the garethhailes org.
- [[wiki/projects/Semble]]—Semantic code search library integration for Hermes agents; replaces grep+read with BM25+semantic hybrid, achieving ~84% token reduction.
- [[wiki/projects/Zsh-Config]]—Zsh command-line editing via `edit-command-line` ZLE widget bound to Vim; chezmoi-managed configuration.
- [[wiki/projects/Calibre Semantic Ebook Research]]—Hermes skill system for semantic search across the Calibre ebook library, generating reading lists and research notes integrated with Obsidian PKM.
- [[wiki/projects/FITFILE Testing Infrastructure]]—Operational infrastructure work on the FITFILE Azure testing environment: AKS cluster management, Terraform state conflicts, Kubernetes secrets propagation; testing cluster `fitfile-cloud-testing-aks-cluster`.
- [[wiki/projects/FITFILE Node — Privacy Architecture & Data Processing]]—Email chain discussing FITFILE Node data processing architecture, privacy treatments (K-anonymity, L-diversity), NHS data governance; open questions on data ephemerality escalated to Leon & Ollie.
- [[wiki/projects/FTFL-511 Nginx HTTPS Hardening]]—FITFILE security ticket to harden TLS configuration of ingress-nginx controller: 14 outdated cipher suites identified in pentest; MR!757 declined; awaiting DevOps re-pick.
- [[wiki/projects/Hermes Multi-Model Routing Strategy]]—Research and architecture for Hermes's multi-model orchestration: free models (Owl Alpha) for planning, premium models (Claude Code, cloud) for complex execution; debugging CLI timeouts and OpenRouter routing.
- [[wiki/projects/FTFL-512 Nginx Security]]—FITFILE security ticket to remediate nginx 302 information disclosure on sandbox-testing-1.fitfile.net; server-snippet annotation blocked by admission webhook.
- [[wiki/projects/FTFL-511-512 Security Scan]]—Security scanning for FTFL-511 & FTFL-512: nmap scans from jumpbox testing subnet to private cluster; discovered Cloudflare proxy (not nginx) on scanned ports; SSH auth troubleshooting with IdentitiesOnly=yes and 1Password.
- [[wiki/projects/Azure Bastion SSH Troubleshooting]]—Diagnosed Azure Bastion SSH failures: MaxAuthTries exhaustion from 1Password keys, IdentitiesOnly=yes backfiring with AAD auth, --ssh-args flag missing in Azure CLI; resolved via `--` separator for SSH arguments.
- [[wiki/projects/Git Tag Management]]—Git tag operations: moved sandbox-testing-1-latest-release tag post-merge, resolved v1.8.65 src refspec push failure (tag missing locally).
- [[wiki/projects/Grafana Upgrade - Testing Cluster]]—Upgraded and configured Grafana in testing cluster using values.yaml; referenced in today's FTFL-511/512 security scan context.
- [[wiki/projects/NGINX Ingress Admission Webhook Fix]]—Investigation and fix for failing ArgoCD sync caused by NGINX Ingress admission webhook rejecting snippet annotations; scoped to IaC-only changes on private network cluster.
- [[wiki/projects/ffnode Helm Chart Review]]—Analysis of the ffnode umbrella Helm chart complexity: named-template patterns, library chart assessment, VSO double-evaluation bug audit across 27 clusters. Triggered by FTFL-673 Faro/Alloy upgrade work with Ollie Rushton.
- [[wiki/projects/Helm Chart Structured Metadata — Grafana Cloud Log Enrichment]]—Experiment to add structured metadata to Helm charts for richer Grafana Cloud log context. Phase 1 pilot on spicedb (fitfiletest), Phase 2 reusable Helm helper pattern. Sibling to ffnode Helm Chart Review.
- [[wiki/projects/FITFILE Frontend — Cohort Discovery]]—Frontend workstream on the FITFILE platform: Next.js cohort discovery screens (App Router), `CohortData` TypeScript type, feature-flagged routes, Jira tickets FTFL-494/501/502/496/31, live at ff-test-a.fitfile.net and AWSSDE.
- [[wiki/projects/FITFILE Deployment — ArgoCD + Helm]]—FITFILE GitOps deployment architecture: deployment repo structure, FFNode umbrella chart at `charts/ffnode/`, FFNodes per-cluster overlays at `ffnodes/`, cluster fleet taxonomy (~15+ clusters), critical `values.yaml` fields, release process, and ArgoCD self-heal constraint.

### `wiki/orgs/`

_(empty—populated on first ingest)_

### `wiki/concepts/`

- [[wiki/concepts/ADHD Procrastination and Productivity]]—Neurodevelopmental executive function deficit model; EF mediation (time management, organization); evidence-based interventions (CBT, DBT, EI training, VR body doubling); temporal motivation theory; bedtime procrastination.
- [[wiki/concepts/Three Polymaths Three Lessons]]—al-Haytham (steelmanning), Leibniz (notation-as-thinking-tool), Feynman (12 favorite problems); meta-principle: reconstruction over recognition.

---

_Updated 2026-06-09 03:35 by Project Check-In (cron/4h): 1 new raw note (FITFILE Deployment Wiki). 1 new project page (FITFILE Deployment — ArgoCD + Helm). 2 existing pages updated with back-links. Flags: 84 new Pieces assets found; 3 deployment wiki assets captured; 81 agent working notes from already-captured sessions skipped._