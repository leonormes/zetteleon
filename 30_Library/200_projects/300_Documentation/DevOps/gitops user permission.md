---
aliases: []
confidence: 
created: 2025-03-05T11:57:01Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:39Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [gitops, IAM]
title: gitops user permission
type: plan
uid: 
updated: 
version: 1
---

To enforce safe and compliant auditing of user permission changes using GitOps with Terraform, Entra (Azure AD), and GitLab, you need to implement several key measures across your workflow and infrastructure. Here's a breakdown of what you need to enforce:

## Git Repository Security
 - Branch Protection:
   - Enforce Merge Requests: Require all changes to user permissions to be submitted via merge requests (MRs) and prevent direct pushes to the main branch (or any protected branches used for GitOps). This ensures that every change goes through a review process.
   - Code Reviews: Mandate code reviews for all MRs by at least one or two other authorized team members before they can be merged. Reviews should focus on the correctness, security implications, and compliance of the permission changes.
   - Protected Branches: Configure your main branch (and any branches used for deployment) as protected branches in GitLab. This prevents force pushes, direct deletions, and ensures only authorized users with specific roles can merge changes after successful reviews and automated checks.
 - Access Control:
   - Principle of Least Privilege: Grant access to the Git repository and specific branches only to those who absolutely need it. Use GitLab's role-based access control to define granular permissions.
   - Segregation of Duties: Separate roles for those who can propose changes (e.g., developers, permission requestors) and those who can approve and merge them (e.g., security team, compliance officers, senior operations). This prevents any single person from unilaterally making changes.
   - Two-Factor Authentication (2FA): Enforce 2FA for all users who have access to the GitLab repository, especially those with write or merge permissions.
 - History Immutability:
   - Prevent Force Pushes: Branch protection should prevent force pushes to ensure the history of changes remains immutable and auditable.
   - Signed Commits: Consider enforcing signed commits to cryptographically verify the author of each change, adding another layer of integrity to the audit trail.
## Terraform Configuration Security
 - Secure State Management:
   - Remote State Backend: Use a secure remote state backend (like Azure Storage Account with encryption, AWS S3 with encryption, or HashiCorp Consul) to store Terraform state. Avoid storing state locally.
   - State Encryption: Ensure state backend encryption is enabled both in transit and at rest to protect sensitive information potentially stored in the state file.
   - State Versioning: Enable versioning for your state backend (if supported) to track changes to the state file itself and allow for rollback if necessary.
   - State Access Control: Restrict access to the state backend to only the GitLab CI/CD pipeline and authorized users. Use access control mechanisms provided by your cloud provider or state backend service.
 - Secrets Management:
   - Avoid Hardcoding Secrets: Never hardcode credentials or sensitive information directly in Terraform code.
   - Secrets Manager Integration: Use a secrets management solution (like HashiCorp Vault, Azure Key Vault, AWS Secrets Manager, or GitLab Secrets) to securely inject credentials into your Terraform configurations at runtime.
   - Least Privilege for Secrets: Grant access to secrets only to the necessary components (e.g., GitLab CI/CD pipelines) and roles.
 - Code Quality and Security Scans:
   - Linting and Formatting: Integrate linters (like terraform fmt and terraform validate) into your GitLab CI/CD pipeline to automatically check Terraform code for syntax errors, style inconsistencies, and best practices.
   - Static Code Analysis: Use static code analysis tools (like Checkov, Terrascan, or tfsec) in your CI/CD pipeline to scan Terraform code for security vulnerabilities and compliance violations before deployment.
   - Dependency Scanning: If using Terraform modules from external sources, implement dependency scanning to identify and address any known vulnerabilities in those modules.
## GitLab Workflow Enforcement
 - Automated CI/CD Pipeline:
   - Pipeline for Every Change: Set up a GitLab CI/CD pipeline that automatically triggers on every merge request to the main branch. This pipeline should:
     - Run linters and static code analysis tools.
     - Execute terraform plan to generate an execution plan and store it as an artifact for review.
     - Require manual approval to proceed with terraform apply after successful plan and review.
     - Execute terraform apply automatically after approval, applying the changes to Entra.
     - Log all pipeline activities, including approvals, applies, and any errors.
   - Immutable Pipeline Definition: Store your CI/CD pipeline definition (e.g., .gitlab-ci.yml) in the Git repository and treat it as code. Protect it from unauthorized modifications.
 - Change Approval Process:
   - Manual Approval Gate: Implement a manual approval stage in your CI/CD pipeline before the terraform apply step. This requires authorized personnel to review the terraform plan output and approve the changes before they are applied to Entra.
   - Approval Logging: Ensure that all approvals and rejections in the CI/CD pipeline are logged and auditable, including who approved or rejected and when.
   - Notification System: Set up notifications (e.g., email, Slack) to alert relevant teams (security, compliance, operations) about permission changes being proposed, approved, and applied.
 - Rollback Strategy:
   - Version Control for Rollback: Git inherently provides version control, making it easy to revert to previous commits if necessary.
   - Automated Rollback (Consideration): For more advanced setups, consider implementing an automated rollback mechanism in your CI/CD pipeline that can be triggered in case of errors or unintended consequences after applying changes.
## Auditing and Monitoring
 - Comprehensive Audit Logs:
   - Git History as Audit Log: Treat the Git commit history as the primary audit log for all changes to user permissions. Ensure commit messages are descriptive and clearly explain the purpose of each change.
   - GitLab Audit Events: Leverage GitLab's audit events feature to track actions within GitLab itself, such as user logins, permission changes within GitLab, and pipeline executions.
   - Entra Audit Logs: Enable and monitor Entra audit logs to capture all changes made to user permissions within Entra itself. This provides an additional layer of auditing and can be correlated with GitOps changes.
 - Monitoring and Alerting:
   - Real-time Monitoring: Set up monitoring for your GitOps pipeline and infrastructure components (GitLab, state backend, Entra) to detect any anomalies or security incidents.
   - Alerting on Policy Violations: Implement automated checks and alerts for deviations from defined permission policies or security best practices.
   - Regular Audit Reviews: Conduct periodic reviews of audit logs (GitLab, Entra, CI/CD pipeline logs) to proactively identify any unauthorized or non-compliant changes.
## Compliance and Governance
 - Define and Document Policies:
   - Permission Management Policies: Clearly define policies and procedures for managing user permissions, including who is authorized to request, approve, and implement changes.
   - GitOps Workflow Documentation: Document your GitOps workflow, including all the enforced measures, roles and responsibilities, and escalation procedures.
   - Compliance Requirements: Identify and document all relevant compliance requirements (e.g., GDPR, SOC 2, HIPAA) that your permission management system must adhere to.
 - Regular Audits and Reviews:
   - Compliance Audits: Conduct regular internal and external audits to ensure adherence to defined policies and compliance requirements.
   - Process Reviews: Periodically review and update your GitOps workflow and enforcement measures to adapt to evolving security threats and compliance landscapes.
 - Training and Awareness:
   - Security Training: Provide security awareness training to all team members involved in the GitOps workflow, emphasizing the importance of secure permission management and compliance.
   - GitOps Training: Train users on the GitOps workflow, GitLab CI/CD, and Terraform best practices to ensure they understand and follow the enforced procedures.
By implementing these measures, you can establish a robust GitOps framework for managing user permissions in Entra with Terraform and GitLab, ensuring safe, compliant, and auditable changes. Remember to tailor these recommendations to your specific organizational context, risk tolerance, and compliance requirements.

Yes, you can definitely use GitOps to automatically revert privileged escalations after a set time. Here’s how you can achieve this using Terraform, GitOps principles, and GitLab, focusing on safety and compliance:

There are a few main approaches you can take, each with varying levels of complexity and features:

1. Time-Based Logic within Terraform with an External Scheduler (GitLab CI Scheduled Pipelines)
This approach uses Terraform to define both the elevated and standard permission states and relies on GitLab CI scheduled pipelines to trigger the rollback.
Workflow:
 - Define Two Terraform Configurations:
   - Standard Permissions (permissions.tf): This configuration defines the baseline, non-privileged user permissions. This is your default GitOps state.
   - Elevated Permissions (elevated_permissions.tf): This configuration defines the elevated permissions.
 - GitLab Repository Structure:
   - Store both permissions.tf and elevated_permissions.tf in your GitLab repository, possibly in separate directories or using different Terraform workspaces to manage state separately.
 - GitLab CI Pipelines:
   - Apply Pipeline (Manual Trigger):
     - This pipeline is triggered manually (e.g., via a merge request to a specific branch or a manual pipeline run).
     - It executes terraform apply using the elevated_permissions.tf configuration to grant the elevated permissions.
     - You can include a step to record the elevation time and duration (e.g., in a file in the state backend, or an external database, though keeping it simple is often better for GitOps).
   - Rollback Pipeline (Scheduled):
     - This pipeline is scheduled to run periodically (e.g., every hour, or at specific times).
     - It checks for active permission elevations that have exceeded their allowed duration. This check could involve:
       - Simple Time-Based Schedule: If all elevations are for the same duration, the scheduled pipeline can simply run after that duration has passed since the apply pipeline was last run. This is less flexible.
       - State-Based Tracking: A more robust approach is to store metadata about the elevation (start time, duration) in the Terraform state itself (using Terraform state outputs or data sources) or in an external system. The scheduled pipeline can then query this information.
     - If a rollback is needed (duration expired), the pipeline executes terraform apply using the permissions.tf configuration. This reverts the permissions to the standard, non-privileged state.
## Enforcement and Safety
 - GitOps for Both Configurations: Both permissions.tf and elevated_permissions.tf are managed under GitOps. Changes to either configuration require merge requests, reviews, and pipeline execution.
 - Scheduled Rollback Pipeline Security: Secure the scheduled rollback pipeline. Ensure only authorized pipelines can modify permissions. Consider using protected branches and environment-scoped variables in GitLab CI.
 - Logging and Auditing: Log all actions in both pipelines (apply and rollback), including who triggered them, when, and the outcome. This provides a clear audit trail.
 - Idempotency: Terraform's idempotency is crucial here. Applying the permissions.tf configuration repeatedly should safely revert permissions to the standard state without causing issues.
Example (Simplified GitLab CI for Scheduled Rollback):
## .gitlab-ci.yml

```yaml
stages:
  - rollback
scheduled-rollback:
  stage: rollback
  image: hashicorp/terraform:latest
  script:
    - echo "Checking for permission elevations to rollback..."
    - |
## In a Real Scenario, You'd Have Logic here to
## 1. Check if Any Elevations Are Active and Their Expiry time
## 2. If Rollback is Needed, Run Terraform Apply for 'permissions.tf'
## (e.g., Using a Separate Terraform Workspace for Standard permissions)
      # For this example, let's just simulate a rollback after a fixed time
      # (This is NOT production-ready, needs proper state tracking)
      CURRENT_TIME=$(date +%s)
      ELEVATION_END_TIME=$((CURRENT_TIME - (24 * 3600))) # Example: Rollback after 24 hours
      if [ "$CURRENT_TIME" -gt "$ELEVATION_END_TIME" ]; then
        echo "Performing permission rollback..."
        cd permissions_config # Directory containing permissions.tf
        terraform init -backend-config="..." # Your backend config
        terraform apply -auto-approve
      else
        echo "No permission rollbacks needed at this time."
      fi
  schedule: "0 * * * *" # Run every hour (adjust as needed)
  rules:
    - if: '$CI_PIPELINE_SOURCE == "schedule"' # Only run on schedule
```

Important Considerations for this Approach:

 - State Management: You need to carefully manage Terraform state for both configurations (elevated_permissions.tf and permissions.tf). Using separate Terraform workspaces in GitLab CI is a good practice.
 - Complexity of Rollback Logic: The logic to determine when to rollback permissions can become complex if you need different durations for different elevations or more sophisticated tracking.
 - Drift Detection: Regularly run terraform plan for your permissions.tf configuration in a scheduled pipeline to detect any drift from the desired standard permission state.
1. Entra Privileged Identity Management (PIM) with Terraform
A more robust and recommended approach is to leverage Azure AD Privileged Identity Management (PIM) directly. PIM is designed specifically for managing, controlling, and monitoring privileged access in Azure AD.
Workflow:
 - Enable and Configure Entra PIM:
   - Enable PIM for the relevant Azure AD roles you want to manage with temporary elevation.
   - Define PIM policies for these roles, specifying:
     - Maximum activation duration: How long a user can activate a role for.
     - Approval requirements: Whether role activation needs approval and by whom.
     - MFA requirements: Whether multi-factor authentication is required for activation.
     - Notifications: Configure notifications for role activations and expirations.
 - Terraform for PIM Role Assignment Management:
   - Use Terraform to manage PIM role assignments. Terraform can interact with Azure AD and PIM to:
     - Define eligible role assignments (users who can request elevation).
     - Potentially automate the request process for role activation (though direct activation is often preferred for GitOps).
     - Monitor and audit PIM activations.
 - GitOps Workflow for PIM Configuration:
   - Manage your PIM policies and eligible role assignments using Terraform and GitOps. Changes to PIM configurations go through merge requests, reviews, and GitLab CI pipelines.
 - User-Initiated Role Activation (or Automated via API):
   - Users who need elevated permissions can activate their eligible roles through the Azure portal, PowerShell, or the Microsoft Graph API.
   - For GitOps alignment: You could potentially build a GitLab CI pipeline that, upon manual trigger (e.g., a merge request), uses the Azure AD/Microsoft Graph API to programmatically activate a PIM role for a specific user and duration. This gives you GitOps control over the activation as well.
## Enforcement and Safety
 - PIM Built-in Features: PIM provides strong built-in security features for privileged access:
   - Time-bound activation: Roles are automatically deactivated after the configured duration.
   - Approval workflows: Enforce approval for role activation.
   - Audit logging: Comprehensive audit logs of role activations and deactivations within Azure AD.
   - MFA enforcement: Require MFA for privileged role activation.
   - Justification: Require users to provide a justification for role activation.
 - GitOps for PIM Configuration: GitOps ensures that your PIM policies and eligible assignments are version-controlled, auditable, and reviewed.
 - Reduced Terraform Complexity: Terraform focuses on managing PIM configuration, not complex time-based logic.
Example (Conceptual Terraform for PIM Eligible Role Assignment):

```hcl
resource "azuread_role_eligibility_schedule_request" "example" {
  principal_id  = "user_object_id" # User to be eligible
  role_definition_id = "role_definition_id" # Azure AD Role Definition ID
  justification = "Make user eligible for temporary Global Admin"
  schedule {
    start_date_time = "2025-03-05T12:00:00Z" # Example start time
    expiration {
      type = "afterDateTime"
      duration = "PT1H" # Example: Eligible for 1 hour
      date_time = "2025-03-05T13:00:00Z" # Example expiry time
    }
  }
}
```

Tool Use for PIM Research:

To effectively implement the PIM approach, you'll need to research:

Comparison of Approaches:

| Feature           | Time-Based Logic in Terraform | Entra PIM with Terraform |
| ----------------- | ----------------------------- | ------------------------ |
| Complexity        | Higher                        | Lower                    |
| Robustness        | Less                          | More                     |
| Security Features | Relies on custom logic        | Built-in PIM features    |
| Auditability      | Requires custom logging       | PIM built-in audit logs  |
| Maintenance       | More                          | Less                     |
| Best Practice     | Less Recommended              | Highly Recommended       |

Recommendation:

The Entra PIM with Terraform approach is strongly recommended. It leverages a purpose-built service for privileged access management, providing better security, auditability, and features specifically designed for time-bound elevations. Terraform then becomes the GitOps tool to manage the configuration of PIM, ensuring your PIM policies are also under version control and follow GitOps principles.

If Entra PIM is not feasible for some reason, the Time-Based Logic within Terraform with GitLab Scheduled Pipelines is a possible fallback, but it requires more careful design and implementation to achieve similar levels of security and compliance.

Remember to thoroughly test and document your chosen approach and adapt it to your organization's specific security and compliance requirements.

Yes, there is a way to use GitOps to automatically revert privileged escalations after a set time, and leveraging Entra Privileged Identity Management (PIM) with Terraform is the most robust and recommended approach.

Here's a breakdown of how to use Entra PIM with Terraform for time-bound privileged access, aligning with GitOps principles:

Entra Privileged Identity Management (PIM) with Terraform

Entra PIM is specifically designed for managing, controlling, and monitoring privileged access in Azure AD. By integrating PIM with Terraform and GitOps, you gain a secure and auditable way to handle temporary privilege escalations.

Key Benefits of using Entra PIM:

 - Time-Bound Activation: PIM allows you to define a maximum duration for role activations. Roles are automatically deactivated after the set time, ensuring temporary access.
 - Just-In-Time Access: Users only gain privileged access when they explicitly activate an eligible role, reducing the attack surface.
 - Approval Workflows: You can require approvals for role activations, adding another layer of control.
 - Multi-Factor Authentication (MFA) Enforcement: PIM can enforce MFA for role activations, enhancing security.
 - Audit Logging: PIM provides comprehensive audit logs of all role activations and deactivations within Azure AD, crucial for compliance.
Terraform Resources for Entra PIM:
Terraform's AzureAD provider offers resources to manage Entra PIM configurations. The primary resource for time-bound role assignments is azuread_directory_role_eligibility_schedule_request.
Workflow with Entra PIM and Terraform:
 - Enable PIM and Define Policies:
   - In Azure AD, enable PIM for the Azure AD roles you want to manage with temporary elevation.
   - Define PIM policies for these roles directly in the Azure portal or ideally, manage these policies as code using Terraform if possible (though direct Terraform resource management of PIM policies might be limited, focus on role assignments). Policies include:
     - Maximum activation duration.
     - Approval requirements.
     - MFA requirements.
 - Terraform Configuration for PIM Eligible Role Assignments:
   - Use the azuread_directory_role_eligibility_schedule_request resource in your Terraform code to define eligible role assignments. This means you are making users eligible to activate a privileged role, not directly assigning them the role permanently.
   - Within the azuread_directory_role_eligibility_schedule_request resource, you can specify:
     - principal_id: The user or group to make eligible for the role.
     - role_definition_id: The Azure AD role (e.g., Global Administrator).
     - justification: A reason for the eligibility.
     - schedule: Define the schedule for eligibility, including start_date_time and expiration (using afterDateTime or duration).
 - GitOps Workflow for PIM Configuration:
   - Manage your Terraform code defining PIM eligible role assignments in GitLab.
   - Changes to these configurations go through standard GitOps practices: merge requests, code reviews, and GitLab CI pipelines for applying the Terraform changes.
 - User-Initiated or Automated Role Activation:
   - User-Initiated Activation (Most Common): Users needing elevated permissions activate their eligible roles themselves through the Azure portal, PowerShell, or Microsoft Graph API. They will be bound by the PIM policies (MFA, justification, approval, time limits).
   - Automated Activation via GitLab CI (For GitOps Alignment): For tighter GitOps integration, you could create a GitLab CI pipeline that, when triggered (manually or by a specific event like a merge request), uses the Azure AD/Microsoft Graph API to programmatically activate a PIM role for a user for a predefined duration. This gives you GitOps control over the entire elevation process, including activation.
Example Terraform Configuration for PIM Eligible Role Assignment:
resource "azuread_directory_role_eligibility_schedule_request" "temporary_admin_eligibility" {
  principal_id = "user_object_id" # Replace with the object ID of the user
  role_definition_id = "role_definition_id" # Replace with the Role Definition ID of the Azure AD role (e.g., Global Administrator)
  directory_scope_id = "/" # Root directory scope

  justification = "Granting temporary Global Admin for emergency maintenance."

  schedule {

    start_date_time = "2025-03-05T12:00:00Z" # Example start time (adjust as needed)

    expiration {

      type     = "duration"

      duration = "PT2H" # Example: Eligible for 2 hours (ISO 8601 duration format)

    }

  }

}

Key Enforcement and Compliance Points with PIM & GitOps:

 - GitOps for PIM Configuration: All PIM eligible role assignments are defined as code in Git and managed through GitOps workflows, ensuring version control and auditability of who is made eligible for roles.
 - PIM Policies Enforce Time Limits: PIM policies inherently enforce the time-bound nature of privileged access. You configure the maximum activation duration within PIM, and users cannot exceed it.
 - Azure AD Audit Logs for Activations: Azure AD and PIM automatically log all role activations, deactivations, and PIM-related events. This provides a comprehensive audit trail of when and by whom roles were activated.
 - Separation of Duties: GitOps can control who can make users eligible for roles (through repository access and merge request approvals). PIM policies can control who can activate those eligible roles (potentially with separate approvers defined in PIM policies).
 - Compliance: This approach helps meet compliance requirements by providing auditable, time-bound, and controlled privileged access.
Steps to Implement:
 - Research Azure AD PIM: Thoroughly understand Entra PIM features and how it aligns with your security and compliance needs.
 - Enable Entra PIM: Enable PIM in your Azure AD tenant and configure basic policies.
 - Identify Roles for PIM: Determine which Azure AD roles should be managed with temporary elevation.
 - Terraform Implementation:
   - Set up the AzureAD Terraform provider.
   - Create Terraform configurations using azuread_directory_role_eligibility_schedule_request to define eligible role assignments for the identified roles.
 - GitLab Integration:
   - Store your Terraform code in GitLab.
   - Create GitLab CI pipelines for applying Terraform changes to PIM configurations (following GitOps workflow).
 - User Training: Train users on how to activate their eligible roles through PIM when needed.
 - Monitoring and Auditing: Regularly review Azure AD audit logs and PIM activity reports.
By using Entra PIM with Terraform and GitOps, you establish a robust and compliant system for managing temporary privileged access, ensuring automatic reversion of escalations and a strong audit trail. This approach is significantly more secure and manageable than trying to build time-based rollback logic solely within Terraform and scheduled pipelines.
