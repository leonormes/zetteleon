---
created: 2026-04-28T00:00:00+00:00
modified: 2026-05-06T12:50:00+00:00
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

- [[wiki/projects/12 Million Patient Synthetic NHS-OMOP Pipeline]]—FITFILE synthetic NHS OMOP data generation & stress-test initiative (up to 12M patients, 5-node Parquet datasets).
- [[wiki/projects/Azure AKS Backup — FTFL]]—Azure Backup for AKS covering FTFL-596/599/615: vault, extension, RBAC, trusted access binding, Terraform dependencies; 9 validated components (private storage, PE subnet, DNS, vault, snapshot RG, extension, policy, trusted binding, backup instance); IaC action plan defined with Phase 1–3 roadmap and validation criteria; Terraform module review completed (2026-05-01) validating plan against manual CLI end-state, identifying import vs creation distinction, secrets configuration gaps, and security considerations.
- [[wiki/projects/Azure Backup Restore Runbook]]—FTFL-599: operational runbook documenting az dataprotection CLI sequences for backup initialization, validation, and restore operations.
- [[wiki/projects/Future Roadmap Planning]]—team roadmap presentation meeting set up by WJ; preparing two topics.
- [[wiki/projects/MKUH Azure Backup]]—Azure Backup deployment for Milton Keynes University Hospital; part of EoE Data Providers program.
- [[wiki/projects/NNU Azure Backup]]—FTFL-596: Azure Backup configuration for Norfolk and Norwich University Hospital via private endpoint on private test cluster.
- [[wiki/projects/Security and Maintenance Roadmap]]—moving from annual pen tests to continuous security and maintenance as a first-class track.
- [[wiki/projects/Terraform IaC Modules]]—FTFL-596/615: Terraform modules for Azure Backup for AKS, handling Vault/AKS MSI role assignments and trusted access role bindings; LLM prompt created to audit module and produce implementable plan with current state inventory, gaps, proposed changes, migration steps, and git-friendly patch diffs.
- [[wiki/projects/Unified LLM Router Cockpit]]—unifying LLM tooling (Ollama, Hermes, Claude, Gemini, Pieces) into a deterministic chezmoi-managed workflow.
- [[wiki/projects/AWS SSM Session Troubleshooting]]—AWS Systems Manager session login failure diagnosis: missing `s3:GetEncryptionConfiguration` permission on SSM role preventing session log writes to S3 bucket.
- [[wiki/projects/Hermes Integration — Provider Adapter Setup]]—concrete implementation project to wire Claude and Gemini as first-class providers within Hermes via provider adapters, keeping Hermes as orchestrator and PKM hub.
- [[wiki/projects/Hermes Iteration Limit Configuration]]—Debugging workstream resolving 10/10 turn freeze: identified confusion between `max_turns` (main chat loop) vs `max_iterations` (background delegation) configuration parameters.
- [[INSIGHTFILE_PIPELINE_REPORT]]—GitLab CI/CD automation research for FITFILE/Hermes: comprehensive search synthesis, 7-phase TRANSFER artifact, cursor-based pagination workflow (2026-05-18).
- [[wiki/projects/Grafana Alloy Monitoring — FTFL-638]]—Kubernetes monitoring stack: Grafana/Alloy Helm deployment, Loki log labeling, values.yaml schema design, and testing cluster fix plan for FTFL-638/511/512; acceptance criteria include cue vet validation, job label alignment (namespace/container), and ArgoCD-synced Alloy-logs DaemonSet.
- [[wiki/projects/MCP Proxy Robustness and High Availability]]—Planning initiative to make mcp-proxy resilient across multiple AI consumers (Hermes, Claude, Cursor, Gemini); triggered by Hermes disabling four MCP servers without approval; 10-server restoration plan and chezmoi-config-guardrails.

### `wiki/orgs/`

_(empty—populated on first ingest)_

### `wiki/concepts/`

_(empty—populated on first ingest)_

---

_Updated: 2026-05-06 by Project Check-In_
