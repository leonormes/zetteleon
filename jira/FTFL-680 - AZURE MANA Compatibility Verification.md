---
tags:
  - jira
  - fitfile
  - task
  - azure
  - networking
  - mana
  - accelerated-networking
status: To Do
priority: High
issuetype: Task
assignee: Leon Ormes
reporter: Leon Ormes
labels:
  - azure
  - networking
  - mana
created: 2026-05-28
updated: 2026-05-28
jira_id: "31913"
jira_key: FTFL-680
jira_url: https://fitfile.atlassian.net/browse/FTFL-680
---

# FTFL-680 — [AZURE] Verify MANA Compatibility for Intel v5 and Cobalt 100 v6 VMs

| Field | Value |
|---|---|
| **Jira ID** | [31913](https://fitfile.atlassian.net/browse/FTFL-680) |
| **Status** | To Do |
| **Priority** | High |
| **Issue Type** | Task |
| **Assignee** | Leon Ormes |
| **Reporter** | Leon Ormes |
| **Labels** | azure, networking, mana |
| **Created** | 2026-05-28 |
| **Updated** | 2026-05-28 |

## Summary

Azure Service Health advisory: Verify MANA (Microsoft Azure Network Adapter) compatibility for Intel D/E v5 and Cobalt 100 D/E v6-series VMs before regional rollout begins **26 May 2026**.

**Tracking ID:** 5RWW-K4G

## What's Changing

Azure is deploying MANA-enabled hardware. VMs listed below using Accelerated Networking may be placed on MANA hardware for new deployments or redeployments.

**Intel v5-series:** Dsv5, Dv5, Ddsv5, Ddv5, Dlsv5, Dldsv5, Esv5, Ev5, Edsv5, Edv5, Ebsv5, Ebdsv5

**Cobalt 100 v6-series:** Dpsv6, Dpdsv6, Dplsv6, Dpldsv6, Epsv6, Epdsv6

## Regional Rollout

| Date | Region |
|---|---|
| 26 May 2026 | West Central US |
| 27 May 2026 | East Asia |
| 28 May 2026 | Norway West |
| 29 May 2026 | Spain Central |
| TBA (announced 29 May) | Additional regions |

## Who Is Affected

- Any VM in the above sizes using **Accelerated Networking**
- Any **Network Virtual Appliance (NVA)** workloads on these sizes
- VMs redeployed due to maintenance or customer action

**Not affected:** VMs not using Accelerated Networking, or running a supported Windows OS version.

## Affected Azure Subscriptions

| Subscription ID | Name |
|---|---|
| `3dfad624-29f7-4cdf-8cd2-47fbae492438` | AZURE VIRTUAL DESKTOP - POC |
| `709f3d57-b6d7-48c6-8252-6b1c1174a541` | FITFILE |

## Required Actions

1. **Identify** all Intel D/E v5 and Cobalt 100 D/E v6 VMs using Accelerated Networking running NVA workloads
2. **Verify** Linux OS is MANA compatible
3. **Upgrade** OS or NVA product to MANA-compatible versions if needed (contact NVA provider)
4. **Optional:** Apply `LegacyVMNVA` tag for a temporary MANA exception (expires **31 May 2027**)
5. **Complete migration** to MANA-compatible OS/NVA by **31 May 2027**

## If No Action Taken

- VMs without MANA compatibility remain supported on Mellanox hardware but may experience **network performance degradation**
- After 31 May 2027, any VM could land on MANA-enabled hardware regardless

## Resources

- [Microsoft Azure Network Adapter overview](https://learn.microsoft.com/en-us/azure/virtual-network/accelerated-networking-mana-overview)
- [MANA support for existing VM sizes](https://learn.microsoft.com/en-us/azure/virtual-machines/setup-mana)
- [MANA support for Network Virtual Appliances](https://learn.microsoft.com/en-us/azure/virtual-network/nva-mana-overview)
- [Windows VMs with the Microsoft Azure Network Adapter](https://learn.microsoft.com/en-us/azure/virtual-machines/setup-mana-windows)

## Support

Contact your CSAM or Azure Support for assistance.
