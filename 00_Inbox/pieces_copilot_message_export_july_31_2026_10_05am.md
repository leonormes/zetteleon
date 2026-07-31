---
created: 2026-07-31T09:05:20+00:00
modified: 2026-07-31T09:07:02+00:00
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-31-2026-10-05am
title: pieces_copilot_message_export_july_31_2026_10_05am
type: note
---

## FITFILE Customer Deployment Permissions Inventory

### Ticket: FTFL-799—Update Permissions Docs for a Customer Deployment

You are investigating cloud identity and access permissions required for a customer to run a FITFILE deployment. The goal is a customer-facing permissions breakdown used during discovery: exactly what identities exist, what each needs, why, and optional least-privilege alternatives. Work in this order:
AWS first, then Azure. For each cloud, capture both:

1. Terraform / automation Service Principal (SP)—used by HCP Terraform
   (FITFILE-Platforms) to provision the platform
2. Developer / operator identities—human access for FITFILE engineers
   and (where relevant) customer IT admins during install, ops, and support

New permissions discovered while making customer cluster backups private

must be included if present in live IAM / Terraform / docs.

---

### Global Rules

- Prefer evidence over assumption. Cite: IAM/Azure AD object names, ARNs /
  principal IDs, policy/role names, Terraform resource names, Confluence/GitLab
  paths, AWS account IDs / Azure subscription IDs when found.
- Separate:
  - Required to deploy (Terraform SP)
  - Required to operate / support (Developer)
  - Assigned by Terraform to other identities (workload IRSA / managed
    identities / node roles)—list as "roles the SP must be able to assign"
- Prefer least-privilege equivalents over blanket `Administrator` /
  `Owner` when the live config uses custom policies.
- Flag anything temporary, overly broad, or customer-environment-specific
  (e.g. SCP/deny overrides, private AKS/Private Link extras, backup/KMS).
- Output must be copy-paste ready for Confluence / customer discovery packs.

Do not invent permissions. If you cannot confirm an action/resource, mark

`UNVERIFIED` and say what to check next.

---

## PHASE 1—AWS (Do tHis cOmpletely before Azure)

### 1A. Discover Terraform SP / Deployment Principal

Search and inventory:

Sources (check all that apply):

- HCP Terraform org `FITFILE-Platforms`—workspaces, variable sets, and
  AWS provider auth (OIDC / assumed role / IAM user keys)
- AWS IAM identity used by TFC—historically named patterns like
  `tf-deployment`, `*-terraform*`, `*-tfc*`, `FITFILE*` deployment roles
- GitLab `fitfile/deployment` and Terraform modules under
  `fitfile/terraform-infrastructure` (EKS, VPC, central-services, jumpbox)
- Confluence FITFILE space: deployment / IAM / permissions / discovery docs
- Live AWS account(s) used for customer or reference deployments (e.g. eu-west-2)

For the Terraform SP/role, extract:

1. Identity type (IAM role for TFC OIDC, IAM user, cross-account role)
2. Trust policy (who can assume it—TFC OIDC issuer, external ID, account)
3. Attached managed policies (full names + ARNs)
4. Inline / customer-managed policies—every Action, Resource, Condition
5. Permission boundaries / SCPs that constrain it
6. Ability to create and pass roles (`iam:PassRole`, `iam:CreateRole`,
   `iam:AttachRolePolicy`, instance profile permissions)
7. Ability to create binary-specific attachments: EKS, EC2, VPC, ELB/ALB,
   S3, KMS, SSM, CloudWatch, Route53, ECR, EBS/CSI, IAM Roles for Service
   Accounts (IRSA) / Pod Identity, backup-related (AWS Backup, S3,
   volume snapshots), PrivateLink if used
8. Roles/policies this SP creates for other principals (cluster node
   roles, LB controller, autoscaler, external-dns, cert-manager, Velero/
   backup, Hyve/S3 export, Grafana, Vault, jumpbox SSM role, etc.)

Produce table A1—AWS Terraform SP:

| Permission / Policy | Scope (account / region / resource ARN pattern) | Purpose in FITFILE deploy | Required? | Source of truth |
|---|---|---|---|---|

Produce table A2—Roles the AWS Terraform SP must assign/create:

| Workload / component | Role name pattern | Key permissions granted | Why Terraform SP needs iam:PassRole / create |

### 1B. Discover AWS Developer Permissions

Inventory human/operator access used by FITFILE developers and customer IT:

- IAM groups/roles for engineers (SSO permission sets, Identity Center, or
  IAM roles like `Developer`, `PowerUser`, jumpbox SSM roles)
- Jumpbox / bastion access (SSM Session Manager, EC2 Instance Connect, SSH)
- EKS access (`aws-auth` ConfigMap / EKS Access Entries, `kubectl` groups)
- Read-only vs break-glass
- Console vs CLI
- S3 / logs / Grafana / Vault operational access if granted at AWS layer
- KMS decrypt for support if required
- Any extra permissions needed for private backup workflows

Produce table A3—AWS Developer permissions:

| Role / group | Principal type | Key actions | Used by (FITFILE eng / customer IT) | Notes |

### 1C. AWS Customer-facing Narrative

Write a short customer section:

1. What the customer must create before FITFILE deploys (TFC trust + SP role)
2. Exact minimum policy set (or link to managed policies + custom JSON)
3. What FITFILE developers need from the customer (IAM Identity Center
   assignment, network path to jumpbox, EKS access entry, etc.)
4. What is not required (call out if AdminAccess is unnecessary)
5. Recent additions (backup / private cluster / KMS / S3 encryption) with
   rationale suited to FTFL-799

### 1D. AWS Verification Checklist (Commands)

List concrete read-only CLI/console checks the assistant should run or recommend:

```bash
# Examples — adapt to actual principal names found
aws sts get-caller-identity
aws iam list-attached-role-policies --role-name <tfc-role>
aws iam get-role-policy --role-name <tfc-role> --policy-name <inline>
aws iam get-policy-version --policy-arn <arn> --version-id <v>
aws iam list-role-tags --role-name <tfc-role>
aws eks list-access-entries --cluster-name <cluster>
# plus Terraform state / code paths for aws_iam_* resources
```

Stop Phase 1 only when tables A1–A3 are complete or gaps are explicitly listed.

---

## PHASE 2—Azure (Only after AWS is cOmplete)

### 2A. Discover Terraform Service Principal

Search and inventory:

Sources:

- HCP Terraform `FITFILE-Platforms` Azure workspaces / variable sets
  (ARM_CLIENT_ID, OIDC federation, client secret—prefer OIDC where used)
- Entra ID app registrations / service principals used by TFC
- Confluence: "Azure Permissions for Private AKS Deployment via Terraform",
  "TFC Service Principal for Azure", Deployment View, customer checklists
- GitLab Azure AKS / private-infrastructure Terraform modules
- Subscription IAM (Access control) role assignments on the SP

For the Terraform SP, extract:

1. App registration name, Application (client) ID, Object ID
2. Auth method (federated credential OIDC to TFC vs client secret)
3. Azure RBAC role assignments at subscription / RG / management group:
   - Built-in (e.g. Contributor, Network Contributor, AcrPush,
     Key Vault Administrator/Secrets Officer, Private DNS Zone Contributor,
     DNS Zone Contributor, AKS-related roles, Storage, etc.)
   - Custom roles (full `Actions` / `NotActions` / `DataActions`)
4. PrivilegedRole assignment ability—`Microsoft.Authorization/roleAssignments/write`
   (User Access Administrator or scoped custom role). FITFILE TFC SPs often
   need to assign roles to managed identities without blanket Owner.
5. Exact role → identity relationships Terraform creates, e.g.:
   - AKS kubelet / cluster identity
   - AGIC / load balancer / ingress identity
   - ACR pull
   - Key Vault secrets CSI / VSO
   - Storage / backup identities
   - DNS contributors
6. Private AKS extras: Private Link, private DNS zone link, VNet join,
   route tables, firewall / UDR if applicable
7. Backup-related permissions (Recovery Services vault, disk snapshots,
   storage) discovered for private backups

Produce table B1—Azure Terraform SP:

| Role or custom permission | Scope (MG / sub / RG / resource) | Purpose | Required? | Source |

Produce table B2—Role assignments the Azure SP must be allowed to create:

| Target identity (MI / SP / AKS) | Role assigned | Scope | Why |

Document preferred pattern:

> Prefer Contributor (or reduced custom role) plus a narrowly scoped
> role-assignment permission limited to known managed identities and roles,
> rather than subscription-wide User Access Administrator, where policy allows.

### 2B. Discover Azure Developer Permissions

Inventory:

- Entra groups / PIM eligible roles for FITFILE engineers
- Azure RBAC for humans: Reader, Azure Kubernetes Service Cluster User/Admin,
  VM login (jumpbox), Key Vault access policies/RBAC, ACR, Storage
- AKS credentials (`az aks get-credentials`) requirements
- Jumpbox (AAD SSH / Bastion) access
- Graph API permissions on any app registrations if developers use them
- Customer-IT vs FITFILE-eng split

Produce table B3—Azure Developer permissions (same shape as A3).

### 2C. Azure Customer-facing Narrative

Mirror the AWS section for Azure customers (NNUH/MKUH/NWSDE-style tenants):

1. Pre-create Entra app + federated credential (or secret if unavoidable)
2. Assign listed RBAC roles at agreed scope
3. Grant role-assignment rights only for the identities Terraform must configure
4. Developer access path (PIM, groups, jumpbox, AKS)
5. Private AKS + private backup deltas
6. What not to grant (Owner at MG unless mandatory)

### 2D. Azure Verification Checklist

```bash
az ad sp list --display-name <name>
az role assignment list --assignee <appId> --all -o table
az role definition list --name "Contributor" -o json
# custom roles:
az role definition list --custom-role-only true
az aks show -g <rg> -n <cluster> --query identity
# Terraform azurerm_role_assignment resources in modules
```

---

## PHASE 3—Unified Customer Deliverable

After both clouds are inventoried, produce one document:

### Title

FITFILE Deployment—Required Cloud Permissions (AWS & Azure)

### Sections

1. Purpose & audience (customer IT / cloud / security teams during discovery)
2. Identity model overview (diagram or bullets):
   - Terraform SP (automation)
   - Developer / operator identities
   - Workload identities created by Terraform
3. AWS—SP permissions (table) → Developer permissions (table) →
   pre-deployment checklist → sample policy JSON or links
4. Azure—SP permissions (table) → Developer permissions (table) →
   pre-deployment checklist → sample role assignment plan
5. Cross-cutting:
   - Network prerequisites only where they gate IAM (Private Link, endpoints)
   - KMS / Key Vault key policy needs
   - Backup / restore permissions (explicit FTFL-799 delta)
   - Logging / support access boundaries
6. Change log—permissions added/removed recently and why
7. Open questions / UNVERIFIED items for FITFILE platform review

### Tone

Professional, NHS/customer-security friendly, least-privilege first,

no internal-only jargon without a one-line explanation.

### Format

Markdown suitable for Confluence; tables over long prose; include ARNs /

role names exactly as found.

---

## Working Method for You (The aSsistant)

1. Search internal docs first (Confluence FITFILE, GitLab `fitfile/deployment`,
   Terraform modules, existing pages referencing
   "Azure Permissions for Private AKS", "TFC Service Principal",
   `tf-deployment`, customer Technical Overview).
2. Then inspect live cloud config with read-only commands if credentials
   allow; never mutate IAM.
3. Cross-check Terraform code (`aws_iam_*`, `azurerm_role_assignment`,
   OIDC provider, `tfe_variable` sets) against live attachments.
4. AWS complete artifact → then Azure complete artifact → then unified doc.
5. Call out FTFL-799 / private-backup permission deltas explicitly so the
   discovery pack stays current.

Begin with Phase 1 (AWS) now. Report findings before starting Azure.
