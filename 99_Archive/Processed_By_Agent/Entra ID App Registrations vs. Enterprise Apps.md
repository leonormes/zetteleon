---
captured: "2026-02-09T16:08:20+00:00 2026-02-09T16:08:20+00:00"
created: 2026-02-09T16:08:23+00:00
modified: 2026-02-09T16:51:47+00:00
source: "https://gemini.google.com/share/4119b252f402"
status: "processing"
tags: ["input"]
title: Entra ID App Registrations vs. Enterprise Apps
type: "head"
---

## Raw Output / Content

help me re-write the following quote as a well formatted question for my notes:

"I am confused by azure Entra's enterprise applications and application registrations. Give me a data structure overview of how they fit together in the broader Entra context. Only use information that you can validate via the Entra documentation as of 2026"

To help structure your notes effectively, here is a clear, professionally phrased question and a summary of the relationship between these two concepts based on current Microsoft Entra documentation.

## Microsoft Entra ID: App Registrations vs. Enterprise Applications

Question for your notes:

> "How do Application Registrations and Enterprise Applications (Service Principals) relate to one another within the Microsoft Entra ID data structure, and what are their distinct roles in identity management?"

---

### Data Structure Overview

In the Entra context, the relationship is best understood as a 1:N (One-to-Many) relationship between a global definition and its local instances.

| Feature | Application Registration | Enterprise Application |
| --- | --- | --- |
| Identity Type | Global Object / Template | Service Principal / Local Instance |
| Location | Resides in the "Home" tenant where the app was created. | Resides in every tenant where the app is used. |
| Purpose | Defines the application's DNA (Redirect URIs, Secrets, API permissions). | Manages local execution (User assignment, Conditional Access, Provisioning). |
| Analogy | The Blueprint for a building. | The Actual Building at a specific address. |

### How They Fit Together

1. The Registration (The Definition): When you register an application, you are creating a global object. This defines _what_ the application is and its security requirements.
2. The Service Principal (The Instance): When a user or admin consents to that application in a tenant, Entra creates a "Service Principal" (visible under Enterprise Applications). This is the security identity that allows the app to actually access resources in that specific tenant.
3. The Relationship: If you delete the Application Registration in the home tenant, the Enterprise Application instances in all other tenants become orphaned and lose their ability to function, as the "blueprint" no longer exists.

---

Would you like me to create a more detailed technical breakdown of the specific attributes (like `AppID` vs `ObjectID`) for these objects?

Google Account

Leon Ormes

leonormes@gmail.com
