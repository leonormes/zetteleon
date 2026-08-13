---
created: 2026-05-15T12:34:55+00:00
modified: 2026-08-13T10:53:18+00:00
permalink: llmeon/30-library/200-projects/break-glass-identity-the-complete-plan
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
title: Break-Glass Identity The Complete Plan
type: null
---

## 1. Critique of the Draft

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

## 2. Design Principles

Five principles. If a design decision violates one, redesign.

1. No dependencies on the thing being broken. Not on Entra federation, not on M365 mail, not on a password manager that uses SSO, not on a phone number the IT team controls.
2. Direct, explicit, individual. Every CA exclusion is direct user assignment. Every privilege is permanent and active. Nothing inferred from group membership.
3. Phishing-resistant only. FIDO2 hardware keys or platform passkeys. No SMS, no voice, no push-only Authenticator.
4. Use is auditable, alerting, and triggers process. A break-glass sign-in is _never_ business-as-usual. It always fires alerts, always triggers post-use rotation, always produces an incident record.
5. Two-person practical redundancy. Any single human's loss (resignation, accident, bus) must not lock the tenant.

---

## 3. Complete Specification

### 3.1 Account Identity

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

### 3.2 Authentication

| Factor | Specification |
| --- | --- |
| Password | ≥20 characters, generated randomly, never reused, never typed into a password manager that depends on the same tenant. Printed on paper, stored physically. |
| Primary MFA | FIDO2 security key (e.g. YubiKey 5 series or equivalent). |
| Backup MFA | A second FIDO2 key, stored in a separate physical location. Ideally different vendor/model to avoid single-supply-chain compromise. |
| Prohibited | SMS, voice call, Authenticator push (alone), email OTP, security questions. |
| Authentication strength | Each break-glass account requires its own phishing-resistant authentication strength if you use that feature elsewhere—and be sure the policy applies to break-glass without breaking it. |

### 3.3 Authorisation

| Aspect | Specification |
| --- | --- |
| Role | Global Administrator, permanently and actively assigned (not PIM-eligible). |
| Why not PIM-eligible? | PIM activation requires sign-in to the portal and a working JIT pipeline. In a break-glass scenario, that may be the broken thing. |
| Other roles | None. Break-glass holds only what's needed for emergency recovery. |
| Group membership | None. Membership in any group creates indirection that can be tampered with. |

### 3.4 Conditional Access Exclusion

| Aspect | Specification |
| --- | --- |
| Mechanism | Direct user assignment in the _Users → Exclude_ tab of every policy. Never via group. |
| Coverage | Every CA policy, with no exceptions. Including: location-based blocks, device compliance, risk-based, legacy auth block, session controls, sign-in frequency, MFA. |
| Verification | Automated check (Graph API: `GET /identity/conditionalAccess/policies`) confirms break-glass UPNs appear in `conditions.users.excludeUsers` for every policy. Run in CI. |
| PR gate | New CA policy PRs cannot merge without break-glass exclusion present. |
| Documentation | Every CA policy description field includes: _"Break-glass accounts ea1-… and ea2-… are excluded by direct assignment."_ |

### 3.5 Credential Storage

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

### 3.6 People & Access

| Role | Specification |
| --- | --- |
| Safe-holders | ≥2 named individuals per safe, with clear succession on departure. |
| Suggested roles | CTO/Engineering Director + Principal Platform Engineer (you) for Site A; Security Lead + secondary platform engineer for Site B. |
| Departure procedure | On any safe-holder's departure: rotate the password they had access to, replace the FIDO2 key, re-test, document. |
| Authorisation to use | Documented in runbook. In a true emergency, no approval required—but use triggers mandatory post-event review. |

### 3.7 Monitoring & Alerting

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

### 3.8 Runbook Contents

The printed runbook in each safe must include:

1. Tenant identifiers—tenant ID, initial domain, UPNs, IDs.
2. Trigger conditions—what qualifies as an emergency justifying use.
3. Authorisation—who can authorise, or "no approval required if [condition]".
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

### 3.9 Post-Use Procedure

After any break-glass sign-in—including a routine test:

1. Rotate the password (generate new, print, reseal, return to safe).
2. Audit MFA methods on the account; reset to known-good state.
3. Review the sign-in and audit logs for the session; capture evidence.
4. File an incident record with timestamp, user, reason, actions taken.
5. Within 5 working days: incident review meeting, lessons captured.
6. If post-use is from a _real_ emergency (not a test), consider replacing the FIDO2 key that was used.

### 3.10 IaC Boundary

This is the connection back to your Entra IaC project (the previous conversation):

- Break-glass account _objects_ are explicitly out of scope for Terraform management. Manage manually. Do not import into state.
- Break-glass account _UPNs and object IDs_ are inputs to the Terraform that manages CA policies. Stored as variables / data sources, referenced in every policy's `excludeUsers`.
- CI validation (Graph API check) verifies all CA policies in code include the break-glass exclusions, before plan/apply.
- The CI/CD service principal that runs Terraform must not have rights to modify break-glass accounts or their CA exclusions. Use directory role scoping or custom roles to enforce.

### 3.11 Testing Cadence

| Activity | Frequency |
| --- | --- |
| Sign-in test (both accounts, full MFA, role exercise, sign-out) | Quarterly—calendared and assigned |
| Alert pipeline test (trigger known event, confirm page received) | Quarterly, paired with sign-in test |
| Runbook walkthrough by someone who didn't write it | Annually |
| CA exclusion audit (automated CI check should run on every PR, plus standalone monthly run) | Monthly |
| Safe-holder review (departures, succession) | Quarterly |
| Full DR exercise (simulate locked-out scenario) | Annually |

---

## 4. Pitfalls and Over-Advice

### 4.1 The Password Manager Trap

If your password manager (1Password, Bitwarden, etc.) is configured with Entra SSO, storing break-glass credentials in it is catastrophic—the credential needed to recover access is locked behind the same system that's broken. This is a real and frequent failure mode. Paper, in safes, full stop.

### 4.2 The "We'll Test it lAter" Trap

The single most common failure: accounts created, never tested again. Untested break-glass is _worse_ than no break-glass—it creates false confidence. Calendar the quarterly tests now, before anything else.

### 4.3 The "Shared pHone" Trap

If MFA uses a phone number, whose phone is it? The IT team's? Then it's a single point of failure on a person and a device. Phone-based MFA for break-glass is not acceptable; this is why FIDO2 keys are the answer.

### 4.4 The CA Exclusion Drift Trap

You exclude the accounts today. Six months later, a hurried PR adds a new policy without the exclusion. You don't notice until an actual emergency. The CI gate is non-negotiable—write the Graph API check before declaring the project done.

### 4.5 The "Let's Give it a Licence to Monitor iT" Trap

Tempting: assign a licence so the account has a mailbox you can monitor. Don't. Monitoring goes via Log Analytics on the _sign-in and audit logs_, not via the account's own mailbox. A licensed account has more attack surface, more failure modes, and more standing dependencies.

### 4.6 The "Register Security iNfo" Trap

A user with Global Admin rights can self-register new MFA methods on themselves. If an attacker reaches a break-glass session, they can add their own FIDO2 key as a method. The audit alert on "MFA method added" catches this _after_ the fact—useful, but consider also Conditional Access User Actions ("Register security information") policies… with the break-glass accounts excluded, because they _do_ need to register methods initially. Tension to think through; not a clean answer.

### 4.7 The "Global Admin is eNough" Assumption

Global Administrator role does not automatically grant access to Azure subscriptions (RBAC is separate). For full recovery, the break-glass accounts may also need standing User Access Administrator at the root management group level—and toggling the "Elevate access" flag in Entra. Decide and document.

### 4.8 The Forgotten Service Principals

This plan covers human break-glass. What about service principals running critical infra (the Terraform Cloud SP, the ArgoCD SP)? Separate problem, often forgotten—but if those credentials lapse and the rotation pipeline is broken, you have a similar lockout. Out of scope for this plan, but on the register.

### 4.9 The Microsoft 365 Backup Angle

Break-glass restores _access_. It does not restore _configuration_ if a bad change deleted critical objects. Complementary control: tenant configuration backup (e.g. via `Microsoft.Graph` PowerShell exports committed to git nightly, or paid tools like Veeam for M365). Out of scope here, but should be a follow-on project.

### 4.10 ADHD-specific Note

This is the project type that ADHD brains under-deliver on—high-context, low-novelty, no external praise, and 90% of the work is invisible if it succeeds. Counter-measures: make the next action absurdly small (see §5), and book the quarterly test in your calendar _now_, before you've finished the project, so that even partial completion accrues maintenance habit.

---

## 5. Your Next Physical Action

This project decomposes into clean sub-tasks. Today's task is 15 minutes, no more. Open your notes app. Create one file: `break-glass/plan-v0.md`.

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

[[Restructuring Entra ID—Scoping, IaC & PIM]]
