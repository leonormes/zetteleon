---
created: 2026-01-14T12:33:35+00:00
modified: 2026-03-14T11:10:54+00:00
title: Golden_context
---

## 🧬 The Golden Context: LCA-DP Infrastructure

1. The Mission (Architectural Intent)

This project (`LCA-DP`) is the Root Module deployment for a specific customer. It orchestrates a 4-Stage Multi-Repo flow using a Generative Engine approach.

- Role: Orchestrator. Connects `private-infrastructure` (AKS/VNet) to `central-services` (Auth0/Vault/GitLab).
- Strategy: "Code is Law". No hardcoded names or IPs. All values are derived from `customer.yaml` via `locals.tf`.

2. The Generative Engine (The "Math")

- Input: `customer.yaml` (Name, Env, Region, VNet CIDR).
- Derivation:
- Prefix: `${customer_name}-${environment}-${instance_id}`
- Subnet Calculation:
- System: Index 0 (Base + 0)
- Workflows: Index 1 (Base + 16)
- App: Index 2 (Base + 32)
- Jumpbox: Index 3 (Base + 48)
- Ingress IP: System Subnet Base + 8.

3. The Map (Module Hierarchy)

- Root: `Deployment/Clusters/nwsde/Production/LCA-DP/`
- Submodule A (`private-infrastructure`):
- _Purpose:_ Metal & Networking (AKS, VNet, NAT Gateway, Jumpbox).
- _Critical Logic:_ All subnets (System, Jumpbox, Workflows) must bind to the NAT Gateway defined here.
- Submodule B (`central-services`):
- _Purpose:_ SaaS & Soft Infra (Auth0, Vault, GitLab, TFC).
- _Wiring:_ Receives AKS credentials via TFC Variable Injection (Bridge) from the Root.

4. The "Gold Master" Constraints (Non-Negotiables)

- British English: All documentation and comments must use British spelling.
- Wiring Rule: `azurerm_subnet_nat_gateway_association` resources must exist at the Root Level, not inside submodules, to prevent circular logic.
- Data Flow: `customer.yaml` -> `locals.tf` -> `private-infrastructure` -> `tfe_variable` -> `central-services`.
- Current State: Verified that System Subnet is at Index 0. Refactor of `report.py` is the next technical debt item.
