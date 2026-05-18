*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Monday May 18, 2026 - 10:53 AM*
---
Both pagination chains are now resolved to `sufficient`. The Robin Mofakham chain returned `sufficient` at 100 results, confirming no specific CUH RBAC plan document was captured in memory beyond what's already in the earlier draft. The permissions plan email itself was found in memory (event `9b0894f3` — the draft saved to Obsidian earlier in the session). The web search conclusively verified Robin's technical idea is feasible. Here is the fully revised email incorporating Robin's suggestion:

---

## Revised Email — Including Robin's Constraint

**Subject:** Security Enhancement: Private Backup Implementation for CUH AKS Cluster — Permission Request

Hi Alexis,

I hope you're having a good week.

I'm writing to request a targeted permission update for our Terraform Service Principal (SP) at CUH. This is related to the additional work we are doing on top of the deployed cluster to implement **Fully Private Backups** — a security enhancement we've already validated in our sandbox environment.

**What is the Private Backup doing, and why is it extra work?**

Although the initial `cuh-prod-1` cluster is live and operational, private backups require a separate configuration step. Rather than backing up cluster data over the public internet, we are implementing a **Private Endpoint** — a dedicated connection that keeps all backup traffic entirely within the NHS internal private network. This is the Azure-recommended approach for handling sensitive data in a Secure Data Environment (SDE), and is part of our ongoing pentest remediation programme.

**The Blocker:**

Our Terraform automation hits a `403 Forbidden` error (`Microsoft.Authorization/roleAssignments/write`) because it needs to delegate a specific storage permission to the backup agent it installs. The current **Contributor** role it holds cannot do this.

**Requested Permission Update — Tightly Scoped:**

Following advice from our team, we would like to request the most minimal possible grant. Rather than a broad **Role Based Access Control Administrator**, we would like the Terraform SP to be granted the ability to assign only one specific role: **Storage Blob Data Contributor** (Azure built-in role ID: `ba92f5b4-2d11-453d-a403-e96b0029c9fe`).

This can be achieved by granting the SP the **Role Based Access Control Administrator** role with an **Azure ABAC condition** that restricts what it can delegate — constraining it to only ever assign `Storage Blob Data Contributor`, and nothing else. This is a supported Azure pattern per [Microsoft's role assignment conditions documentation](https://learn.microsoft.com/en-us/azure/role-based-access-control/conditions-format).

The scope should be limited to the following three Resource Groups only (not the full subscription):
- `rg-ff-uks-gp-net`
- `pentest-1-backup-rg`
- `pentest-1-backup-snapshots-rg`

**In plain terms:** we are asking for the minimum possible footprint — the SP can only ever grant one specific, read/write-to-blob role, and only within these three named groups. It cannot assign any other role, and cannot act anywhere else in your Azure environment.

This is a prerequisite for completing the private backup pipeline and closing the remaining open security loops on the cluster.

Please let me know if you'd like me to share the specific condition syntax for the grant, or if a quick call would be helpful to walk through it.

Best regards,

Leon Ormes
Principal Platform Architect, FITFILE