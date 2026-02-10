---
captured: "2026-02-09T16:07:57+00:00 2026-02-09T16:07:57+00:00"
created: 2026-02-09T16:08:01+00:00
modified: 2026-02-09T16:51:52+00:00
source: "https://gemini.google.com/share/193de7df7daa"
status: "processing"
tags: ["input"]
title: Entra App Registration vs. Enterprise App
type: "head"
---

## Raw Output / Content

I am confused by azure entra's enterprise applications and application registrations. Give me a data structure overview of how they fit together in the broader entra context. Only use information that you can validate via the Entra documentation as of 2026

To understand Azure Entra ID (formerly Azure AD) as of 2026, you must distinguish between the definition of an application and its instantiation.

The confusion often stems from the UI naming versus the actual data objects. In the Entra admin centre, you see "App Registrations" and "Enterprise Applications". Under the hood, these map to two distinct Graph API resources: the Application Object and the Service Principal Object.

Here is the data structure overview of how they fit together.

### 1\. The Conceptual Model: Class vs. Instance

Think of this relationship like object-oriented programming:

- App Registration (Application Object): This is the Class (the blueprint). It lives in the home tenant only. It defines _what_ the app is (name, logo, permissions it needs).
- Enterprise Application (Service Principal): This is the Instance (the object). It lives in _every_ tenant where the app is used. It defines _how_ the app runs in that specific environment (who can log in, what specific access it has been granted).

### 2\. Data Structure Relationship

The critical link between these two objects is the Application ID (Client ID). This ID remains constant across all tenants, whereas the Object ID is unique to every single object instance.

#### A. Application Object (The Blueprint)

- Location: Exists _only_ in the "Home Tenant" (where you created it).
- Purpose: Defines the application's identity and requirements.
- Key Data Fields:
	- `appId` (Client ID): Global unique identifier (e.g., `a1b2…`).
	- `signInAudience`: Defines who can use it (Single Tenant vs. Multi-Tenant).
	- `requiredResourceAccess`: The permissions the app _wants_ (e.g., "I need to read emails").
	- `appRoles`: Custom roles defined by the developer (e.g., "Admin", "Reader").
	- `web`: Redirect URIs and authentication settings.

#### B. Service Principal Object (The Instance)

- Location: Exists in the Home Tenant _and_ every Consumer Tenant.
- Purpose: The local security principal that actually holds permissions and policies.
- Key Data Fields:
	- `objectId`: Unique ID for _this specific instance_ in _this specific tenant_.
	- `appId`: The foreign key linking back to the Application Object.
	- `appRoleAssignments`: Which specific users/groups in _this_ tenant have which roles.
	- `oauth2PermissionGrants`: The actual consent records (e.g., "User John consented to Read Email").
	- `tags`: Used to categorise the app (e.g., "WindowsAzureActiveDirectoryGalleryApplication").

### 3\. Visual Architecture

The following diagram illustrates a Multi-Tenant scenario, which is the best way to see the distinction.

### 4\. Why This Matters for You (2026 Context)

As of 2026, this architecture remains the bedrock of the Microsoft Identity Platform. Even as "Entra" expands into Global Secure Access and Verified ID, this core pair (Application vs. Service Principal) controls all authorisation.

- When you change the App Registration: You are changing the code/definition (e.g., adding a new redirect URI). This replicates globally.
- When you change the Enterprise Application: You are changing local security (e.g., assigning a Conditional Access policy or hiding the app from users). This affects _only your tenant_.

### Summary Table

| Feature | App Registration (Application Object) | Enterprise App (Service Principal) |
| --- | --- | --- |
| Primary Role | The Developer's Definition | The IT Admin's Control Plane |
| Cardinality | 1 (Globally) | 1 per Tenant (1:N globally) |
| You edit this to… | Add a Client Secret, change Redirect URI, define Roles. | Assign Users, set Conditional Access, Rotate Keys (Managed Identity). |
| Data Anchor | `manifest.json` | Local Directory Object |

Would you like me to explain how "Managed Identities" fit into this structure, as they are a special type of Service Principal?

yes

In the context of the data structure we just discussed, Managed Identities are essentially "headless" Service Principals.

To stick to our Class vs. Instance analogy: with a Managed Identity, Microsoft manages the Class (App Registration), and you only interact with the Instance (Service Principal).

Here is how they fit into the Entra architecture.

### 1\. The Structural Difference

In the standard model, you create an App Registration (the blueprint) and then a Service Principal is created. You are responsible for maintaining the credentials (client secrets or certificates) on that App Registration.

With a Managed Identity, the architecture changes in two specific ways:

1. Hidden Blueprint: You do not create an App Registration. The Application Object exists in the background, but it is fully managed by the Azure platform. You cannot edit its manifest or config.
2. Automated Credentials: The Service Principal has credentials, but you never see them. The Azure resource (like a Virtual Machine or Logic App) and Entra ID negotiate and rotate the password automatically (typically every 46 days).

### 2\. The Two Types of Data Structures

Managed Identities come in two flavours, defined by their lifecycle relationship with the Azure resource.

#### A. System-Assigned (Strict 1:1 Binding)

This creates a Service Principal that is inextricably linked to a single Azure resource.

- Data Relationship: The Service Principal's lifecycle is hard-coded to the Resource's lifecycle.
- Behaviour: If you delete the Virtual Machine, Entra automatically deletes the Service Principal.
- Naming Convention: The Service Principal usually takes the exact name of the Azure resource (e.g., `vm-frontend-prod`).

#### B. User-Assigned (N:1 Binding)

This creates a standalone Service Principal that exists as its own resource in Azure.

- Data Relationship: Independent lifecycle. You can create it once and assign it to multiple Azure resources (e.g., 5 different VMs sharing the same identity to access a SQL logic).
- Behaviour: If you delete the VMs, the Identity (and its permissions) remains in Entra until you explicitly delete it.

### 3\. Visual Architecture

The diagram below illustrates how the "Credentials" part of the data structure is removed from your responsibility.

### 4\. Comparison Table: Standard vs. Managed

| Feature | Standard Enterprise App | Managed Identity |
| --- | --- | --- |
| App Registration | Visible & Editable by you. | Hidden & Managed by Microsoft. |
| Service Principal | Visible in "Enterprise Apps". | Visible in "Enterprise Apps" (filter by _Managed Identities_). |
| Credentials | You create/rotate Secrets or Certs. | Azure rotates internals automatically. |
| Use Case | Apps you write/host or SaaS apps. | Azure Resources connecting to other Azure services. |

### Summary

In your Entra data view, a Managed Identity appears simply as a specific type of Service Principal. It has an Object ID and an Application ID, and you can assign it Roles (permissions), just like any other Enterprise App. The key difference is that the "Credentials" tab is locked, ensuring you cannot leak a password because you never possessed it in the first place.

Would you like to look at "Workload Identity Federation," which allows software running _outside_ of Azure (like AWS or on-prem) to use this same secure structure?

Google Account

Leon Ormes

leonormes@gmail.com
