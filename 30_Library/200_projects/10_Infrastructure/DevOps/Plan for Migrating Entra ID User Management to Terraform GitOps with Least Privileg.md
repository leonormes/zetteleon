---
aliases: []
confidence: 
created: 2025-03-05T12:36:53Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:40Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [gitops, IAM]
title: Plan for Migrating Entra ID User Management to Terraform GitOps with Least Privileg
type: plan
uid: 
updated: 
version: 1
---

This plan assumes you'll be using Terraform to define the desired state of your Entra ID users and their privileges within a GitLab repository. Changes to user privileges will then be made by modifying these Terraform configurations and applying them via a GitOps pipeline, ideally using Terraform Cloud.

## Phase 1: Preparation and Analysis

1. Comprehensive Security Analysis: Begin by thoroughly analysing your current Entra ID user landscape. Identify all existing users and their current privilege levels. Document which users are currently managed and unmanaged by any form of infrastructure-as-code [this is an inference based on your query].
2. Define the Desired State with Least Privilege: For each user (or type of user based on roles), clearly define the minimum set of permissions they require to perform their job functions. This aligns with the zero trust principle of least privilege. Consider using Azure built-in roles where possible to avoid creating overly specific permissions.
3. Establish a Single Source of Truth: Designate your GitLab repository with the Terraform configurations as the authoritative source for all Entra ID user management [this is an inference based on GitOps principles]. Aim for consistency and clarity to reduce security risks.
4. Plan for Exceptions: Anticipate scenarios where temporary privilege elevation might be necessary. Define a process for managing these exceptions within the GitOps framework, ensuring they are time-bound and auditable. Consider using Microsoft Entra Privileged Identity Management (PIM) concepts for temporary access, even if the provisioning is done via Terraform.
5. Secure the GitOps Pipeline: Ensure your GitLab repository and Terraform Cloud environment are secured according to best practices. This includes access controls, multi-factor authentication for administrators, and potentially using dedicated service principals with minimal permissions for Terraform to interact with Entra ID. Secure your IaC templates by scanning them for vulnerabilities using SAST/DAST tools and avoid hardcoding secrets.

## Phase 2: Setting Up the GitOps Workflow

1. Initial Terraform Configuration: Begin creating Terraform configuration files that represent the desired state of a small, non-critical subset of your Entra ID users and their roles. Focus on users who are currently not managed by Terraform.
2. Version Control with GitLab: Store your Terraform configuration files in a dedicated GitLab repository. Implement code review processes to ensure all changes to user privileges are reviewed and approved before being applied.
3. Integrate with Terraform Cloud: Connect your GitLab repository to Terraform Cloud. Configure workspaces to manage the state of your Entra ID resources. This provides a centralised platform for executing Terraform plans and applies, as well as governance and auditing capabilities.
4. Establish Continuous Integration/Continuous Deployment (CI/CD): Configure your GitLab repository to trigger Terraform Cloud workflows on specific events, such as merging changes to the main branch. This automates the process of applying the desired state defined in your Git repository to your Entra ID environment.

## Phase 3: Migrating Existing Users Safely

1. Identify Unmanaged Users: Create a comprehensive list of users in your Entra ID that are not currently represented in your Terraform configuration.
2. Import Existing Users into Terraform State (Carefully) [this is a Terraform-specific operation implied by the need to manage existing resources]: Terraform allows you to "import" existing infrastructure resources into its state. Start by importing a small number of non-critical unmanaged users into your Terraform state files. This links the existing Entra ID users to your Terraform configuration without making any immediate changes to their privileges.
3. Review Imported Configurations: After importing, review the Terraform configuration generated for these users. Ensure it accurately reflects their current (and desired, based on your least privilege analysis) state.
4. Apply Terraform Configuration (Pilot Group): For the pilot group of imported users, apply the Terraform configuration. Monitor closely to ensure no unintended changes occur. Previewing changes with `terraform plan` before applying is crucial.
5. Gradual Rollout: Once you have successfully migrated a small pilot group, gradually expand the scope to include more unmanaged users. Follow the "log then enforce" procedure if possible (though direct logging of Entra ID configuration changes might be limited within Terraform itself; careful planning and monitoring are key).
6. Reconcile Privileges: As you bring users under Terraform management, ensure their assigned roles and permissions align with your least privilege principles. You might need to adjust the Terraform configurations during this process to reduce excessive permissions.

## Phase 4: Enforcing Least Privilege and Ongoing Management

1. Terraform as Policy Enforcement: With all user privileges defined in Terraform, any attempt to grant excessive privileges outside of the GitOps workflow will be reverted in the next Terraform apply.
2. Git-Based Changes: All modifications to user privileges must now be made by committing changes to the Terraform configuration files in your GitLab repository. This ensures all changes are version-controlled, auditable, and subject to your review process.
3. Regular Audits: Implement regular audits of your Entra ID user configurations in GitLab and the applied state in Terraform Cloud/Entra ID to ensure ongoing compliance with your least privilege policies and identify any drift.
4. Automated Compliance Checks: Consider integrating automated checks into your CI/CD pipeline to validate Terraform configurations against your defined least privilege standards before they are applied.
5. Offboarding Process: Ensure you have a clear process for deprovisioning users through the GitOps workflow when they leave the organisation or change roles, promptly removing their Terraform configurations.

## Phase 5: Security Considerations

1. Secure Credentials: Avoid storing any sensitive credentials directly in your Terraform configuration files. Use Terraform Cloud's variable management or a secure secrets management tool like HashiCorp Vault (though its integration with Entra ID user management via Terraform would need to be architected) to handle API keys or service principal secrets.
2. Principle of Least Privilege for Automation: Ensure the service principal or managed identity used by Terraform Cloud to interact with Entra ID has only the necessary permissions to manage users and roles, adhering to the principle of least privilege for automation itself.
3. Monitor Audit Logs: Regularly monitor the audit logs in GitLab, Terraform Cloud, and Entra ID to detect any suspicious activity or unauthorised changes.
4. Implement Multi-Factor Authentication: Enforce MFA for all users who have access to the GitLab repository and the Terraform Cloud environment, especially administrators.
5. Background Checks (for Administrators): For administrators managing this critical infrastructure, consider appropriate background checks.

By following this phased approach, you can safely migrate your Entra ID user management to a GitOps model with Terraform, enforcing the principle of least privilege and establishing a secure and auditable workflow for managing user access.

What would you like to explore next? Would you like me to elaborate on any specific phase of this plan, perhaps focusing on how to define least privilege roles or secure the GitOps pipeline? Or would you prefer a short quiz to check your understanding of the overall plan?
