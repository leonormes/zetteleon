---
aliases: []
confidence: 
created: 2025-03-05T01:25:01Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:40Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Tickets for GitOps Azure Tenant Management with Terraform
type:
uid: 
updated: 
version:
---

## Tickets for GitOps Azure Tenant Management with Terraform

Here's a breakdown of the implementation into actionable tickets, focusing on the initial repository setup and user management as requested.

### Phase 1: Initial Repository Setup

Ticket 1: Create Core Git Repositories in GitLab

- Description: Set up the foundational Git repositories in GitLab to host Terraform configurations and manage the GitOps workflow.
- Acceptance Criteria:
    - Create a GitLab project for infrastructure as code (IaC), e.g., `azure-tenant-infra`.
    - Within the `azure-tenant-infra` project, create the following repositories:
        - `00-bootstrap`: For initial bootstrapping configurations (Terraform Cloud setup, Service Principal creation, initial pipeline).
        - `01-users`: For managing Azure user objects.
        - `02-groups`: For managing Azure AD groups (to be implemented later).
        - `03-roles`: For managing Azure RBAC roles (to be implemented later).
        - `04-permissions`: For managing Azure RBAC role assignments (to be implemented later).
        - `environments`: For environment-specific configurations (e.g., `dev`, `staging`, `prod`).
    - Initialize each repository with a basic `.gitignore` and `README.md` file.
    - Enforce repository access controls: restrict write access to the `main` branch to authorized personnel only.

Ticket 2: Configure GitLab Project Settings

- Description: Configure GitLab project settings to enhance security and workflow.
- Acceptance Criteria:
    - Enable Merge Requests for all changes to the `main` branch.
    - Require at least one code review approval for Merge Requests targeting the `main` branch.
    - Enable GitLab CI/CD pipelines for automated Terraform workflows.
    - Set up branch protection rules for the `main` branch to prevent direct pushes.

Ticket 3: Set up Terraform Cloud Organization and Workspace

- Description: Create a Terraform Cloud organization and the initial workspace to manage the Azure tenant state.
- Acceptance Criteria:
    - Create a Terraform Cloud organization (if one doesn't exist).
    - Create a Terraform Cloud workspace, e.g., `azure-tenant-bootstrap`.
    - Configure the workspace to use remote state management in Terraform Cloud.
    - Set up workspace variables for Azure provider authentication (initially, consider using environment variables for simplicity during bootstrapping, but plan to transition to a more secure secrets' management solution).
    - Connect the Terraform Cloud workspace to the `00-bootstrap` Git repository.

### Phase 2: Initial User Management

Ticket 4: Create Service Principal for Terraform Cloud

- Description: Create a dedicated Azure AD Service Principal to be used by Terraform Cloud for managing Azure resources.
- Acceptance Criteria:
    - Create an Azure AD Service Principal via the Azure portal or Azure CLI.
    - Grant the Service Principal the necessary initial permissions to manage Azure AD users (e.g., `User Administrator` role - for initial bootstrapping, refine later to least privilege).
    - Securely store the Service Principal credentials (client ID and client secret) in Terraform Cloud workspace variables. (Important: For production, transition to Azure Managed Identities or a dedicated secrets management solution as soon as feasible.)

Ticket 5: Bootstrap Terraform Cloud with Initial Configuration (in `00-bootstrap` repo)

- Description: Create the initial Terraform configuration in the `00-bootstrap` repository to set up the Terraform Cloud workspace and the basic GitOps pipeline.
- Acceptance Criteria:
    - Create a Terraform configuration in the `00-bootstrap` repository that includes:
        - Azure provider configuration using the Service Principal credentials.
        - Terraform Cloud backend configuration.
        - Potentially, initial setup of a basic logging/monitoring resource in Azure for audit trails.
    - Commit and push the initial configuration to the `00-bootstrap` repository.
    - Trigger a Terraform Cloud run from the `00-bootstrap` workspace to apply the initial configuration.
    - Verify that the Terraform Cloud workspace is correctly configured and connected to the repository.

Ticket 6: Import Existing Azure Users into Terraform State (in `01-users` repo)

- Description: Import existing Azure users into Terraform state within the `01-users` repository.
- Acceptance Criteria:
    - Create a Terraform configuration in the `01-users` repository to manage Azure AD users.
    - Use the `terraform import` command to import existing Azure users into the Terraform state. Start with a small subset of users for initial testing.
        - Example: `terraform import azuread_user.example "userPrincipalName"` (replace `example` with a resource name and `"userPrincipalName"` with the actual User Principal Name of an existing user).
    - Define data sources in Terraform to dynamically fetch existing users if needed.
    - Commit and push the Terraform configuration and state to the `01-users` repository.
    - Trigger a Terraform Cloud run from a new workspace (e.g., `azure-tenant-users`) connected to the `01-users` repository to verify the import.
    - Verify that the Terraform state now manages the imported Azure user objects.

Ticket 7: Manage User Objects with Terraform (in `01-users` repo)

- Description: Implement basic management of Azure user objects using Terraform. Initially, focus on attributes like `userPrincipalName`, `displayName`, `mailNickname`, and `passwordProfile` (for initial user creation if needed, handle password resets and more complex attributes later).
- Acceptance Criteria:
    - Extend the Terraform configuration in the `01-users` repository to:
        - Create new Azure AD users via Terraform.
        - Update attributes of existing Azure AD users managed by Terraform.
        - (Initially, focus on basic attributes as requested, deferring permissions, roles, and groups management to later tickets.)
    - Test user creation and updates in a non-production environment (if available).
    - Commit and push changes to the `01-users` repository.
    - Trigger a Terraform Cloud run to apply the user management configurations.
    - Verify that user objects are correctly managed in Azure AD through Terraform.

### Phase 3: Iteration and Expansion (Future Tickets)

- Ticket 8: Manage Azure AD Groups with Terraform (in `02-groups` repo)
- Ticket 9: Manage Azure RBAC Roles with Terraform (in `03-roles` repo)
- Ticket 10: Manage Azure RBAC Role Assignments with Terraform (in `04-permissions` repo)
- Ticket 11: Implement Policy as Code (Azure Policy/Sentinel)
- Ticket 12: Set up Comprehensive Monitoring and Logging
- Ticket 13: Implement Secrets Management with Azure Key Vault
- Ticket 14: Refine Service Principal Permissions (Least Privilege)
- Ticket 15: Implement Break-Glass Account Procedures and PIM
- ... (and so on, for further platform components and security enhancements)

### Notes

- Iterative Approach: This ticket breakdown follows an iterative approach. Start with the core infrastructure and user management, then gradually expand to groups, roles, permissions, security policies, and more complex configurations.
- Prioritization: Prioritize tickets based on your immediate needs and risk assessment. Initial security setup and user management are crucial.
- Environment Strategy: Consider setting up separate Terraform Cloud workspaces and Git branches for different environments (dev, staging, prod) as you progress beyond the initial bootstrapping phase.
- Testing: Thoroughly test all Terraform configurations in non-production environments before applying them to production.
- Documentation: Document each step, configuration, and decision made throughout the implementation process.

This ticket breakdown should provide a structured approach to implementing GitOps for your Azure tenant management. Remember to adapt and refine these tickets based on your specific requirements and environment. Let me know if you'd like a more detailed breakdown of any specific ticket or phase!
