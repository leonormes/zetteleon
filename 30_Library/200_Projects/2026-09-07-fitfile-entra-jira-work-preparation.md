---
conformant: true
created: 2026-09-07T13:10:00+01:00
modified: 2026-09-08T09:00:00+01:00
permalink: llmeon/30-library/200-projects/2026-09-07-fitfile-entra-jira-work-preparation
project_category: devops
project_name: Entra IAM Hardening
project_status: active
status: stable
tags: [backlog-prep, entra, fitfile, ftfl-584, ftfl-1029, ftfl-1030, iam, jira, pim, security]
title: 2026-09-07-fitfile-entra-jira-work-preparation
type: project
---

## FITFILE — Entra IAM Programme: Plan of Record

**This is the definitive "what to do" document for the Entra IAM work.** It supersedes the proposal version of this note: the tickets it recommended now exist, so it has been rewritten around real keys.

Division of labour between the three notes:

| Note | Answers |
|---|---|
| [[Restructuring Entra ID—Scoping, IaC & PIM]] | *Why*, and how the programme should be framed |
| [[2026-09-07-fitfile-entra-pim-least-privilege-plan]] (Rev 2) | *What is actually in the tenant* — the audit evidence |
| **This note** | *What to do, in what order, and who decides* |

Jira holds the working detail (acceptance criteria, evidence, remediation commands). **Jira is the source of truth for each ticket; this note is the source of truth for the map, the ordering and the reasoning.** Do not maintain acceptance criteria in both.

---

## 1. Status

Created in Jira on 2026-09-07: **2 epics, 24 tickets, 20 issue links**, plus an evidence comment on a closed pentest ticket. All tickets are in `Backlog` — nothing has entered a sprint.

| | Key | Owner | Priority |
|---|---|---|---|
| Epic A | [FTFL-1029](https://fitfile.atlassian.net/browse/FTFL-1029) — Entra IAM: Zero Standing Privilege | Robin | High |
| Epic B | [FTFL-1030](https://fitfile.atlassian.net/browse/FTFL-1030) — Entra IAM as Code | Leon | Medium |

Both linked `relates to` [FTFL-584](https://fitfile.atlassian.net/browse/FTFL-584); Epic B also linked to [FTFL-971](https://fitfile.atlassian.net/browse/FTFL-971).

> **⚠ Correction, 2026-09-08.** [FTFL-1036](https://fitfile.atlassian.net/browse/FTFL-1036) was withdrawn. Its premise — a FITFILE subscription (`NNUHFT-SDE`) with nine standing external Owners — was based on a scope error: that subscription belongs to a **customer's own Azure tenant** (confirmed distinct `tenantId`), reachable only via federated/guest access as a vendor supporting that customer, and was mistakenly included when `az account list --all` surfaced it alongside FITFILE's genuine six subscriptions. Full correction recorded in [[2026-09-07-fitfile-entra-pim-least-privilege-plan]] (Revision 3). Every table below has been updated; no customer personnel or role data is retained here.

**Why two epics and not one, and not folded into FTFL-584.** FTFL-584's definition of done is "close the 26 pentest findings by 2026-10-31" and it is Robin's. Epic A is "no standing privileged access". Epic B is "all Entra changes go via git". Three different definitions of done, two different owners, two different horizons. Merging them means the pentest deadline drags or the IaC work gets truncated to fit it.

**Why A is separate from B, and this is the important one.** Everything in Epic A can be done today, by hand, with no Terraform and no provider upgrade — and it holds nearly all the risk (two Criticals, four Highs). Epic B is slower, gated on the provider upgrade and P2 licences, and **reduces no risk on its own**. If only one gets resourced this quarter it must be A. In a single epic that trade-off is invisible.

---

## 2. Start here

Five things, no dependencies between them, highest risk reduction per hour:

1. **[FTFL-1031](https://fitfile.atlassian.net/browse/FTFL-1031)** — remove Privileged Role Administrator from `JumpCloud Connector`. Single highest-value change in the programme. A password-authenticating shared service account that can grant itself Global Administrator, bypassing every other control here.
2. **[FTFL-1032](https://fitfile.atlassian.net/browse/FTFL-1032)** — the CIPP-SAM decision. Commercial, not technical. **Decide early even if the change lands later**, because it caps what everything else can achieve.
3. **[FTFL-546](https://fitfile.atlassian.net/browse/FTFL-546)** — Robin to decide reopen vs. let [FTFL-1046](https://fitfile.atlassian.net/browse/FTFL-1046)/[FTFL-1034](https://fitfile.atlassian.net/browse/FTFL-1034) carry it. Evidence comment posted 2026-09-07 (§4.1).
4. **[FTFL-1035](https://fitfile.atlassian.net/browse/FTFL-1035)** — remove root-scope User Access Administrator. No capability lost; the PIM path already exists.
5. **Promote [FTFL-569](https://fitfile.atlassian.net/browse/FTFL-569)** — already Selected for Dev at High. Unblocks the break-glass evidence requirement and the Tier 0 monitoring. Cheapest unblock available.

Then, in parallel:

- **Risk reduction, no Terraform:** [FTFL-1033](https://fitfile.atlassian.net/browse/FTFL-1033), [FTFL-1034](https://fitfile.atlassian.net/browse/FTFL-1034), [FTFL-1041](https://fitfile.atlassian.net/browse/FTFL-1041)
- **Unblocking Terraform:** [FTFL-1044](https://fitfile.atlassian.net/browse/FTFL-1044) → [FTFL-1045](https://fitfile.atlassian.net/browse/FTFL-1045) → [FTFL-1048](https://fitfile.atlassian.net/browse/FTFL-1048) → [FTFL-1046](https://fitfile.atlassian.net/browse/FTFL-1046)

### ⚠ The ordering trap

**`terraform apply` on the `fitfile-entra-id` workspace must not be run until [FTFL-1046](https://fitfile.atlassian.net/browse/FTFL-1046) is resolved.** An apply would write permanent members into `DevOpsEngineers`, which PIM manages just-in-time and which holds `User Access Administrator` on the `Testing` subscription — converting JIT privilege into standing privilege as a side effect of a routine run.

The shortest safe path is **1044 → 1045 → 1048 → 1046**, roughly two weeks. Until that lands the workspace is read-only **by policy, not by configuration**. Say this out loud to anyone who might run it; nothing in the tooling prevents it.

---

## 3. The backlog of record

### Epic A — Zero Standing Privilege ([FTFL-1029](https://fitfile.atlassian.net/browse/FTFL-1029))

| Key | Ref | Summary | Pri | Assignee |
|---|---|---|---|---|
| [FTFL-1031](https://fitfile.atlassian.net/browse/FTFL-1031) | EntraIAM-01 | Remove Privileged Role Administrator from JumpCloud Connector | Highest | — |
| [FTFL-1032](https://fitfile.atlassian.net/browse/FTFL-1032) | EntraIAM-02 | Decide and document CIPP-SAM permission scope | Highest | Robin |
| [FTFL-1042](https://fitfile.atlassian.net/browse/FTFL-1042) | EntraIAM-12 | Decide Entra ID P2 seat count — **blocker** | Highest | Robin |
| [FTFL-1033](https://fitfile.atlassian.net/browse/FTFL-1033) | EntraIAM-03 | Reduce `Application.ReadWrite.All` grants | High | — |
| [FTFL-1034](https://fitfile.atlassian.net/browse/FTFL-1034) | EntraIAM-04 | Constrain privileged Azure RBAC on automation identities | High | — |
| [FTFL-1035](https://fitfile.atlassian.net/browse/FTFL-1035) | EntraIAM-05 | Remove User Access Administrator at tenant root scope | High | Robin |
| [FTFL-1037](https://fitfile.atlassian.net/browse/FTFL-1037) | EntraIAM-07 | Migrate engineers from standing Azure Owner to PIM-eligible | High | — |
| [FTFL-1038](https://fitfile.atlassian.net/browse/FTFL-1038) | EntraIAM-08 | Second break-glass account and tested runbook | High | — |
| [FTFL-1039](https://fitfile.atlassian.net/browse/FTFL-1039) | EntraIAM-09 | Leaver cleanup: 39 disabled accounts and guest review | Medium | — |
| [FTFL-1040](https://fitfile.atlassian.net/browse/FTFL-1040) | EntraIAM-10 | Diary the mid-2027 PIM eligibility expiry cliff | Medium | — |
| [FTFL-1041](https://fitfile.atlassian.net/browse/FTFL-1041) | EntraIAM-11 | Identify two GUID-named managed identities on Production | Medium | — |
| [FTFL-1043](https://fitfile.atlassian.net/browse/FTFL-1043) | EntraIAM-13 | Directory role housekeeping (deprecated role, GA activation review) | Low | — |

### Epic B — Entra IAM as Code ([FTFL-1030](https://fitfile.atlassian.net/browse/FTFL-1030))

| Key | Ref | Summary | Type | Pri |
|---|---|---|---|---|
| [FTFL-1044](https://fitfile.atlassian.net/browse/FTFL-1044) | EntraIAM-20 | Unblock identity discovery reads (Graph consent) | Task | Highest |
| [FTFL-1045](https://fitfile.atlassian.net/browse/FTFL-1045) | EntraIAM-21 | Identify which Terraform-managed groups are PIM-managed | **Spike** | Highest |
| [FTFL-1046](https://fitfile.atlassian.net/browse/FTFL-1046) | EntraIAM-22 | Terraform overwrites PIM-managed membership — JIT becomes standing | **Bug** | Highest |
| [FTFL-1047](https://fitfile.atlassian.net/browse/FTFL-1047) | EntraIAM-23 | HCP Terraform → Azure workload identity federation | Task | High |
| [FTFL-1048](https://fitfile.atlassian.net/browse/FTFL-1048) | EntraIAM-24 | Upgrade azuread v2.46→v3.x, azurerm 3.108→4.x | Task | High |
| [FTFL-1049](https://fitfile.atlassian.net/browse/FTFL-1049) | EntraIAM-25 | Split Tier 0 control plane from Tier 1 access plane | Task | High |
| [FTFL-1050](https://fitfile.atlassian.net/browse/FTFL-1050) | EntraIAM-26 | Role-assignable groups and PIM policies as code | Task | Medium |
| [FTFL-1051](https://fitfile.atlassian.net/browse/FTFL-1051) | EntraIAM-27 | Make JumpCloud the user source of truth | Task | Medium |
| [FTFL-1052](https://fitfile.atlassian.net/browse/FTFL-1052) | EntraIAM-28 | Dynamic groups for baseline access | Task | Medium |
| [FTFL-1053](https://fitfile.atlassian.net/browse/FTFL-1053) | EntraIAM-29 | Naming standard, retire duplicates, import ~95 groups | Task | Low |
| [FTFL-1054](https://fitfile.atlassian.net/browse/FTFL-1054) | EntraIAM-30 | Commit a dated state snapshot as audit evidence | Task | Medium |

### Existing tickets to prioritise rather than duplicate

| Key | Why it matters here |
|---|---|
| [FTFL-569](https://fitfile.atlassian.net/browse/FTFL-569) | EntraFF-12 Activity Log Export. **Prerequisite** for break-glass evidence ([FTFL-1038](https://fitfile.atlassian.net/browse/FTFL-1038)) and Tier 0 monitoring ([FTFL-1049](https://fitfile.atlassian.net/browse/FTFL-1049)). Already Selected for Dev. |
| [FTFL-570](https://fitfile.atlassian.net/browse/FTFL-570) | EntraFF-13 Activity Log Alerts. Extend its AC with the four Tier 0 alerts rather than raising new. |
| [FTFL-583](https://fitfile.atlassian.net/browse/FTFL-583) | EntraFF-26 App Registrations with Credentials (Highest). Count has grown 39 → **59 registrations, 44+ credentials**. Update the ticket. |
| [FTFL-765](https://fitfile.atlassian.net/browse/FTFL-765) | Review App Registrations spike. Overlaps FTFL-583; reconcile. |
| [FTFL-835](https://fitfile.atlassian.net/browse/FTFL-835) | OIDC migration. **Reconcile with [FTFL-1047](https://fitfile.atlassian.net/browse/FTFL-1047)** — close as duplicate, retitle, or narrow. Do not deliver both. |

### Dependency graph

```
FTFL-1044 (consent) ──▶ FTFL-1045 (which groups are PIM) ──▶ FTFL-1046 (the bug)
FTFL-1048 (provider) ──▶ FTFL-1046
                      └▶ FTFL-1049 (Tier 0/1) ──▶ FTFL-1050 (role-assignable groups)
FTFL-1042 (P2 seats) ──▶ FTFL-1050
                      └▶ FTFL-1037 (Owner migration)
FTFL-1044            ──▶ FTFL-1054 (snapshot)
FTFL-569  (log export) ▶ FTFL-1038 (break-glass evidence)
```

Three tickets gate most of the programme: **[FTFL-1042](https://fitfile.atlassian.net/browse/FTFL-1042)** (P2 seats), **[FTFL-1044](https://fitfile.atlassian.net/browse/FTFL-1044)** (discovery consent), **[FTFL-1048](https://fitfile.atlassian.net/browse/FTFL-1048)** (provider upgrade).

---

## 4. The highest-value finding: two closed tickets that were not remediated

A closed pentest finding that is still live is worse than an open one, because nobody is looking at it.

### 4.1 FTFL-546 / EntraFF-04 — incomplete remediation ✅ evidenced

[FTFL-546](https://fitfile.atlassian.net/browse/FTFL-546) "Remove User Access Administrator from DevOpsEngineers group" — closed **Done** 2026-07-13, comment *"All requirements are fulfilled."*

**The assignment is still live.** Re-verified 2026-09-07:

```
role        : User Access Administrator
principal   : DevOpsEngineers (Group, 8db586bd-8f20-4613-8ed3-530990b832c1)
scope       : /subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a   (Testing)
createdOn   : 2026-03-04T14:07:22Z
condition   : none — unconstrained
assignment  : …/roleAssignments/bde646e2-0cd7-4594-9edf-660092204f63
```

The group holds **zero** assignments on the other six subscriptions — so the remediation genuinely worked, it just followed the Prowler scan's scope (one subscription) rather than the estate's (seven). The assignment predates the closure, so it was never a regression.

**Evidence comment posted** to FTFL-546 on 2026-09-07 (comment `35429`), including the exact assignment ID so removal is a one-liner. Framed as a flag, not a reopen — **Robin's call on tracking**.

**Systemic implication, and the reason this matters beyond one ticket:** if the original scan covered one subscription, the same scope gap plausibly affects other closed EntraFF findings. Worth a re-verification pass across all six subscriptions and four management groups before FTFL-584 closes out. [FTFL-1054](https://fitfile.atlassian.net/browse/FTFL-1054) builds the tooling that makes this cheap and repeatable.

### 4.2 FTFL-545 / EntraFF-03 — scope gap, not regression

[FTFL-545](https://fitfile.atlassian.net/browse/FTFL-545) reviewed **one** service principal: `FITFILE Terraform Cloud Provisioner`. The estate has **nine** Terraform/automation identities, and the most privileged was not the one reviewed — `Terraform AAD Provisioner` holds `Application.ReadWrite.All` **and unconstrained `User Access Administrator` at the `FITFILE` management group**, inherited to all six subscriptions.

Correctly closed against its own scope. Follow-ups linked: [FTFL-1033](https://fitfile.atlassian.net/browse/FTFL-1033) and [FTFL-1034](https://fitfile.atlassian.net/browse/FTFL-1034).

### 4.3 Also uncovered, previously untracked

`admin.mofakham@fitfile.com` holds unconstrained `User Access Administrator` at `/` (tenant root), permanent and inherited to everything — Global Admin *elevate access* residue, which Microsoft says should be disabled once the task is done. Now [FTFL-1035](https://fitfile.atlassian.net/browse/FTFL-1035).

---

## 5. Coverage map — every audit finding has a home

Findings numbered per the plan note's §2 table (Revision 2). Nothing is unassigned.

| # | Finding | Severity | Ticket |
|---|---|---|---|
| 1 | Terraform authoritative over PIM-managed group membership | Critical | [FTFL-1046](https://fitfile.atlassian.net/browse/FTFL-1046) |
| 2 | JumpCloud Connector holds standing Privileged Role Administrator | Critical | [FTFL-1031](https://fitfile.atlassian.net/browse/FTFL-1031) |
| 3 | CIPP-SAM ~120 Graph app permissions | Critical | [FTFL-1032](https://fitfile.atlassian.net/browse/FTFL-1032) |
| 4 | Terraform SP unconstrained UAA at FITFILE MG | Critical | [FTFL-1034](https://fitfile.atlassian.net/browse/FTFL-1034) |
| 5 | Six holders of `Application.ReadWrite.All` | High | [FTFL-1033](https://fitfile.atlassian.net/browse/FTFL-1033) |
| 6 | ~~Withdrawn — out-of-scope customer subscription~~ | — | — |
| 7 | HCP Terraform on a long-lived client secret | High | [FTFL-1047](https://fitfile.atlassian.net/browse/FTFL-1047) |
| 8 | Standing Owner via `Azure RBAC Subscription …` groups | High | [FTFL-1037](https://fitfile.atlassian.net/browse/FTFL-1037) |
| 9 | Dead-but-privileged identities; GUID managed identities on Production | High | [FTFL-1034](https://fitfile.atlassian.net/browse/FTFL-1034), [FTFL-1041](https://fitfile.atlassian.net/browse/FTFL-1041) |
| 10 | Unconstrained UAA on HCP Vault / HCP-vault-sp | High | [FTFL-1034](https://fitfile.atlassian.net/browse/FTFL-1034) |
| 11 | Break-glass cannot be shown to have been tested | High | [FTFL-1038](https://fitfile.atlassian.net/browse/FTFL-1038) + [FTFL-569](https://fitfile.atlassian.net/browse/FTFL-569) |
| 12 | Only one break-glass account | Medium | [FTFL-1038](https://fitfile.atlassian.net/browse/FTFL-1038) |
| 13 | Azure PIM eligibility all expires mid-2027 | Medium | [FTFL-1040](https://fitfile.atlassian.net/browse/FTFL-1040) |
| 14 | Zero role-assignable groups | Medium | [FTFL-1050](https://fitfile.atlassian.net/browse/FTFL-1050) |
| 15 | CA / PIM reads blocked — az CLI app has no SP | Medium | [FTFL-1044](https://fitfile.atlassian.net/browse/FTFL-1044) |
| 16 | 39 disabled member accounts; 23 unreviewed guests | Medium | [FTFL-1039](https://fitfile.atlassian.net/browse/FTFL-1039) |
| 17 | 40+ expired credentials; 9 overlapping automation SPs | Medium | [FTFL-583](https://fitfile.atlassian.net/browse/FTFL-583), [FTFL-1034](https://fitfile.atlassian.net/browse/FTFL-1034) |
| 18 | `users.tf` declares users the SP cannot write | Medium | [FTFL-1051](https://fitfile.atlassian.net/browse/FTFL-1051) |
| 19 | `azuread ~> 2.46.0` — PIM resources are v3-only | Medium | [FTFL-1048](https://fitfile.atlassian.net/browse/FTFL-1048) |
| 20 | Secret in state, shared across workspaces, no rotation | Medium | [FTFL-1047](https://fitfile.atlassian.net/browse/FTFL-1047) |
| 21 | GA activated 13× in the retained window | Low | [FTFL-1043](https://fitfile.atlassian.net/browse/FTFL-1043) |
| 22 | Group naming inconsistent; duplicate groups | Low | [FTFL-1053](https://fitfile.atlassian.net/browse/FTFL-1053) |
| 23 | Deprecated `AdHoc License Administrator` assignment | Low | [FTFL-1043](https://fitfile.atlassian.net/browse/FTFL-1043) |
| — | Tier 0/Tier 1 architecture; state snapshot; dynamic groups | design | [FTFL-1049](https://fitfile.atlassian.net/browse/FTFL-1049), [FTFL-1054](https://fitfile.atlassian.net/browse/FTFL-1054), [FTFL-1052](https://fitfile.atlassian.net/browse/FTFL-1052) |

**Withdrawn from Revision 1:** *"Standing named Global Administrator (Robin (Admin))"* — incorrect. Robin (Admin) is PIM-eligible and activates just-in-time. The `roleAssignments` endpoint returns *currently effective* assignments, live activations included, and Revision 1 queried it mid-activation.

---

## 6. Decisions needed, with owners

Sequenced by how much else they gate.

| # | Decision | Owner | Gates |
|---|---|---|---|
| 1 | **CIPP-SAM** — keep, prune, or remove? | Robin / Philip | The ceiling on the whole programme |
| 2 | **P2 seat count**, and the GA approver model | Robin | [FTFL-1037](https://fitfile.atlassian.net/browse/FTFL-1037), [FTFL-1050](https://fitfile.atlassian.net/browse/FTFL-1050) |
| 3 | **Consent route** for blocked reads — widen az CLI tenant-wide, or standardise on Graph PowerShell? | Leon / Robin | [FTFL-1045](https://fitfile.atlassian.net/browse/FTFL-1045), [FTFL-1046](https://fitfile.atlassian.net/browse/FTFL-1046), [FTFL-1054](https://fitfile.atlassian.net/browse/FTFL-1054) |
| 4 | **FTFL-546** — reopen, or let the new tickets carry it? | Robin | Audit trail cleanliness |
| 5 | **Does JumpCloud own group membership**, or only users? | Leon / Robin | [FTFL-1051](https://fitfile.atlassian.net/browse/FTFL-1051), [FTFL-1052](https://fitfile.atlassian.net/browse/FTFL-1052) |
| 6 | **JumpCloud Connector's remaining roles** after PRA removal | Leon | [FTFL-1031](https://fitfile.atlassian.net/browse/FTFL-1031) |
| 7 | **`ROLE-` naming standard** — agree *before* any role-assignable group is created (`assignable_to_role` is immutable) | Leon | [FTFL-1050](https://fitfile.atlassian.net/browse/FTFL-1050) |
| 8 | **Entra ID Governance licensing** — worth it for access packages and Lifecycle Workflows? | Robin | Onboarding architecture |
| 9 | **Guest governance** (23 guests) — this programme or a separate cross-tenant workstream? | Robin | [FTFL-1039](https://fitfile.atlassian.net/browse/FTFL-1039) |
| 10 | **Sandbox tenant** — still unresolved from the framing note. A `sandbox` *management group* exists, which is not the same thing; CA and PIM policy cannot be rehearsed in one. | Leon | [FTFL-1050](https://fitfile.atlassian.net/browse/FTFL-1050) |
| 11 | **Two GUID-named managed identities** with Contributor on Production — what are they? | Oliver / Leon | [FTFL-1041](https://fitfile.atlassian.net/browse/FTFL-1041) |

### The two decisions worth arguing about

**CIPP-SAM sets the ceiling.** It holds `RoleManagement.ReadWrite.Directory`, `Policy.ReadWrite.ConditionalAccess`, `UserAuthenticationMethod.ReadWrite.All` and `Application.ReadWrite.All` — Global-Administrator-equivalent, **app-only**, and therefore subject to neither Conditional Access nor PIM. Hardening human admin access to phishing-resistant JIT while that sits alongside it moves the attack path rather than closing it. That is not an argument against doing the rest; it is an argument for deciding this consciously and writing down the residual risk.

**The approver quorum is one person.** Microsoft's recommended PIM setting for Global Administrator is "approval by another Global Administrator". There are two GAs, one of which is break-glass and must never be used for routine approvals. So either buy a P2 seat and make a second person GA-eligible, or accept self-service activation with mandatory justification plus real-time alerting — recorded as an owner-accepted risk, not left as an oversight.

---

## 7. Reference data — do not re-derive this

Read-only audit, tenant `45e73aa3-1ee9-47c0-ba25-54eda9da021a`, 2026-09-07.

**Estate shape.** 6 subscriptions — `Testing` `7bbc8ae5`, `FITCloud Production` `a448d869`, `FITCloud Non-Production` `249df46b`, `Shared Services` `a085dd04`, `Management` `a9602426`, `Identity` `c1c459c8`. 4 management groups — `FITFILE` → `LANDING-ZONES`, `PLATFORM`, `sandbox`.

**Directory.** 100 users (38 enabled members, **39 disabled members**, 21 enabled guests, 2 disabled guests). 105 groups — **0 role-assignable, 0 dynamic**. 59 app registrations, 1063 service principals.

**Licences — the binding constraint.** `AAD_PREMIUM_P2` **5 of 5 consumed**: Oliver Rushton, Leon Ormes, Robin Mofakham, Robin (Admin), Philip (Admin). `SPB` (Business Premium → P1) 11 of 15. **No Entra ID Governance SKU** — so entitlement management, access packages and Lifecycle Workflows are unavailable, which is why onboarding leans on JumpCloud plus dynamic groups.

**PIM is already deployed and working** — this is the fact Revision 1 got wrong. 114 PIM events in the retained window: Global Administrator ×13, PIM-for-Groups `Member` ×7, Application Administrator ×5, Global Reader ×2, plus Azure Owner/Contributor/VM Contributor/AKS RBAC Cluster Admin. Activations expire correctly. `admin.mofakham` and `admin.russmeyer` are eligible for `Owner` on **all six subscriptions**, expiring 2027-07.

**Terraform.** Workspace `fitfile-entra-id`, org `FITFILE-Platforms`. SP `Terraform AAD Provisioner`, app object `a129784b-4b08-44af-9398-a7c3c82e3717`, client `f8b9419b-e586-40da-b99b-cff830d98238`. Two client secrets (one expired 2025-10-14, one live to 2027-02-08), **zero federated credentials**. Manages ~10 of 105 groups, 7 users, 6 app registrations.

### Already correct — leave it alone

Worth recording so nobody "improves" it:

- **Tenant authorisation policy**: `allowedToCreateApps: false`, `allowedToCreateSecurityGroups: false`, `allowedToCreateTenants: false` — delivered under [FTFL-563](https://fitfile.atlassian.net/browse/FTFL-563)–[FTFL-566](https://fitfile.atlassian.net/browse/FTFL-566).
- **Guest posture**: `allowInvitesFrom: adminsAndGuestInviters`, most restricted `guestUserRoleId`, `allowEmailVerifiedUsersToJoinOrganization: false` — [FTFL-567](https://fitfile.atlassian.net/browse/FTFL-567)/[FTFL-568](https://fitfile.atlassian.net/browse/FTFL-568).
- **Separate admin accounts** already exist (`admin.mofakham`, `admin.russmeyer`).
- **Group-based Azure RBAC** with a management-group hierarchy — consistent and PIM-ready.
- **`Group.Create` + group ownership** on the Terraform SP rather than `Group.ReadWrite.All`. Microsoft's recommended least-privilege pattern for app-managed groups. **Do not broaden it.**
- **ABAC-constrained UAA on five of eight assignments** — restricting grantable `roleDefinitionId`s. Sophisticated, and the template for fixing the three unconstrained ones.
- **Workload identity federation is a proven in-house pattern** — [FTFL-978](https://fitfile.atlassian.net/browse/FTFL-978)/[FTFL-980](https://fitfile.atlassian.net/browse/FTFL-980)/[FTFL-981](https://fitfile.atlassian.net/browse/FTFL-981) did it for GitLab CI, including deleting the secrets afterwards.

---

## 8. What must not go into Terraform

Deliberate scope exclusions, not gaps:

- **Break-glass accounts and their GA assignments.** If the pipeline manages them, a bad apply or a compromised pipeline removes the last route in.
- **The CIPP-SAM grant.** A pipeline that can re-grant it defeats the point of pruning it.
- **Individual PIM activations.** Runtime, JIT, human — by design. Terraform declares who *may* become an admin; PIM decides when they are.
- **User objects.** JumpCloud owns them.
- **Long-lived secrets.** OIDC where possible; where unavoidable, `time_rotating` + `rotate_when_changed`, never a bare 6-month expiry with no trigger.
- **Dynamic group rules for anything privileged.** A rule that silently adds someone to an admin group is exactly the unreviewed grant this programme exists to remove.

### The honest limitation

There is **no least-privilege way to automate the granting of privilege**. `azuread_directory_role_eligibility_schedule_request` requires Privileged Role Administrator or `RoleManagement.ReadWrite.Directory` app-only. The best available position — minimise, isolate, gate behind human approval on a protected branch, monitor — is what [FTFL-1049](https://fitfile.atlassian.net/browse/FTFL-1049) builds. It does not eliminate the risk, and the design should not be presented as if it did.

---

## 9. Gotchas

**Terraform / provider**

- `assignable_to_role` is **immutable at creation** — agree naming first.
- `Group.Create` is insufficient for role-assignable groups; needs `RoleManagement.ReadWrite.Directory`. Cap 500/tenant.
- Durations reject `P1Y` and `P6M` despite being valid ISO 8601 — use `P365D` ([#1813](https://github.com/hashicorp/terraform-provider-azuread/issues/1813)).
- A PIM policy must exist for **both** `member` and `owner` on a group before assignments succeed ([#1450](https://github.com/hashicorp/terraform-provider-azuread/issues/1450)).
- Drift detection on eligibility/assignment schedules is unreliable ([#1729](https://github.com/hashicorp/terraform-provider-azuread/issues/1729)) — rely on audit-log alerting, not `plan`.
- CA policy API throttles to 1 req/sec; reduce parallelism.
- `azuread_conditional_access_policy` with `filter` needs the separate `Attribute Definition Reader` role, not included in Global Administrator.
- `require_multifactor_authentication` conflicts with `required_conditional_access_authentication_context` — prefer the latter.
- azuread v2 → v3 is breaking, especially application resources.
- **`azuread_user` has destroy semantics that delete the directory object.** `terraform state rm` before any apply on [FTFL-1051](https://fitfile.atlassian.net/browse/FTFL-1051). Pair on it.

**Entra behaviour**

- `roleManagement/directory/roleAssignments` returns *currently effective* assignments, **including live PIM activations**. Not a snapshot of permanent grants. This is what broke Revision 1 — use `roleEligibilityScheduleInstances` or the PIM audit log to separate them.
- A directory role **cannot** substitute for a delegated scope the client never requested. The az CLI app has no service principal in this tenant, so activating Global Reader changes nothing for the blocked reads.
- Service principals cannot be made PIM-**eligible**, only given a time-limited active assignment.
- Protected actions do not apply to app-only calls, and Azure PowerShell fails against them outright.
- Sign-in and audit logs retain **30 days** on P1/P2 — hence [FTFL-569](https://fitfile.atlassian.net/browse/FTFL-569) being a prerequisite rather than a nice-to-have.

**Jira / process**

- The `Story` issue type in FTFL requires a **"Clinical Safety Considered"** field. [FTFL-1049](https://fitfile.atlassian.net/browse/FTFL-1049) was created as a Task for this reason. If team convention wants it as a Story, that field needs populating.
- Markdown **tables do not survive** the ADF comment path — they flatten to unreadable single lines. Use code blocks in comments. Ticket *descriptions* go through Jira wiki markup and render tables correctly.

---

## 10. Outstanding admin

- **[FTFL-546](https://fitfile.atlassian.net/browse/FTFL-546)** — Robin to decide reopen vs. leave closed. Evidence comment `35429` posted.
- **[FTFL-835](https://fitfile.atlassian.net/browse/FTFL-835)** — reconcile with [FTFL-1047](https://fitfile.atlassian.net/browse/FTFL-1047) before either is picked up.
- **[FTFL-583](https://fitfile.atlassian.net/browse/FTFL-583)** — update counts to 59 registrations / 44+ credentials.
- **[FTFL-570](https://fitfile.atlassian.net/browse/FTFL-570)** — extend AC with the four Tier 0 alert rules.
- **Cross-references** — most new tickets use `[EntraIAM-NN]` shorthand in their bodies rather than clickable FTFL links. Only [FTFL-1046](https://fitfile.atlassian.net/browse/FTFL-1046) was converted. Cosmetic; worth a pass if the board gets used heavily.
- **Assignees** — 15 of 24 tickets are unassigned, deliberately, for refinement. The four needing Robin's authority are assigned.
- **Re-verification pass** across all six subscriptions for the other 18 closed EntraFF findings (§4.1).

---

## 11. Provenance

All tenant and Azure operations across this work were **read-only**. No configuration was changed, no secret value was read. The only writes were to Jira (2 epics, 24 tickets, 20 links, 1 comment) and this vault.

Two audit passes: Revision 1 with no directory role, Revision 2 with Global Reader activated via PIM. Revision 2 corrected three material errors in Revision 1 — see that note's banner before re-running any of this analysis.

**Sources.** Microsoft Learn: [Best practices for Entra roles](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/best-practices) · [Plan a PIM deployment](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-deployment-plan) · [Privileged roles and permissions](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/privileged-roles-permissions) · [Protected actions](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/protected-actions-overview) · [Emergency access accounts](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access) · [Elevate access](https://learn.microsoft.com/en-us/azure/role-based-access-control/elevate-access-global-admin). HashiCorp: [Azure dynamic credentials](https://developer.hashicorp.com/terraform/cloud-docs/dynamic-provider-credentials/azure-configuration) · [OIDC federation blog](https://www.hashicorp.com/en/blog/access-azure-from-hcp-terraform-with-oidc-federation). Tenant evidence: Microsoft Graph v1.0, ARM `2020-10-01`/`2022-04-01`, `az` CLI 2.90.0.

---

## Related

- [[2026-09-07-fitfile-entra-pim-least-privilege-plan]] — the audit evidence (Revision 2)
- [[Restructuring Entra ID—Scoping, IaC & PIM]] — the framing this answers
- [[Break-Glass Identity The Complete Plan]] — executed by [FTFL-1038](https://fitfile.atlassian.net/browse/FTFL-1038)

[depends_on:: [[Break-Glass Identity The Complete Plan]]]
