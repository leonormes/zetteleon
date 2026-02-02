---
created: 2026-02-02T14:02:27+00:00
modified: 2026-02-02T14:03:51+00:00
title: NNUH Inbound IP
---

## Status: Needs Verification

- Potential IP Found: 195.171.151.154
   - Source: Obsidian note "Test Cluster A to B Connectivity" (accessed ~20 hours ago).
   - Context: The note describes "Cluster B" having this public IP and allowing traffic from "Cluster A". It is highly likely this corresponds to the NNUH inbound endpoint, but it is explicitly labeled as "Cluster B" in the notes.
- Related Network Context:
   - Miro Board: A "NNUH Network Diagram" was accessed (~30 mins ago). It details:
       - NNUH to create VNET and set up peering.
       - Traffic flow involves a Checkpoint Firewall.
       - "To let Ben know what changes we know will be relevant to the checkpoint firewall."

## Report: Work Done So Far

  1. Infrastructure & Connectivity (NNUH Focus)
   - Node Installation (FTFL-82): Progressed on NNUH integration.
   - Certificate Configuration (FTFL-88): Configuration work is underway.
   - Secure Traffic Investigation: Investigated technical requirements for secure HTTPS traffic between two Kubernetes clusters (likely the "Cluster A to B" scenario mentioned above).

## LCA-DP Deployment (FitFile)

- Configuration Analysis: Completed a "Deployment Configuration Analysis Report" for the LCA-DP customer.
   - Analyzed Ingress, DNS, and hostname configurations.
   - Traced data flow from customer.yaml to Helm values.
- Cost Optimization:
   - Decommissioned expensive resources in the FitFileLZ subscription (stopped aks-lca-uks-prd-01, deleted bastion-lca-plat-uks-01).
   - Confirmed strategy to delete/recreate Bastion hosts while preserving the Public IP to save costs.

## Tooling & Automation

- CloudHop (Rust CLI):
   - Finalized end-to-end functional flow for the cloudhop tool (automated cloud SSH logins).
   - Implemented core execution logic (execute_plan, execute_preflight).
   - Troubleshot binary installation with mise.

## Next Steps

   1. Confirm IP: Verify if 195.171.151.154 is indeed the intended NNUH Inbound IP.
   2. Firewall Rules: Compile the list of changes for the Checkpoint Firewall to send to Ben.
   3. LCA-DP: Continue with the deployment configuration based on the analysis report.
