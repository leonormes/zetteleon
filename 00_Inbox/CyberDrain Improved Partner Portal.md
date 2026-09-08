---
created: 2026-09-08T07:01:49+00:00
modified: 2026-09-08T07:30:35+00:00
permalink: llmeon/00-inbox/untitled
title: Untitled
type: note
---

CIPP is CyberDrain Improved Partner Portal—a well-known open-source multi-tenant M365/Entra management tool built for MSPs, built by Kelvin Tegelaar/CyberDrain. It's self-hosted (typically as an Azure Static Web App + Function App) and it manages _client_ tenants (like yours) via a "SAM" app registration—Secure Application Model—that it needs pushed into every tenant it manages, with broad Graph permissions. That's exactly the shape of what's in your tenant (`CIPP-SAM`, ~120 permissions).

Let me pull the tenant-specific facts you need for the ticket rather than just the general background.

Good—this needed more digging than the first pass caught. Here's what I found, plus a real problem: there isn't one CIPP-SAM, there are five app registrations under that pattern, and two of them are live simultaneously.

This needed real digging—the original finding undersold it. Here's the full picture, then I'll flag what changes.

## What CIPP is

CyberDrain Improved Partner Portal—an open-source, free MSP tool (built by Kelvin Tegelaar / CyberDrain) for managing Microsoft 365 and Entra across multiple client tenants from one console: users, mailboxes, Conditional Access, Defender, Teams, SharePoint, licensing, the lot. It works by installing a "SAM" (Secure Application Model) app registration into each client tenant it manages—which is exactly the shape of what's in yours.

## Where it Actually is—and This is the Real Finding

It's not in your tenant at all. `CIPP-SAM` has no `application` object here—only `servicePrincipal` objects (i.e., consented Enterprise Apps). The actual app is registered in an external tenant, `53874a5a-5ada-45dd-b54a-1aae894aa581` (EU region)—that's the MSP's own Entra tenant, hosting their CIPP instance. One of the reply URLs on the registration gives away exactly where:

```
https://happy-island-07e778303.2.azurestaticapps.net/api/ExecSAMSetup
```

That's their CIPP frontend, an Azure Static Web App, and `ExecSAMSetup` is CIPP's own built-in setup wizard endpoint—this confirms it beyond doubt.

But there isn't one CIPP-SAM—there are five, and I'd missed this the first time:

|App ID|Created|App-role assignments|Status|
|---|---|---|---|
|`fd7008c7-…`|2024-06-19|81 (Graph, Exchange, RMS, SharePoint, Azure AD, Defender ATP)|live|
|`576ecbcf-…`|2023-10-16|49 (Graph, Azure AD, Exchange, Defender ATP)|live|
|`ccb9e482-…`|2023-02-01|0|dead—no permissions|
|`09a5a18b-…`|2023-02-16|0|dead—no permissions|
|`4b83d41e-…` "Tech Ahoy Lifecycle App"|2026-08-16 (3 weeks before this audit)|0 (only basic `openid profile email`)|new, unprivileged so far|

So the original ticket's "duplicated grant" framing was wrong—it's not one over-granted app, it's two separate, fully live, GA-equivalent entry points into your tenant simultaneously, most likely from CIPP being reinstalled or upgraded at some point without the old registration being decommissioned. That's worse, not the same. I'll correct the ticket.

## Who's behind it

The name resolves: "Tech Ahoy" is a contractor/MSP already in your tenant, not a mystery vendor. Evidence:

- Four named accounts in `SharePoint - Tech Ahoy`: Mike Hill, Scott Bevan, Luke Scammell, Jono Whitewick (`ta_*@fitfileltd.onmicrosoft.com`)
- A disabled shared `techahoy@fitfileltd.onmicrosoft.com` account
- Two of _your own_ prior tickets: [FTFL-542](https://fitfile.atlassian.net/browse/FTFL-542) "Remove Global Administrator from Tech Ahoy contractor account" (Done), and [FTFL-810](https://fitfile.atlassian.net/browse/FTFL-810) "Remove all Tech Ahoy Entra accounts"—assigned to you, closed as Abandoned on 2026-07-27.

That last one is the key thread to pull. You were removing Tech Ahoy's access and it got called off. That decision—whatever the reason—is almost certainly what FTFL-1032 needs to resolve now, and the brand-new "Tech Ahoy Lifecycle App" from 3 weeks ago suggests the relationship isn't winding down, it's being extended.

## How to Investigate from here

1. Ask yourself/the team why FTFL-810 was abandoned—check its comments in Jira (I haven't read them; worth doing). That decision is the missing context.
2. Ask whoever owns the Tech Ahoy contract (commercial side—Robin/Philip) what Tech Ahoy is actually engaged for right now, and whether CIPP is how they deliver it.
3. Get the current CIPP-SAM permission set from Tech Ahoy directly rather than reverse-engineering it—ask them for their SAM manifest/permission list and compare it against the 130 role assignments actually granted here.
4. Decide the two dead SAM registrations and the new Lifecycle App now, separately from the main decision—the dead ones are safe to delete regardless of what you decide about the live ones; the Lifecycle App holds nothing privileged yet, so it's a "what is this for" question rather than an urgent one.

One caveat: I couldn't pull the directory audit log (consent-grant history—who approved which app, when) this session—it's returning `Authentication_RequestFromUnsupportedUserRole` now, whereas it worked yesterday. That's almost certainly because your Global Reader PIM activation from yesterday has expired. Reactivate it if you want that trail.

I'll post this as an evidence comment on [FTFL-1032](https://fitfile.atlassian.net/browse/FTFL-1032) now, since it materially corrects the ticket's premise—say if you'd rather I hold off.

Global Reader plus Application Administrator active now. Retrying the blocked queries.

That query just surfaced something important: CIPP-SAM's permissions were modified last night, hours after this audit began.

That resolves everything. Full detail on the two events from last night:

Actor: "Tech Ahoy Technician" (`b9116af0-c1ec-4770-ae95-89cf76d58a6d`), home tenant `Tech Ahoy` (`53874a5a-…`—the exact tenant that owns the CIPP-SAM app registration), from IP `4.159.58.164`. Not a guest object in your tenant—a cross-tenant admin-consent actor.

What they added, at 23:07:27 UTC yesterday, to the live 81-permission `CIPP-SAM` (`fd7008c7-…`):

- `ExchangeMessageTrace.Read.All` on Microsoft Graph—read mail-flow trace data (sender/recipient/subject/delivery status) tenant-wide, no per-mailbox scoping
- `User.ReadWrite.All` on the SharePoint Online resource specifically (a separate grant from Graph's own `User.ReadWrite.All`)—write access to user profile properties in SharePoint/OneDrive context

This isn't a dormant 2024 legacy grant. Tech Ahoy is actively administering your tenant through CIPP right now, and actively expanding what it can do, hours after this audit flagged it. That changes the urgency of FTFL-1032—this isn't "clean up an old thing when convenient," it's "a live vendor relationship with a growing permission footprint that needs a decision soon."

Posting the consolidated evidence to the ticket now.

That table flattened again in the ADF conversion—the same issue from FTFL-546. Fixing it, and pulling FTFL-810's comments since I referenced them without reading them.

I need to correct something I said—my read of FTFL-810 was wrong, and the actual story is better evidence than what I guessed.

FTFL-810 was not abandoned—it succeeded. "Abandoned" is just Jira's resolution-type label on this ticket; the comment history shows you disabled all 7 Tech Ahoy accounts on 2026-07-27, using a temporary Global Admin elevation from Robin to strip their 8 admin roles first when User Administrator wasn't sufficient. Full completion, verified via Graph. I shouldn't have inferred "called off" from a resolution label without reading the comments—that was careless given how much weight I put on it.

But the ticket's own description is the actual lead, and it's better than my guess: _"Tech Ahoy have confirmed that they do not need their individual Entra accounts as their GDAP permissions allow them the required access."_

GDAP—Granular Delegated Admin Privileges—is Microsoft's own partner delegated-admin framework. It's how a Microsoft partner gets scoped admin access to a customer tenant _without_ local accounts. Tech Ahoy told you themselves that GDAP is how they access FITFILE.

That reframes the question entirely. It's not "why does Tech Ahoy have local accounts" (resolved, correctly, in July)—it's: if GDAP is how Tech Ahoy accesses this tenant, why is there also a ~130-permission app-only CIPP-SAM grant sitting alongside it? Let me check what GDAP actually grants them, so the comparison is concrete rather than rhetorical.

That empty result is real, not a permission block (I'd have gotten a Forbidden like the CA/PIM queries did). There are zero GDAP relationships in this tenant—active, pending, or historical.

That's a bigger finding than the redundancy I first suspected. Tech Ahoy told you in July that their GDAP access covered what they needed, and you removed their local accounts on that basis. But GDAP doesn't exist here right now. So either it expired since July and nobody renewed it, or "GDAP" wasn't quite what they had—either way, the app-only CIPP-SAM grant isn't a redundant second access path alongside GDAP. It's very likely the _only_ access path Tech Ahoy has into this tenant now. That reframes the decision: it's not "which of two paths do we keep," it's "this app-only, unmonitored, un-PIM'd grant may be the entire vendor relationship's access mechanism."

Fixing the ticket comment—both for the table-flattening issue and to correct my FTFL-810 read and add this.

Comment corrected and posted. Summary of where this landed:

## What CIPP Is, Concretely

CyberDrain Improved Partner Portal—free open-source MSP tool, manages M365/Entra across client tenants via a "SAM" (Secure Application Model) app registration installed into each tenant it manages. Confirmed by its reply URL: `https://happy-island-07e778303.2.azurestaticapps.net/api/ExecSAMSetup`—that's the vendor's actual CIPP instance.

## Where it is

Not registered in your tenant at all—only Enterprise App objects, no `application` object. Home tenant `53874a5a-…` (EU), which resolves to Tech Ahoy—a contractor you already know.

## The Corrections, in order of how Wrong I Was

1. Not one CIPP-SAM—five. Two are fully live simultaneously (81 and 49 app-role assignments), two are dead (0 assignments, safe deletes), one is a 3-week-old unprivileged "Tech Ahoy Lifecycle App" of unknown purpose.
2. It's actively being administered, not legacy. Last night at 23:07 UTC—hours after this audit started—a named actor ("Tech Ahoy Technician," from the Tech Ahoy tenant, IP `4.159.58.164`) added two new permissions to the live 81-role app: `ExchangeMessageTrace.Read.All` and a SharePoint-scoped `User.ReadWrite.All`.
3. I was wrong about FTFL-810. I read "Abandoned" as "called off" without checking the comments. It actually completed—you disabled all 7 Tech Ahoy accounts on 2026-07-27, using a temporary GA elevation from Robin to strip roles first. That's on me; I should have opened the ticket before asserting what happened in it.
4. But FTFL-810's own description is the real lead, and it points somewhere sharper than I first said. Tech Ahoy told you in July their GDAP access covered what they needed, so local accounts weren't required. I checked: there are zero GDAP relationships in this tenant—not blocked, a genuine empty result. So either GDAP expired since July and nobody renewed it, or it wasn't really GDAP. Either way, CIPP-SAM's ~130 app-only permissions are very likely the entire access mechanism Tech Ahoy has into this tenant right now—not a backup alongside a monitored, Microsoft-native channel. That's a materially different risk position than "redundant path," and it's the question worth putting to whoever owns the commercial relationship.

Your next move is a conversation, not more digging on my end: ask Tech Ahoy (or whoever manages that relationship) whether GDAP should exist and doesn't, or whether CIPP-SAM was always the real mechanism. That answer decides whether FTFL-1032 is "reduce this app's permissions" or "stand up proper GDAP and retire the app-only grant entirely."

Verified two things against the tenant that refine the email's implications—worth having before this goes to Robin, since the "were the accounts reinstated" question is more precise than a yes/no.

Only Luke Scammell was actually reinstated—enabled, zero directory roles (exactly matching Robin's own 29 July description), and he holds Owner on one of the two `NetBird` service principals. Mike Hill's account and the shared `techahoy@` account are still disabled today. So the August NetBird work was very likely done through Luke, not Mike Hill—Robin's July decision on the two riskier asks (Mike Hill's reinstatement, the shared break-glass GA account) held firm; only the narrowest option went through.

One extra thing this surfaced: the _other_ NetBird service principal (`f94e9462-…`) has zero owners in Entra right now—nobody's the designated app owner if it ever needs config changes there.

Here's the summary, ready to send:

---

Tech Ahoy access—where things actually stand (2026-09-08)

Background. Following the pentest remediation (FTFL-542, FTFL-810), Tech Ahoy's local Entra accounts were removed in July on the stated basis that "GDAP provides everything they need." Confirmed in the July thread that this was Tech Ahoy's own assessment, not an assumption—but it's more specific than a blanket yes:

- Luke Scammell, 30 Jul: _"We use GDAP for all daily IT functions and this works well."_
- Same email, immediately after: two things Luke says GDAP does not cover, and asks back—
    1. The shared break-glass GA account `techahoy@`—for SaaS integration/emergencies. Luke says Tech Ahoy would prefer it back but accepts it's your call.
    2. NetBird VPN admin—specifically Mike Hill as sole owner of the NetBird service, needed for user onboarding/offboarding. Luke separately notes: if NetBird moves to Tech Ahoy's own hosted MSP offering, these accounts become unnecessary entirely.

What actually happened, verified against the tenant just now:

|Account|Status today|Roles/access|
|---|---|---|
|`techahoy@` (shared GA)|Disabled|0 directory roles. 3 stale app-role assignments left over (Graph CLI Tools, PnPAccessReport, Phishr Sync)—harmless, just untidy.|
|`ta_luke.scammell@`|Enabled|0 directory roles. Owner of `NetBird` SP `0d554ce0-…`.|
|`ta_mike.hill@`|Disabled|0 directory roles. Not an owner of either NetBird SP.|

So: the shared GA and Mike Hill's account were not reinstated—your original call held. Luke's was reinstated exactly as you described (roles stripped), and he already holds NetBird ownership, which is almost certainly how the August NetBird VPN work got done. This looks like the right outcome, not a walk-back.

Minor gap worth a look: the second `NetBird` SP (`f94e9462-…`, created two days after the first) has no owner in Entra at all. Not urgent, but if that one's the live one, nobody has a governed path to manage its Entra-side config.

The part that doesn't fit—and matters for the CIPP-SAM decision:

I checked `tenantRelationships/delegatedAdminRelationships` in Graph this week: there is no GDAP relationship in this tenant right now—not blocked, a genuine empty result. But Tech Ahoy told you in July that GDAP was working well for daily IT. Either it's lapsed since July and nobody renewed it, or something about the "GDAP" description didn't map to an actual GDAP relationship. Worth putting to Tech Ahoy directly rather than guessing—I haven't got visibility into GDAP's own history (only a snapshot of what exists today), so I can't tell you which.

Separately, and not mentioned anywhere in this email thread: there's a `CIPP-SAM` app registration—actually two live ones simultaneously, ~130 app-only permissions between them (Graph, Exchange, SharePoint, Defender, Rights Management)—and it was actively modified last night (2026-09-07 23:07 UTC) by a named Tech Ahoy technician, adding `ExchangeMessageTrace.Read.All` and a SharePoint-scoped `User.ReadWrite.All`. This is a completely separate access channel from GDAP, from the local accounts, and from NetBird—it's how Tech Ahoy's CIPP tool (their MSP management platform) reaches into this tenant, and it isn't mentioned in either email thread. Full detail is on [FTFL-1032](https://fitfile.atlassian.net/browse/FTFL-1032).

So there are really three separate questions, not one:

1. GDAP—does it still exist, and if not, was that intentional or did it just lapse?
2. NetBird—current state (Luke as sole practical admin) looks fine; the ownerless second SP is a small tidy-up.
3. CIPP-SAM—unrelated to the above, actively growing in privilege, and the one that actually needs a decision (FTFL-1032).

Worth asking Tech Ahoy directly: is CIPP-SAM's app-only access meant to be a third, parallel channel alongside GDAP and NetBird—or is it filling in for something GDAP used to cover before it lapsed?

---

Want this posted to FTFL-1032 as well, or is the chat version enough for you to send on to Robin yourself?

Hi Helena—need your input on a supplier access question (Tech Ahoy)

Came up during an internal Entra/Azure security review. Wanted to flag it to you before it goes further, since it's a third-party access / compliance question as much as a technical one.

Quick background Tech Ahoy is our MSP for day-to-day IT support. Back in July, as part of pentest remediation, Robin removed their shared admin account and most individual accounts, on the basis that Tech Ahoy told us their GDAP access covers what they need for daily work.

Two very different kinds of access, and why it matters

- GDAP (Granular Delegated Admin Privileges) is Microsoft's own framework for MSPs to get admin access to a customer's tenant. It's scoped to specific roles, time-bound, centrally revocable by us, and every action is tied back to a named Tech Ahoy technician's own identity—it shows up in our own access reviews.
- CIPP-SAM is a _different_ mechanism—an app registration belonging to Tech Ahoy's own management tool (CIPP), which we've granted a broad set of standing permissions to (mail, SharePoint, directory roles, security data—roughly 130 permission grants across two separate app registrations). This is machine-to-machine, API-level access. It isn't tied to a named individual at the point of use, it isn't time-bound, and—because it authenticates as an application rather than a person—it sits outside our MFA, Conditional Access, and access-review processes entirely.

Where things actually stand

- Tech Ahoy's own local accounts: mostly removed as planned; one (Luke Scammell) was reinstated with no admin roles, for a specific narrow purpose (NetBird VPN administration).
- GDAP: we currently have zero GDAP relationship with Tech Ahoy in the tenant, despite them describing it in July as how they do daily IT work. Either it's lapsed since July, or it wasn't quite what we thought.
- CIPP-SAM: still fully active, and its permissions were expanded again as recently as last night by a Tech Ahoy technician, without any request or approval on our side that I'm aware of.

So it looks like the well-governed access path (GDAP) may not currently exist, while the less-governed one (CIPP-SAM) is live and growing. I don't know yet whether that's deliberate on Tech Ahoy's side or an oversight—I've asked Robin to raise it with them.

Why I'm bringing it to you

This looks squarely relevant to our NHS Data Security and Protection Toolkit (DSPT) obligations:

- Standard 9 (IT Protection) explicitly requires that we "closely manage privileged user access to networks and information systems," and separately asks whether our IT suppliers hold Cyber Essentials / ISO 27001—if they don't, we're expected to have a documented remediation plan with named owners and dates. (This is actually the same standard Robin cited in July when he removed the shared account.)
- Standard 4 (Managing Data Access) expects role-based, least-privilege access that's removed as soon as it's no longer needed, and expects us to be able to name who holds elevated access to which system. An unattributed app-level grant is hard to answer that question about.
- Standard 10 (Accountable Suppliers) puts the accountability on us, not the supplier—even where we've delegated responsibility, we're expected to know contract by contract who's responsible for what, and to keep an eye on supplier assurance on an ongoing basis, not just at onboarding.

What I'd like from you

1. Do we have an existing internal policy on third-party/vendor access—and if so, does it draw any distinction between "named individual admin access" (like GDAP) and "application/API-level access" (like CIPP-SAM)? My instinct is it should, since the second one is much harder to attribute and review.
2. Should something like CIPP-SAM's permission set be documented and risk-assessed formally as part of our supplier assurance process, the way a new GDAP grant presumably would be?
3. Is this the kind of thing that needs a mention in our own DSPT submission, given it touches Standards 4, 9 and 10?

Happy to walk through the technical detail if useful—full write-up is in [FTFL-1032](https://fitfile.atlassian.net/browse/FTFL-1032)—but the actual decision here (what Tech Ahoy is allowed to hold, and how we govern it) needs your steer on policy, not just the technical fix.

---

Sources for the DSPT points: [NHS England — DSPT Guide 9, IT Protection](https://digital.nhs.uk/cyber-and-data-security/guidance-and-resources/data-security-and-protection-toolkit-assessment-guides/guide-9---it-protection/assurance/), [NHS England — DSPT Guide 10, Accountable Suppliers](https://digital.nhs.uk/cyber-and-data-security/guidance-and-assurance/data-security-and-protection-toolkit-assessment-guides/guide-10---accountable-suppliers/your-suppliers-and-contracts/), [DSPT Standard 4 overview](https://www.dsptoolkit.nhs.uk/News/Attachment/761). Worth double-checking these against your own DSPT portal login, since the toolkit gets refreshed annually and I'm going from published guidance, not FITFILE's actual submission history.
