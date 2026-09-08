---
conformant: true
project_category: devops
project_name: Entra IAM Hardening
project_status: active
status: draft
revision: 3
tags:
- fitfile
- entra
- iam
- pim
- least-privilege
- terraform
- hcp-terraform
- azuread
- oidc
- jumpcloud
- security
title: 2026-09-07-fitfile-entra-pim-least-privilege-plan
type: project
permalink: llmeon/30-library/200-projects/2026-09-07-fitfile-entra-pim-least-privilege-plan
created: 2026-09-07T11:26:10+00:00
modified: 2026-09-07T12:52:52+00:00
---

## FITFILE — Entra IAM Least Privilege & PIM-in-Terraform Plan

Tenant: FITFILE Group Limited, `45e73aa3-1ee9-47c0-ba25-54eda9da021a`
Code reviewed: `central-services/azure/ad` (HCP Terraform workspace `fitfile-entra-id`, org `FITFILE-Platforms`)
Date: 2026-09-07/08 (Revision 3 — corrects a scope error introduced in Revision 2). **All tenant operations read-only.** No secret value was read; no configuration was changed.

Audit identity: `leon.ormes@fitfile.com` (Business Premium/P1 + Entra ID P2). Revision 1 ran with no directory role; Revision 2 with **Global Reader** activated via PIM. Four data sets remain unreadable for a reason unrelated to roles — see §1.6.

> **Relationship to prior work.** [[Restructuring Entra ID—Scoping, IaC & PIM]] (2026-05-15) set the framing: five sub-projects with separate definitions of done, Sub-Project 0 (break-glass) as an existential prerequisite, and "tidy before you codify". Its §2.H asked *"what dirt do you actually have?"* and left the numbers blank. **This note is the answer to that question**, plus the CI/CD identity design its §2.D flagged as the deal-breaker. It does not supersede the framing note — read that one for the *why*, this one for the *what is actually there*. Break-glass detail stays in [[Break-Glass Identity The Complete Plan]]; §2 finding 8 below is the one new fact that note needs.

> **Provenance.** Authored by an agent into `30_Library/200_projects/` per [[SoT - HEAD Note Contract (The Workbench)]] §1.2 (finished engineering analysis goes here, not the Workbench). Written via filesystem because `note_create` over MCP errored on this payload and the `obsidian` CLI cannot take a 25KB body — the file was created through the CLI first, so `metadataCache` is seeded. Open decisions are collected in §8 rather than left implicit.

---

> ### ⚠ Revision 2 — 2026-09-07, second pass with Global Reader activated
>
> A second read with Global Reader active, plus the ARM PIM APIs and the PIM audit log, **corrected several findings in Revision 1**. Anything below marked **[R1 WRONG]** or **[R1 RESCOPED]** was materially incorrect first time. Summary of what changed:
>
> 1. **PIM is already deployed and working** — Entra directory roles, Azure resource roles across all six subscriptions, *and* PIM for Groups. Revision 1 read the tenant as pre-PIM. It is not. The plan's centre of gravity moves from "build PIM" to **"extend PIM, and stop Terraform undermining it."**
> 2. **[R1 WRONG] Robin (Admin) is not a standing Global Administrator.** They are PIM-eligible and activate JIT. Revision 1 queried `roleAssignments` at 11:15 during a live activation window (activated 11:01, expires automatically) and mistook the activation for a permanent assignment. **Only `breakglass.azure` is permanent.** Finding 7 is withdrawn.
> 3. **[R1 RESCOPED] The drift finding was right to worry, wrong about the mechanism — and the real risk is worse.** `DevOpsEngineers` is under **PIM for Groups**; its at-rest membership is *deliberately* smaller than its eligible set. Terraform's authoritative `members` list would convert a JIT privilege path into **standing** privilege, and that group holds `User Access Administrator` on the Testing subscription. See §1.4a.
> 4. **[R1 RESCOPED] Terraform's Azure-side privilege is worse than reported.** `Terraform AAD Provisioner` holds **unconstrained `User Access Administrator` at the `FITFILE` management group**, inherited to every subscription beneath it. Revision 1 only caught the Vault SP's assignment.
> 5. **[R1 WRONG] Scope: there are six subscriptions and four management groups, not two.** Revision 1 audited `FITCloud Non-Production` and `Shared Services` only. See §1.9. *(Revision 2 also miscounted this as seven, including an out-of-scope customer subscription — corrected in Revision 3 above.)*
> 6. **The two audit gaps are not role problems and Global Reader does not fix them.** The Azure CLI application **has no service principal in this tenant**, so it holds no consent grant — its token simply never carries `RoleManagement.Read.All` or `Policy.Read.All`. See §1.6.
>
> Revision 1's *design* recommendations (tiering, OIDC federation, eligibility-in-git, what to keep out of Terraform) all survive unchanged. The findings table in §2 has been reordered accordingly.

---

> ### ⚠ Revision 3 — 2026-09-08, scope correction
>
> Revision 2's estate sweep used `az account list --all`, which returns every subscription the signed-in principal can reach across **any** tenant it has access to — not only the home tenant. One of the seven subscriptions swept, `NNUHFT-SDE`, belongs to a **customer's own Azure tenant** (confirmed distinct `tenantId`), reachable only via the auditor's federated/guest access as a vendor supporting that customer. It was mistakenly analysed as part of FITFILE's own estate.
>
> **Correction:** the FITFILE Entra tenant's own Azure estate is **six subscriptions**, not seven. Every finding, count and recommendation below that referenced `NNUHFT-SDE` or a seven-subscription estate has been corrected or withdrawn. No customer personnel or role data is retained in this note — that information belongs to the customer's own tenant and has no bearing on FITFILE's IAM programme. The general lesson carries into [[2026-09-07-fitfile-entra-jira-work-preparation]] and into Phase 0 tooling ([FTFL-1054](https://fitfile.atlassian.net/browse/FTFL-1054)): any future sweep must filter `az account list --all` by `tenantId` before treating a subscription as in-scope.

## Minimum Viable Understanding

Four things are true at once, and the plan follows from their interaction:

1. **PIM already works here — the gap is coverage and encroachment, not absence.** 114 PIM events in the retained window: Global Administrator activated 13 times, Application Administrator 5, Global Reader 2, plus Azure resource Owner/Contributor and PIM-for-Groups member activations. Two dedicated admin accounts (`admin.mofakham`, `admin.russmeyer`) are eligible for `Owner` on **all six subscriptions**. This is a working control, built around July 2026. Treat it as an asset to extend, not a greenfield.
2. **The privilege problem is in the standing grants that sit *beside* PIM.** A JumpCloud sync **user account** holding Privileged Role Administrator; an MSP tool (CIPP-SAM) with ~120 app permissions including `RoleManagement.ReadWrite.Directory`; the Terraform SP with unconstrained `User Access Administrator` at the top management group. Each is a path that bypasses PIM entirely. Tidying group definitions in HCL touches none of them.
3. **Terraform is on a collision course with PIM.** `azuread_group.members` is authoritative. Pointed at a group that PIM manages for JIT membership, it will churn against activations and convert just-in-time access into standing access. This is the single most urgent code change, and it is a correctness bug, not a hardening nicety.
4. **You cannot put all of PIM in Terraform without handing the pipeline Global-Administrator-equivalent power.** Microsoft is explicit that a system which can manage or broker privileged roles *is itself* a control-plane (Tier 0) asset. The design must therefore be *tiered*, not uniform — and the answer to "how do we give TFC the creds" is different per tier.

The workable target: **Terraform declares who may *become* an admin; PIM decides when they actually are.** Eligibility in git, activation at runtime. That gives full git audit of the privilege graph without standing access, and without the pipeline needing to hold the roles it grants.

---

## 1. What Is Actually In Place

### 1.1 Directory shape — answering §2.H of the framing note

| Object | Count | Notes |
|---|---|---|
| Users | 100 | 38 enabled members, **39 disabled members**, 21 enabled guests, 2 disabled guests |
| Groups | 105 | **0 role-assignable**, **0 dynamic** — all static |
| App registrations | 59 | |
| Service principals | 1063 | mostly Microsoft first-party |
| Global Administrators | 2 | one is break-glass |
| Standing privileged role assignments | 8 to non-Microsoft principals | see §1.2 |

**The "employees only" premise needs qualifying.** There are 23 guest accounts, including Mersey Care NHS, NHS.net, UCL, Wellcome, Avicenna, and penetration-test suppliers (ProCheckUp, Evalian). The tenant does hold external B2B identities. That is not necessarily wrong — the guest posture is well configured (§1.5) — but a plan written on the assumption of employees-only would miss them, and the framing note's option **A4** (cross-tenant trust topology) is therefore live, not hypothetical.

**39 disabled member accounts** is a leaver-cleanup backlog; disabled accounts still hold group memberships and licences.

### 1.2 Standing directory role assignments

The whole privilege picture at `/` scope, from `roleManagement/directory/roleAssignments`:

> **[R1 WRONG] Read this table with care.** `roleManagement/directory/roleAssignments` returns *currently effective* assignments, which includes live PIM activations. Revision 1 read it during an activation window and reported Robin (Admin) as a standing GA. It is not a snapshot of permanent grants. To separate the two you need `roleEligibilityScheduleInstances` (blocked, §1.6) or the PIM audit log (§1.2a).

| Role | Principal | Type | Assessment |
|---|---|---|---|
| Global Administrator | `breakglass.azure` | user | Correct — permanent by design, the only true standing GA |
| Global Administrator | Robin (Admin) | user | **PIM activation in flight when queried** — eligible, not standing. Correct posture. |
| **Privileged Role Administrator** | **JumpCloud Connector** | **user** | **Highest-severity finding** |
| User Administrator | JumpCloud Connector | user | |
| Groups Administrator | JumpCloud Connector | user | |
| Directory Readers | JumpCloud Connector | user | |
| Groups Administrator | FITFILE Gitlab Integration Test Pipelines | SP | Test pipeline with group write at tenant scope |
| Compliance Administrator | CIPP-SAM | SP | Plus ~120 Graph app roles |
| Directory Readers | Microsoft.Azure.SyncFabric, MicrosoftAzureActiveAuthn | SP | Microsoft first-party, expected |
| AdHoc License Administrator | Microsoft Office 365 Portal | SP | Role is marked *"Deprecated — Do Not Use"* |

Two Global Administrators is inside Microsoft's "fewer than five" guidance. That part is fine.

**The JumpCloud Connector finding.** It is a *user object*, not a service principal, holding Privileged Role Administrator permanently. Privileged Role Administrator can grant any directory role — including Global Administrator — to any principal, itself included. So this is a GA-equivalent standing grant on a shared service account that:

- cannot use certificate or federated credentials (it is a user, so it authenticates by password);
- is excluded from the human MFA/PIM story by construction;
- is a *synced-in* identity, which Microsoft's best-practice #9 specifically warns against for role assignments.

JumpCloud's SCIM/provisioning function needs `User.ReadWrite.All`, `Group.ReadWrite.All` and `GroupMember.ReadWrite.All` — it does **not** need Privileged Role Administrator. Note there is *also* a separate `JumpCloud Office 365 Sync` **service principal** already holding `User.ReadWrite.All`, `Group.ReadWrite.All`, `Directory.ReadWrite.All` and `MailboxSettings.ReadWrite`. The connector user's roles look like a legacy duplicate of a capability the SP already has.

**The CIPP-SAM finding.** CIPP is an open-source MSP multi-tenant management tool. Its SP holds roughly 120 Graph application permissions, including `RoleManagement.ReadWrite.Directory`, `RoleEligibilitySchedule.ReadWrite.Directory`, `RoleAssignmentSchedule.ReadWrite.Directory`, `RoleManagementPolicy.ReadWrite.Directory`, `Policy.ReadWrite.ConditionalAccess`, `UserAuthenticationMethod.ReadWrite.All`, `Application.ReadWrite.All` and `Directory.ReadWrite.All`. Many grants are duplicated (the same app role assigned twice). This is GA-equivalent, app-only, and — being app-only — **is not subject to Conditional Access or PIM at all**.

Whether CIPP should be there is a business question about the MSP relationship, not a technical one. But it must be a *conscious, documented* decision, because it sets the ceiling on what the rest of this work can achieve. Hardening human admin access to phishing-resistant JIT while an app-only GA-equivalent grant sits alongside it moves the attack path; it does not close it.

### 1.2a PIM as actually deployed — evidence from the audit log

`auditLogs/directoryAudits` filtered to `loggedByService eq 'PIM'` returns **114 events** in the retained window. Activation counts by target:

| Target | Activations | Type |
|---|---|---|
| Global Administrator | 13 | Entra directory role |
| Member (of `DevOpsEngineers`) | 7 | **PIM for Groups** |
| Application Administrator | 5 | Entra directory role |
| Global Reader | 2 | Entra directory role |
| Contributor | 2 | Azure resource role |
| Owner | 1 | Azure resource role |
| Virtual Machine Contributor | 1 | Azure resource role |
| Billing Administrator | 1 | Entra directory role |
| Azure Kubernetes Service RBAC Cluster Admin | 1 | Azure resource role |

What this establishes:

- **All three PIM surfaces are live** — directory roles, Azure resource roles, and PIM for Groups. Revision 1 assumed none were.
- **Activations expire correctly.** `Remove member from role (PIM activation expired)` events appear against Global Administrator and Application Administrator, so the time-bound mechanism is functioning, not just configured.
- **Robin (Admin) is the operating PIM administrator**, actively granting and revoking eligibility (`Add`/`Remove eligible member to role in PIM`) — e.g. Billing Administrator on 2026-09-03, AKS RBAC Cluster Admin on `Testing` 2026-09-02, and a Reader eligibility on `FITCloud Non-Production` granted and revoked within ten minutes on 2026-09-07.
- **`DevOpsEngineers` group membership is activated through PIM** by both Oliver and Leon. This is the finding that reframes §1.4.
- **Global Administrator at 13 activations** is the highest-frequency privileged activation. Worth reviewing whether some of that work needs a narrower role — Microsoft's least-privilege-by-task guidance exists precisely for this.

Azure resource PIM eligibility, read from ARM (`roleEligibilityScheduleInstances`), is broad and consistent:

| Scope | Eligible principal | Role | Expires |
|---|---|---|---|
| All 6 subscriptions + `sandbox` MG | Robin (Admin), Philip (Admin) | Owner | 2027-07-16/17 |
| `FITFILE` MG (inherited everywhere) | Robin (Admin) | Virtual Machine Contributor | 2027-07-15 |
| `Testing` | Robin (Admin) | Contributor, AKS RBAC Cluster Admin | 2027-08-05 / 2027-09-02 |

Two observations. The eligibility windows all expire mid-2027, so there is a **cliff-edge renewal** to diary rather than discover. And eligibility is confined to the two `admin.*` accounts — no engineer is eligible for anything at Azure resource scope, which is consistent but means engineers who need elevated Azure access have only the standing group path (§1.9).

### 1.3 `Application.ReadWrite.All` holders — the shared escalation path

Microsoft classifies `microsoft.directory/applications/credentials/update` as a **PRIVILEGED** permission. `Application.ReadWrite.All` includes it, so any holder can add a client secret to *any* application in the tenant and then authenticate as it. Every holder is therefore equivalent to the union of every app's permissions.

Current holders: **CIPP-SAM** (×2, duplicated), **HCP Vault**, **HCP-vault-sp** (legacy duplicate), **FITFILE Gitlab Integration Test Pipelines**, **Terraform AAD Provisioner**.

Six grants of a mutual-escalation permission. Each can become each of the others, and all can become CIPP-SAM, which is GA-equivalent. **The practical privilege ceiling of the Terraform pipeline today is Global Administrator**, regardless of what its own permission list says.

For Terraform this is avoidable: `azuread_application*` resources accept **`Application.ReadWrite.OwnedBy`**, which restricts writes to applications the SP owns. The SP already owns 22 objects (§1.4), so the ownership model is in place — the broad grant is simply unnecessary.

### 1.4 What Terraform manages today — answering §2.C

`azure/ad` is roughly 863 lines across 8 files plus one `entra_group` module. **Coverage: about 10 groups of 105, 7 users, 6 app registrations.** Nothing else in the tenant is in code. So the framing note's posture question resolves to **"partial, and drifted"**.

**One thing is done well and should be kept.** The Terraform SP holds `Group.Create` + `Group.Read.All` + `GroupMember.Read.All` — deliberately *not* `Group.ReadWrite.All` or `GroupMember.ReadWrite.All` — and manages membership by being the group **owner**. `ownedObjects` on the SP confirms 22 owned objects including `Developers` and `DevOpsEngineers`. This is exactly Microsoft's recommended least-privilege pattern for app-managed groups: create-plus-ownership rather than tenant-wide group write. **Preserve this in the redesign; do not "fix" it by broadening the grant.**

**Committed HCL and live state disagree:**

| Group | In HCL | Live in tenant |
|---|---|---|
| `Developers` (`897b6c39`) | Oliver Rushton, Leon Ormes, Enric Serra, Pavlo Kotov, Yasir Mansoor, Oliver Rushton (guest) | Oliver Rushton, Leon Ormes, Pavlo Kotov, Oliver Rushton (guest), Robin Mofakham, Robin (Admin), Connor Price |
| `DevOpsEngineers` (`8db586bd`) | Oliver Rushton, Leon Ormes, Gareth Hailes | Oliver Rushton |

### 1.4a [R1 RESCOPED] This is not drift — Terraform is fighting PIM

Revision 1 read the table above as portal drift and concluded an apply "would remove three people's access and grant three others'". **That reasoning was wrong.** The PIM audit log (§1.2a) shows seven `Member` activations against **`DevOpsEngineers`** by Oliver and Leon, and expiry events against it. The group is under **PIM for Groups**: its at-rest membership is *supposed* to be near-empty, because members activate just-in-time. `DevOpsEngineers` showing only Oliver is the control working, not drift.

The actual defect is worse, and it is a live correctness bug:

- **`azuread_group.members` is authoritative.** Terraform will reconcile the group to exactly the listed set on every apply.
- So Terraform would write Oliver, Leon and Gareth in as **permanent** members of a group designed to be held just-in-time — **converting a JIT privilege path into standing privilege**, silently, as a side effect of a routine apply.
- **`DevOpsEngineers` holds `User Access Administrator` on the `Testing` subscription.** So the concrete effect is granting Leon and Gareth *permanent* User Access Administrator where PIM currently grants it for a bounded window.
- Every PIM activation by a colleague then shows as drift in the next `plan`, and every apply revokes it. The two systems will fight indefinitely, and PIM loses because Terraform runs on a schedule.

`Developers` is the same shape and needs the same check — its extra live members (Robin Mofakham, Robin (Admin), Connor Price) are as likely to be legitimate PIM/portal grants as drift, and Revision 1 should not have asserted otherwise without the eligible set in hand (still blocked, §1.6).

**The fix is not reconciliation, it is a change of resource.** For any group PIM manages:

- Use `azuread_group_without_members` and manage *eligibility* with `azuread_privileged_access_group_eligibility_schedule`, so Terraform owns who *may* activate and PIM owns who *has*; or
- keep `azuread_group` but add `lifecycle { ignore_changes = [members] }` as a stopgap.

Never point `azuread_group.members` at a PIM-managed group. Determining which of the ~10 managed groups are PIM-managed is a Phase 0 prerequisite, and needs the eligibility read in §1.6.

**Do not run `apply` on this workspace until that is settled.**

**`users.tf` cannot work as written.** It declares seven `azuread_user` resources, but the SP holds only `User.Read.All` — no write. Any change to a user attribute fails. Meanwhile the users carry `onpremises_immutable_id` values that are JumpCloud object IDs, and JumpCloud provisions them. **JumpCloud is the user source of truth; Terraform is pretending to be.**

**App-registration duplication.** The SP's owned objects include `ArgoCD Non Production` ×2, `ArgoCD Production` ×2, `Argo Workflows Non Production` ×2 and `Argo Workflows Production` ×2 — duplicate registrations for the same SSO application, consistent with a re-create after state loss.

**Provider versions are well behind.** `azuread ~> 2.46.0` against **v3.9.0** current (released 2026-06-18); `azurerm 3.108.0` against 4.x. This matters directly: **every PIM resource lives in v3** — `azuread_directory_role_eligibility_schedule_request`, `azuread_privileged_access_group_eligibility_schedule`, `azuread_privileged_access_group_assignment_schedule`, `azuread_group_role_management_policy`, plus `azuread_conditional_access_policy`, `azuread_custom_directory_role`, `azuread_administrative_unit`, `azuread_authentication_strength_policy`, `azuread_named_location` and `azuread_application_flexible_federated_identity_credential`. **The provider upgrade is a prerequisite, not a nice-to-have.**

**Secrets in state — relevant to §2.G.** `azuread_service_principal_password.vault_sp_secret` has no rotation (the `time_rotating` block is commented out), and its value is written via `tfe_variable` into a *different* workspace. Secret material therefore sits in two state files.

### 1.5 What is already correct — leave it alone

Worth recording so it does not get "improved":

- **Tenant authorisation policy**: `allowedToCreateApps: false`, `allowedToCreateSecurityGroups: false`, `allowedToCreateTenants: false`. Standard users cannot self-service privileged objects.
- **Guest posture**: `allowInvitesFrom: adminsAndGuestInviters`, `guestUserRoleId` = `2af84b1e-32c8-42b7-82bc-daa82404023b` (the most restricted guest role), `allowEmailVerifiedUsersToJoinOrganization: false`.
- **Separate admin accounts already exist**: `admin.mofakham@fitfile.com`, `admin.russmeyer@fitfile.com`, distinct from the day-to-day accounts. Right shape, and it predates this work.
- **A break-glass account exists** (`breakglass.azure`) and there is an `Exclude - Breakglass` group, implying CA policies are written with a break-glass exclusion. Sub-Project 0 is therefore *partly* satisfied — see finding 8.
- **Group-based Azure RBAC with a management-group hierarchy**: `FITFILE` → `LANDING-ZONES`, with `Azure RBAC Subscription …` / `Azure RBAC Group …` groups carrying Owner/Contributor/Reader. Consistent and PIM-ready.
- **`Group.Create` + ownership** on the Terraform SP (§1.4).

### 1.6 Gaps in this audit — and why Global Reader did not close them

Global Reader was activated via PIM and confirmed present in the token (`wids` contains `f2ef992c-3afb-46b9-b7cf-a126ee74c451`). **Both gaps persisted.** The reason is not the role:

**The Azure CLI application has no service principal in this tenant.** `servicePrincipals(appId='04b07795-8ddb-461a-bbee-02f9e1bf7b46')` returns `Request_ResourceNotFound`. With no SP there is no `oauth2PermissionGrant`, so the token carries only Microsoft's pre-authorised scope set:

```
AppRoleAssignment.ReadWrite.All  Application.ReadWrite.All  AuditLog.Read.All
DelegatedPermissionGrant.ReadWrite.All  Directory.AccessAsUser.All
Group.ReadWrite.All  SubjectNameRegistration.ReadWrite  User.Read.All  User.ReadWrite.All
```

Missing: `RoleManagement.Read.All`, `Policy.Read.All`, `PrivilegedEligibilitySchedule.Read.AzureADGroup`. **A directory role cannot substitute for a delegated scope the client never requested.** Still blocked:

| Read | Endpoint | Blocker |
|---|---|---|
| Directory role eligibility | `roleManagement/directory/roleEligibilityScheduleInstances` | scope `RoleManagement.Read.All` |
| PIM role settings / policies | `policies/roleManagementPolicies` | scope `RoleManagement.Read.All` |
| PIM for Groups eligibility | `identityGovernance/privilegedAccess/group/eligibilityScheduleInstances` | scope `PrivilegedEligibilitySchedule.Read.AzureADGroup` |
| Conditional Access policies | `identity/conditionalAccess/policies` (v1.0 and beta) | scope `Policy.Read.All` |
| `signInActivity` per user | `users?$select=signInActivity` | `Authentication_RequestFromUnsupportedUserRole` |

What *did* work, and carried the second pass: the **ARM** PIM APIs (Azure resource eligibility and assignment schedules — governed by Azure RBAC, not Graph scopes) and **`auditLogs/directoryAudits`** (`AuditLog.Read.All` is pre-authorised). Together these reconstructed most of the PIM picture indirectly — see §1.2a.

**Two ways to close the rest.** The second needs no admin action:

1. **A Global Admin grants the Azure CLI app the scopes once.** Creates the SP and an admin-consent grant for `RoleManagement.Read.All`, `Policy.Read.All`, `PrivilegedEligibilitySchedule.Read.AzureADGroup`. After that any Global Reader can run these reads from `az` indefinitely. Note this permanently widens what *every* `az` user in the tenant can request, so scope it deliberately.
2. **Use Microsoft Graph PowerShell instead — partially works today.** `Microsoft Graph Command Line Tools` (`14d82eec-…`) *does* have an SP here (`5c052c1c-213f-4fe3-bb94-f55f50228eae`) with **`RoleManagement.Read.Directory` already consented for `AllPrincipals`**. So directory-role eligibility and PIM settings are readable right now by any Global Reader via that client, with no admin involvement. `Policy.Read.All` on that app is consented only for two named individuals, so **CA still needs option 1** (or adding your own principal to that grant).

Neither `pwsh` nor `mgc` is installed on this machine, which is why option 2 was not exercised in this pass.

This is Phase 0 step 1, and it is now a concrete, costed action rather than a vague "stand up a discovery identity".

### 1.6a Break-glass cannot be verified as tested — [NEW]

`auditLogs/signIns` filtered to `breakglass*` returns **zero sign-ins** in the retained window. Zero is the *expected* steady state for a break-glass account, so this is not a finding about misuse. It is a finding about evidence: Entra retains 30 days of sign-in logs on P1/P2, so **there is no way to demonstrate the account has ever been successfully tested.**

The framing note makes "tested within the last 90 days" a hard gate on Sub-Project 0, and that gate is currently unprovable. Two consequences:

- A break-glass test must be performed and **recorded outside Entra** (runbook with date, tester, outcome).
- The Log Analytics / Sentinel export in §3.4 is needed **independently of the Terraform work**, purely so that break-glass sign-ins and PIM activations survive beyond 30 days. Promote it out of Phase 2 and into Phase 0.

### 1.7 Credential hygiene

44+ password credentials across app registrations; **the large majority are long expired and were never removed** — the oldest from 2021-09-30. Expired credentials are not directly exploitable, but they defeat inventory and hide live ones.

`Terraform AAD Provisioner` (app object `a129784b-4b08-44af-9398-a7c3c82e3717`, client `f8b9419b-e586-40da-b99b-cff830d98238`) holds **two client secrets** — `hcp-terraform-2` (expired 2025-10-14) and `Terraform Cloud pipelines` (valid to 2027-02-08) — and **zero `federatedIdentityCredentials`**. So HCP Terraform authenticates to Entra with a long-lived shared secret today. This is the framing note's §4.5 recommendation, still outstanding.

**Terraform SP sprawl.** At least seven distinct provisioner identities: `Terraform AAD Provisioner`, `Terraform Cloud Prod Provisioner`, `Terraform Cloud Non Prod Provisioner`, `Terraform Cloud Shared Services Provisioner`, `FITFILE Terraform Cloud Provisioner`, `Terraform Provisioner - GH Private Test`, `TEMP-PrivateTerraformCluster`. Several have expired secrets still attached.

Also: `azuread_application_password` for ArgoCD/Argo Workflows uses `end_date_relative = "4380h"` (6 months) with **no rotation trigger** — so the secrets duly expired (Dec 2025, May/Jun 2026) and stayed expired. A 6-month expiry without a rotation mechanism is a scheduled outage, not a control.

### 1.8 Licensing — the binding constraint

| SKU | Entitled | Consumed |
|---|---|---|
| `AAD_PREMIUM_P2` | 5 | **5** |
| `SPB` (Business Premium → P1) | 15 | 11 |
| `DEFENDER_SUITE_FOR_BUSINESS_PREMIUM_NEW` | 3 | 3 |
| `AAD_PREMIUM` (standalone P1) | 0 | 0 |

**The five P2 seats are fully allocated**: Oliver Rushton, Leon Ormes, Robin Mofakham, Robin (Admin), Philip (Admin).

Consequences, and they are hard limits:

- **PIM requires Entra ID P2 per user who is eligible** for a role, plus approvers. There is **no spare seat**. Gareth Hailes (DevSecOps Engineer) has no P2 and **cannot be made PIM-eligible** without buying one. Enric Serra, Pavlo Kotov and Yasir Mansoor likewise.
- **There is no Entra ID Governance SKU.** So **entitlement management, access packages and Lifecycle Workflows are unavailable** — the `azuread_access_package*` resources are off the table, and automated joiner/mover/leaver in Entra is not licensed. Hence the onboarding design in §5 leans on JumpCloud plus dynamic groups rather than access packages.
- **Access reviews of roles and groups do work** on P2, for those five users.
- **P1 (Business Premium) covers Conditional Access, dynamic groups, named locations, authentication strengths and protected actions** for the other 11 staff. Dynamic groups are the cheap win.

**Decide the P2 seat count before Phase 2.** The design is licence-bound, not effort-bound.

### 1.9 Azure estate — the real scope [NEW]

Revision 1 audited two subscriptions. There are **six subscriptions and four management groups**:

`Testing` · `FITCloud Production` · `FITCloud Non-Production` · `Shared Services` · `Management` · `Identity`

*(A seventh subscription, `NNUHFT-SDE`, is reachable via federated cross-tenant guest access but belongs to a customer's own Azure tenant — confirmed by its distinct `tenantId` — and was wrongly included in Revision 2. See the Revision 3 note above.)*
Management groups: `FITFILE` → `LANDING-ZONES`, `PLATFORM`, `sandbox`

Standing (non-PIM) holders of Owner / User Access Administrator / RBAC Administrator, direct assignments only:

| Scope | Role | Principal | Note |
|---|---|---|---|
| `FITFILE` MG | User Access Administrator | **Terraform AAD Provisioner** (SP) | **Unconstrained, inherited to all 7 subs** |
| `Shared Services` | User Access Administrator | HCP Vault, **HCP-vault-sp** (SP) | Both unconstrained |
| `Shared Services` | User Access Administrator | Terraform AAD Provisioner | ABAC-constrained ✓ |
| `Non-Production` | User Access Administrator | HCP-vault-sp, Terraform Cloud Non Prod, **Terraform Provisioner - GH Private Test** | All ABAC-constrained ✓ |
| `Production` | User Access Administrator | Terraform Cloud Prod Provisioner | ABAC-constrained ✓ |
| `Testing` | User Access Administrator | **`DevOpsEngineers` group** | See §1.4a — the PIM-managed group |
| `Testing` | User Access Administrator | FITFILE Terraform Cloud Provisioner | ABAC-constrained ✓ |
| `Production`/`Non-Prod`/`Identity` | RBAC Administrator | CloudPosture/securityOperators | Microsoft Defender, expected |
| `Testing` | Contributor | Leon Ormes, Oliver Rushton, Robin Mofakham | Standing |
| Per-sub Owner/Contributor | via `Azure RBAC Subscription …` groups | Oliver, Leon, Robin | **The path that bypasses PIM** |

Three things fall out of this:

**1. ABAC-constrained UAA is already used well — credit where due.** Five of the eight UAA assignments carry a `condition` restricting which `roleDefinitionId`s the principal may grant. That is a sophisticated control and exactly the right pattern. **The three unconstrained ones are the outliers**: Terraform AAD Provisioner at `FITFILE` MG, and both Vault SPs on Shared Services. Constrain them to match — the template already exists in your own estate.

**2. The Terraform SP is both tenant-admin and cloud-admin.** Graph side: `Application.ReadWrite.All` → mint credentials for any app → GA-equivalent. ARM side: unconstrained UAA at the top management group → grant itself Owner anywhere. Revision 1 understated this. It is the strongest argument for the Tier 0 / Tier 1 split in §3.2.

**3. There are two parallel routes to Owner, one JIT and one permanent.** `admin.mofakham` and `admin.russmeyer` reach Owner through PIM. Oliver, Leon and Robin reach it permanently through `Azure RBAC Subscription … Owner` group membership. **The good path already exists** — so the fix is to empty those groups and make the engineers PIM-eligible, not to build anything new. That is much cheaper than Revision 1 implied, subject only to P2 seats (§1.8).

**Dead credentials, live privilege.** Two SPs whose only secrets expired long ago still hold standing Azure privilege: `TEMP-PrivateTerraformCluster` (secret expired 2024-11, holds Contributor on Non-Production) and `Terraform Provisioner - GH Private Test` (secret expired 2025-01, holds Contributor **and** UAA on Non-Production). Also two managed identities named only by GUID — `160876b472ad47a1bcea63a0` and `f42542b7c87a46dd815d83c7`, both created 2022-05-30 — holding **Contributor on `FITCloud Production`**. Unnamed, undocumented, production-privileged: identify or remove.

**Provisioner sprawl is worse than Revision 1's seven.** Add `tfc-application` (Contributor, Non-Production) and `fitfile-automation_MW4K8p/Y99F…` (Contributor, Management) to the list.

---

## 2. Findings, ranked

Reordered after Revision 2. Severity changes are marked.

| # | Finding | Severity | Fix |
|---|---|---|---|
| 1 | **Terraform's `azuread_group.members` points at PIM-managed groups** — an apply converts JIT access to standing, and grants permanent UAA on `Testing` via `DevOpsEngineers` (§1.4a) | **Critical** ↑ | `azuread_group_without_members` + eligibility schedules, or `ignore_changes = [members]`. **Do not apply until fixed.** |
| 2 | JumpCloud Connector (user) holds standing **Privileged Role Administrator** | **Critical** | Remove PRA; keep the SP's SCIM permissions only |
| 3 | CIPP-SAM SP holds ~120 app permissions incl. `RoleManagement.ReadWrite.Directory` — app-only, so no CA and no PIM | **Critical** | Business decision on MSP scope; prune duplicates; if kept, treat as Tier 0 and monitor |
| 4 | **Terraform AAD Provisioner: unconstrained UAA at the `FITFILE` MG** + `Application.ReadWrite.All` → both cloud-admin and tenant-admin (§1.9) | **Critical** ↑ | Add ABAC condition (pattern already used in 5 places); split Tier 0/Tier 1 (§3.2) |
| 5 | Six holders of `Application.ReadWrite.All` form a mutual-escalation ring reaching GA | **High** | Move Terraform to `Application.ReadWrite.OwnedBy`; retire `HCP-vault-sp`; scope the GitLab test SP |
| 6 | ~~Withdrawn in Revision 3~~ | — | — |
| 7 | HCP Terraform authenticates with a long-lived client secret; no federated credential | **High** | Workload identity federation (§3.3) |
| 8 | Standing Owner via `Azure RBAC Subscription … Owner` groups (Oliver, Leon, Robin) **bypasses the working PIM path** | **High** ↓ scope | Empty the groups; make engineers PIM-eligible using the **existing** Azure PIM setup. Needs P2 seats |
| 9 | **Dead-but-privileged identities**: `TEMP-PrivateTerraformCluster`, `Terraform Provisioner - GH Private Test` (expired secrets, live Contributor/UAA); two GUID-named managed identities with **Contributor on Production** | **High** NEW | Identify and remove |
| 10 | Unconstrained UAA on `HCP Vault` and `HCP-vault-sp` (Shared Services) | **High** NEW | Constrain via ABAC or retire `HCP-vault-sp` |
| 11 | **Break-glass cannot be shown to have been tested** — 0 sign-ins, 30-day retention (§1.6a) | **High** NEW | Test and record out-of-band; export logs to Log Analytics — promote to Phase 0 |
| 12 | Only one break-glass account | Medium | Microsoft recommends two — feeds [[Break-Glass Identity The Complete Plan]] |
| 13 | Azure PIM eligibility all expires mid-2027 | Medium NEW | Diary the renewal; consider access reviews to drive it |
| 14 | Zero role-assignable groups exist — blocks PIM **for directory roles via groups** | Medium | Create with `assignable_to_role = true` (immutable at creation) |
| 15 | CA policies, PIM settings and eligibility unreadable — **az CLI app has no SP in tenant** (§1.6) | Medium | Admin-consent the scopes, or use Graph PowerShell (partially works today) |
| 16 | 39 disabled member accounts retained | Medium | Leaver process; reclaim licences |
| 17 | 40+ expired app credentials never removed; **9+** overlapping Terraform/automation SPs; duplicate app registrations | Medium | Inventory and cull |
| 18 | `users.tf` declares users the SP cannot write; JumpCloud is the real source | Medium | Convert to `data` lookups (§5) |
| 19 | `azuread ~> 2.46.0` — all PIM resources are in v3 | Medium | Upgrade to v3.x — prerequisite |
| 20 | Secret in state, shared across two workspaces, no rotation | Medium | OIDC where possible; rotation trigger otherwise |
| 21 | Global Administrator activated 13× in the retained window — highest-frequency privileged activation | Low NEW | Review whether a narrower role covers some of that work |
| 22 | Group naming inconsistent; duplicate `Developers` and `Exclaimer Test Group` | Low | Naming standard; retire legacy duplicates |
| 23 | `AdHoc License Administrator` (deprecated) assigned to Microsoft Office 365 Portal | Low | Remove |

**Withdrawn from Revision 1:** *"Standing named Global Administrator (Robin (Admin))"* — incorrect. Robin (Admin) is PIM-eligible and activates JIT; the posture is correct as-is.

**Withdrawn from Revision 2:** *finding 6, "`NNUHFT-SDE`: nine standing external Owners"* — the subscription is not part of FITFILE's Entra tenant. It is a customer's own Azure subscription, reachable only via the auditor's federated guest access, and was mistakenly swept in alongside FITFILE's genuine six subscriptions. See the Revision 3 banner above.

---

## 3. Giving HCP Terraform the Credentials — the Core Design

This answers §2.D of the framing note, which called it the deal-breaker question. It is, because the naive version ("give the workspace `RoleManagement.ReadWrite.Directory`") creates a pipeline that can make anyone a Global Administrator.

### 3.1 The principle that decides it

Microsoft's guidance on privileged intermediaries: any system that can manage or broker privileged roles belongs to the **control plane (Tier 0)** and must be protected at that level — explicitly naming *"automation runbooks, and service principals or applications that hold highly privileged roles."* If a lower-tier system can administer a control-plane asset, compromising the lower tier escalates privilege.

So: **HCP Terraform, once it can grant directory roles, is a Tier 0 asset.** Not a CI system that happens to touch identity. That reframing drives everything below.

The second constraint is structural: **app-only tokens bypass Conditional Access and PIM.** A service principal's client-credentials call is not subject to CA policy or role activation. So there is no compensating runtime control on the pipeline's own permissions — the only controls are (a) how small the permission set is, (b) who can trigger an apply, and (c) how well it is monitored. This also settles the framing note's open question about whether the CI/CD identity itself goes through PIM: **it cannot**, so the controls must be structural instead.

### 3.2 Two identities, not one

Split by blast radius, with separate workspaces, separate state, separate VCS paths:

| | **Tier 1 — Access plane** | **Tier 0 — Control plane** |
|---|---|---|
| SP | `Terraform AAD Provisioner` (existing) | `Terraform Entra Control Plane` (**new**) |
| Workspace | `fitfile-entra-id` (existing) | `fitfile-entra-control-plane` (**new**) |
| Manages | Groups, membership, app registrations for SSO, named locations | Role-assignable groups, PIM eligibility, PIM role-management policies, custom roles, CA policies |
| Graph app roles | `Group.Create`, `Group.Read.All`, `GroupMember.Read.All`, `Application.ReadWrite.OwnedBy`, `User.Read.All` | `RoleManagement.ReadWrite.Directory`, `RoleEligibilitySchedule.ReadWrite.Directory`, `RoleManagementPolicy.ReadWrite.Directory`, `PrivilegedEligibilitySchedule.ReadWrite.AzureADGroup`, `RoleManagementPolicy.ReadWrite.AzureADGroup`, `Policy.ReadWrite.ConditionalAccess`, `Policy.Read.All` |
| Auth | OIDC, no secret | OIDC, no secret |
| Apply | Auto-apply acceptable | **Manual apply, mandatory human approval** |
| Effective ceiling | Groups it owns | GA-equivalent — treat accordingly |

Why two and not one: the Tier 1 workspace changes weekly (people join teams, apps get redirect URIs). The Tier 0 workspace should change monthly at most, and every change should be read by a second person. Merging them means either the frequent changes get bureaucratic or the dangerous ones get waved through — in practice the latter.

**Deliberately kept out of Terraform** (§6): the break-glass accounts and their GA assignments, and the CIPP-SAM grant.

### 3.3 Workload identity federation — replace the client secret

HCP Terraform exchanges a short-lived OIDC token per run and discards it. Configuration:

**On each app registration**, two federated identity credentials — one per run phase:

- Issuer: `https://app.terraform.io` (no trailing slash)
- Audience: `api://AzureADTokenExchange`
- Subject: `organization:FITFILE-Platforms:project:<project>:workspace:<workspace>:run_phase:plan`
- Subject: `organization:FITFILE-Platforms:project:<project>:workspace:<workspace>:run_phase:apply`

**Workspace environment variables:**

- `TFC_AZURE_PROVIDER_AUTH = true`
- `TFC_AZURE_RUN_CLIENT_ID = <client id>`
- `ARM_TENANT_ID`, `ARM_SUBSCRIPTION_ID`

Do **not** set `client_id`, `use_oidc`, `oidc_token`, or `ARM_CLIENT_ID` / `ARM_CLIENT_SECRET` in the provider block — HCP Terraform injects them.

Two refinements worth taking:

1. **Split plan and apply into different service principals** via `TFC_AZURE_PLAN_CLIENT_ID` and `TFC_AZURE_APPLY_CLIENT_ID`. Give the plan SP **read-only** Graph permissions. A speculative plan on an untrusted branch then cannot write anything — which matters a lot for a Tier 0 workspace where MRs are the entry point.
2. **`azuread_application_flexible_federated_identity_credential`** — one credential with a `claims_matching_expression` instead of one per workspace per phase. Avoids credential sprawl as workspaces multiply. It is v3-only (another reason the provider upgrade is a prerequisite) and needs `Application.ReadWrite.OwnedBy` on the *managing* SP.

The `azuread` provider has supported OIDC since v2.43.0, so this works for both providers in the same run.

### 3.4 Controls that must accompany the Tier 0 identity

Because the pipeline's permissions cannot be constrained by CA or PIM, the controls sit around it:

- **Dedicated GitLab project** for `azure/ad-control-plane`, protected `master`, `CODEOWNERS` requiring a second approver, no direct pushes.
- **Manual apply with human confirmation** on the Tier 0 workspace. Never auto-apply role eligibility.
- **Diagnostic settings → Log Analytics/Sentinel** on `AuditLogs`, alerting on: any change to a role-assignable group's membership; any `Add eligible member to role`; any credential added to an application; any CA policy change. `sec-sentinel-readers` already exists, so a Sentinel path is likely in place. This is the framing note's §4.8 ("audit logs first, policy changes second") applied.
- **Quarterly access review** (P2) over the role-assignable groups.
- **No `Application.ReadWrite.All`** on the control-plane SP. It does not need it, and granting it would let the Tier 0 SP mint credentials for CIPP-SAM.

### 3.5 The honest limitation

Terraform can declare **eligibility**. It cannot declare **activation** — by design, that is the human, JIT, approval-gated step. It also cannot see activation history; that lives in the Entra audit log for 30 days (hence the Log Analytics export).

And there is an irreducible chicken-and-egg: `azuread_directory_role_eligibility_schedule_request` requires the calling principal to be Privileged Role Administrator or Global Administrator (or hold `RoleManagement.ReadWrite.Directory` app-only). **There is no least-privilege way to automate the granting of privilege.** The best available position is: minimise it, isolate it, gate it behind human approval on a protected branch, and monitor it — which is what §3.2–3.4 do. Anyone claiming a fully-least-privilege PIM pipeline is mistaken about the API.

---

## 4. Phased Plan

Mapped onto the framing note's sub-projects: Phase 0 ≈ Sub-Project I (audit & tidy) plus the prerequisite half of C; Phase 1 ≈ the rest of I; Phase 2 ≈ C + P; Phase 3 ≈ G.

### Phase 0 — Reconcile and see (do first; nothing else is safe until this is done)

> **Revised after Revision 2.** Step 1 is now a specific action, and two items are promoted in from Phase 2 because they turned out to be prerequisites rather than improvements.

1. **Unblock the reads.** Either (a) have Robin admin-consent `RoleManagement.Read.All`, `Policy.Read.All` and `PrivilegedEligibilitySchedule.Read.AzureADGroup` for the Azure CLI app — which creates its missing SP — or (b) install Microsoft Graph PowerShell, which already has `RoleManagement.Read.Directory` consented tenant-wide and covers everything except CA. See §1.6.
2. **[PROMOTED] Enumerate PIM eligibility and PIM role settings**, then work out **which of the ~10 Terraform-managed groups are PIM-managed**. Everything in step 4 depends on this. Currently unknown, and guessing risks converting JIT access to standing access.
3. **[PROMOTED] Export `AuditLogs` and `SignInLogs` to Log Analytics/Sentinel.** Needed for its own sake (§1.6a: break-glass is unverifiable at 30-day retention), not just for the Tier 0 controls in §3.4. Then perform and record a break-glass test.
4. **Fix the Terraform/PIM collision (§1.4a).** For each PIM-managed group, move to `azuread_group_without_members` plus `azuread_privileged_access_group_eligibility_schedule`, or add `ignore_changes = [members]`. **This is the gate on running `apply` at all.**
5. **Export current state to git as evidence** — role assignments, PIM eligibility and settings, CA policies, group membership, app permissions, and Azure RBAC across **all six subscriptions and four management groups**. A dated JSON snapshot under `docs/`. The Revision 2 sweep script is a starting point.
6. **Reconcile the remaining genuine drift.** Only after step 2 distinguishes PIM activations from real drift. For any name that is genuinely out-of-band: decide whether the tenant or the code is right.
7. **Run `terraform plan` and confirm it is empty.** Only then is the workspace the source of truth — the framing note's definition of done for Sub-Project C.
8. **Upgrade providers**: `azuread` → `~> 3.9`, `azurerm` → `~> 4.0`. `azuread_group_without_members` and every PIM resource need v3, so this now blocks step 4 as well.
9. **Fix `users.tf`**: replace the seven `azuread_user` resources with `data "azuread_user"` lookups keyed on UPN, removing the pipeline's need for user write. JumpCloud owns users.

*Exit criteria: PIM eligibility enumerated and PIM-managed groups identified; no Terraform resource authoritative over PIM-managed membership; empty plan; providers current; audit logs exported; break-glass tested and recorded; snapshot committed for all 6 subscriptions.*

### Phase 1 — Cut the standing privilege (independent of Terraform; highest value)

7. **Remove Privileged Role Administrator from JumpCloud Connector.** Verify JumpCloud provisioning still works — it should, via the `JumpCloud Office 365 Sync` SP. Then review whether User Administrator and Groups Administrator on the connector user are needed at all.
8. **Decide on CIPP-SAM.** Document the MSP relationship and required scope; prune duplicated grants; remove permissions outside agreed scope. If it stays, register it as a Tier 0 asset with monitoring.
9. **Second break-glass account**, per Microsoft's recommendation of two — cloud-only on `*.onmicrosoft.com`, excluded from CA, in `Exclude - Breakglass`, credentials split across two storage methods and two authentication methods. Execute against [[Break-Glass Identity The Complete Plan]]; also confirm the *existing* account's last successful test sign-in, since the framing note makes that a hard gate.
10. **Retire `HCP-vault-sp`** (legacy duplicate of `HCP Vault`, both holding `Application.ReadWrite.All`).
11. **Scope or retire `FITFILE Gitlab Integration Test Pipelines`** — Groups Administrator at tenant scope plus `Application.ReadWrite.All` for a *test* pipeline is not defensible.
12. **Move Terraform to `Application.ReadWrite.OwnedBy`.** The SP already owns its 22 objects.
13. **Credential cull**: delete the 40+ expired credentials; consolidate the seven Terraform provisioner SPs; delete the duplicate app registrations.
14. **Remove `AdHoc License Administrator`** from Microsoft Office 365 Portal.

*Nothing here needs new Terraform. Phase 1 is where the risk actually falls.*

### Phase 2 — Build the control plane (needs the P2 decision from §1.8)

15. **Buy P2 seats** for everyone who will be PIM-eligible. Currently 0 spare.
16. **Create the Tier 0 SP and workspace** per §3.2, OIDC-only per §3.3, with the controls in §3.4.
17. **Create role-assignable groups** — `assignable_to_role = true`, which is **immutable at creation**, so the naming standard must be agreed first. One per privileged function, not one per person:

    ```hcl
    resource "azuread_group" "role_global_admin" {
      display_name       = "ROLE-Entra-GlobalAdministrator"
      security_enabled   = true
      assignable_to_role = true   # immutable — cannot be changed later
    }
    ```

    Requires `RoleManagement.ReadWrite.Directory` — `Group.Create` is not sufficient. Cap: 500 per tenant.

18. **Assign directory roles to those groups** (permanent active on the *group*), then make **people eligible members of the group** rather than eligible for the role. This is Microsoft best-practice #7 and #8: one activation covers several roles, and group ownership becomes the delegation boundary.

    ```hcl
    resource "azuread_privileged_access_group_eligibility_schedule" "gareth_platform_admin" {
      group_id        = azuread_group.role_platform_admin.object_id
      principal_id    = data.azuread_user.gareth_hailes.object_id
      assignment_type = "member"
      justification   = "Platform engineering on-call — FTFL-XXXX"
      duration        = "P365D"   # NOT P1Y — see §7
    }
    ```

19. **Codify PIM role settings** with `azuread_group_role_management_policy` — the policy *is* the control, and this is where it becomes reviewable in git:

    | Function | MFA / CA context | Approval | Justification | Ticket | Activation | Permanent active |
    |---|---|---|---|---|---|---|
    | Global Administrator | Phishing-resistant via CA auth context | Yes — another GA | Yes | Yes | 1 hour | Break-glass only |
    | Privileged Role Admin | Phishing-resistant | Yes | Yes | Yes | 1 hour | None |
    | Azure Subscription Owner (prod) | Phishing-resistant | Yes — another owner | Yes | Yes | 1 hour | None |
    | Platform / DevOps admin | MFA | No | Yes | No | 4 hours | None |
    | Helpdesk-tier | MFA | No | Yes | No | 8 hours | None |

    Prefer `required_conditional_access_authentication_context` (e.g. `c1`) over `require_multifactor_authentication` — it lets a CA policy demand phishing-resistant MFA *and* a compliant device at activation. The two arguments conflict; pick one.

    **Solo-approver problem** (framing note §4.7): with 5 P2 seats and 2 GAs, "approval by another GA" has a quorum of one. Either buy a seat so there are two non-break-glass GA-eligible people, or accept self-service activation with mandatory justification plus real-time alerting, and record that as a conscious risk acceptance.

20. **Close the standing Owner bypass.** [REVISED] Azure PIM already works — `admin.mofakham` and `admin.russmeyer` are eligible for `Owner` on all six subscriptions. So this is not a build, it is a migration: make Oliver, Leon and Robin **eligible** with `azurerm_pim_eligible_role_assignment`, then **empty** `Azure RBAC Subscription … Owner`. Any security group works for Azure resource roles — role-assignable is only required for *directory* roles. Gated on P2 seats (§1.8).
21. **Constrain the three unconstrained UAA assignments** — Terraform AAD Provisioner at `FITFILE` MG, `HCP Vault` and `HCP-vault-sp` on Shared Services — by copying the ABAC `condition` already in use on the other five (§1.9).
22. **Diary the mid-2027 eligibility expiry** (§1.2a) and, if P2 allows, drive renewal through access reviews rather than a calendar reminder.

*Withdrawn from Revision 1: "Move Robin (Admin) from standing GA to PIM-eligible" — they already are.*
22. **CA policies into code** — once readable — with `azuread_conditional_access_policy`, deployed in rings per framing note §4.4. Watch the 1 req/sec API limit; reduce parallelism. Always exclude `Exclude - Breakglass`. Consider `azuread_authentication_strength_policy` and `azuread_named_location` alongside.
23. **Protected actions** (P1, already licensed) on `microsoft.directory/conditionalAccessPolicies/*` and `microsoft.directory/deletedItems/delete`, bound to a phishing-resistant CA auth context. Caveat: protected actions apply to *interactive user* calls and step-up-capable clients only; **Azure PowerShell fails outright** and app-only calls are unaffected. So this hardens humans in the portal, not the pipeline.

### Phase 3 — Scale and sustain

24. **Dynamic groups for baseline access** (P1). Rules on `department` / `jobTitle`, populated from JumpCloud attributes, so routine onboarding needs no Terraform change:

    ```hcl
    resource "azuread_group" "all_engineering" {
      display_name     = "DYN-All-Engineering"
      security_enabled = true
      types            = ["DynamicMembership"]
      dynamic_membership {
        enabled = true
        rule    = "user.department -eq \"Tech\" -and user.accountEnabled -eq true -and user.userType -eq \"Member\""
      }
    }
    ```

    This depends on JumpCloud populating `department` consistently — worth verifying, since several existing users have it blank.

25. **Naming standard** (framing note §4.9 — cheapest leverage), then migrate the legacy groups (`ARGOCD-Dev-Admins`, `grp-`, `sec-`, `sg-`, `VPN-`) and retire the duplicates. Suggested prefixes: `ROLE-` (role-assignable, PIM), `DYN-` (dynamic), `APP-` (application access), `AZRBAC-` (Azure RBAC), `SP-` (SharePoint).
26. **Bring the remaining ~95 groups into code** — import, do not recreate. `terraform import` or `import` blocks.
27. **Quarterly access reviews** (P2) over role-assignable groups and Azure Owner roles.
28. **Leaver process** for the 39 disabled accounts — including licence reclaim and group cleanup.
29. **Administrative units** (`azuread_administrative_unit`) if per-team delegation is ever needed. Not needed at 38 staff; noted for later.
30. **Custom directory roles** (`azuread_custom_directory_role`) where a built-in role is too broad. Also not needed yet.

---

## 5. Employee Onboarding — the "easily set up" answer

Today's model asks Terraform to be the user store, which it cannot be (§1.4) and should not be. The clean division:

| Layer | Owner | Mechanism |
|---|---|---|
| Identity lifecycle (joiner/mover/leaver) | **JumpCloud** | SCIM provisioning to Entra |
| Baseline access by role/department | **Entra dynamic groups** | Rules over JumpCloud-populated attributes — zero Terraform per joiner |
| Named application access | **Terraform, Tier 1** | Static group membership, MR-reviewed |
| Privileged eligibility | **Terraform, Tier 0** | PIM eligible assignment, MR-reviewed by a second person |

Onboarding a developer becomes: JumpCloud creates the account and sets `department` → dynamic groups grant baseline access automatically → **no Terraform change**. Granting a privileged function is a one-line MR in the Tier 0 repo:

```hcl
locals {
  platform_admins = [
    "leon.ormes@fitfile.com",
    "gareth.hailes@fitfile.com",   # ← the whole onboarding change
  ]
}
```

with `for_each` producing the eligibility schedules. Every privilege change is then a reviewed, attributable, revertible commit — precisely the git-audit outcome wanted — while activation stays JIT.

The constraint to be honest about: **each name added to a privileged list costs one Entra ID P2 seat**, and there are none spare.

---

## 6. What Must Not Go Into Terraform

Being deliberate about this is part of the design, not a gap in it — and it matches the framing note's §2.E "don't try" list:

- **Break-glass accounts and their GA assignments.** If Terraform manages them, a bad apply or a compromised pipeline can remove the last way in. Keep them manual, documented and tested quarterly.
- **The CIPP-SAM grant.** A pipeline that can re-grant it defeats the point of pruning it.
- **Individual PIM *activations*.** Runtime, JIT, human — by design.
- **User objects.** JumpCloud owns them (§5).
- **Long-lived secrets.** OIDC where possible; where a secret is unavoidable, `time_rotating` plus `rotate_when_changed`, never a bare 6-month expiry with no trigger (§1.7).

---

## 7. Known Gotchas

- **`assignable_to_role` is immutable.** Agree naming before creating any role-assignable group; changing it later means recreate.
- **`Group.Create` is not enough** for role-assignable groups — needs `RoleManagement.ReadWrite.Directory`.
- **ISO-8601 durations are restricted.** PIM for Groups rejects `P1Y` and `P6M` even though they are valid ISO-8601. Use `P365D`. Live provider issue.
- **Drift detection is unreliable** on `azuread_privileged_access_group_eligibility_schedule` / `_assignment_schedule` — out-of-band changes may not be detected. Compensate with audit-log alerting (§3.4), not with trust in `plan`.
- **PIM policy must exist for both `member` and `owner`** roles on a group before assignments succeed; otherwise `RoleAssignmentRequestPolicyValidationFailed`.
- **CA policy API is throttled to 1 req/sec.** Reduce parallelism on bulk changes.
- **`azuread_conditional_access_policy` with `filter`** needs the separate `Attribute Definition Reader` role — not included in Global Administrator.
- **`require_multifactor_authentication` conflicts with `required_conditional_access_authentication_context`.** Choose one; prefer the latter.
- **Protected actions do not apply to app-only calls**, and Azure PowerShell fails against them outright.
- **`azuread` v2 → v3 is a breaking upgrade**, particularly application resources. Budget for it.
- **Service principals cannot be made PIM-*eligible*** — only given a time-limited *active* assignment. Relevant to any idea of putting the pipeline itself behind PIM.

---

## 8. Open Decisions

These need a human answer; the plan branches on them.

1. **CIPP-SAM** — keep, prune, or remove? Everything else is capped by this. *Owner: Robin / Philip.*
2. **How many P2 seats to buy?** Determines who can be PIM-eligible, and whether the solo-approver problem is solvable. Currently 0 spare. *Owner: Robin.*
3. **Drift reconciliation (§1.4 / Phase 0.3)** — for each of six people, is the tenant right or the code? *Owner: Leon / Oliver.*
4. **Does JumpCloud own group membership too, or only users?** If JumpCloud also pushes groups, the Terraform group model needs a carve-out or it will fight the sync.
5. **JumpCloud Connector's remaining roles** — after PRA is removed, are User Administrator and Groups Administrator still needed, or does the `JumpCloud Office 365 Sync` SP cover it?
6. **Entra ID Governance licensing** — worth it for access packages and Lifecycle Workflows, or is JumpCloud-plus-dynamic-groups sufficient? The plan currently assumes the latter.
7. **Guest governance** (23 guests, §1.1) — in scope for this work, or the separate A4 cross-tenant project the framing note describes? Access reviews for guests need P2 or Governance.
8. **Sandbox tenant** — the framing note's §4.2 recommendation is still unresolved. Note a `sandbox` **management group** exists, which is not the same thing; CA and PIM policy changes cannot be rehearsed in a management group. *Owner: Leon.*
9. **[NEW] Which of the ~10 Terraform-managed groups are PIM-managed?** Blocks Phase 0 step 4. Answered by Phase 0 steps 1–2, not by discussion. *Owner: Leon.*
10. **[NEW] Consent route for the blocked reads** — widen the Azure CLI app tenant-wide (convenient, but widens what every `az` user can request), or standardise on Graph PowerShell for identity reads (narrower, needs tooling installed)? *Owner: Leon / Robin.*
11. **[NEW] The two GUID-named managed identities with Contributor on `FITCloud Production`** (created 2022-05-30) — what are they? *Owner: Oliver / Leon.*
12. **[NEW] An out-of-scope customer subscription (`NNUHFT-SDE`) was mistakenly included in Revision 2's estate sweep and withdrawn in Revision 3** — no action needed here, but any future automated sweep (see [FTFL-1054](https://fitfile.atlassian.net/browse/FTFL-1054)) must filter by `tenantId` first. *Owner: Leon.*

---

## 9. Sources

**Microsoft Learn**

- [Best practices for Microsoft Entra roles](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/best-practices) — the ten practices; <5 GAs; <10 privileged assignments; groups for role assignment; PIM for Groups; cloud-native accounts; layered controls
- [Plan a Privileged Identity Management deployment](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-deployment-plan) — zero permanently active except break-glass; role-setting tables; 500 role-assignable group cap; service principals cannot be *eligible*, only time-limited active
- [Privileged roles and permissions in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/privileged-roles-permissions) — `applications/credentials/update` is PRIVILEGED; *"Isolate privileged intermediaries as control plane assets"*
- [What are protected actions?](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/protected-actions-overview) — protectable permissions, P1 requirement, client limitations
- [Securing privileged access for hybrid and cloud deployments](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-planning)
- [Emergency access accounts](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access)

**HashiCorp**

- [Dynamic credentials with the Azure provider in HCP Terraform](https://developer.hashicorp.com/terraform/cloud-docs/dynamic-provider-credentials/azure-configuration) — `TFC_AZURE_PROVIDER_AUTH`, `TFC_AZURE_RUN_CLIENT_ID`, plan/apply subjects, `azuread` support from v2.43.0
- [Access Azure from HCP Terraform with OIDC federation](https://www.hashicorp.com/en/blog/access-azure-from-hcp-terraform-with-oidc-federation)
- Provider docs: [`azuread_privileged_access_group_eligibility_schedule`](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/privileged_access_group_eligibility_schedule) · [`azuread_group_role_management_policy`](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/group_role_management_policy) · [`azuread_directory_role_eligibility_schedule_request`](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/directory_role_eligibility_schedule_request) · [`azuread_conditional_access_policy`](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/conditional_access_policy) · [`azuread_application_flexible_federated_identity_credential`](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/application_flexible_federated_identity_credential)
- Provider issues: [#1813 duration `P1Y` rejected](https://github.com/hashicorp/terraform-provider-azuread/issues/1813) · [#1729 drift not detected](https://github.com/hashicorp/terraform-provider-azuread/issues/1729) · [#1450 policy validation failure](https://github.com/hashicorp/terraform-provider-azuread/issues/1450)

**Tenant evidence** — Microsoft Graph v1.0, read-only, 2026-09-07: `organization`, `subscribedSkus`, `users`, `groups`, `applications`, `servicePrincipals`, `roleManagement/directory/roleAssignments`, `roleManagement/directory/roleDefinitions`, `policies/authorizationPolicy`, `servicePrincipals/{graph}/appRoleAssignedTo`, `servicePrincipals/{tf}/ownedObjects`, `applications/{id}/federatedIdentityCredentials`; plus `az role assignment list` on subscription `249df46b-f75d-4492-8e78-b33a00473548`.

---

[implements:: [[Restructuring Entra ID—Scoping, IaC & PIM]]]
[depends_on:: [[Break-Glass Identity The Complete Plan]]]

## Related

- [[FITFILE Audit - ACR and Identity]]
- [[FITFILE Audit - Security Findings and Remediation]]
