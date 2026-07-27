---
title: pieces_copilot_message_export_july_25_2026_12_23pm
type: note
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-25-2026-12-23pm
---

*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Saturday Jul 25, 2026 - 12:23 PM*
---
## FitFile ↔ Fabric Connectivity for the Clinical Informatics DB — Summary

### The thread you're looking at

**Robin Mofakham** (robin.mofakham@fitfile.com) replied on 24 Jul 2026 at 18:27 to **Oliver Rushton** and you, cc'ing **Weronika Jastrzebska**, **Susannah Thomas**, and **Helena Ahlfors**, giving the green light on **Sean Donnelly**'s (Telefónica Tech) proposed connectivity approach. Robin's message: no issues with the approach, it goes to **CAB next Thursday** (30 July), and he wants confirmation from your side "early next week." From FitFile's side he lists four steps:

- Attaching the VNET to the three DNS zones
- Testing the raw connection
- Setting up a new connection in the FITFILE app
- Testing that connection

Once proven, the next step is discussing the **CUH switch-over plan**.

### Sean Donnelly's underlying proposal (quoted in the thread, sent 23 Jul 2026 at 17:17)

Sean (Telefónica Tech) revised an earlier plan. Instead of deploying a new Private Endpoint inside the FitFile subscription, he proposes reusing the **existing Private Endpoint already in the Fabric F64 subscription**, requiring only:

- A rule on the Azure Firewall in the Hub subscription allowing FitFile ↔ Fabric F64 traffic on **port 1433** — this firewall change itself is what's going to **CAB on Thursday 30 July**.
- Linking three Private DNS zones from Fabric F64 into the FitFile VNET:
  - `privatelink.analysis.windows.net`
  - `privatelink.pbidedicated.windows.net`
  - `privatelink.prod.powerquery.microsoft.com`

Sean noted testing can only start after the 30 July CAB approval.

### Historical context from your LTM

This connectivity effort has been in motion since **March 2026**, when **Seferin James** (surfaced in your persona search as a CUH-side technical/administrative contact) first raised the idea in a Teams message shared in the "Sprint Demo & Release Planning" chat (12 Mar 2026): migrating the OMOP pipeline's data processing into **MS Fabric**, moving away from the "ad hoc" Clinical Informatics DB arrangement, and hosting a dedicated SQL Server instance under FitFile's existing **F64 capacity**. Seferin explicitly asked FitFile for a preference between that Fabric-hosted approach versus a Kubernetes-cluster-hosted data store, and raised a related question about where change control/support for FitFile would sit.

A related but distinct Azure DNS issue turned up from **19 May 2026**: a Terraform plan run against the CUH-DP project failed with `Error: Private Dns Zone ... "privatelink.blob.core.windows.net" was not found` in resource group `rg-ff-uks-gp-net` (subscription `709f3d57-b6d7-48c6-8252-6b1c1174a541`), tied to the AKS backup module. This is a different DNS zone (`blob.core.windows.net`, for storage) than the three zones Sean's plan covers, but it confirms `rg-ff-uks-gp-net` is the resource group already handling FitFile's private DNS zone linkages — likely the same VNET/RG context Sean's proposed DNS zone attachments would land in.

### What this means / open threads

- **CAB timing is the current gate.** Sean's Azure Firewall port-1433 rule change goes to CAB Thursday 30 July; testing (raw connection, then FITFILE app connection) can't start before that.
- **Robin is waiting on your (and Oliver's) confirmation "early next week"** (week of 27 July) before the CAB submission proceeds.
- **The CUH switch-over plan** is explicitly deferred until the connection is proven — that's a follow-on conversation, not yet scheped.
- No further FitFile-side detail on the actual VNET attachment / connection-testing steps was found beyond Robin's four-bullet outline — worth checking with Robin/Weronika directly if you need lower-level execution detail once CAB clears.

I did not find a dedicated Confluence/Jira ticket specifically tracking this Fabric-connectivity work (distinct from the FFNode stress-testing epics FTFL-476/480, which are a separate initiative) — if one exists, it wasn't surfaced by these searches, so you may want to check Robin's or Weronika's Jira queue directly.