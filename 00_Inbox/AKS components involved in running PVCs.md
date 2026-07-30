---
title: pieces_copilot_message_export_july_30_2026_12_38pm
type: note
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-30-2026-12-38pm
---

*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Thursday Jul 30, 2026 - 12:38 PM*
---
## FTFL-691 — what your memory and browser history actually show

Your browsing history confirms you visited [`FTFL-691`](https://fitfile.atlassian.net/browse/FTFL) directly — a single visit lasting roughly 68 million ms (~19 hours of open-tab time), title **"[FTFL-691] EoE SLA Inbox: Low effort"**. I need to flag a discrepancy here rather than assume your framing is right:

- **FTFL-691's own title and content are not about disks.** Per the page capture: `Parent: FTFL-1 Bugs, BAU & Debt`, `Assignee: Unassigned`, `Reporter: Robin Mofakham`, `Priority: High`, `Labels: eoe`. That's an "End of Encounter SLA Inbox" ticket — unrelated to storage.
- **The disk-related tickets sit alongside it in the same Jira sidebar/board, not as children of FTFL-691 itself.** The same page capture lists under "Recent Work": `FTFL-722: Upgrade disks from GP2 to GP3`, `FTFL-723: Test MigrateToGraviton in HIE Test`, `FTFL-724: Identify disk usage and make recommendation for action`.

So the disk checklist you're referencing likely lives on `FTFL-722`/`FTFL-723`/`FTFL-724` (all parented under `FTFL-1`, same as FTFL-691), not literally inside FTFL-691. I did not find a tool result that opens FTFL-722/723/724 individually with a disk-by-disk list — you'd need to open those tickets directly to get the enumerated disk list; I don't have page content for them in your browsing/memory history.

**On "TEST Node" specifically:** the clearest match in your history is `FTFL-723: Test MigrateToGraviton in HIE Test`, and a Terraform Cloud run you visited yesterday against workspace [`hie-test-34`](https://app.terraform.io/app/FITFILE-Platforms/workspaces/hie-test-34/runs/run-CG36HVYKsBD57TaA) (2026-07-29, 16:41 BST). A separate, older board snapshot also shows a distinct `FTFL-534: EE Test Node` ticket, which appears to be a different "test node" (EE = presumably a customer/site abbreviation, not the generic infra test env) — don't conflate the two. Given the gp2→gp3 upgrade context, the "TEST Node" you're asked to do first is most plausibly the `hie-test-34` HIE Test environment tied to `FTFL-723`, but I can't confirm that with 100% certainty from what's indexed — it's worth confirming directly on the FTFL-722/723/724 tickets before you start.

## AKS components involved in running PVCs (Azure)

Since you flagged you're unsure how PVCs work end-to-end, here's the AKS-side component chain (parallel to the EKS one already covered above):

### The chain from pod to disk

| Component | Role |
|---|---|
| `PersistentVolumeClaim` (PVC) | Namespaced request object a pod references; declares size/access mode/storage class |
| `StorageClass` | Cluster-wide template naming a provisioner + parameters (disk SKU, caching mode, encryption) |
| `PersistentVolume` (PV) | Cluster-wide object representing the actual bound storage; created dynamically by the provisioner in response to a PVC |
| CSI driver (`disk.csi.azure.com`) | Azure Disk CSI driver — the controller/node plugins that actually call the Azure API to create, attach, format, and mount the managed disk |
| Azure Managed Disk | The underlying billable resource (Standard_LRS / Premium_LRS / StandardSSD_LRS / PremiumV2_LRS, etc.) |
| `VolumeAttachment` | Internal Kubernetes object tracking which node a PV is currently attached to |

### How it flows

1. You (or a workload manifest) create a `PersistentVolumeClaim` referencing a `StorageClass` (e.g. `managed-csi`, AKS's default gp2-equivalent, which maps to `StandardSSD_LRS`).
2. The `disk.csi.azure.com` CSI controller (running as a Deployment in `kube-system`) watches for unbound PVCs, calls the Azure Resource Manager API, and provisions a **Managed Disk** with the SKU/params from the `StorageClass`.
3. A `PersistentVolume` object is created in-cluster to represent that disk, and gets bound 1:1 to the PVC.
4. When the pod is scheduled, kubelet's CSI node plugin (`disk.csi.azure.com` node DaemonSet) attaches the disk to the VM (or VMSS instance) hosting that node, formats it if needed, and bind-mounts it into the pod's volume path.
5. A `VolumeAttachment` object tracks the disk↔node binding so Kubernetes knows where it's currently attached (this matters on reschedule — the disk has to detach from the old node before it can attach to the new one, which is a common source of `FailedAttachVolume` events on AKS).

### Where the gp2→gp3-equivalent question maps on AKS

AKS doesn't use gp2/gp3 naming (that's AWS EBS) — the Azure Disk equivalents are:

- `Standard_LRS` (HDD-backed, cheapest, roughly gp2-era economy tier)
- `StandardSSD_LRS` (SSD-backed, general purpose — closest analog to gp2/gp3 "just works" default)
- `Premium_LRS` (provisioned IOPS SSD, higher/steadier performance)
- `PremiumV2_LRS` (newer, lets you tune IOPS/throughput independently of size — the closer Azure analog to gp3's independent IOPS/throughput knobs)

Migrating StorageClass defaults on AKS follows the same two-part pattern as the EKS walkthrough above: create/patch a `StorageClass` with `storageclass.kubernetes.io/is-default-class: "true"` pointing at the new SKU for *new* PVCs, and for *existing* PVCs either (a) resize/change SKU in-place via `az disk update --sku <NewSku>` (analogous to Option A's `aws ec2 modify-volume` — no data movement, brief detach/reattach may be required depending on SKU transition) or (b) snapshot-and-restore via `VolumeSnapshot` + a new PVC on the new class (analogous to Option B).

One AKS-specific caveat worth knowing: unlike AWS's `modify-volume`, not every Azure Disk SKU transition is a pure online no-downtime change — some `Standard_LRS`→`Premium_LRS` type transitions require the disk to be detached from the VM first. Worth checking `az disk update` docs against your specific source/target SKU pair before assuming the AWS-style zero-downtime path applies identically.