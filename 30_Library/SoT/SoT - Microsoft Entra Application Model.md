---
created: 2026-02-09T17:00:00+00:00
modified: 2026-04-06T20:04:19+00:00
tags: [architecture, azure, entra, identity, SoT]
title: SoT - Microsoft Entra Application Model
---

## Minimum Viable Understanding (MVU)

Microsoft Entra ID (formerly Azure AD) separates the definition of an application from its instantiation to support multi-tenancy.

> One-Sentence Summary: Application Registrations define apps; Service Principals run apps inside tenants.

- Application Registration (The Blueprint): The abstract definition. Defines _what_ the app is (Client ID, Redirect URIs, Scopes). Lives in the home tenant only.
- Enterprise Application / Service Principal (The Instance): The runtime identity. Defines _how_ the app behaves in a specific tenant (User Assignment, Conditional Access, Consented Permissions). Lives in every tenant where the app is used.

---

## 1. The Core Data Structure

### The Rule

Every Enterprise Application (Service Principal) points back to exactly one Application Registration. One Application Registration can have many Service Principals (one per tenant).

### Why Entra Splits Them (Operational Concerns)

| Concern | Responsibility | Target Object |
|:--- |:--- |:--- |
| App Design | Blueprint, OAuth2 Scopes, Roles, Manifest | Application Registration |
| Identity Control | Users/Groups, MFA, Conditional Access | Service Principal |
| Permissions | _Requesting_ API access (Scopes) | Application Registration |
| Permissions | _Granting_ Admin Consent | Service Principal |

---

## 2. Attribute Mapping

| Feature | App Registration (Application Object) | Enterprise App (Service Principal) |
|:--- |:--- |:--- |
| Primary Role | The Developer's Definition | The IT Admin's Control Plane |
| Cardinality | 1 (Globally) | 1 per Tenant (1:N globally) |
| You edit this to… | Add a Client Secret, change Redirect URI, define Roles. | Assign Users, set Conditional Access, Consent to Permissions. |
| Data Anchor | `manifest.json` | Local Directory Object (`objectId`) |
| Key ID | `appId` (Client ID) | `objectId` (Instance ID) |
| Runtime Use | Identifying the app during Auth | Getting the token and enforcing policy |

---

## 3. Managed Identities: The "Headless" Service Principal

Managed Identities are a special case of this model where the "Blueprint" is hidden and managed by Microsoft.

- Hidden Blueprint: You do not create an App Registration. The Platform manages the Application Object.
- Automated Credentials: The Service Principal exists, but you never see the credentials. Azure rotates the underlying certificate automatically (typically every 46 days).

### Types

1. System-Assigned (1:1): Hard-linked to a resource (e.g., a VM). If the VM dies, the Identity dies.
2. User-Assigned (N:1): Independent lifecycle. Can be assigned to multiple resources (e.g., 5 VMs sharing one identity).

---

## 3. Critical Design Analysis

### Architectural Strengths

1. Scalability: One definition supports unlimited tenant deployments (SaaS model).
2. Security Boundaries: Customer tenants cannot modify the App Definition (preventing privilege escalation), but fully control Access (User Assignment).
3. Clean Consent Model:
    - App asks: "I need `User.Read`" (Registration).
    - Admin grants: "I allow `User.Read`" (Service Principal).

### Architectural Weaknesses & Friction

1. Cognitive Overhead: The terms "Enterprise Application" (a UI construct) and "Service Principal" (the API object) are used interchangeably, confusing developers.
2. Configuration Fragmentation:
    - _Redirect URIs_ live in the App Registration.
    - _User Assignments_ live in the Service Principal.
    - _Troubleshooting_ requires checking both.
3. Runtime Discovery: Misconfigurations (e.g., mismatched Client Secrets or Redirect URIs) are often only discovered at runtime during authentication, lacking compile-time validation.

### Configuration Fragility (The Kubernetes Parallel)

Similar to Kubernetes manifests, Entra configuration relies on string alignment (Client IDs, Scopes, URIs) across distributed objects without a strong type system. This creates "fragility" where a valid change in the App Registration (e.g., new Redirect URI) does not automatically propagate to dependent systems, leading to silent failures.

---

## 4. Troubleshooting Heuristics

- "I deleted the app but it's still there": You likely deleted the App Registration, but the Service Principal remains (orphaned), or vice-versa.
- "Permissions aren't working": You updated the _Requested_ permissions in the App Registration but did not grant _Admin Consent_ on the Service Principal.
- "Where is the Client Secret?": Always on the App Registration (Certificates & Secrets).
- "Where do I assign a User?": Always on the Enterprise Application (Users & Groups).
