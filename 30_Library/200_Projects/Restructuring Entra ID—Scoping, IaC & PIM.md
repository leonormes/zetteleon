---
created: 2026-05-15T08:22:11+00:00
modified: 2026-06-08T11:49:22+00:00
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
title: Restructuring Entra ID—Scoping, IaC & PIM
type:
---

## 1. The Real Problem (Reframe)

This is the highest-stakes project of the three you've brought me, and the framing pattern is now familiar—but with one critical addition:

> There is a Sub-Project Zero that precedes scoping. Before _anything_ else—before scoping, before audit, before a single line of Terraform—you must verify that break-glass access exists, is documented, is monitored, and was tested within the last 90 days.

If break-glass is uncertain, all other work stops until it is. Tenant lockout is the only project failure mode that you cannot recover from with a `git revert`.

After that, the same investigation-vs-improvement split applies, with a third axis:

- Sub-Project 0—Break-Glass Verification. Existential prerequisite. Done when documented, tested, alerted on.
- Sub-Project I—Audit & Tidy. Discovery + manual cleanup _in the portal_. Done when the tenant is in a state worth codifying.
- Sub-Project C—Codification (IaC). Import or recreate cleaned state. Done when plan = zero diff.
- Sub-Project P—PIM Rollout. Eligibility model + activation policies. Done when standing human privilege ≈ 0 (excluding break-glass).
- Sub-Project G—Governance. Access reviews, lifecycle, ongoing controls.

The LLM response collapsed all of these into "phases" of one project. They are not phases—they are five separate projects with separate definitions of done. I will only natural-plan Sub-Project I with you, after Sub-Project 0 is signed off.

A second framing point: the worst risk in Entra IaC is not a bad deploy—it is enshrining the existing mess in code. Codifying chaos doesn't fix it, it _calcifies_ it. Tidy first, codify second. Never the reverse.

---

## 2. Scoping Trigger List

### A. Which tenant(s) Are in Scope?

You operate across multi-tenant Azure architectures. These are _very different projects_:

- A1. Fitfile's home/corporate tenant only
- A2. A single customer tenant (e.g. MKUH's)
- A3. All customer tenants (a programme, not a project)
- A4. The cross-tenant trust topology—B2B, multi-tenant app registrations, cross-tenant access settings

Pick one. I'd strongly suggest A1 first—your own house—to validate the pattern before applying to customer tenants.

### B. What is the Single Primary Driver?

You can only optimise for one at a time:

- Recent/upcoming audit (DSP Toolkit, ISO27001, SOC2, NHS DTAC)?
- Drift elimination from portal-clicking?
- Zero standing privilege (Zero Trust posture)?
- Compliance with a specific control framework?
- Recovery from an incident or near-miss?
- A push to reduce on-call/credential-rotation toil?

If you say "all of them", you have a programme, not a project.

### C. What's the Current IaC Posture for Entra Specifically?

- Zero IaC today, all portal?
- Partial—some objects in Terraform, most not?
- Wrong IaC—written but unmaintained / drifted?
- Multiple competing IaC efforts (e.g. Bicep here, Terraform there)?

### D. What is the CI/CD Identity Story?

This is the deal-breaker question for Entra IaC, and the LLM didn't ask it:

- What identity will Terraform Cloud use to make Entra changes?
- Client secret, certificate, workload identity federation, or managed identity?
- What Entra roles will it hold? (Application Administrator? Privileged Role Administrator? Global Admin?—each has implications.)
- Does that identity itself need to go through PIM? _(For service principals this is nuanced—PIM for Groups is the modern answer.)_

If the CI/CD identity itself has standing high privilege, your PIM project undermines itself.

### E. Coverage—what's Actually IaC-able?

Provider support is uneven. Be honest about scope:

- Well-covered: App Registrations, Service Principals, security groups, named locations, most Conditional Access policy shapes
- Mixed: PIM role settings, PIM-for-Groups, authentication strengths, cross-tenant access settings
- Poor / procedural: identity protection policies, identity governance access reviews, B2B guest lifecycle, authentication methods migration
- Don't try: end-user attributes, one-off admin actions, break-glass account management _(deliberately manual)_

Define the IaC scope explicitly—what's in, what's deliberately out, and why.

### F. Tooling—answered, not Asked

The LLM ended by asking you which tool to use. Given your stack (Terragrunt, Terraform Cloud, Azure throughout), the default is:

- Terraform `hashicorp/azuread` provider—primary
- `microsoft/azapi` provider—for resources the AzureAD provider lacks
- `Microsoft.Graph` PowerShell modules—for discovery scripts and one-off ops
- Avoid Bicep here unless you already standardise on it elsewhere—splitting your IaC ecosystem is expensive.

The non-trivial question is _where the state lives_—see G.

### G. State File Security

Entra IaC state contains object IDs, group memberships, app registration metadata. Treat as secret-level material.

- Backend: Terraform Cloud workspace, AzureRM blob, something else?
- Who can read the state? (TF Cloud team membership, blob RBAC)
- Encryption at rest, customer-managed keys?
- State backup / disaster recovery plan?

### H. Discovery—what Dirt Do You Actually Have?

You will not know scope until you've enumerated. Order of magnitude estimates today:

- of users (members vs guests)?
- of security groups?
- of app registrations (and how many with secrets expiring in 90 days)?
- of Conditional Access policies (and how many overlap or conflict)?
- of Global Admins?
- of standing privileged role assignments (any role)?
- Last sign-in age distribution for guests?

You don't need exact numbers yet—order of magnitude tells you whether tidy is days or weeks.

### I. Test/sandbox Tenant?

- Does Fitfile own a non-production Entra tenant?
- If not, acquiring one is part of this project—it's free for dev/test purposes and indispensable for testing CA policy changes before production.

### J. Audit Log Retention

- Are Entra sign-in and audit logs exported to Log Analytics?
- Retention period?
- If you need to analyse 90 days of sign-in patterns and retention is 30, that's a prerequisite to fix first.

### K. Definition of done—for the Audit & Tidy Sub-project

> _"The audit & tidy sub-project is finished when ___ has been documented, ___ has been deleted/remediated in the portal, and the tenant is in a state where importing it into Terraform would yield a meaningful and maintainable codebase."_

If you can complete that sentence, you have a project.

---

## 3. Critique of the LLM Response

It's competent and uses the right vocabulary, but it has three serious structural errors and several content gaps.

### Structural Errors

1. Break-glass is mentioned as a "principle" and barely a "phase". It should be Sub-Project Zero, the existential prerequisite, with its own runbook, alerting (sign-in alerts on the accounts), quarterly test, and Conditional Access exclusions for every single policy. The plan treats it as a checkbox; it is the whole foundation.
2. PIM/IaC sequencing is wrong. The LLM phases as: Audit → Safety Net → PIM → Codification. The safer order is: Audit → Break-glass verify → Tidy in portal → Codify → PIM on top of codified state. Reason: if you enforce PIM before codification, your IaC service principal still needs privilege to operate, you create a chicken-and-egg, and you have no codified record of the role model you are about to PIM-ify.
3. Audit & Tidy is presented as a phase, not its own project. Tidying is the unbounded part—most teams discover _weeks_ of accumulated cruft. Conflating it with codification means codification never starts cleanly.

### Content Gaps

1. No engagement with your stack. No mention of Terragrunt patterns for Entra modules, Terraform Cloud workspace scoping for IAM resources, the recent SIC-001/OAuth issue (relevant—TF Cloud's identity to Entra is the same class of problem), or your multi-customer tenant topology.
2. No CI/CD identity bootstrap discussion (see §2D). Asking "how does the pipeline authenticate without being a massive security risk itself?" is correct—but it doesn't answer it. The modern answer is workload identity federation, which deserves explicit naming.
3. "Eradicate standing Global Admin" overstates correctly. You always need ≥2 standing break-glass Global Admins. The principle should be _"no standing Global Admin for humans doing their day job; break-glass excepted, monitored, and tested."_
4. No mention of report-only mode for Conditional Access. Every CA change should land in report-only for ≥7 days, sign-in logs analysed, then promoted to enforce. Skipping this is how tenants lock everyone out at 2am.
5. No mention of the "What If" tool, named locations, authentication strengths, or PIM-for-Groups. PIM-for-Groups in particular is the modern way to handle just-in-time access for security groups—which is often the actual unit of access in customer tenants.
6. No discussion of import strategy. Importing existing Entra objects into Terraform is the painful part. The plan needs explicit guidance: enumerate, decide manage/ignore per object, write HCL to match exactly, import, verify zero diff. This is days of work per dozen objects, not minutes.
7. No mention of naming conventions as a prerequisite. Before codification: CA policy names, group names, app reg names, tags. If naming isn't standardised first, the codebase will calcify the mess.
8. No app registration secret/credential audit. A typical neglected tenant has dozens of app reg client secrets at various stages of expiry, with no clear owner. This is its own mini-project hiding in the audit.
9. No mention of cross-tenant access settings. For Fitfile's multi-customer model, B2B configuration with each customer tenant is significant surface area.
10. Risks section is bland. The single worst risk—tenant-wide lockout from a bad CA policy merge—isn't sharply named. It deserves a sentence in _every_ PR description for the rest of the project.
11. Asks the tool question back to you. It should be answered as part of the scoping conversation (see §2F).

---

## 4. Over-Advice (Things You Didn't Ask About)

### 4.1 Break-glass Deserves Its Own Runbook

Minimum contents:

- 2× cloud-only accounts, no MFA _via_ a federated provider (use phishing-resistant FIDO2 keys stored in two physical safes)
- Excluded from every Conditional Access policy _individually and explicitly_ (not via a group—groups can be edited or deleted)
- Passwords in a physical safe, not a password manager that depends on the same tenant
- Sign-in alerts via Log Analytics → email/SMS to ≥2 humans
- Quarterly test, calendared, with a documented procedure
- Used break-glass triggers an automatic incident review

If you do nothing else from this whole response, do this first.

### 4.2 Get a sandbox/test Tenant before You Start

Microsoft offers free dev tenants via the Microsoft 365 Developer Program (or you can spin one up). Every CA policy change, every PIM setting change, every import flow gets tested there first. Without this, you are testing in production against your own livelihood.

### 4.3 Tidy before You Codify

The single biggest mistake in Entra IaC migrations: importing the mess. Importing 47 conflicting Conditional Access policies into Terraform doesn't fix them—it just makes them harder to fix because now changes are PR-mediated. Rules:

- Stale guests (no sign-in 90 days): delete
- Empty groups: delete
- Groups with one member: review purpose
- App registrations with no recent sign-ins and no owner: review
- Overlapping CA policies: consolidate
- Then codify what's left.

### 4.4 CA Policies Need a Ring Deployment Model

Treat CA changes like kernel patches. Suggested rings:

- Ring 0: sandbox tenant
- Ring 1: report-only in production, monitored for 7 days
- Ring 2: enforce against a pilot group (you + 2 trusted engineers)
- Ring 3: enforce against platform team
- Ring 4: enforce tenant-wide

Build this into the IaC module from day one—make ring promotion a code change, not a portal change.

### 4.5 Workload Identity Federation, not Client Secrets

For the Terraform Cloud → Entra identity, use OIDC federation. TF Cloud signs a short-lived token, Entra trusts it, no secret to rotate, no secret to leak. This is the 2026 default; introducing this project is the moment to do it.

### 4.6 The PIM Model is a Design Exercise, not a Configuration Exercise

Before flipping anyone to PIM, design the role catalogue on paper:

- Which Entra roles are eligible vs. active?
- Maximum activation duration per role (15 min for Global Admin, 8h for Reader, etc.)?
- Approval required (and from whom)?
- MFA on activation?
- Justification required?
- Ticket/change reference required?

Then implement. The cleanup of "who has what today" feeds this design.

### 4.7 PIM Solo-approver Problem

If you're the only platform engineer, you cannot approve your own activations. Options:

- Self-approval permitted for non-Global-Admin roles, with after-the-fact review
- Two-person rule with a senior engineer or manager
- Break-glass-style covered by an after-the-fact attestation
- An external approver (managed service partner, security lead)

Decide this in design, not at first activation.

### 4.8 Audit Logs First, Policy Changes Second

Before any CA policy change, query 90 days of sign-in logs to predict impact:

- How many users would have been blocked?
- From which locations / device states / risk levels?
- Are there service-account sign-ins hiding in interactive flows that would break?

Sentinel KQL in Log Analytics. If you don't have 90 days of sign-in log retention, fixing that is task one.

### 4.9 Naming Conventions Are the Cheapest Leverage

Lock these in before writing any Terraform:

- CA policies: `CA{nnn}-{audience}-{control}-{state}` e.g. `CA001-AllUsers-RequireMFA-Enforce`
- Security groups: `sg-{purpose}-{scope}` e.g. `sg-pim-globaladmins-eligible`
- App registrations: `app-{owner}-{purpose}-{env}`
- Tags / extension attributes for ownership

The cost of doing this on day one is zero. The cost of doing it on day 200 is rewriting every reference.

### 4.10 Compliance Lens

Given Fitfile's NHS context (MKUH), DSP Toolkit and ISO27001 controls likely apply. This project is _catnip for auditors_—they love IaC-managed IAM with PIM. Capture this:

- Map each control area to an artefact this project produces
- Save the auditor a discovery exercise; you save yourself a re-explanation in six months

### 4.11 Watch for the "while I'm in here" Trap

Entra is a coral reef of barnacles. Once you're auditing, you'll find:

- An old guest account
- An app reg with no owner
- A Teams app integration nobody remembers
- A SCIM connector to an HR system that's been off for 2 years

Make a backlog. Do not detour. Each barnacle is its own ticket; the audit's job is to surface them, not fix them.

### 4.12 The Change Muscle is Different here

Most platform changes can be rolled forward with another deploy. CA policies and Global Admin assignments cannot—by the time you realise a CA policy is bad, you may have lost the ability to sign in to fix it. The cultural shift is: slower PRs, smaller diffs, mandatory plan review, never apply on a Friday.

---

## 5. Your Next Physical Action

This project has a different first action than the previous two. Before you write `scoping-v0.md`, you must verify break-glass.

15-minute task—pick the appropriate path:

### If You Know Break-glass Exists and Was Tested Recently

Open your notes app, create `entra-overhaul/scoping-v0.md`, and answer three questions:

1. Which tenant am I scoping first—Fitfile home (A1), one customer tenant (A2), or the cross-tenant topology (A4)?
2. What is the single primary driver—audit, drift, Zero Trust, compliance, or incident response?
3. Does the test/sandbox tenant exist today, or do I need to acquire one first?

### If Break-glass is Uncertain, Untested, or Unknown

Stop. Create `entra-overhaul/break-glass-status.md` and answer:

1. Do break-glass accounts exist, and where are their credentials physically stored?
2. When were they last tested with a successful sign-in?
3. Are they excluded from _every_ Conditional Access policy individually?

If any answer is "no" or "I don't know", break-glass verification is the entire project this week. Scoping waits. Everything waits.

Don't fill in the trigger list yet. Don't write Terraform. Don't even open the Azure portal beyond what these three questions require. Just the scoping doc, or the break-glass doc—whichever applies.

Once one of those two files exists with three answers, you have a project. Then—and only then—run the trigger list (§2), then Phase 1 of Natural Planning.

---

You

Dive deeper into the break glass Identity. What is the complete plan? Here is the draft Here is a plan for crafting a best-in-class emergency access (break-glass) account in Microsoft Entra ID, structured from the provided sources: Phase 1: Account Configuration * It is recommended that you create two or more emergency access accounts. * These must be cloud-only accounts utilising the *.onmicrosoft.com domain. * The accounts must not be federated or synchronised from an on-premises environment. * Ensure the accounts have no dependency on external identity providers. * The Global Administrator role should be active on the account without requiring Privileged Identity Management (PIM) activation. Phase 2: Policy Exclusions * Break-glass accounts should not be included in any Conditional Access policies. * You might consider creating an "emergency" management group that is above or completely exempt from your other standard policies. Phase 3: Securing Credentials * You must store the account credentials safely and securely. * Store the credentials using two separate methods. * Implement two separate authentication methods, ensuring you do not rely solely on one method, such as using the Microsoft Authenticator app for both accounts. Phase 4: Monitoring and Alerting * You must actively monitor the sign-in and audit logs for these emergency accounts. * Set up an Azure Monitor alert that is designed to fire immediately when the account logs in. Phase 5: Validation and Maintenance * It is essential to test your emergency accounts regularly to validate them. * A general rule of thumb is to check these accounts on a quarterly basis. * Document the process properly so that when an emergency arises, you are completely ready rather than trying to figure things out.

---

Claude

[[Break-Glass Identity The Complete Plan]]
