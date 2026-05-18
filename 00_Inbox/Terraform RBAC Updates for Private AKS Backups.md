---
created: 2026-05-18T08:26:52+00:00
modified: 2026-05-18T08:28:47+00:00
---
*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Monday May 18, 2026 - 9:26 AM*
---
## Email to Alexis at CUH: Terraform RBAC Updates for Private AKS Backups

Based on recent testing against the sandbox and CUH-prod environment, your Terraform Service Principal (SP) currently lacks the necessary authorization to manage role assignments required for private endpoint-based backups. Specifically, the SP has hit the `Microsoft.Authorization/roleAssignments/write` block repeatedly when attempting to configure the Azure Backup extension for Kubernetes.

The investigation findings from May 14 confirm that a standard **Contributor** role is insufficient because it does not include permission to assign roles, which is a structural requirement for initializing the private backup pipeline.

### Reasons for the changes

1. **RBAC Self-Governance Gap:** As part of the private AKS deployment and backup extension setup, Terraform needs to assign permissions (such as `Storage Blob Data Contributor`) to the extension's Managed Service Identity (MSI). A **Contributor** can create resources but cannot delegate rights to them.
2. **ABAC Condition Blocks:** Your recent error logs (e.g., `run-qeQ41dgowhaGbMLn`) indicate that even when some write permissions exist, they are often gated by Attribute-Based Access Control (ABAC) conditions on existing roles, requiring a higher-level administrator to modify the assignment state.
3. **Least Privilege Principle:** While **User Access Administrator** would solve the issue, your own research notes from early 2026 flag that role as "overpowered" for an automated SP. The goal is to move to a specialized role that can handle role assignments without full subscription-level owner permissions.

### Required updates for the SP

You should ask Alexis to grant the Terraform Service Principal one of the following, scoped strictly to the relevant Resource Groups:

*   **Preferred Role:** **Role Based Access Control Administrator**
    *   **Reason:** This allows the SP to perform the `Microsoft.Authorization/roleAssignments/write` actions needed for the backup extension's MSI without granting the broader compliance and user-management rights of a full User Access Admin.
    *   **Required Scope:** This should be applied to the following RGs:
        *   `rg-ff-uks-gp-net` (AKS Cluster RG)
        *   `pentest-1-backup-rg` (Backup Vault RG)
        *   `pentest-1-backup-snapshots-rg` (Snapshot RG)

### Draft email content

**Subject:** Technical Update: Required Terraform Permissions for CUH Private AKS Backups

Hi Alexis,

I hope you're well.

Following our recent work on the test cluster for the Fully Private Backup implementation, we've identified a permission gap in our Terraform Service Principal (SP) that is blocking the deployment of the private endpoint storage used by the backups.

**Current Issue:**
The SP currently has **Contributor** access at the subscription level. While this allowed us to create most resources, it has hit a `403 Forbidden` error on `Microsoft.Authorization/roleAssignments/write`. This is because the Azure Backup extension for Kubernetes requires the SP to automatically assign the **Storage Blob Data Contributor** role to the extension's Managed Identity so it can securely write cluster data to our blob containers.

**Requested Update:**
To resolve this while maintaining least privilege, we need to upgrade the Terraform SP to the **Role Based Access Control Administrator** role. This will grant it the authority to handle these specific identity assignments.

For security, we recommend scoping this role assignment only to the following Resource Groups rather than the full subscription:
*   `rg-ff-uks-gp-net`
*   `pentest-1-backup-rg`
*   `pentest-1-backup-snapshots-rg`

This update is a prerequisite for us to move forward with the private backups and meet the HDRUK SLA requirements for the `cuh-prod-1` node.

Please let me know if you need any further detail on the specific error logs or RBAC requirements.

Best regards,

Leon Ormes
FITFILE