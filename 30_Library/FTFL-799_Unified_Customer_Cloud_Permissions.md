---
created: 2026-07-31T09:34:18+00:00
modified: 2026-08-13T10:53:04+00:00
permalink: llmeon/30-library/ftfl-799-unified-customer-cloud-permissions
tags: [axiom:FTFL-799, customer-facing, infrastructure/aws, infrastructure/azure, permissions, terraform, typed-edge]
title: FTFL-799_Unified_Customer_Cloud_Permissions
---

## FITFILE Deployment—Required Cloud Permissions (AWS & Azure)

Status: Phase 3 (unified deliverable)—draft ready for FITFILE platform review before release to customers.

Ticket: Jira FTFL-799—"Update the permissions docs for a customer deployment."

Sources: [[FTFL-799_AWS_Phase1_Permissions_Inventory]] · [[FTFL-799_Azure_Phase2_Permissions_Inventory]] (full evidence, live CLI output, and internal caveats live in those two documents—this page is the customer-safe synthesis)

> Editorial note for FITFILE reviewers: a few judgment calls were made in drafting this synthesis where the internal investigation surfaced open questions. Each is marked with a 📋 and repeated in Section 7. Do not release this document externally until those are confirmed.

---

### 1. Purpose & Audience

This document tells a prospective or onboarding FITFILE customer's cloud, security, and infrastructure teams exactly what access FITFILE needs to deploy and operate the FITFILE platform in their own AWS or Azure environment, and why. It is used during technical discovery, before any infrastructure is provisioned.

Two identities matter throughout this document:

- The Terraform Service Principal (automation)—an identity FITFILE's deployment pipeline (HCP Terraform, organisation `FITFILE-Platforms`) uses to provision infrastructure. It never has a human behind it and does not have standing interactive access.
- FITFILE Developer/Operator identities (people)—a small number of named FITFILE engineers who need access during initial installation and, more narrowly, for ongoing support.

Nothing in this document requires handing FITFILE your cloud account's root/owner credentials, nor `AdministratorAccess`/subscription `Owner` on an ongoing basis.

---

### 2. Identity Model Overview

```
┌─────────────────────────────────────────────────────────┐
│  Your AWS Account / Azure Subscription                  │
│                                                           │
│   ┌───────────────────────┐                              │
│   │ Terraform Service     │  ← created once, per deploy  │
│   │ Principal (automation)│    key permissions in §3/§4  │
│   └──────────┬────────────┘                              │
│              │ creates & configures                      │
│              ▼                                           │
│   ┌───────────────────────┐                              │
│   │ Workload identities   │  ← created BY the SP, not     │
│   │ (node roles, IRSA /   │    given to any human:        │
│   │ managed identities,   │    cluster nodes, autoscaler, │
│   │ backup service role)  │    storage drivers, backup    │
│   └───────────────────────┘                              │
│                                                           │
│   ┌───────────────────────┐                              │
│   │ FITFILE Developer     │  ← a small number of named    │
│   │ access (jumpbox/      │    engineers, install + support│
│   │ bastion + cluster     │    only, no standing admin     │
│   │ access)               │                                │
│   └───────────────────────┘                              │
└─────────────────────────────────────────────────────────┘
```

- Terraform SP: provisions everything—networking, the Kubernetes cluster, storage, DNS, encryption keys.
- Workload identities: created _by_ the Terraform SP to let individual platform components (e.g. the storage driver, the autoscaler, the backup service) do their specific job. No human ever assumes these.
- Developer access: scoped to a single jump-host/bastion. FITFILE engineers do not get individual, direct cloud-console access as a matter of course.

---

### 3. AWS

#### 3.1 Terraform Service Principal—permissions

Authentication: OpenID Connect (OIDC) federation to HCP Terraform. FITFILE does not need long-lived AWS access keys—the deployment pipeline authenticates per-run via a short-lived, workspace-scoped token. This is the current, proven pattern (no static credentials in use).

| Permission area | What it's for |
|---|---|
| EC2 (full) | Create the private network (VPC, subnets, gateways), the management jump-host, and storage volumes |
| EKS (full lifecycle) | Create and manage the Kubernetes cluster, node groups, and cluster access controls |
| IAM (role/policy/OIDC-provider lifecycle) | Create the workload identities listed in §3.2—FITFILE does not need a human IAM user for this |
| IAM (user lifecycle)—_optional_ | Only if you require a static-credential export path (e.g. for a legacy data-integration tool); off by default |
| KMS (full lifecycle) | Create and manage your encryption keys for cluster secrets, storage, and data at rest |
| S3 (full) | Buckets used for deployment state, data export, and log storage |
| Route 53 (+ Route 53 Domains) | DNS zone and record management for the platform's private naming convention |
| Elastic Load Balancing (read-only) | Confirm load balancer health/state as part of deployment outputs |
| AWS Network Firewall | Egress filtering, where a managed firewall is part of the design |
| CloudWatch Logs (read-only) | Discover existing log delivery configuration to avoid conflicts |

Not required: `AdministratorAccess`, root credentials, or any permission on resources outside the target account.

#### 3.2 Workload Identities the Terraform SP Creates (No hUman eVer hOlds tHese)

| Component | Purpose |
|---|---|
| EKS cluster role | Lets the managed Kubernetes control plane operate |
| Node group role | Lets worker nodes join the cluster, run container networking, and pull images |
| EBS CSI driver role | Enables dynamic persistent storage for stateful workloads |
| Cluster Autoscaler role | Scales node capacity up/down with demand |
| Jump-host (bastion) role | See §3.3—this is how FITFILE engineers reach the cluster |
| AWS Backup service role _(see §5.3)_ | Performs scheduled backup/restore of the private cluster |

#### 3.3 FITFILE Developer/Operator Access

FITFILE engineers reach your environment through a single jump-host (bastion) instance, accessed via AWS Systems Manager Session Manager:

- No SSH keys, no public IP address, no direct account-level IAM user is required for FITFILE engineers.
- The jump-host's own role is scoped to: cluster administration (for the FITFILE-managed cluster only), read-only EC2 visibility, and decryption access to a specific encryption key used for operational tooling.
- Optionally, and only if agreed during discovery, named FITFILE or customer engineers can be granted direct, scoped Kubernetes access without going through the jump-host—this is off by default.

#### 3.4 AWS Pre-deployment Checklist

- [ ] Target AWS account and region confirmed, with sufficient service quotas (vCPU, EBS, load balancers)
- [ ] OIDC identity provider trust established for `app.terraform.io` (preferred), or an IAM user with access keys if OIDC cannot be supported
- [ ] IAM role created and bound to the trust above, with the permissions in §3.1
- [ ] Confirmation of who manages firewall/egress rules on your side, and your change-request process for updates

#### 3.5 Sample Policy Reference

The full, current IAM policy JSON is maintained by FITFILE platform engineering and provided directly during discovery (it changes as the platform evolves—do not rely on a cached copy from a previous engagement). A structural example is available on request.

---

### 4. Azure

#### 4.1 Terraform Service Principal—permissions

Authentication: an Entra ID (Azure AD) App Registration with a client secret, created in your own tenant. 📋 _FITFILE is evaluating a move to OIDC/workload-identity federation for Azure, matching the AWS pattern above, to remove the need for a stored secret—see §7._

| Permission | Scope | Purpose |
|---|---|---|
| `Contributor` (built-in role) | Subscription | Deploy the Kubernetes cluster, disks, virtual machines, storage, and networking |
| `User Access Administrator`, constrained to only assign "Network Contributor" (via an Azure role-assignment condition) | Subscription | Lets the deployment grant the cluster's own managed identity the network access it needs, without giving FITFILE's automation the ability to grant _any_ role to _any_ identity |

> The constrained `User Access Administrator` grant above is the important detail: it is not an unrestricted "manage all access" permission. It is scoped by an Azure condition so that it can only ever assign one specific, narrow role (Network Contributor) to the cluster's own identity. This is the least-privilege pattern FITFILE recommends over an unconditional grant.

Also required before deployment:

- Registration of five Azure resource providers: `Microsoft.ContainerService`, `Microsoft.ManagedIdentity`, `Microsoft.Network`, `Microsoft.Storage`, `Microsoft.Compute`
- The `EncryptionAtHost` compute feature enabled on the subscription (host-level disk encryption)
- A vCPU quota increase for the relevant VM family in your chosen region (FITFILE will confirm the exact family/quota during discovery)

Alternative—narrower custom role: for customers whose security policy prohibits subscription-wide `Contributor`, FITFILE can instead provide a custom role scoped to only the specific actions needed (cluster, compute, networking, DNS, Key Vault, and monitoring management, plus the constrained role-assignment permission above). 📋 _FITFILE platform engineering to confirm this is the recommended default going forward—see §7._

#### 4.2 Workload Identities the Terraform SP Creates

| Component | Purpose |
|---|---|
| Cluster managed identity | The Kubernetes cluster's own identity, granted `Network Contributor` on the resource group containing your virtual network (and, where your network lives in a separate resource group, on that resource group too) |

Azure Kubernetes Service itself extends a small number of additional, standard permissions to this same managed identity automatically (load balancer, disk, and storage account management) as part of its normal operation—these are not separately requested by FITFILE.

#### 4.3 FITFILE Developer/Operator Access

- A single named FITFILE engineer account is invited into your tenant as a guest (or member) user, with `Contributor` on the subscription for the duration of initial setup and ongoing support.
- Operational access to the cluster is via a jump-host (bastion) virtual machine, reached by SSH key (preferred) or, optionally, Azure Bastion for browser-based access without exposing a public IP.
- FITFILE engineers use short-lived, "just-in-time" privilege activation for any elevated access, rather than standing admin rights.

#### 4.4 Azure Pre-deployment Checklist

- [ ] Target subscription and region confirmed, with the required resource providers registered
- [ ] App Registration created for "FITFILE Terraform Cloud Provisioner" (or equivalent name), with a client secret generated and shared with FITFILE via a secure channel
- [ ] `Contributor` (or the narrower custom role, if agreed) granted to the App Registration's service principal at subscription scope
- [ ] `User Access Administrator`, constrained to "Network Contributor" only, granted to the same service principal
- [ ] `EncryptionAtHost` feature registered; vCPU quota increase requested
- [ ] Named FITFILE engineer invited to the tenant with `Contributor` access

#### 4.5 Sample Role-assignment Plan

1. Create App Registration → generate client secret → record Application (client) ID, Tenant ID, Subscription ID
2. Assign `Contributor` to the new service principal, scope: subscription
3. Assign `User Access Administrator` to the same service principal, scope: subscription, condition: constrain assignable roles to "Network Contributor" only
4. Register resource providers and the `EncryptionAtHost` feature
5. Provide FITFILE with: Tenant ID, Subscription ID, Application (client) ID, Client Secret

---

### 5. Cross-Cutting Considerations

#### 5.1 Network Prerequisites that Gate IAM

Some permissions above only apply if certain network designs are chosen:

- If FITFILE's cluster needs to reach your virtual network via a private connection (AWS PrivateLink / Azure Private Link), the relevant private-endpoint and private-DNS-zone permissions are required—these are already included in §3.1/§4.1.
- If your network uses a shared "hub" virtual network in a different resource group/account than the cluster, an additional, identical role assignment is needed for that resource group/account (see AWS §3.2 and Azure §4.2).

#### 5.2 Encryption Key Management

- AWS: FITFILE's automation creates and manages your KMS keys directly (§3.1). No separate key-policy action is needed from you unless you require a customer-managed key with a restricted key policy—flag this during discovery.
- Azure: if Key Vault is used for secrets or customer-managed keys, the permissions in §4.1's custom-role option (`Microsoft.KeyVault/vaults/*`) apply. Confirm during discovery whether you require a dedicated, customer-managed Key Vault versus one FITFILE provisions and manages.

#### 5.3 Backup / Restore permissions—FTFL-799 Delta

- AWS: a dedicated backup service role and vault/plan have been introduced to support backing up the FITFILE cluster without exposing it publicly (i.e. compatible with a fully private cluster). This role can describe cluster/networking state and perform backup and restore actions, scoped to the backup service itself—it has no access to your other AWS resources.
- Azure: 📋 the equivalent private-cluster backup capability is not yet available on Azure. No additional permissions are required today, and none should be requested. This section will be updated once the capability ships—see §7.

#### 5.4 Logging / Support Access Boundaries

- Comprehensive platform metrics and sanitised logs are transmitted outbound to FITFILE's centrally managed observability platform for monitoring and alerting.
- No raw or identifiable patient data is transmitted outside your network boundary as part of this logging, and none of the permissions in this document grant FITFILE read access to your underlying data stores.
- Support access during live incidents uses the same jump-host/bastion path described in §3.3/§4.3—there is no separate "support-only" credential with broader reach.

---

### 6. Change Log

| Change | Cloud | Why |
|---|---|---|
| Added dedicated backup service role, vault, and plan permissions | AWS | Supports scheduled, restorable backups of the FITFILE cluster while keeping it fully private (FTFL-799) |
| Documented the constrained `User Access Administrator` (Network-Contributor-only) pattern as the recommended role-assignment grant | Azure | Replaces prior guidance that implied an unconditional grant; this is materially narrower and was already in use, just undocumented as the default recommendation |
| Clarified OIDC as the standard AWS authentication method (no static access keys) | AWS | Previous customer-facing guidance referenced access keys; the deployed pattern uses short-lived, workspace-scoped OIDC tokens |
| ~~Azure backup permissions~~ | Azure | Not added—capability does not yet exist; do not include in customer packs until it ships |

---

### 7. Open Questions for FITFILE Platform Review

These must be resolved before this document is finalised for external, customer-facing use:

1. Azure: Contributor vs. custom role—internal source documents present blanket subscription `Contributor` and a narrower custom role as alternatives without stating which is the actual recommendation. This draft presents the custom role as the least-privilege option and Contributor as the simpler default; confirm this is correct, or state the intended default explicitly.
2. Azure: move to OIDC—confirm whether migrating the Azure Terraform Service Principal from client-secret to OIDC/workload-identity federation (matching AWS) is planned, and on what timeline, so this document's wording can be firmed up from "evaluating" to a stated commitment or dropped if not planned.
3. Azure backup—confirm this is correctly out of scope for the current release of FTFL-799 (i.e., Azure private-cluster backup is a known, separate gap) rather than an oversight.
4. AWS: broad `ec2:*`/`s3:*` grants—confirm whether these blanket grants are the intended long-term posture or should be itemised further; this document currently describes them at the category level ("EC2 (full)", "S3 (full)") rather than promising a fully itemised action list, to avoid committing to specifics that may tighten.
5. The account ID hardcoded into two places in the live AWS policy/module (a jump-host KMS permission and a Session Manager scope) belonging to an account other than the one hosting the policy—confirm this is intentional shared infrastructure before this pattern is replicated for new customers.
6. FITFILE's own internal Azure test environment for the private-AKS custom role is behind the version documented in this pack (missing Key Vault, monitoring, and networking actions present in the newer source doc)—recommend syncing before using it as a validation reference for new customers.
7. Human developer access breadth—both clouds currently grant a named FITFILE engineer fairly broad standing access (EKS cluster-admin via the jump-host role on AWS; subscription-wide Contributor on Azure). Confirm whether tightening either is planned, so this document doesn't need revising again shortly after release.

---

See also: [[FTFL-799_AWS_Phase1_Permissions_Inventory]] (full AWS evidence & live CLI findings) · [[FTFL-799_Azure_Phase2_Permissions_Inventory]] (full Azure evidence & live CLI findings) · Jira FTFL-799
