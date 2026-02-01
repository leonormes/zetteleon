---
context_files: []
created: 2026-02-01T14:49:57+00:00
enabled_tools: [read_only, vault_ops]
last_active: 2026-02-01T14:50:11.533Z
metadata:
  autoLabeled: true
modified: 2026-02-01T15:07:45+00:00
require_confirmation: [create_files, delete_files, modify_files]
session_id: session_1769954934312_1t9h2n4t0
title: FitFile Auth0 Architecture & Auth Flow
type: agent-session
---

## Agent Session 01-02-2026

### User

> [!metadata]- Message Info
>
> | Property | Value |
> | -------- | ----- |
> | Time | 2026-02-01T14:49:57.081Z |
> | File Version | unknown |

> [!user]+
> Search the Infrastructure project notes for all documentation on Auth0 Object Architecture and summarize the authentication flow for FitFile deployments

---

### Model

> [!metadata]- Message Info
>
> | Property | Value |
> | -------- | ----- |
> | Time | 2026-02-01T14:50:11.524Z |
> | File Version | unknown |

> [!assistant]+
> Based on the documentation in [[Auth0 Object Architecture - FITFILE Deployments]] and [[FITFILE Auth0 Authentication Flow]], here is a summary of the Auth0 architecture and authentication flow for FitFile deployments.
>
> ### 🏗️ Auth0 Object Architecture
> The architecture is divided into **Shared Infrastructure** (managed centrally) and **Deployment-Specific Objects** (created per customer).
>
> #### 1. Shared (Tenant-Level) Objects
> Managed by Central Services in the &#x60;auth0-prod&#x60; workspace. These are single instances shared across all deployments:
> -   **Tenant Settings:** Global settings (friendly name, session lifetimes, support email).
> -   **The Shared Connection (&#x60;Username-Password-Authentication&#x60;):** This is the &quot;Conflicting Object.&quot; All FitFile users authenticate against this single database connection to ensure consistent password policies and centralized user management.
> -   **Branding &amp; Security:** Global logos, colors, and Attack Protection policies (brute force protection, suspicious IP throttling).
> 
> #### 2. Deployment-Specific Objects
> Created for each new customer deployment (e.g., MKUH, CUH):
> -   **SPA Client:** A Single Page Application client for the web interface (e.g., &#x60;app.mkuh-prod-1.eoe.fitfile.net&#x60;).
> -   **M2M Clients:** Non-interactive clients for automated access (API Explorer, GitLab CI/CD pipelines).
> -   **Client Grants:** Specific permissions (scopes) for M2M clients to access the Auth0 Management API.
> -   **Connection Association (&#x60;auth0_connection_clients&#x60;):** **Critical Component.** This resource links the deployment-specific clients to the shared &quot;Username-Password-Authentication&quot; connection.
> 
> ---
>
> ### 🔄 Authentication Flow for FitFile Deployments
> FitFile uses the **OAuth 2.0 Authorization Code Flow with PKCE** (Proof Key for Code Exchange) to secure logins for Single Page Applications.
>
> 1.  **User Access:** The user navigates to the deployment URL (e.g., &#x60;<https://cuh-prod-1.fitfile.net>&#x60;). The frontend detects the user is unauthenticated.
> 2.  **Redirect to Auth0:** The browser is redirected to &#x60;fitfile-prod.eu.auth0.com/authorize&#x60; with:
>     -   &#x60;client_id&#x60;: The specific ID for that deployment&#x27;s SPA.
>     -   &#x60;audience&#x60;: The identifier for the resource server (e.g., &#x60;<https://cuh-prod-1.privatelink.fitfile.net>&#x60;).
>     -   &#x60;code_challenge&#x60;: The PKCE challenge.
> 3.  **User Authentication:** Auth0 presents the login page. Users authenticate against the shared database connection. **Multi-Factor Authentication (MFA)** is enforced for all users.
> 4.  **Authorization Code Return:** After successful login, Auth0 redirects the user back to the application&#x27;s &#x60;/callback&#x60; URL with a temporary &#x60;code&#x60;.
> 5.  **Token Exchange:** The frontend sends the &#x60;code&#x60; and the &#x60;code_verifier&#x60; to Auth0&#x27;s &#x60;/oauth/token&#x60; endpoint.
> 6.  **JWT Tokens Issued:** Auth0 returns:
>     -   **Access Token:** Short-lived (5 minutes), RS256 signed, used for API calls.
>     -   **ID Token:** Contains user profile information.
> 7.  **API Authentication:** The frontend includes the Access Token in the &#x60;Authorization: Bearer&#x60; header for all backend API calls. The backend validates the token signature using Auth0&#x27;s public keys.
> 
> ---
>
> ### 🛠️ Implementation &amp; Best Practices
> -   **Reference, Don&#x27;t Recreate:** Terraform modules for new deployments must use &#x60;data&#x60; sources to reference the existing shared connection. Attempting to create a new connection with the same name results in a &#x60;409 Conflict&#x60;.
> -   **Short-Lived Tokens:** Access tokens are limited to 300 seconds (5 minutes) to minimize the window for token theft.
> -   **SpiceDB Integration:** After authentication, the Auth0 User ID is mapped to **SpiceDB** subjects for fine-grained, role-based access control (RBAC) over healthcare data.
> -   **Private Link Audiences:** Deployments often use private link domains (e.g., &#x60;*.privatelink.fitfile.net&#x60;) for the API audience to secure internal traffic.

---
