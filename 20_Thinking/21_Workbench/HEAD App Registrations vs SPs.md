---
captured: "2026-02-06T15:07:17+00:00 2026-02-06T15:07:17+00:00"
created: 2026-02-06T15:07:23+00:00
modified: 2026-02-12T17:04:54+00:00
source: "https://chatgpt.com/c/6985db97-b720-838a-809f-ea1128d23cd7"
status: "processing"
tags: ["input"]
title: HEAD App Registrations vs SPs
type: "head"
---

## Raw Output / Content

How do Application Registrations and Enterprise Applications (Service Principals) relate to one another within the Microsoft Entra ID data structure, and what are their distinct roles in identity management?

---

Great question—this is _the_ Entra concept that clicks everything else into place once you see the shape of it.

Let's build it up step-by-step, then I'll check your understanding with one quick question.

---

## Big Picture First

Think in terms of _blueprints_ vs _instances_.

- Application Registration = the blueprint / definition of an app
- Enterprise Application (Service Principal) = a live instance of that app inside a tenant

Both live inside Microsoft Entra ID, but they serve very different jobs.

---

## 1️⃣ Application Registrations—what the App is

An Application Registration answers the question:

> _"What is this application, in abstract?"_

It defines:

- App ID (client ID)
- Redirect URIs
- OAuth2/OpenID scopes
- App roles
- Required API permissions
- Whether it's single-tenant or multi-tenant

Key idea:

👉 This object is tenant-independent in concept.

It does not sign in, get tokens, or have permissions _by itself_.

Think: _source code + manifest_.

---

## 2️⃣ Enterprise Applications (Service Principals)—how the App Exists in a Tenant

An Enterprise Application is really a Service Principal, and it answers:

> _"How does this app behave inside this specific tenant?"_

It is the security identity Entra actually uses at runtime.

It holds:

- Assigned users and groups
- Granted permissions (consents)
- Conditional Access policies
- Credentials (secrets, certs)
- Token issuance context

Key idea:

👉 Tokens are issued to service principals, not app registrations.

Think: _a deployed instance with permissions and runtime identity_.

---

## 3️⃣ How They Relate (this is the Core Mental model)

### The Rule

> Every Enterprise Application (Service Principal) points back to exactly one Application Registration.

But:

- One Application Registration can have many Service Principals
- Each Service Principal lives in one tenant

### Common Scenarios

| Scenario | What happens |
| --- | --- |
| You register an app in your tenant | Entra creates both objects |
| Another tenant consents to your multi-tenant app | That tenant gets its own Service Principal |
| You use Microsoft Graph | The App Registration is owned by Microsoft; your tenant only has the Service Principal |

---

## 4️⃣ Why Entra Splits Them (this Matters operationally)

This separation lets Entra cleanly divide concerns:

| Concern | Lives where |
| --- | --- |
| App design & capabilities | Application Registration |
| Security, access, policy | Service Principal |
| Multi-tenant reuse | Application Registration |
| Tenant-specific control | Service Principal |

This is why:

- Deleting a Service Principal does _not_ delete the app globally
- You can lock down access per tenant without changing the app itself
- Conditional Access never touches the App Registration

---

## 5️⃣ One-sentence Summary (commit This to memory)

> Application Registrations define apps.
> Service Principals run apps inside tenants.

---

### Quick Check (one question)

If you assign users, grant admin consent, or apply Conditional Access, which object are you modifying—

the Application Registration or the Service Principal?

Answer that, and I'll help you map this directly to real Azure Portal clicks (and Terraform, if you want 👀).
