---
created: 2026-05-15T08:22:11+00:00
modified: 2026-05-15T08:23:00+00:00
title: Restructuring Entra ID—Scoping, IaC & PIM
---

## 1\. The Real Problem (Reframe)

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

## 2\. Scoping Trigger List

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

> _"The audit & tidy sub-project is finished when \_\_\_ has been documented, \_\_\_ has been deleted/remediated in the portal, and the tenant is in a state where importing it into Terraform would yield a meaningful and maintainable codebase."_

If you can complete that sentence, you have a project.

---

## 3\. Critique of the LLM Response

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

## 4\. Over-Advice (Things You Didn't Ask About)

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

## 5\. Your Next Physical Action

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

Dive deeper into the break glass Identity. What is the complete plan? Here is the draft Here is a plan for crafting a best-in-class emergency access (break-glass) account in Microsoft Entra ID, structured from the provided sources: \*\*Phase 1: Account Configuration\*\* \* It is recommended that you create two or more emergency access accounts. \* These must be cloud-only accounts utilising the \*.onmicrosoft.com domain. \* The accounts must not be federated or synchronised from an on-premises environment. \* Ensure the accounts have no dependency on external identity providers. \* The Global Administrator role should be active on the account without requiring Privileged Identity Management (PIM) activation. \*\*Phase 2: Policy Exclusions\*\* \* Break-glass accounts should not be included in any Conditional Access policies. \* You might consider creating an "emergency" management group that is above or completely exempt from your other standard policies. \*\*Phase 3: Securing Credentials\*\* \* You must store the account credentials safely and securely. \* Store the credentials using two separate methods. \* Implement two separate authentication methods, ensuring you do not rely solely on one method, such as using the Microsoft Authenticator app for both accounts. \*\*Phase 4: Monitoring and Alerting\*\* \* You must actively monitor the sign-in and audit logs for these emergency accounts. \* Set up an Azure Monitor alert that is designed to fire immediately when the account logs in. \*\*Phase 5: Validation and Maintenance\*\* \* It is essential to test your emergency accounts regularly to validate them. \* A general rule of thumb is to check these accounts on a quarterly basis. \* Document the process properly so that when an emergency arises, you are completely ready rather than trying to figure things out.

---

Claude

## Break-Glass Identity: The Complete Plan

### 1\. Critique of the Draft

The draft is structurally sound and hits the canonical points. It is, however, insufficient as an implementation plan—it reads as a summary of Microsoft's documentation rather than a buildable specification. Specific gaps:

1. Account count rationale missing. Why 2? Why not 3 or 5? (Two is the minimum for redundancy; more is more attack surface. The trade-off should be explicit.)
2. No `.onmicrosoft.com` _why_. It's not arbitrary—custom domains can lapse, DNS can fail, federation can break. The initial tenant domain is the only identifier that cannot be lost.
3. No licence guidance. Break-glass accounts must have no licence assigned—no Exchange mailbox, no Teams identity, nothing that creates attack surface or recovery dependencies on M365 services.
4. "Diverse auth methods" is too vague. The 2026 standard is phishing-resistant FIDO2 keys (or platform passkeys), with explicit prohibition on SMS, voice, and Authenticator-push as primary factors.
5. CA exclusion mechanism unspecified. Direct user assignment is mandatory. Group-based exclusion is dangerous (groups can be edited, emptied, or deleted). The draft's "emergency management group" idea is actively wrong—Azure Management Groups are a different construct entirely, and even security-group-based CA exclusion is anti-pattern.
6. Monitoring is too narrow. Sign-in alerts are necessary but not sufficient. Audit alerts on the _accounts themselves_ (MFA method changes, role changes, password resets, exclusion removals) matter equally.
7. Alert channel dependency unaddressed. If Entra is broken, alerts via M365 email are also broken. The runbook must use out-of-band channels.
8. No runbook contents. "Document the process properly" is a wish, not a specification.
9. No post-use procedure. What happens _after_ the glass is broken? Mandatory rotation, key replacement, incident review.
10. No IaC boundary discussion. Break-glass accounts must be explicitly out of scope for the new Entra IaC project—they are managed manually, by deliberate exception.
11. No succession/people plan. Two accounts in two safes is half the answer; _who_ has access to which safe, and what happens when they leave?

---

### 2\. Design Principles

Five principles. If a design decision violates one, redesign.

1. No dependencies on the thing being broken. Not on Entra federation, not on M365 mail, not on a password manager that uses SSO, not on a phone number the IT team controls.
2. Direct, explicit, individual. Every CA exclusion is direct user assignment. Every privilege is permanent and active. Nothing inferred from group membership.
3. Phishing-resistant only. FIDO2 hardware keys or platform passkeys. No SMS, no voice, no push-only Authenticator.
4. Use is auditable, alerting, and triggers process. A break-glass sign-in is _never_ business-as-usual. It always fires alerts, always triggers post-use rotation, always produces an incident record.
5. Two-person practical redundancy. Any single human's loss (resignation, accident, bus) must not lock the tenant.

---

### 3\. Complete Specification

#### 3.1 Account Identity

| Attribute | Specification |
| --- | --- |
| Count | 2 minimum. A third in a separate geography is justified for very high-stakes tenants; for Fitfile's home tenant, 2 is correct. |
| Domain | `*.onmicrosoft.com` (initial tenant domain). Never a custom domain. |
| UPN | Deliberately uninformative. Suggested: `ea1-{8 random chars}@<tenant>.onmicrosoft.com`. Avoid `breakglass@`, `emergency@`, `globaladmin@`—these advertise the target in logs. |
| Display name | Same principle. Use opaque names. |
| Source | Cloud-only. Not synced from on-prem AD, not federated. |
| Licence | None. No M365, no Exchange, no Teams, no Power Platform. |
| Mailbox | Disabled (consequence of no licence). |
| Phone number | None registered. |
| Alternate email | None registered. |
| Usage location | Set (required by Entra), but no licence assigned. |

#### 3.2 Authentication

| Factor | Specification |
| --- | --- |
| Password | ≥20 characters, generated randomly, never reused, never typed into a password manager that depends on the same tenant. Printed on paper, stored physically. |
| Primary MFA | FIDO2 security key (e.g. YubiKey 5 series or equivalent). |
| Backup MFA | A second FIDO2 key, stored in a separate physical location. Ideally different vendor/model to avoid single-supply-chain compromise. |
| Prohibited | SMS, voice call, Authenticator push (alone), email OTP, security questions. |
| Authentication strength | Each break-glass account requires its own phishing-resistant authentication strength if you use that feature elsewhere—and be sure the policy applies to break-glass without breaking it. |

#### 3.3 Authorisation

| Aspect | Specification |
| --- | --- |
| Role | Global Administrator, permanently and actively assigned (not PIM-eligible). |
| Why not PIM-eligible? | PIM activation requires sign-in to the portal and a working JIT pipeline. In a break-glass scenario, that may be the broken thing. |
| Other roles | None. Break-glass holds only what's needed for emergency recovery. |
| Group membership | None. Membership in any group creates indirection that can be tampered with. |

#### 3.4 Conditional Access Exclusion

| Aspect | Specification |
| --- | --- |
| Mechanism | Direct user assignment in the _Users → Exclude_ tab of every policy. Never via group. |
| Coverage | Every CA policy, with no exceptions. Including: location-based blocks, device compliance, risk-based, legacy auth block, session controls, sign-in frequency, MFA. |
| Verification | Automated check (Graph API: `GET /identity/conditionalAccess/policies`) confirms break-glass UPNs appear in `conditions.users.excludeUsers` for every policy. Run in CI. |
| PR gate | New CA policy PRs cannot merge without break-glass exclusion present. |
| Documentation | Every CA policy description field includes: _"Break-glass accounts ea1-… and ea2-… are excluded by direct assignment."_ |

#### 3.5 Credential Storage

| Element | Storage |
| --- | --- |
| Account 1 password | Printed, sealed in tamper-evident envelope, in physical safe Site A. |
| Account 1 FIDO2 key (primary) | In safe Site A with the password. |
| Account 1 FIDO2 key (backup) | In safe Site B. |
| Account 2 password | Printed, sealed in tamper-evident envelope, in physical safe Site B. |
| Account 2 FIDO2 key (primary) | In safe Site B with the password. |
| Account 2 FIDO2 key (backup) | In safe Site A. |
| Tenant ID, UPNs, runbook (printed) | Both safes. |

Result: any single site's loss leaves a complete working account at the other.

#### 3.6 People & Access

| Role | Specification |
| --- | --- |
| Safe-holders | ≥2 named individuals per safe, with clear succession on departure. |
| Suggested roles | CTO/Engineering Director + Principal Platform Engineer (you) for Site A; Security Lead + secondary platform engineer for Site B. |
| Departure procedure | On any safe-holder's departure: rotate the password they had access to, replace the FIDO2 key, re-test, document. |
| Authorisation to use | Documented in runbook. In a true emergency, no approval required—but use triggers mandatory post-event review. |

#### 3.7 Monitoring & Alerting

Configure alerts in Microsoft Sentinel or Log Analytics. Sources: `SigninLogs`, `AuditLogs`.

| Event | Severity | Action |
| --- | --- | --- |
| Successful interactive sign-in by break-glass | Critical | Page on-call + email security team + SMS to ≥2 owners |
| Failed sign-in (any) by break-glass | High | Investigate immediately—possible attack |
| MFA method added/removed | Critical | Treat as compromise until disproven |
| Password reset | Critical | Same |
| Role assignment change touching break-glass | Critical | Same |
| CA policy modified to remove break-glass exclusion | Critical | Same |
| Account disabled or deleted | Critical | Same |
| Account excluded from a new CA policy | Informational | Logged, reviewed weekly |

Alert channels must not depend on Entra. Recommended pipeline: Log Analytics → Logic App / Azure Function → external paging service (PagerDuty, Opsgenie) with a non-Entra-federated account, plus SMS via a third party (Twilio), plus personal email _not_ hosted on the same M365 tenant.

Example KQL for sign-in alert:

```
SigninLogs
| where UserPrincipalName in~ ("[email protected]", "[email protected]")
| where ResultType == 0  // successful
| project TimeGenerated, UserPrincipalName, AppDisplayName, IPAddress, Location, ClientAppUsed, DeviceDetail
```

Log retention: minimum 1 year for these UPNs, via Log Analytics workspace with appropriate retention setting.

#### 3.8 Runbook Contents

The printed runbook in each safe must include:

1. Tenant identifiers—tenant ID, initial domain, UPNs, IDs.
2. Trigger conditions—what qualifies as an emergency justifying use.
3. Authorisation—who can authorise, or "no approval required if \[condition\]".
4. Step-by-step sign-in procedure—including clean browser, private window, expected MFA prompts, what to do if MFA prompt is unexpected (stop, investigate).
5. Scenario playbooks—at minimum:
	- "Locked out by a bad Conditional Access deployment"
		- "Sole Global Admin departed without handover"
		- "Suspected admin account compromise—need to revoke sessions"
		- "Tenant federation broken"
6. What NOT to do—don't use break-glass for routine admin, don't enable mailbox to "just check something", don't leave the session open.
7. Mandatory post-use checklist—rotate password, re-enrol FIDO2, file incident, schedule review.
8. Out-of-band contact list—names + personal numbers/emails of safe-holders and security lead.
9. Independent copy of this runbook—referenced URL or location that does _not_ require Entra to access.

#### 3.9 Post-Use Procedure

After any break-glass sign-in—including a routine test:

1. Rotate the password (generate new, print, reseal, return to safe).
2. Audit MFA methods on the account; reset to known-good state.
3. Review the sign-in and audit logs for the session; capture evidence.
4. File an incident record with timestamp, user, reason, actions taken.
5. Within 5 working days: incident review meeting, lessons captured.
6. If post-use is from a _real_ emergency (not a test), consider replacing the FIDO2 key that was used.

#### 3.10 IaC Boundary

This is the connection back to your Entra IaC project (the previous conversation):

- Break-glass account _objects_ are explicitly out of scope for Terraform management. Manage manually. Do not import into state.
- Break-glass account _UPNs and object IDs_ are inputs to the Terraform that manages CA policies. Stored as variables / data sources, referenced in every policy's `excludeUsers`.
- CI validation (Graph API check) verifies all CA policies in code include the break-glass exclusions, before plan/apply.
- The CI/CD service principal that runs Terraform must not have rights to modify break-glass accounts or their CA exclusions. Use directory role scoping or custom roles to enforce.

#### 3.11 Testing Cadence

| Activity | Frequency |
| --- | --- |
| Sign-in test (both accounts, full MFA, role exercise, sign-out) | Quarterly—calendared and assigned |
| Alert pipeline test (trigger known event, confirm page received) | Quarterly, paired with sign-in test |
| Runbook walkthrough by someone who didn't write it | Annually |
| CA exclusion audit (automated CI check should run on every PR, plus standalone monthly run) | Monthly |
| Safe-holder review (departures, succession) | Quarterly |
| Full DR exercise (simulate locked-out scenario) | Annually |

---

### 4\. Pitfalls and Over-Advice

#### 4.1 The Password Manager Trap

If your password manager (1Password, Bitwarden, etc.) is configured with Entra SSO, storing break-glass credentials in it is catastrophic—the credential needed to recover access is locked behind the same system that's broken. This is a real and frequent failure mode. Paper, in safes, full stop.

#### 4.2 The "we'll Test it later" Trap

The single most common failure: accounts created, never tested again. Untested break-glass is _worse_ than no break-glass—it creates false confidence. Calendar the quarterly tests now, before anything else.

#### 4.3 The "shared phone" Trap

If MFA uses a phone number, whose phone is it? The IT team's? Then it's a single point of failure on a person and a device. Phone-based MFA for break-glass is not acceptable; this is why FIDO2 keys are the answer.

#### 4.4 The CA Exclusion Drift Trap

You exclude the accounts today. Six months later, a hurried PR adds a new policy without the exclusion. You don't notice until an actual emergency. The CI gate is non-negotiable—write the Graph API check before declaring the project done.

#### 4.5 The "let's Give it a Licence to Monitor it" Trap

Tempting: assign a licence so the account has a mailbox you can monitor. Don't. Monitoring goes via Log Analytics on the _sign-in and audit logs_, not via the account's own mailbox. A licensed account has more attack surface, more failure modes, and more standing dependencies.

#### 4.6 The "register Security info" Trap

A user with Global Admin rights can self-register new MFA methods on themselves. If an attacker reaches a break-glass session, they can add their own FIDO2 key as a method. The audit alert on "MFA method added" catches this _after_ the fact—useful, but consider also Conditional Access User Actions ("Register security information") policies… with the break-glass accounts excluded, because they _do_ need to register methods initially. Tension to think through; not a clean answer.

#### 4.7 The "global Admin is enough" Assumption

Global Administrator role does not automatically grant access to Azure subscriptions (RBAC is separate). For full recovery, the break-glass accounts may also need standing User Access Administrator at the root management group level—and toggling the "Elevate access" flag in Entra. Decide and document.

#### 4.8 The Forgotten Service Principals

This plan covers human break-glass. What about service principals running critical infra (the Terraform Cloud SP, the ArgoCD SP)? Separate problem, often forgotten—but if those credentials lapse and the rotation pipeline is broken, you have a similar lockout. Out of scope for this plan, but on the register.

#### 4.9 The Microsoft 365 Backup Angle

Break-glass restores _access_. It does not restore _configuration_ if a bad change deleted critical objects. Complementary control: tenant configuration backup (e.g. via `Microsoft.Graph` PowerShell exports committed to git nightly, or paid tools like Veeam for M365). Out of scope here, but should be a follow-on project.

#### 4.10 ADHD-specific Note

This is the project type that ADHD brains under-deliver on—high-context, low-novelty, no external praise, and 90% of the work is invisible if it succeeds. Counter-measures: make the next action absurdly small (see §5), and book the quarterly test in your calendar _now_, before you've finished the project, so that even partial completion accrues maintenance habit.

---

### 5\. Your Next Physical Action

This project decomposes into clean sub-tasks. Today's task is 15 minutes, no more.

Open your notes app. Create one file: `break-glass/plan-v0.md`.

Answer these three questions, one or two sentences each:

1. Who are the two safe-holders for each safe? Name two people for Site A, two for Site B. (Names, not roles—people leave roles.)
2. Where are Site A and Site B physically? (Office + home? Two office locations? Office + Director's home?)
3. What is the budget approval path for two pairs of FIDO2 keys (≈£200) and any safes not already in place?

That's it. Don't buy keys yet. Don't create accounts yet. Don't open the Entra portal.

Once `plan-v0.md` has three answers, the break-glass project is born with people, places, and procurement identified. From there the next session can:

1. Procure FIDO2 keys (1 day).
2. Procure / locate safes (1 day).
3. Create the two accounts in a maintenance window (≈1 hour).
4. Configure CA exclusions (≈30 min).
5. Configure monitoring and alerts (≈half day).
6. Run the first test (≈1 hour).
7. Hand over to maintenance cadence.

But all of that is downstream of the three answers above. Today: those three answers.

---

[[Operating Protocol for High-Friction Engineering Work]]