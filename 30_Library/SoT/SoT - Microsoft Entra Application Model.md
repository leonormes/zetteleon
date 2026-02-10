---
created: 2026-02-09T17:00:00+00:00
modified: 2026-02-09T16:56:06+00:00
tags: [architecture, azure, entra, identity, SoT]
title: SoT - Microsoft Entra Application Model
---

## Minimum Viable Understanding (MVU)

Microsoft Entra ID (formerly Azure AD) separates the definition of an application from its instantiation to support multi-tenancy.

- Application Registration (The Class): The global blueprint. Defines _what_ the app is (Client ID, Redirect URIs, Required Permissions). Lives in the home tenant only.
- Enterprise Application / Service Principal (The Instance): The local representation. Defines _how_ the app runs in a specific tenant (User Assignment, Conditional Access, Granted Permissions). Lives in every tenant where the app is used.

> Analogy: App Registration is the DNA/Class; Service Principal is the Organism/Object Instance.

---

## 1. The Core Data Structure

This architectural split enables SaaS vendors to define an app once (App Registration) and have it consumed by thousands of customers (Service Principals) with independent security policies.

```d2
direction: down

home_tenant: "Home Tenant (Developer)" {
  app_reg: "Application Registration\n(The Blueprint)"
  app_id: "Application ID\n(Global GUID)"
  manifest: "Manifest\n(Redirect URIs, Roles)"
  sp_home: "Service Principal\n(Local Instance)"

  app_reg -> app_id: Defines
  app_reg -> manifest: Defines
  app_reg -> sp_home: Instantiates {
    style: {
      stroke-dash: 5
    }
  }
}

tenant_a: "Customer Tenant A" {
  sp_a: "Service Principal\n(Local Instance)"
  users_a: "User Assignments"
  pol_a: "Conditional Access"

  sp_a -> home_tenant.app_id: References
  sp_a -> users_a: Controls
  sp_a -> pol_a: Controls
}

tenant_b: "Customer Tenant B" {
  sp_b: "Service Principal\n(Local Instance)"

  sp_b -> home_tenant.app_id: References
}
```

### Attribute Mapping

| Feature | App Registration (Application Object) | Enterprise App (Service Principal) |
|:--- |:--- |:--- |
| Primary Role | The Developer's Definition | The IT Admin's Control Plane |
| Cardinality | 1 (Globally) | 1 per Tenant (1:N globally) |
| You edit this to… | Add a Client Secret, change Redirect URI, define Roles. | Assign Users, set Conditional Access, Consent to Permissions. |
| Data Anchor | `manifest.json` | Local Directory Object (`objectId`) |
| Key ID | `appId` (Client ID) | `objectId` (Instance ID) |

---

## 2. Managed Identities: The "Headless" Service Principal

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
